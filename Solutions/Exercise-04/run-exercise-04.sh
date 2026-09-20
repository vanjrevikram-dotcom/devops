#!/bin/bash
# Exercise 4: Docker Networking with multiple containers (host Docker Engine in WSL)
cd "$(dirname "$0")"
source ../common/run.sh

# clean leftovers from earlier runs
docker rm -f mysql redis flask >/dev/null 2>&1; docker network rm my-bridge-net >/dev/null 2>&1

# Task 1-3
run docker network create --driver bridge my-bridge-net
run docker network ls
run docker network inspect my-bridge-net
# Task 4
run docker build -t flask-api .
# mysql:latest refuses to start without a root-password option, so one is supplied.
run docker run -d --name mysql --net=my-bridge-net -e MYSQL_ROOT_PASSWORD=labpass mysql:latest
run docker run -d --name redis --net=my-bridge-net redis:latest
run docker run -d --name flask --net=my-bridge-net -p 5001:5001 flask-api
sleep 15
run "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'"
run docker logs flask
run "docker network inspect my-bridge-net --format '{{range .Containers}}{{.Name}} -> {{.IPv4Address}}{{println}}{{end}}'"
# Task 5: test connectivity from inside the flask container
run docker exec flask ping -c 3 mysql
run docker exec flask ping -c 3 redis
run "docker exec flask python -c \"import urllib.request;print(urllib.request.urlopen('http://localhost:5001/about').read().decode())\""
# Task 6: clean up
run "docker stop mysql redis flask && docker rm mysql redis flask"
run docker network rm my-bridge-net
