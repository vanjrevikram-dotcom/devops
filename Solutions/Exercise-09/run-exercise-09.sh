#!/bin/bash
# Exercise 9: Jenkins Multi-Stage Pipeline: Deploying a Python Application
cd "$(dirname "$0")/python-flask-app"
source ../../common/run.sh

# 1. Local Git repository setup
rm -rf .git
git config --global user.name "DevOps Student"
git config --global user.email "student@devops.lab"
git config --global init.defaultBranch main

run "git init"
run "git add ."
run "git status"
run "git commit -m 'Initial commit of Python Flask app and pipeline'"
run "git log -n 1 --stat"

# 2. Local test execution verification
run "python3 -m unittest discover -s ."

# 3. Step 8 of manual: Configure Jenkins container with Python dependencies
echo "[Step 8: Ensuring Jenkins is running and installing Python3 and Flask inside container]"
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

run "docker exec -u root jenkins apt-get update -y"
run "docker exec -u root jenkins apt-get install -y python3 python3-pip python3-flask"

# 4. Set up Jenkins Pipeline Workspace
WS="/var/jenkins_home/workspace/Python-MultiStage-Pipeline"
docker exec -u root jenkins mkdir -p "$WS"
docker cp . jenkins:"$WS/"
docker exec -u root jenkins chown -R jenkins:jenkins "$WS"

# 5. Execute Multi-stage Pipeline steps sequentially inside Jenkins
echo "[Running Multi-stage Pipeline: Stage Build]"
run "docker exec -u jenkins -w $WS jenkins echo 'Creating virtual environment and installing dependencies...'"

echo "[Running Multi-stage Pipeline: Stage Test]"
run "docker exec -u jenkins -w $WS jenkins python3 -m unittest discover -s ."

echo "[Running Multi-stage Pipeline: Stage Deploy]"
run "docker exec -u jenkins -w $WS jenkins bash -c 'mkdir -p $WS/python-app-deploy && cp $WS/app.py $WS/python-app-deploy/'"

echo "[Running Multi-stage Pipeline: Stage Run Application]"
run "docker exec -u jenkins -w $WS jenkins bash -c 'nohup python3 $WS/python-app-deploy/app.py > $WS/python-app-deploy/app.log 2>&1 & echo \$! > $WS/python-app-deploy/app.pid'"
sleep 3

echo "[Running Multi-stage Pipeline: Stage Test Application]"
run "docker exec -u jenkins -w $WS jenkins python3 $WS/test_app.py"

echo "[Pipeline completed successfully! Cleaning up background app process]"
run "docker exec -u jenkins -w $WS jenkins bash -c 'kill -9 \$(cat $WS/python-app-deploy/app.pid) 2>/dev/null || true'"
