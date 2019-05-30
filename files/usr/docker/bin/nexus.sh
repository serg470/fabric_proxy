#!/usr/bin/env bash

export IMAGE="sonatype/nexus3"
export NAME="nexus"
export NETWORK="host"
export VOLUME_OPTS="-v /mirror/nexus/data:/nexus-data"
export ARGS=""

if [ -z "$RUN_OPTS" ]; then
    export RUN_OPTS="--rm"
fi

docker run $RUN_OPTS $VOLUME_OPTS --network $NETWORK --name $NAME $IMAGE $ARGS $*