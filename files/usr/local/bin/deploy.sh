#!/bin/sh

REPO1=$1
export CI_COMMIT_REF_NAME=$2
CI_COMMIT_REF_SLUG=$3
DOCKER_USER=$4
DOCKER_PWD=$5
CI_TOKEN=$6

GITLAB_REG="gitlab.welespay.ru"
export DOCKER_REG="docker.welespay.ru"

COMPOSE_YML="-f /usr/local/bin/docker-compose.yml"
DEFAULT_BRANCH="master" #It will be changed to "develop" later

if [ "$CI_COMMIT_REF_NAME" = "" -o "$CI_COMMIT_REF_SLUG" = "" -o "$CI_TOKEN" = "" ]
then
  echo "Need more arguments"
  exit 1
fi

if [ "$REPO1" = "frontend" ]
then
  export FRONTEND_TAG=$CI_COMMIT_REF_NAME
  REPO2="backend"
  REPO2_ID="5"
  git_tag_exists=$(wget -q https://$GITLAB_REG/api/v4/projects/$REPO2_ID/repository/branches?private_token=$CI_TOKEN -O - | grep -oP '(?<="name":")[^"]+' | grep $CI_COMMIT_REF_NAME | wc -l)
  docker_tag_exists=$(wget --user=$DOCKER_USER --password=$DOCKER_PWD -q https://$DOCKER_REG/v2/$REPO2/tags/list -O - | cut -d [ -f2 | grep $CI_COMMIT_REF_NAME | wc -l)
  if [ "$git_tag_exists" -eq 1 -a "$docker_tag_exists" -eq 1 ]; then
    export BACKEND_TAG=$CI_COMMIT_REF_NAME
  else
    echo "Backend tag $CI_COMMIT_REF_NAME doesn't exist, will use default branch"
    export BACKEND_TAG=$DEFAULT_BRANCH
  fi
elif [ "$REPO1" = "backend" ]; then
  export BACKEND_TAG=$CI_COMMIT_REF_NAME
  REPO2="frontend"
  REPO2_ID="3"
  git_tag_exists=$(wget -q https://$GITLAB_REG/api/v4/projects/$REPO2_ID/repository/branches?private_token=$CI_TOKEN -O - | grep -oP '(?<="name":")[^"]+' | grep $CI_COMMIT_REF_NAME | wc -l)
  docker_tag_exists=$(wget --user=$DOCKER_USER --password=$DOCKER_PWD -q https://$DOCKER_REG/v2/$REPO2/tags/list -O - | cut -d [ -f2 | grep $CI_COMMIT_REF_NAME | wc -l)
  if [ "$git_tag_exists" -eq 1 -a "$docker_tag_exists" -eq 1 ]; then
    export FRONTEND_TAG=$CI_COMMIT_REF_NAME
  else
    echo "Frontend tag $CI_COMMIT_REF_NAME doesn't exist, will use default branch"
    export FRONTEND_TAG=$DEFAULT_BRANCH
  fi
else
  echo "Unknown repositry"
  exit 1
fi

docker network disconnect $CI_COMMIT_REF_NAME_default proxy

if  [ ! -h /dev/mapper/secret ] ; then
  printf "Secret not mounted\n"
elif [ -d /secret/letsencrypt/live/$CI_COMMIT_REF_SLUG.sandbox.welespay.ru ] ; then
  printf "Certificate exists, no need to request.\n"
else
  printf "Certificate doesn't exist, reqesting...\n"
  service nginx stop
  certbot certonly --standalone --preferred-challenges http --config-dir /secret/letsencrypt --agree-tos \
   -m helen.shafranova@gmail.com -d $CI_COMMIT_REF_SLUG.sandbox.welespay.ru
  service nginx start
fi

if [ "$COMMIT_REF_NAME" = "master" ]
then
  COMPOSE_YML="$COMPOSE_YML -f /usr/local/bin/docker-compose.master.yml"
#  export MASTER_PORT=$(docker port frontend_$CI_COMMIT_REF_NAME 80 | cut -d : -f2)
fi


docker-compose $COMPOSE_YML -p $CI_COMMIT_REF_NAME down && docker-compose $COMPOSE_YML pull && docker-compose $COMPOSE_YML -p $CI_COMMIT_REF_NAME up -d


docker network connect $CI_COMMIT_REF_NAME_default proxy

docker exec -i redis redis-cli del frontend:$CI_COMMIT_REF_SLUG.sandbox.welespay.ru
#docker exec -i redis redis-cli del frontend:$CI_COMMIT_REF_SLUG-back.sandbox.welespay.ru

docker exec -i redis redis-cli rpush frontend:$CI_COMMIT_REF_SLUG.sandbox.welespay.ru $CI_COMMIT_REF_NAME
docker exec -i redis redis-cli rpush frontend:$CI_COMMIT_REF_SLUG.sandbox.welespay.ru http://frontend_$CI_COMMIT_REF_NAME:80

#docker exec -i redis redis-cli rpush frontend:$CI_COMMIT_REF_SLUG-back.sandbox.welespay.ru $CI_COMMIT_REF_NAME
#docker exec -i redis redis-cli rpush frontend:$CI_COMMIT_REF_SLUG-back.sandbox.welespay.ru http://backend_$CI_COMMIT_REF_NAME:8080