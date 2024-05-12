#!/usr/bin/env bash

set -euo pipefail

source "$(realpath "$(realpath "$(dirname "${BASH_SOURCE[0]}")")/../utils.sh")"

docker rm -f pyinfra-example-python-web-app-webserver
docker rm -f pyinfra-example-python-web-app-dbserver
docker network rm "$DOCKER_TEST_NETWORK_NAME"
