#!/bin/bash

docker image prune -f

if [ "$1" = "staging" ]; then
    docker-compose -f docker-compose.staging.yml build
    docker-compose -f docker-compose.staging.yml stop
    docker-compose -f docker-compose.staging.yml up -d
fi

if [ "$1" = "release" ]; then
    docker-compose -f docker-compose.prod.yml build
    docker-compose -f docker-compose.prod.yml stop
    docker-compose -f docker-compose.prod.yml up -d
fi
