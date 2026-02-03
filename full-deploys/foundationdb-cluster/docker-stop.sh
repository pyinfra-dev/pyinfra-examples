#!/usr/bin/env bash

set -euo pipefail

source "$(realpath "$(realpath "$(dirname "${BASH_SOURCE[0]}")")/../../utils.sh")"

export DOCKER_TEST_NETWORK_NAME="pyinfra-examples-foundationdb-cluster"

docker rm -f pyinfra-example-foundationdb-node-1
docker rm -f pyinfra-example-foundationdb-node-2
docker rm -f pyinfra-example-foundationdb-node-3
docker rm -f pyinfra-example-foundationdb-node-4
docker rm -f pyinfra-example-foundationdb-node-5
docker network rm "$DOCKER_TEST_NETWORK_NAME"
