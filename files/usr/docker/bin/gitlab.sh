#!/usr/bin/env bash
  
export IMAGE="gitlab/gitlab-ce"
export NAME="gitlab"
export NETWORK="host"
export VOLUME_OPTS="-v /mirror/gitlab/etc:/etc/gitlab -v /mirror/gitlab/data:/var/opt/gitlab -v /mirror/gitlab/log:/var/log/gitlab"
export ARGS=""

if [ -z "$RUN_OPTS" ]; then
    export RUN_OPTS="--rm"
fi

docker run $RUN_OPTS $VOLUME_OPTS -p 8086:80 -p 8087:443 -p 8022:22 --name $NAME $IMAGE $ARGS $*
