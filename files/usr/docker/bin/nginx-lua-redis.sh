#!/usr/bin/env bash

export IMAGE_REDIS="redis"
export NAME_REDIS="redis"

export IMAGE="ermlab/nginx-lua-proxy"
export NAME="nginx-lua-proxy"

export ARGS=""

if [ -z "$RUN_OPTS" ]; then
    export RUN_OPTS="--rm"
fi

docker run -d $RUN_OPTS --name $NAME_REDIS $IMAGE_REDIS
docker run -d $RUN_OPTS --link $NAME_REDIS -p 9090:80 --name $NAME $IMAGE
