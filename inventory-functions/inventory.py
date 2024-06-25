def make_docker_inventory():
    # The function must return a dictionary where the key is the group name
    # and the values are either a list of hosts or a tuple of (hosts, data).
    return {
        "docker_hosts": [
            "@docker/ubuntu:22.04",
        ],
        "docker_hosts_with_data": (
            ["@docker/ubuntu:24.04"],
            {"key": "value"},
        ),
    }
