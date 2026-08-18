#!/bin/bash
# Exercise 1: Hello Pod (nginx on Minikube)
source "$(dirname "$0")/../common/run.sh"
export MINIKUBE_IN_STYLE=false

# Fresh cluster. --force: running as root with the docker driver.
# --container-runtime=docker: minikube v1.39 defaults to containerd; the docker runtime is needed for
# 'eval $(minikube docker-env)' used in Exercises 2 and 3 on this same cluster.
minikube delete >/dev/null 2>&1
run minikube start --force --container-runtime=docker
wait_cluster
run kubectl run hello-k8s --image=nginx --port=80
run kubectl wait --for=condition=Ready pod/hello-k8s --timeout=180s
run kubectl get pods
run kubectl expose pod hello-k8s --type=NodePort --port=80
run kubectl get svc hello-k8s
svc_url hello-k8s
run "curl -s $SVC_URL | head -n 25"
run kubectl get pods -o wide
