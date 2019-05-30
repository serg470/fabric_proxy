#!/usr/bin/env bash

export IMAGE="certbot/certbot"
export NAME="certbot"
export NETWORK="host"
export VOLUME_OPTS="-v /secret/letsencrypt:/etc/letsencrypt \
-v /docker/letsencrypt-docker-nginx/src/letsencrypt/letsencrypt-site:/data/letsencrypt"
export ARGS="certonly --webroot --register-unsafely-without-email --agree-tos \
--webroot-path=/data/letsencrypt --staging -d welespay.ru -d www.welespay.ru"

if [ -z "$RUN_OPTS" ]; then
    export RUN_OPTS="-it --rm"
fi

docker run $RUN_OPTS $VOLUME_OPTS --network $NETWORK --name $NAME $IMAGE $ARGS $*
