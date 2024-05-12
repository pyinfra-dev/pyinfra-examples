inventory = [
    (
        "webserver",
        {
            # SSH details matching the Docker container started in ./docker-start.sh
            "ssh_hostname": "localhost",
            "ssh_port": 9022,
            "ssh_user": "pyinfra",
            "ssh_key": "../docker/insecure_private_key",
            "ssh_known_hosts_file": "/dev/null",
            # This is insecure, don't use in production!
            "ssh_strict_host_key_checking": "off",
            # Flag used in the deploy code to determine what to setup on this host
            "is_web": True,
            "_sudo": True,
        },
    ),
    (
        "dbserver",
        {
            # SSH details matching the Docker container started in ./docker-start.sh
            "ssh_hostname": "localhost",
            "ssh_port": 9023,
            "ssh_user": "pyinfra",
            "ssh_key": "../docker/insecure_private_key",
            "ssh_known_hosts_file": "/dev/null",
            # This is insecure, don't use in production!
            "ssh_strict_host_key_checking": "off",
            # Flag used in the deploy code to determine what to setup on this host
            "is_database": True,
            "_sudo": True,
        },
    ),
]
