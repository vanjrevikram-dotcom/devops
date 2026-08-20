#!/bin/bash
# Exercise 2: Deploy a Flask app on Minikube using kubectl and yaml
cd "$(dirname "$0")"
source ../common/run.sh
export MINIKUBE_IN_STYLE=false

run minikube status
run minikube docker-env
eval $(minikube docker-env)
run docker build -t flask-app .
run "docker images | grep flask-app"

# Steps 5-6: initial deployment only (no Service yet)
run kubectl apply -f flask-deployment-step5.yaml
run kubectl rollout status deployment/flask-app --timeout=180s
run kubectl get deployments
run kubectl get pods -l app=flask-app
run kubectl describe deployment flask-app
POD=$(kubectl get pods -l app=flask-app -o jsonpath='{.items[0].metadata.name}')
run kubectl logs $POD
run kubectl get services
# Step 12: expected to FAIL (port not exposed outside the cluster)
run "curl -sS --max-time 5 http://127.0.0.1:15000"

# Step 13: add the Service
run kubectl apply -f flask-deployment.yaml
run kubectl get services
svc_url flask-app-service
run "curl -s $SVC_URL; echo"
