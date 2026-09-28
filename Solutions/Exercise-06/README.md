# Exercise 06: Real-Time Operations Monitoring and Alerting (Quick-Commerce App)

## Objective
Implement an end-to-end operational monitoring and alerting pipeline for a quick-commerce delivery service using Python Prometheus client metrics, Prometheus scraping, PromQL alert rules, and Grafana visualization.

## Scenario
DevOps engineers at a fast-paced delivery service ("ZAPPTTO") require real-time visibility into operational metrics (total deliveries, pending orders, on-the-way deliveries, and average delivery times), paired with automated alerting thresholds when pending deliveries exceed safe operating limits.

## Tools Used
- **Python Prometheus Client** (`prometheus-client` 0.26.0)
- **Prometheus** (`prom/prometheus:latest`)
- **Grafana** (`grafana/grafana:latest`)
- **Docker Engine** (28.2.2)
- **cURL & jq**

## Visual Verification & Interface Screenshots

### 1. Terminal Interface & Execution Output
![Terminal Interface & Command Output](screenshot-terminal-interface.png)

### 2. Website & Web Service Interface
![Website Interface Screenshot](screenshot-website-interface.png)
## Implementation Details
1. **Metrics Simulator**: Created `delivery_metrics.py` exposing Gauge and Summary metrics on `0.0.0.0:8000/metrics`.
2. **Prometheus Configuration**: Configured `prometheus.yml` targeting the host bridge IP (`172.17.0.1:8000`) and referencing `alert_rules.yml`.
3. **Alert Rules**: Defined rules in `alert_rules.yml`:
   - `HighPendingDeliveries`: triggers warning when `pending_deliveries > 10` for `15s`.
   - `HighAverageDeliveryTime`: triggers critical alert when `(average_delivery_time_sum / average_delivery_time_count) > 30`.
4. **Container Launch**:
   - Launched Prometheus with volume-mounted configuration and alert rules.
   - Launched Grafana on port 3000.
5. **API & Metric Verification**:
   - Verified Prometheus Targets API (`/api/v1/targets`): reports `job: delivery_service` as `health: up`.
   - Verified Prometheus Rules API (`/api/v1/rules`): reports active rules in group `delivery_alerts`.
   - Verified Grafana web interface returning HTTP 302 redirecting to `/login`.
6. **Jenkins Automation Pipeline**: Created `Jenkinsfile` and `Dockerfile` automating the workspace setup, container build, execution, and verification.

## Commands Executed
```bash
python3 delivery_metrics.py &
curl -s http://localhost:8000/metrics | grep -E 'total_deliveries|pending_deliveries'
docker run -d --name prometheus -p 9090:9090 \
  -v "$(pwd)/prometheus.yml":/etc/prometheus/prometheus.yml \
  -v "$(pwd)/alert_rules.yml":/etc/prometheus/alert_rules.yml \
  prom/prometheus
docker run -d --name grafana -p 3000:3000 grafana/grafana
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
curl -s http://localhost:9090/api/v1/targets | jq .
curl -s http://localhost:9090/api/v1/rules | jq .
curl -sI http://localhost:3000
```

## Real Terminal Output & Verification
```text
$ curl -s http://localhost:8000/metrics | grep -E 'total_deliveries|pending_deliveries'
# HELP total_deliveries Total number of deliveries
# TYPE total_deliveries gauge
total_deliveries 67.0
# HELP pending_deliveries Number of pending deliveries
# TYPE pending_deliveries gauge
pending_deliveries 14.0

$ docker ps
NAMES        IMAGE             STATUS          PORTS
grafana      grafana/grafana   Up 10 seconds   0.0.0.0:3000->3000/tcp
prometheus   prom/prometheus   Up 10 seconds   0.0.0.0:9090->9090/tcp

$ curl -s http://localhost:9090/api/v1/targets | jq .data.activeTargets[0]
{
  "discoveredLabels": {
    "__address__": "172.17.0.1:8000",
    "job": "delivery_service"
  },
  "labels": {
    "instance": "172.17.0.1:8000",
    "job": "delivery_service"
  },
  "health": "up",
  "scrapeUrl": "http://172.17.0.1:8000/metrics"
}

$ curl -sI http://localhost:3000
HTTP/1.1 302 Found
Location: /login
```

## Errors Encountered & Fixes Applied
1. **Filename Discrepancy in Original ZIP**: The directory tree listed `alerts_rules.yml` (plural), whereas `prometheus.yml` pointed to `alert_rules.yml` (singular). Standardized to `alert_rules.yml`.
2. **Missing Dockerfile in Original ZIP**: The provided Jenkinsfile ran `docker build -t delivery_metrics .`, but the ZIP omitted the Dockerfile. Authored a clean, production-ready `Dockerfile` containerizing `delivery_metrics.py`.
3. **Jenkinsfile Placeholder Paths**: Replaced the `/path/to/your/local/files` placeholder with real mapped directories and host-path resolution for docker-in-docker volume mounts.

## Result
**COMPLETE & VERIFIED**. All metrics, Prometheus scrape targets, alert rules, and Grafana endpoints were successfully deployed and verified operational.
