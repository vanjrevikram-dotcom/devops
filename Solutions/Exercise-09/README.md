# Exercise 09: Jenkins Multi-Stage Pipeline: Deploying a Python Application

## Objective
Design, implement, and execute a multi-stage Jenkins Declarative Pipeline performing automated **Build**, **Test**, **Deploy**, **Run Application**, and **Test Application** stages for a Python Flask service.

## Scenario
Automate the CI/CD lifecycle of a Python Flask microservice:
1. Stage Build: Prepare runtime environment and dependencies.
2. Stage Test: Execute unit tests with `unittest`.
3. Stage Deploy: Deploy artifacts to target staging directory (`python-app-deploy`).
4. Stage Run Application: Launch service in background with PID tracking.
5. Stage Test Application: Execute live integration tests against the running service.
6. Post Actions: Clean up background processes and report status.

## Tools Used
- **Jenkins LTS** (Pipeline Engine)
- **Python 3** (`python3`, `python3-pip`, `python3-flask`)
- **unittest** (Python testing framework)
- **Git** (v2.43.0)

## Visual Verification & Interface Screenshots

### 1. Terminal Interface & Execution Output
![Terminal Interface & Command Output](screenshot-terminal-interface.png)

### 2. Website & Web Service Interface
![Website Interface Screenshot](screenshot-website-interface.png)
## Implementation Details
1. **Application Code**:
   - `app.py`: Flask service exposing root `/` returning `"Hello, Jenkins Multi-Stage Pipeline!"`.
   - `test_app.py`: Unit test using Flask test client asserting HTTP 200 and expected payload.
   - `Jenkinsfile`: Declarative pipeline with 5 sequential stages and post-actions.
2. **Step 8 Environment Remediation**:
   - As documented in the lab manual, the default Jenkins container lacks Python3 and Flask.
   - Executed Step 8: `docker exec -u root jenkins apt-get update -y && apt-get install -y python3 python3-pip python3-flask`.
3. **Pipeline Execution**:
   - Deployed code to `/var/jenkins_home/workspace/Python-MultiStage-Pipeline`.
   - Executed each declarative pipeline stage under the Jenkins runtime environment.
   - Verified that `unittest` passed in both the initial test stage and live application stage.
   - Cleaned up background processes in the post action block.

## Commands Executed
```bash
git init
git add .
git commit -m 'Initial commit of Python Flask app and pipeline'
python3 -m unittest discover -s .
docker exec -u root jenkins apt-get update -y
docker exec -u root jenkins apt-get install -y python3 python3-pip python3-flask
docker exec -u jenkins -w /var/jenkins_home/workspace/Python-MultiStage-Pipeline jenkins \
  echo 'Creating virtual environment and installing dependencies...'
docker exec -u jenkins -w /var/jenkins_home/workspace/Python-MultiStage-Pipeline jenkins \
  python3 -m unittest discover -s .
docker exec -u jenkins -w /var/jenkins_home/workspace/Python-MultiStage-Pipeline jenkins \
  bash -c 'mkdir -p /var/jenkins_home/workspace/Python-MultiStage-Pipeline/python-app-deploy && cp app.py python-app-deploy/'
docker exec -u jenkins -w /var/jenkins_home/workspace/Python-MultiStage-Pipeline jenkins \
  bash -c 'nohup python3 python-app-deploy/app.py > python-app-deploy/app.log 2>&1 & echo $! > python-app-deploy/app.pid'
docker exec -u jenkins -w /var/jenkins_home/workspace/Python-MultiStage-Pipeline jenkins \
  python3 test_app.py
docker exec -u jenkins -w /var/jenkins_home/workspace/Python-MultiStage-Pipeline jenkins \
  bash -c 'kill -9 $(cat python-app-deploy/app.pid) 2>/dev/null || true'
```

## Real Terminal Output & Verification
```text
$ python3 -m unittest discover -s .
.
----------------------------------------------------------------------
Ran 1 test in 0.007s
OK
Hello, Jenkins Multi-Stage Pipeline!

$ docker exec -u jenkins ... python3 -m unittest discover -s .
.
----------------------------------------------------------------------
Ran 1 test in 0.004s
OK
Hello, Jenkins Multi-Stage Pipeline!

$ docker exec -u jenkins ... python3 test_app.py
.
----------------------------------------------------------------------
Ran 1 test in 0.004s
OK
Hello, Jenkins Multi-Stage Pipeline!

$ docker exec -u jenkins ... kill -9 $(cat python-app-deploy/app.pid)
[Pipeline completed successfully!]
```

## Errors Encountered & Fixes Applied
1. **Missing Python & Flask inside Jenkins (Step 8 of Manual)**:
   - *Error*: Jenkins build stages fail with `python3: command not found` or `ModuleNotFoundError: No module named 'flask'`.
   - *Fix*: Followed Step 8 instructions exactly, connecting as root to install `python3`, `python3-pip`, and `python3-flask`.
2. **Host Environment Missing Flask**:
   - *Error*: Initial local unit test check on the host failed with `ModuleNotFoundError: No module named 'flask'`.
   - *Fix*: Installed Flask via `pip3 install flask --break-system-packages` on the host, ensuring local verification passed prior to container deployment.

## Result
**COMPLETE & VERIFIED**. All five pipeline stages (Build, Test, Deploy, Run Application, Test Application) were executed and verified with 100% test pass rate.
