inventory = (
    # Individual host list with host-specific data
    [
        ("webserver", {"ssh_port": 9022, "is_web": True}),
        ("dbserver", {"ssh_port": 9023, "is_database": True}),
    ],
    # Shared data for all the hosts in the group
    {
        "_sudo": True,  # use sudo for all operations
        # SSH details matching the Docker container started in ./docker-start.sh
        "ssh_hostname": "localhost",
        "ssh_user": "pyinfra",
        "ssh_key": "../.docker/insecure_private_key",
        "ssh_known_hosts_file": "/dev/null",
        # This is insecure, don't use in production!
        "ssh_strict_host_key_checking": "off",
    },
)
