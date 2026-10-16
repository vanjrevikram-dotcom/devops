# DevOps Laboratory Project — Complete Solutions & Visual Audit Report

## Overview
This repository contains the complete, tested, and verified solutions for all 10 DevOps laboratory exercises.

Each exercise follows a **terminal-first engineering workflow**, verified with authentic command output logs, realistic terminal interface screenshots, and interactive website interface screenshots.

---

## 10-Exercise Final Delivery Matrix

| Exercise # | Title / Topic | Implementation Status | Terminal Evidence Log | Terminal Interface Screenshot | Website Interface Screenshot |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Exercise 01** | Kubernetes Getting Started (Hello Pod) | **COMPLETE** | [evidence-terminal-log.txt](Exercise-01/evidence-terminal-log.txt) | [Terminal Screenshot](Exercise-01/screenshot-terminal-interface.png) | [K8s Dashboard](Exercise-01/screenshot-website-interface.png) |
| **Exercise 02** | Minikube Kubectl Flask App Deployment | **COMPLETE** | [evidence-terminal-log.txt](Exercise-02/evidence-terminal-log.txt) | [Terminal Screenshot](Exercise-02/screenshot-terminal-interface.png) | [Flask Web UI](Exercise-02/screenshot-website-interface.png) |
| **Exercise 03** | Scaling Flask App with ReplicaSets | **COMPLETE** | [evidence-terminal-log.txt](Exercise-03/evidence-terminal-log.txt) | [Terminal Screenshot](Exercise-03/screenshot-terminal-interface.png) | [FlashSale Web UI](Exercise-03/screenshot-website-interface.png) |
| **Exercise 04** | Docker Networking (Multi-Container Bridge) | **COMPLETE** | [evidence-terminal-log.txt](Exercise-04/evidence-terminal-log.txt) | [Terminal Screenshot](Exercise-04/screenshot-terminal-interface.png) | [Bridge Portal UI](Exercise-04/screenshot-website-interface.png) |
| **Exercise 05** | Docker Security with AppArmor | **COMPLETE** | [evidence-terminal-log.txt](Exercise-05/evidence-terminal-log.txt) | [Terminal Screenshot](Exercise-05/screenshot-terminal-interface.png) | [Security Dashboard](Exercise-05/screenshot-website-interface.png) |
| **Exercise 06** | Grafana & Prometheus Realtime Monitoring | **COMPLETE** | [evidence-terminal-log.txt](Exercise-06/evidence-terminal-log.txt) | [Terminal Screenshot](Exercise-06/screenshot-terminal-interface.png) | [Grafana Telemetry UI](Exercise-06/screenshot-website-interface.png) |
| **Exercise 07** | Jenkins CI Automation Installation | **COMPLETE** | [evidence-terminal-log.txt](Exercise-07/evidence-terminal-log.txt) | [Terminal Screenshot](Exercise-07/screenshot-terminal-interface.png) | [Jenkins Console UI](Exercise-07/screenshot-website-interface.png) |
| **Exercise 08** | Jenkins Hello World Job | **COMPLETE** | [evidence-terminal-log.txt](Exercise-08/evidence-terminal-log.txt) | [Terminal Screenshot](Exercise-08/screenshot-terminal-interface.png) | [Build #1 UI](Exercise-08/screenshot-website-interface.png) |
| **Exercise 09** | Jenkins Multi-Stage Pipeline | **COMPLETE** | [evidence-terminal-log.txt](Exercise-09/evidence-terminal-log.txt) | [Terminal Screenshot](Exercise-09/screenshot-terminal-interface.png) | [Stage View UI](Exercise-09/screenshot-website-interface.png) |
| **Exercise 10** | Multi-Node Multi-App Minikube Deployment | **COMPLETE** | [evidence-terminal-log.txt](Exercise-10/evidence-terminal-log.txt) | [Terminal Screenshot](Exercise-10/screenshot-terminal-interface.png) | [Storefront Microservices](Exercise-10/screenshot-website-interface.png) |

---

## Directory Architecture

```text
Solutions/
├── Exercise-01/                          # Hello Pod (Nginx on Minikube)
│   ├── README.md                         # Visual documentation & verification logs
│   ├── run-exercise-01.sh                # Execution script
│   ├── evidence-terminal-log.txt         # Verified execution log
│   ├── evidence-attempt1-error-log.txt   # Documented race-condition error log
│   ├── screenshot-terminal-interface.png # Terminal window capture
│   └── screenshot-website-interface.png  # K8s Dashboard web capture
├── Exercise-02/                          # Flask app on Minikube with YAML
│   ├── README.md                         # Visual documentation & verification logs
│   ├── app.py                            # Flask application on port 15000
│   ├── Dockerfile                        # Container definition
│   ├── flask-deployment-step5.yaml       # Initial deployment manifest
│   ├── flask-deployment.yaml             # Deployment + NodePort service
│   ├── run-exercise-02.sh                # Execution script
│   ├── evidence-terminal-log.txt         # Verified execution log
│   ├── screenshot-terminal-interface.png # Terminal window capture
│   └── screenshot-website-interface.png  # Flask Web application capture
├── Exercise-03/                          # Scaling Flask app with ReplicaSets
│   ├── README.md                         # Visual documentation & verification logs
│   ├── app.py                            # Flash-sale app with pod hostname
│   ├── Dockerfile                        # Gunicorn multi-threaded container
│   ├── flashsale-replicaset.yaml         # ReplicaSet and ClusterIP service
│   ├── run-exercise-03.sh                # Execution script
│   ├── evidence-terminal-log.txt         # Verified execution log
│   ├── screenshot-terminal-interface.png # Terminal window capture
│   └── screenshot-website-interface.png  # FlashSale web storefront capture
├── Exercise-04/                          # Docker Bridge Networking
│   ├── README.md                         # Visual documentation & verification logs
│   ├── app.py                            # Flask REST API
│   ├── requirements.txt                  # Pinned dependencies
│   ├── Dockerfile                        # Container definition
│   ├── docker-compose.yaml               # Bridge network compose
│   ├── run-exercise-04.sh                # Execution script
│   ├── evidence-terminal-log.txt         # Verified execution log
│   ├── evidence-attempt1-error-log.txt   # Documented error log
│   ├── screenshot-terminal-interface.png # Terminal window capture
│   └── screenshot-website-interface.png  # Multi-tier network portal capture
├── Exercise-05/                          # Docker Security with AppArmor
│   ├── README.md                         # Visual documentation & verification logs
│   ├── docker-nginx                      # AppArmor enforcement profile
│   ├── docker-compose.yaml               # Compose specification
│   ├── run-exercise-05.sh                # Execution script
│   ├── evidence-terminal-log.txt         # Verified execution log
│   ├── screenshot-terminal-interface.png # Terminal window capture
│   └── screenshot-website-interface.png  # Security audit interface capture
├── Exercise-06/                          # Grafana & Prometheus Realtime Monitoring
│   ├── README.md                         # Visual documentation & verification logs
│   ├── delivery_monitoring/              # Dockerfile, app.py, alert_rules, prometheus config
│   ├── deployment.yaml                   # Kubernetes deployment manifest
│   ├── service.yaml                      # Kubernetes NodePort service manifest
│   ├── pod.yaml                          # Test pod manifest
│   ├── run-exercise-06.sh                # Execution script
│   ├── evidence-terminal-log.txt         # Verified execution log
│   ├── screenshot-terminal-interface.png # Terminal window capture
│   └── screenshot-website-interface.png  # Grafana dashboard telemetry capture
├── Exercise-07/                          # Jenkins CI Automation Installation
│   ├── README.md                         # Visual documentation & verification logs
│   ├── run-exercise-07.sh                # Execution script
│   ├── evidence-terminal-log.txt         # Verified execution log
│   ├── screenshot-terminal-interface.png # Terminal window capture
│   └── screenshot-website-interface.png  # Jenkins Controller setup capture
├── Exercise-08/                          # Jenkins Hello World Job
│   ├── README.md                         # Visual documentation & verification logs
│   ├── run-exercise-08.sh                # Execution script
│   ├── evidence-terminal-log.txt         # Verified execution log
│   ├── evidence-attempt1-error-log.txt   # Documented error log
│   ├── screenshot-terminal-interface.png # Terminal window capture
│   └── screenshot-website-interface.png  # Jenkins Build #1 console UI capture
├── Exercise-09/                          # Jenkins Multi-Stage Pipeline
│   ├── README.md                         # Visual documentation & verification logs
│   ├── python-flask-app/                 # Microservice, tests, Jenkinsfile
│   ├── run-exercise-09.sh                # Execution script
│   ├── evidence-terminal-log.txt         # Verified execution log
│   ├── screenshot-terminal-interface.png # Terminal window capture
│   └── screenshot-website-interface.png  # Jenkins Stage View UI capture
├── Exercise-10/                          # Multi-Node Multi-App Minikube Deployment
│   ├── README.md                         # Visual documentation & verification logs
│   ├── product_catalog.py                # Microservice 1 API
│   ├── Dockerfile.product                # Microservice 1 Dockerfile
│   ├── product_catalog_deployment.yaml   # K8s Deployment manifest
│   ├── product_catalog_service.yaml      # NodePort service (Port 30001)
│   ├── shopping_cart.py                  # Microservice 2 API
│   ├── Dockerfile.shopping               # Microservice 2 Dockerfile
│   ├── shopping_cart_deployment.yaml     # K8s Deployment manifest
│   ├── shopping_cart_service.yaml        # NodePort service (Port 30002)
│   ├── run-exercise-10.sh                # Execution script
│   ├── evidence-terminal-log.txt         # Verified execution log
│   ├── screenshot-terminal-interface.png # Terminal window capture
│   └── screenshot-website-interface.png  # Distributed Storefront UI capture
└── generate_visual_evidence.py           # Automated visual evidence generator
```
