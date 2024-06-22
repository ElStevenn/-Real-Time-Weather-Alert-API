#!/bin/bash

env_file=".env"

get_env() {
    local key=$1
    local value=null
    if grep -q "^$key=" "$env_file"; then
        value=$(grep "^$key=" "$env_file" | cut -d "=" -f2-)
        echo "$value"
    else
        echo "Key does not exist."
    fi
}

export DOCKER_HOST=unix:///run/docker.sock

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed, please install it."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "docker-compose isn't installed, please install it."
    exit 1
fi

# Check if the volume 'data_volume' is created
if ! docker volume ls | grep -q data_volume; then
    docker volume create data_volume
fi

# Check if network is created, otherwise create it ('custom-isolated-network' as bridge network)
if ! docker network ls | grep -q custom-isolated-network; then
    docker network create -d bridge custom-isolated-network
fi

# Check if the database container 'db-container' exists
if ! docker container ls | grep -q db-container; then
    if ! docker container ls -a | grep -q db-container; then
        postgres_passwd=$(get_env DB_PASS)

        docker run -it --name db-container \
        -v data_volume:/var/lib/postgresql/data \
        --network custom-isolated-network --ip 182.18.0.10 \
        -e POSTGRES_PASSWORD=$postgres_passwd -d postgres

    else
        docker start db-container
    fi
fi

# Build Application Image
if ! docker container ls | grep -q weather-app; then
    docker build -t my-application-image .
fi

# Run Application Container
if ! docker container ls -a | grep -q weather-app; then
    docker run -it --name weather-app \
        --network custom-isolated-network \
        -p 8000:8000 \
        -e DB_HOST=182.18.0.10 \
        -e DB_PASS=$(get_env DB_PASS) \
        -d my-application-image
fi

# Display logs
docker logs -f weather-app
