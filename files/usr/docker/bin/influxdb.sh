#!/usr/bin/env bash

export IMAGE="influxdb:alpine"
export NAME="influxdb"
export NETWORK="host"
export VOLUME_OPTS="-v /var/lib/influxdb:/var/lib/influxdb \
                    -v /usr/docker/conf/influxdb/influxdb.conf:/etc/influxdb/influxdb.conf:ro"
export ARGS=""

if [ -z "$RUN_OPTS" ]; then
    export RUN_OPTS="--rm"
fi

docker run $RUN_OPTS $VOLUME_OPTS --network $NETWORK --name $NAME $IMAGE $ARGS $*