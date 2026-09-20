# Exercise 04: Docker Networking with Multiple Containers

## Objective
Understand Docker user-defined bridge networking, container DNS resolution, multi-tier application architecture, and inter-container communication across isolated network namespaces.

## Scenario
Deploying a multi-container web application stack consisting of:
1. Python Flask REST API (`flask-api` on port 5001)
2. MySQL database (`mysql:latest`)
3. Redis cache (`redis:latest`)
All three containers communicate securely over a custom bridge network `my-bridge-net` without exposing internal database or cache ports to the public host.

## Tools Used
- **Docker Engine** (28.2.2)
- **Python 3.9-slim / Flask 2.0.1 / Werkzeug 2.2.3**
- **MySQL Official Image** (`mysql:latest`)
- **Redis Official Image** (`redis:latest`)
- **iputils-ping**

## Visual Verification & Interface Screenshots

### 1. Terminal Interface & Execution Output
![Terminal Interface & Command Output](screenshot-terminal-interface.png)

### 2. Website & Web Service Interface
![Website Interface Screenshot](screenshot-website-interface.png)
## Implementation Details
1. **Network Creation**: Created a custom bridge network `my-bridge-net` with driver `bridge` and verified subnet `172.18.0.0/16`.
2. **Container Build**: Built `flask-api` using `Dockerfile` installing Flask and utilities.
3. **Container Launch**:
   - `mysql` attached to `my-bridge-net` with environment variable `MYSQL_ROOT_PASSWORD`.
   - `redis` attached to `my-bridge-net`.
   - `flask` attached to `my-bridge-net` with host port mapping `-p 5001:5001`.
4. **DNS & Connectivity Testing**:
   - Executed `ping -c 3 mysql` from inside the `flask` container.
   - Executed `ping -c 3 redis` from inside the `flask` container.
   - Performed HTTP GET on `/about` returning JSON description.
5. **Clean Up**: Stopped and removed all 3 containers and deleted the bridge network.

## Commands Executed
```bash
docker network create --driver bridge my-bridge-net
docker network ls
docker network inspect my-bridge-net
docker build -t flask-api .
docker run -d --name mysql --net=my-bridge-net -e MYSQL_ROOT_PASSWORD=labpass mysql:latest
docker run -d --name redis --net=my-bridge-net redis:latest
docker run -d --name flask --net=my-bridge-net -p 5001:5001 flask-api
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
docker network inspect my-bridge-net --format '{{range .Containers}}{{.Name}} -> {{.IPv4Address}}{{println}}{{end}}'
docker exec flask ping -c 3 mysql
docker exec flask ping -c 3 redis
docker exec flask python -c "import urllib.request;print(urllib.request.urlopen('http://localhost:5001/about').read().decode())"
docker stop mysql redis flask && docker rm mysql redis flask
docker network rm my-bridge-net
```

## Real Terminal Output & Verification
```text
$ docker network inspect my-bridge-net --format '{{range .Containers}}{{.Name}} -> {{.IPv4Address}}{{println}}{{end}}'
flask -> 172.18.0.4/16
mysql -> 172.18.0.2/16
redis -> 172.18.0.3/16

$ docker exec flask ping -c 3 mysql
PING mysql (172.18.0.2) 56(84) bytes of data.
64 bytes from mysql.my-bridge-net (172.18.0.2): icmp_seq=1 ttl=64 time=0.222 ms
64 bytes from mysql.my-bridge-net (172.18.0.2): icmp_seq=2 ttl=64 time=0.139 ms
64 bytes from mysql.my-bridge-net (172.18.0.2): icmp_seq=3 ttl=64 time=0.208 ms
--- mysql ping statistics ---
3 packets transmitted, 3 received, 0% packet loss

$ docker exec flask ping -c 3 redis
PING redis (172.18.0.3) 56(84) bytes of data.
64 bytes from redis.my-bridge-net (172.18.0.3): icmp_seq=1 ttl=64 time=0.115 ms
64 bytes from redis.my-bridge-net (172.18.0.3): icmp_seq=2 ttl=64 time=0.220 ms
64 bytes from redis.my-bridge-net (172.18.0.3): icmp_seq=3 ttl=64 time=0.119 ms
--- redis ping statistics ---
3 packets transmitted, 3 received, 0% packet loss

$ docker exec flask python -c "import urllib.request;print(urllib.request.urlopen('http://localhost:5001/about').read().decode())"
{
  "description": "This is a simple REST API built with Flask.", 
  "name": "Simple REST API", 
  "version": "1.0"
}
```

## Errors Encountered & Fixes Applied
1. **Dependency Incompatibility (Flask 2.0.1 vs Werkzeug 3.x)**:
   - *Error*: `ImportError: cannot import name 'url_quote' from 'werkzeug.urls'`.
   - *Cause*: Unpinned Werkzeug resolved to version 3.1.9, which removed legacy APIs expected by Flask 2.0.1.
   - *Fix*: Pinned `Werkzeug==2.2.3` in `requirements.txt`.
2. **Missing Ping Utility in Slim Base Image**:
   - *Error*: `bash: ping: command not found`.
   - *Cause*: `python:3.9-slim` omits network diagnostics utilities.
   - *Fix*: Added `RUN apt-get update && apt-get install -y iputils-ping` to the Dockerfile.
3. **MySQL Root Password Requirement**:
   - *Error*: MySQL container terminates immediately if no password or blank password option is set.
   - *Fix*: Supplied `-e MYSQL_ROOT_PASSWORD=labpass` when launching `mysql:latest`.

## Result
**COMPLETE & VERIFIED**. All three tiers successfully communicated via Docker's embedded DNS on the custom bridge network with 0% packet loss and verified REST output.
