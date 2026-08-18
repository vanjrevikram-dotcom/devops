#!/bin/bash
# Shared helper: prints "$ <command>" then executes it, so logs contain genuine command + output.
run() {
  echo
  echo "\$ $*"
  bash -c "$*" 2>&1
  local rc=$?
  echo "[exit code: $rc]"
  return 0
}

# Fix for race observed in Exercise 1: right after 'minikube start' the API rejects pods with
# 'serviceaccount "default" not found'. Wait until the default SA exists and nodes are Ready.
wait_cluster() {
  echo "[waiting for default service account and Ready nodes]"
  for i in $(seq 1 60); do
    kubectl get serviceaccount default >/dev/null 2>&1 && break
    sleep 2
  done
  kubectl wait --for=condition=Ready nodes --all --timeout=180s
}

# 'minikube service <svc> --url' with the docker driver on Linux keeps a tunnel open in the foreground
# ("the terminal needs to be open"). Run it in the background, print its real output, export SVC_URL.
# Usage: svc_url <service> [extra minikube args...]
svc_url() {
  local svc=$1; shift
  local out=/tmp/svc-$svc.out
  echo
  echo "\$ minikube $* service $svc --url    (kept running in background)"
  nohup minikube "$@" service "$svc" --url > "$out" 2>&1 &
  for i in $(seq 1 30); do grep -q '^http' "$out" && break; sleep 1; done
  cat "$out"
  SVC_URL=$(grep -m1 '^http' "$out")
}
