#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

if [ -e .env ]; then
	source .env
fi
echo $AUDIOSERVICE_DOCKER_IMAGE_LOCAL

docker build -t $AUDIOSERVICE_DOCKER_IMAGE_LOCAL:$AUDIOSERVICE_IMAGE_VERSION . 
