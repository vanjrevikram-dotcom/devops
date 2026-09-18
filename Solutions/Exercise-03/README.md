# Exercise 03: Scaling Flask App on Single Node using ReplicaSets

## Objective
Understand Kubernetes ReplicaSet mechanics, horizontal pod scaling (scaling out and in), self-healing resilience when pods fail or are deleted, and traffic load distribution across active replicas.

## Scenario
Simulating an e-commerce "Flash Sale" backend service where sudden traffic surges require scaling from 3 to 5 worker pods, followed by verifying automatic replacement of crashed pods and round-robin request distribution.

## Tools Used
- **Minikube** (v1.39.0)
- **Kubectl** (v1.37.1)
- **Docker Engine inside Minikube**
- **Python 3.11 / Flask / Gunicorn**
- **cURL test client container (`curlimages/curl`)**

## Visual Verification & Interface Screenshots

### 1. Terminal Interface & Execution Output
![Terminal Interface & Command Output](screenshot-terminal-interface.png)

### 2. Website & Web Service Interface
![Website Interface Screenshot](screenshot-website-interface.png)
## Implementation Details
1. **Application Logic**: Flask application with endpoints `/`, `/health`, and `/buy?user=X` which returns the serving pod's hostname (`socket.gethostname()`) to observe load distribution.
2. **Dockerfile & Gunicorn**: Containerized with Gunicorn multi-threaded WSGI server listening on port 5000.
3. **ReplicaSet Manifest**: Initialized with `replicas: 3`, liveness and readiness probes pointing to `/health`, resource requests and limits.
4. **Horizontal Scaling**: Scaled dynamically to 5 replicas via `kubectl scale rs flashsale-rs --replicas=5`.
5. **Self-Healing Simulation**: Targeted and deleted pod `flashsale-rs-bvctp`. Monitored the ReplicaSet controller as it immediately spawned replacement pod `flashsale-rs-2kgj5` to maintain the desired count of 5.
6. **Traffic Distribution Verification**: Executed 10 sequential curl requests against `http://flashsale-svc/buy` via a test pod and recorded the `served_by_pod` response field across all replicas.

## Commands Executed
```bash
minikube start --nodes=1 --force --container-runtime=docker
eval $(minikube docker-env)
docker build -t flashsale:1.0 .
kubectl apply -f flashsale-replicaset.yaml
kubectl wait --for=condition=Ready pod -l app=flashsale --timeout=180s
kubectl get pods
kubectl get rs
kubectl scale rs flashsale-rs --replicas=5
kubectl wait --for=condition=Ready pod -l app=flashsale --timeout=180s
kubectl get rs
kubectl get pods
kubectl delete pod flashsale-rs-bvctp
kubectl wait --for=condition=Ready pod -l app=flashsale --timeout=180s
kubectl get pods -o wide
kubectl describe rs flashsale-rs
kubectl run curl-test --rm -i --restart=Never --image=curlimages/curl --command -- \
  sh -c 'for i in 1 2 3 4 5 6 7 8 9 10; do curl -s http://flashsale-svc/buy?user=$i; echo; done'
```

## Real Terminal Output & Verification
```text
$ kubectl get rs
NAME           DESIRED   CURRENT   READY   AGE
flashsale-rs   3         3         3       7s

$ kubectl scale rs flashsale-rs --replicas=5
replicaset.apps/flashsale-rs scaled

$ kubectl get rs
NAME           DESIRED   CURRENT   READY   AGE
flashsale-rs   5         5         5       14s

$ kubectl delete pod flashsale-rs-bvctp
pod "flashsale-rs-bvctp" deleted from default namespace

$ kubectl get pods
NAME                 READY   STATUS    RESTARTS   AGE
flashsale-rs-2kgj5   1/1     Running   0          8s
flashsale-rs-ccqth   1/1     Running   0          15s
flashsale-rs-fmswt   1/1     Running   0          23s
flashsale-rs-svcmt   1/1     Running   0          23s
flashsale-rs-zpfhm   1/1     Running   0          23s

$ kubectl run curl-test ...
{"item":"Laptop","served_by_pod":"flashsale-rs-svcmt","status":"success","time":"12:53:20","user":"1"}
{"item":"Smartphone","served_by_pod":"flashsale-rs-2kgj5","status":"success","time":"12:53:20","user":"2"}
{"item":"Laptop","served_by_pod":"flashsale-rs-ccqth","status":"success","time":"12:53:20","user":"3"}
{"item":"Laptop","served_by_pod":"flashsale-rs-fmswt","status":"success","time":"12:53:20","user":"4"}
{"item":"Laptop","served_by_pod":"flashsale-rs-zpfhm","status":"success","time":"12:53:20","user":"5"}
```

## Errors Encountered & Fixes Applied
1. **Naming Inconsistencies in Lab Manual**: The original manual created `flashsale-rs` in the YAML but used `flask-app-rs` in subsequent scaling commands. Standardized all manifests and CLI commands to `flashsale-rs`.
2. **Dockerfile COPY Mismatch**: The manual instructed copying `ex3-flash-sale.py` while starting `app:app`. Fixed `COPY app.py .` so Gunicorn accurately resolved the WSGI entrypoint.
3. **Image Pull Policy**: Because images are built inside the local Minikube daemon without remote push to Docker Hub, added `imagePullPolicy: Never` to prevent ImagePullBackOff errors.

## Result
**COMPLETE & VERIFIED**. Successfully proved scaling from 3 to 5 pods, automatic self-healing upon pod deletion, and distributed request handling across all pods.
