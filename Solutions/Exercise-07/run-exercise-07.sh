#!/bin/bash
# Exercise 7: Introduction to Continuous Integration (CI) and Jenkins Installation
cd "$(dirname "$0")"
source ../common/run.sh

# Clean up any existing jenkins container
docker rm -f jenkins 2>/dev/null || true

# Start Jenkins with Docker
run "docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts"

# Wait for Jenkins to initialize and generate the initial password
echo "[Waiting for Jenkins to generate initialAdminPassword...]"
for i in $(seq 1 60); do
  if docker exec jenkins test -f /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null; then
    break
  fi
  sleep 2
done

# Verify container is running
run "docker ps -a | grep jenkins"

# Retrieve Initial Admin Password
run "docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword"

# Wait for Jenkins web interface to return 200 OK
echo "[Waiting for Jenkins to be fully ready and return HTTP 200...]"
for i in $(seq 1 60); do
  if curl -sI http://localhost:8080/login | grep -q "200 OK"; then
    break
  fi
  sleep 2
done

# Verify HTTP response from Jenkins on port 8080
run "curl -sI http://localhost:8080/login | head -n 15"
