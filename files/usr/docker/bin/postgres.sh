#!/usr/bin/env bash

export IMAGE="postgres:9.6.7-alpine"
export NAME="postgres"
export NETWORK="host"
export ENV_OPTS="-e POSTGRES_PASSWORD_FILE=/secret/postgres.passwd"
export VOLUME_OPTS="-v /var/docker/posgres/data:/var/lib/postgresql/data -v /secret/postgres:/secret -v /usr/docker/conf/postgres/:/etc/postgresql/ -v /striped/data/postgres/archive:/var/lib/postgresql/data/archive -v /striped/logs/postgres:/var/lib/postgresql/data/pg_log"
export ARGS="-c config_file=/etc/postgresql/postgresql.conf"

if [ -z "$RUN_OPTS" ]; then
    export RUN_OPTS="--rm"
fi

docker run $RUN_OPTS $VOLUME_OPTS $ENV_OPTS --network $NETWORK --name $NAME $IMAGE $ARGS $*
