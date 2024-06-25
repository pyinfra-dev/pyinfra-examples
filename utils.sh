#!/bin/bash

DOCKER_TEST_IMAGE_NAME="pyinfra-examples-docker-test-image"

function ensure_test_container() {
    docker image inspect $DOCKER_TEST_IMAGE_NAME > /dev/null 2>&1 && return 0
    docker_dir=$(realpath "$(realpath "$(dirname "${BASH_SOURCE[0]}")")/.docker")
    cd "$docker_dir" || return 1
    docker build -f Dockerfile-test-server -t $DOCKER_TEST_IMAGE_NAME .
}

function run_test_container() {
    docker run -d "${@:2}" \
        --network "$DOCKER_TEST_NETWORK_NAME" \
        --name "$1" \
        --cgroupns=host \
        --volume /sys/fs/cgroup:/sys/fs/cgroup \
        --tmpfs /run \
        --tmpfs /run/lock \
        --tmpfs /tmp \
        "$DOCKER_TEST_IMAGE_NAME"
}
