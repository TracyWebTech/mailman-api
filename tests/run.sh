#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

DOCKER_IMAGE="tracywebtech/mailman-api"

DOCKER_CMD="docker run -w /srv/mailman-api -v $DIR/../:/srv/mailman-api $DOCKER_IMAGE"

$DOCKER_CMD python setup.py nosetests --with-coverage --cover-package=mailmanapi

$DOCKER_CMD flake8 mailmanapi
