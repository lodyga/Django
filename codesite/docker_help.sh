# List all running containers
docker ps
docker container ls

# List images
docker images      

# Execute a command in a running container
docker exec -it CONTAINER_ID/NAME bash
docker exec -it judge0-v1131-workers-1 bash
docker exec -it judge0-v1131-server-1 bash
docker exec -it judge0-v1131-db-1 psql -U judge0 -d judge0

# Build or rebuild services
docker compose build

# List containers
docker compose ps

# Create and start containers
docker compose up -d
docker compose -f judge0-v1.13.1/docker-compose.yml up -d

# Stop and remove containers, networks
docker compose down -v

# Restart service containers
docker compose restart

# build/rebuild a container, where Dockerfile is
$ docker build -t <name>:<tag> .
$ docker build -t lodyga/codesite:latest .
$ docker build -t judge0-custom:1.13.1 .

# push container to dockerhub
$ docker push lodyga/codesite:latest

# run a container
$ docker run --rm -d -p 8000:8000/tcp lodyga/codesite:latest
$ docker run --rm -it judge0-custom:1.13.1 bash

# Remove one or more images
docker rmi IMAGE ID
docker rmi REPOSITORY:TAG

# Stop one or more running containers
docker stop <container_id>

# Remove one or more containers
docker rm <container_id>

# List volumes
docker volume ls

# Remove unused local volumes
docker volume prune

# Inspect the specific volume
docker volume inspect judge0-v1131_data

# Show server log
docker logs --tail 200 judge0-v1131_server_1

# login
$ docker login
