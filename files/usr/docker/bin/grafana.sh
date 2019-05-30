#!/usr/bin/env bash

export IMAGE="grafana/grafana:latest"
export NAME="grafana"
export NETWORK="host"
export ENV="-e GF_SERVER_HTTP_ADDR=127.0.0.1 -e GF_SERVER_HTTP_PORT=8085"
export VOLUME_OPTS="-v  /var/lib/grafana:/var/lib/grafana"
export ARGS=""

if [ -z "$RUN_OPTS" ]; then
    export RUN_OPTS="--rm"
fi

docker run $RUN_OPTS $VOLUME_OPTS $ENV --network $NETWORK --name $NAME $IMAGE $ARGS $*
