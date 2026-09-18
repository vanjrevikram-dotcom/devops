#!/bin/bash
# Exercise 3: Scaling Flask App on Single Node using ReplicaSets
cd "$(dirname "$0")"
source ../common/run.sh
export MINIKUBE_IN_STYLE=false

# Step 1: clean up previous minikube
run minikube stop
run minikube delete
# Step 2: single-node cluster
run minikube start --nodes=1 --force --container-runtime=docker
wait_cluster
run kubectl get nodes

# Build image inside Minikube's Docker daemon (no Docker Hub push - no account assumed)
run minikube docker-env
eval $(minikube docker-env)
run docker build -t flashsale:1.0 .

# Steps 3-4: apply ReplicaSet + Service
run kubectl apply -f flashsale-replicaset.yaml
run "kubectl wait --for=condition=Ready pod -l app=flashsale --timeout=180s"
# Step 6
run kubectl get pods
run kubectl get rs
# Step 7-9: scale to 5
run kubectl scale rs flashsale-rs --replicas=5
run "kubectl wait --for=condition=Ready pod -l app=flashsale --timeout=180s"
run kubectl get rs
run kubectl get pods
# Step 10-11: delete one pod -> self-healing
POD=$(kubectl get pods -l app=flashsale -o jsonpath='{.items[0].metadata.name}')
run kubectl delete pod $POD
sleep 5
run "kubectl wait --for=condition=Ready pod -l app=flashsale --timeout=180s"
run kubectl get pods
run kubectl get pods -o wide
run kubectl describe rs flashsale-rs

# Load distribution: call /buy through the ClusterIP service from a temporary pod
run "kubectl run curl-test --rm -i --restart=Never --image=curlimages/curl --command -- sh -c 'for i in 1 2 3 4 5 6 7 8 9 10; do curl -s http://flashsale-svc/buy?user=\$i; echo; done'"
