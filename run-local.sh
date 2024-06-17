# /bin/bash

env_file=".env"

get_env() {
    local key=$1
    local value=null
    if grep -q "^$key=" "$env_file"; then
        value=$(grep "^$key=" "$env_file" | cut -d "=" -f2)
        echo $value
    fi

    return value
}

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

# Chck if network is created, otherwise it'll be created ('custom-isolated-network' as bridge network)
if ! docker network ls | grep -q custom-isolated-network; then
    docker network create -d bridge custom-isolated-network
fi

# Check if the database container 'some-postgres' exists
if ! docker container ls | grep -q custom-isolated-network; then
    if ! docker container ls -a | grep -q custom-isolated-network; then
        postgres_passwd=$(get_env DB_PASS)

        docker run -it --name some-postgres \
        -v data_volume:/var/lib/postgresql/data \
        --network custom-isolated-network --ip 182.18.0.10 \
        -e POSTGRES_PASSWORD=$postgres_passwd -d postgres

    else
        docker start custom-isolated-network
    fi
fi

# Run Application Container


