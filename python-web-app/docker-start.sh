#!/usr/bin/env bash

set -euo pipefail

source "$(realpath "$(realpath "$(dirname "${BASH_SOURCE[0]}")")/../utils.sh")"
ensure_test_container

echo "Create Docker network..."
docker network create "$DOCKER_TEST_NETWORK_NAME"

echo "Starting Docker containers..."
run_test_container pyinfra-example-python-web-app-webserver -p 9022:22 -p 5000:5000
run_test_container pyinfra-example-python-web-app-dbserver -p 9023:22

echo
echo "Doker containers are now ready to run the pyinfra deploy, you can do this by running:"
echo
echo "    pyinfra inventories/docker.py deploy.py"
echo
echo "Once complete, don't forget to remove the Docker containers and network using the ./docker-stop.sh script!"
