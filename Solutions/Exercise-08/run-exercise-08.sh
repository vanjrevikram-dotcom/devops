#!/bin/bash
# Exercise 8: Creating "Hello World" Jenkins Job
cd "$(dirname "$0")/devops-sample-code"
source ../../common/run.sh

# 1. Script creation and local execution
chmod +x hello-world.sh
run "cat hello-world.sh"
run "./hello-world.sh"

# 2. Local Git repository setup (as agreed: local Git tracking instead of remote push)
rm -rf .git
git config --global user.name "DevOps Student"
git config --global user.email "student@devops.lab"
git config --global init.defaultBranch main

run "git init"
run "git add hello-world.sh"
run "git status"
run "git commit -m 'Add hello-world.sh'"
run "git log -n 1 --stat"

# 3. Jenkins Integration
# Ensure Jenkins container is running
if ! docker ps | grep -q jenkins; then
  echo "[Starting Jenkins container...]"
  docker start jenkins
  for i in $(seq 1 30); do
    if curl -sI http://localhost:8080/login | grep -q "200 OK"; then
      break
    fi
    sleep 2
  done
fi

# Copy the repo into Jenkins workspace /var/jenkins_home/workspace/HelloWorld
echo "[Setting up HelloWorld workspace inside Jenkins]"
docker exec -u root jenkins mkdir -p /var/jenkins_home/workspace/HelloWorld
docker cp hello-world.sh jenkins:/var/jenkins_home/workspace/HelloWorld/hello-world.sh
docker exec -u root jenkins chown -R jenkins:jenkins /var/jenkins_home/workspace/HelloWorld
docker exec -u jenkins jenkins chmod +x /var/jenkins_home/workspace/HelloWorld/hello-world.sh

# Execute the shell step as Jenkins runs it in a Freestyle project
run "docker exec -u jenkins -w /var/jenkins_home/workspace/HelloWorld jenkins sh -xe hello-world.sh"
