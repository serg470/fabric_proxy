#!/usr/bin/env bash

export HOSTNAME=`hostname`

/usr/bin/confd -interval 5 -backend consul -node consul.welespay.ru:80