#!/usr/bin/env bash

export IMAGE="consul"
export NAME="consul"
export NETWORK="host"
export VOLUME_OPTS="-v /var/docker/consul/data:/consul/data -v /secret/consul/encrypt.json:/secret/consul/encrypt.json:ro"
export HN=`hostname`
export CONSUL_EXT=`ip addr show eth0 | grep -oP 'inet \K\S[0-9.]+'`
export BOOTSTRAP_NODE=i01

if [ "$HN" == "i01" ]; then
 export ARGS="agent -server -client 127.0.0.1 -ui -bootstrap -config-file=/secret/consul/encrypt.json -bind=$CONSUL_EXT"
else
 export ARGS="agent -server -client 127.0.0.1 -ui --retry-join $BOOTSTRAP_NODE.welespay.ru -bind 0.0.0.0  \
             -advertise $CONSUL_EXT -bootstrap-expect 3 -config-file=/secret/consul/encrypt.json"
fi
export ENV='-e CONSUL_CLIENT_INTERFACE=lo'

if [ -z "$RUN_OPTS" ]; then
    export RUN_OPTS="--rm"
fi

echo "docker run $RUN_OPTS $ENV $VOLUME_OPTS --network $NETWORK --name $NAME $IMAGE $ARGS $*"
docker run $RUN_OPTS $ENV $VOLUME_OPTS --network $NETWORK --name $NAME $IMAGE $ARGS $*
