# Exercise 05: Docker Security with AppArmor and Python

## Objective
Understand container security enforcement using Linux AppArmor Mandatory Access Control (MAC) profiles, applying profiles via the Docker CLI and Docker SDK for Python, and testing restricted actions within a confined container.

## Scenario
Securing a containerized Flask application by restricting access to critical system directories (`/etc/**`, `/var/**`), denying execution of system binaries (`/bin/**`, `/usr/bin/**`), and stripping unnecessary Linux capabilities (`deny capability sys_admin`).

## Tools Used
- **Docker Engine** (28.2.2)
- **AppArmor / AppArmor Utilities** (`apparmor_parser`, `aa-status`)
- **Python 3.14** with `docker` Python SDK (v7.2.0)
- **Linux Kernel**: 6.18.54.1-microsoft-standard-WSL2

## Visual Verification & Interface Screenshots

### 1. Terminal Interface & Execution Output
![Terminal Interface & Command Output](screenshot-terminal-interface.png)

### 2. Website & Web Service Interface
![Website Interface Screenshot](screenshot-website-interface.png)
## Implementation Details
1. **Flask Application**: Created `app.py` returning `"Hello, this is a secure Flask application running inside a Docker container!"`.
2. **Dockerfile**: Containerized `app.py` on `python:3.8-slim` and built image `flask-apparmor`.
3. **AppArmor Profile**: Defined `/etc/apparmor.d/my-apparmor-profile` confining `/usr/bin/python3` with restricted file and capability permissions.
4. **Python Docker SDK Enforcement**: Created `apply_apparmor.py` to launch the container with `security_opt=["apparmor=my-apparmor-profile"]` and inspect the container's applied security options.
5. **Restricted Actions Test**: Created `test_restricted_actions.py` attempting to read `/etc/passwd` and execute `/bin/bash` via `container.exec_run()`.

## Commands Executed
```bash
pip3 install docker
docker build -t flask-apparmor .
cp my-apparmor-profile /etc/apparmor.d/my-apparmor-profile
cat /etc/apparmor.d/my-apparmor-profile
apparmor_parser -r /etc/apparmor.d/my-apparmor-profile
aa-status
docker run -d --name flask-apparmor --security-opt='apparmor=my-apparmor-profile' -p 5000:5000 flask-apparmor
docker inspect --format '{{.HostConfig.SecurityOpt}}' flask-apparmor
docker rm -f flask-apparmor
python3 apply_apparmor.py
python3 test_restricted_actions.py
```

## Real Terminal Output & Environmental Findings
```text
$ apparmor_parser -r /etc/apparmor.d/my-apparmor-profile
Cache read/write disabled: interface file missing. (Kernel needs AppArmor 2.4 compatibility patch.)
Warning: unable to find a suitable fs in /proc/mounts, is it mounted?
Use --subdomainfs to override.
[exit code: 1]

$ aa-status
apparmor filesystem is not mounted.
apparmor module is loaded.
[exit code: 3]

$ python3 apply_apparmor.py
Container started: 024d65a6146b
AppArmor profile applied: ['apparmor=my-apparmor-profile']
[exit code: 0]

$ python3 test_restricted_actions.py
Attempt to read /etc/passwd: Exit Code 0, Output: root:x:0:0:root:/root:/bin/bash ...
Attempt to execute /bin/bash: Exit Code 0, Output: 
[exit code: 0]
```

## Technical Analysis of Environmental Constraint
1. **Docker Configuration Passed**: Docker correctly accepted and stored the security option:
   `HostConfig.SecurityOpt: ['apparmor=my-apparmor-profile']`.
2. **Kernel Limitation**: The WSL2 kernel (`6.18.54.1-microsoft-standard-WSL2`) has the AppArmor kernel module loaded, but the `securityfs` filesystem is not mounted at `/sys/kernel/security/apparmor` by the virtualized environment.
3. **Parser Failure**: `apparmor_parser` exited with code 1 because `/proc/mounts` does not expose the securityfs interface required to inject profiles into the running kernel.
4. **Consequence**: Without active kernel policy compilation, Docker cannot enforce profile restrictions at the syscall level, allowing commands such as `cat /etc/passwd` to return exit code 0 rather than the expected exit code 1 (Permission denied).

## Result
**NOT COMPLETE (ENVIRONMENT LIMITATION)**.
- **Code & Configuration**: 100% complete (`app.py`, `Dockerfile`, `my-apparmor-profile`, `apply_apparmor.py`, `test_restricted_actions.py`).
- **Execution & SDK**: 100% verified via Docker CLI and Python SDK.
- **Enforcement Status**: Not enforced due to WSL2 kernel missing the active `securityfs` interface for AppArmor. Fully documented with authentic reproduction logs according to agreed instructions.
