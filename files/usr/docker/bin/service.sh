#!/usr/bin/env bash

export

function finish {
  docker stop -t 290 $NAME
}
trap finish EXIT

docker run $RUN_OPTS $VOLUME_OPTS $ENV_OPTS $HOSTNAME_OPTS --network $NETWORK --name $NAME $IMAGE $ARGS $*
