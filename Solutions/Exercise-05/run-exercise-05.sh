#!/bin/bash
# Exercise 5: Docker Security with AppArmor and Python
cd "$(dirname "$0")"
source ../common/run.sh

# Install python docker SDK
pip3 install docker --break-system-packages 2>/dev/null || pip3 install docker

# Clean previous containers
docker rm -f flask-apparmor 2>/dev/null || true

# Task 2: Build docker image
run docker build -t flask-apparmor .

# Task 3: Create & Load AppArmor Profile
run "cp my-apparmor-profile /etc/apparmor.d/my-apparmor-profile"
run "cat /etc/apparmor.d/my-apparmor-profile"
run "apparmor_parser -r /etc/apparmor.d/my-apparmor-profile"
run "aa-status"

# Test Task 3 via docker CLI directly
run "docker run -d --name flask-apparmor --security-opt='apparmor=my-apparmor-profile' -p 5000:5000 flask-apparmor"
run "docker inspect --format '{{.HostConfig.SecurityOpt}}' flask-apparmor"
run "docker rm -f flask-apparmor"

# Task 4: Run apply_apparmor.py (using Docker SDK)
run "python3 apply_apparmor.py"

# Task 5: Run test_restricted_actions.py (using Docker SDK)
run "python3 test_restricted_actions.py"
