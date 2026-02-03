# Example: FoundationDB Cluster

This example deploys a 5-node FoundationDB cluster using pyinfra and Docker containers. Usage:

```sh
# Start Docker containers
./docker-start.sh

# Run pyinfra against them
pyinfra inventories/docker.py deploy_foundationdb.py

# Verify the cluster is health
ssh -p 9022 -i ../../.docker/insecure_private_key pyinfra@localhost
fdbcli --exec "status details"

# Delete Docker containers
./docker-stop.sh
```

## File Layout

```
foundationdb-cluster/
├── deploy_foundationdb.py       # Main deployment entry point
├── tasks/
│   ├── install.py               # Package download and installation
│   ├── configure.py             # Config files and service management
│   └── bootstrap.py             # Cluster initialization
├── templates/
│   └── foundationdb.conf.j2     # fdbmonitor configuration template
├── group_data/
│   └── all.py                   # Shared settings for all hosts
└── inventories/
    └── docker.py                # Docker inventory with host data
```
