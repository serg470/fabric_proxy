#!/usr/bin/env bash

export IMAGE="docker.welespay.ru/telegraf:current"
export NAME="telegraf"
export NETWORK="host"
export ENV="-e HOST_ROOT_FS=/rootfs"
export VOLUME_OPTS="-v /var/run/docker.sock:/var/run/docker.sock:ro \
                    -v /:/rootfs:ro \
                    -v /usr/docker/conf/telegraf/telegraf.conf:/etc/telegraf/telegraf.conf:ro"
export ARGS=""

if [ -z "$RUN_OPTS" ]; then
    export RUN_OPTS="--rm"
fi

docker run $RUN_OPTS $VOLUME_OPTS $ENV --hostname=`hostname` --network $NETWORK --name $NAME $IMAGE $ARGS $*

