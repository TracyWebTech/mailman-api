#!/bin/bash

if [ "$(uname)" == 'Darwin' ]; then
    eval "$(boot2docker shellinit)"
fi

status=0

GREEN="\033[32m"
RED="\033[31m"
COLOR_OFF='\033[0m'

function run {
    echo $@

    echo "#!/bin/bash" > /tmp/test-script.sh
    echo $@ >> /tmp/test-script.sh
    chmod +x /tmp/test-script.sh
    /tmp/test-script.sh

    exit=$?
    msg="The program \"$@\" exited with $exit."

    if [[ $exit -eq 0 ]]; then
        echo -ne $GREEN
    else
        echo -ne $RED
        status=1
    fi
    echo $msg
    echo -e $COLOR_OFF
}

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

DOCKER_IMAGE="tracywebtech/mailman-api-test"

DOCKER_CMD="docker run -w /srv/mailman-api -v $DIR/../:/srv/mailman-api $DOCKER_IMAGE"

run $DOCKER_CMD bash -c "'python setup.py nosetests --with-coverage --cover-package=mailmanapi --cover-erase'"
run $DOCKER_CMD flake8 mailmanapi

exit $status
