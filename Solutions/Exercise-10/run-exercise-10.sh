#!/bin/bash
# Exercise 10: Multi-Node Kubernetes Cluster with Multiple Applications and ReplicaSets
cd "$(dirname "$0")"
source ../common/run.sh
export MINIKUBE_IN_STYLE=false
P=devops-multinode

# Step 0
run minikube stop
run minikube delete
run minikube delete -p $P
# Step 1a / 1b
run minikube start --nodes 3 -p $P --force --container-runtime=docker
wait_cluster
run kubectl get nodes -o wide
run minikube -p $P addons enable registry
# Step 4: build on the WSL host Docker daemon
run docker build -t product-catalog:latest -f Dockerfile.product .
run docker build -t shopping-cart:latest -f Dockerfile.shopping .
run "docker images | grep -E 'product-catalog|shopping-cart'"
# Step 5: load into every node of the profile
run minikube -p $P image load product-catalog:latest
run minikube -p $P image load shopping-cart:latest
run "minikube -p $P ssh -- docker images | grep -E 'REPOSITORY|product-catalog|shopping-cart'"
run "minikube -p $P ssh -n ${P}-m02 -- docker images | grep -E 'product-catalog|shopping-cart'"
run "minikube -p $P ssh -n ${P}-m03 -- docker images | grep -E 'product-catalog|shopping-cart'"
# Step 6-7
run kubectl apply -f product_catalog_deployment.yaml
run kubectl apply -f shopping_cart_deployment.yaml
run kubectl apply -f product_catalog_service.yaml
run kubectl apply -f shopping_cart_service.yaml
run kubectl rollout status deployment/product-catalog --timeout=240s
run kubectl rollout status deployment/shopping-cart --timeout=240s
# Step 8
run kubectl get pods -o wide
run kubectl get rs
run kubectl get svc
# Step 9-10
svc_url product-catalog-service -p $P
PURL=$SVC_URL
svc_url shopping-cart-service -p $P
CURL_=$SVC_URL
echo "Product Catalog URL: $PURL"
echo "Shopping Cart URL:   $CURL_"
run "curl -s $PURL/products; echo"
run "curl -s $CURL_/cart; echo"
run "curl -s -X POST $CURL_/cart -H 'Content-Type: application/json' -d '{\"id\": 1, \"name\": \"Laptop\", \"quantity\": 1}'; echo"
