#!/bin/bash
# Exercise 6: Real-Time Operations Monitoring and Alerting (Prometheus, Grafana, Delivery Metrics)
cd "$(dirname "$0")/delivery_monitoring"
source ../../common/run.sh

pip3 install prometheus-client --break-system-packages 2>/dev/null || pip3 install prometheus-client

# Clean up any existing containers
docker rm -f prometheus grafana delivery_metrics 2>/dev/null || true

# Step 1: Start python metrics simulator in background
echo "[Starting delivery_metrics.py in background]"
python3 delivery_metrics.py > delivery_metrics.log 2>&1 &
METRICS_PID=$!
sleep 3

# Verify /metrics endpoint
run "curl -s http://localhost:8000/metrics | head -n 30"
run "curl -s http://localhost:8000/metrics | grep -E 'total_deliveries|pending_deliveries|on_the_way_deliveries|average_delivery_time'"

# Step 2: Run Prometheus
HOST_IP=$(ip -4 addr show docker0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}' || echo "172.17.0.1")
echo "Docker host bridge IP: $HOST_IP"

run docker run -d --name prometheus -p 9090:9090 \
  -v "$(pwd)/prometheus.yml":/etc/prometheus/prometheus.yml \
  -v "$(pwd)/alert_rules.yml":/etc/prometheus/alert_rules.yml \
  prom/prometheus

# Step 3: Run Grafana
run docker run -d --name grafana -p 3000:3000 grafana/grafana

sleep 10
run "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'"

# Verify Prometheus Targets & API
run "curl -s http://localhost:9090/api/v1/targets | jq . || curl -s http://localhost:9090/api/v1/targets | head -c 500"
run "curl -s http://localhost:9090/api/v1/rules | jq . || curl -s http://localhost:9090/api/v1/rules | head -c 500"

# Wait for Grafana to finish startup
echo "[Waiting for Grafana to initialize...]"
for i in $(seq 1 30); do
  if curl -sI http://localhost:3000 | grep -q "302 Found\|200 OK"; then
    break
  fi
  sleep 2
done

# Verify Grafana HTTP response
run "curl -sI http://localhost:3000"

# Stop background simulator
kill -9 $METRICS_PID 2>/dev/null || true
