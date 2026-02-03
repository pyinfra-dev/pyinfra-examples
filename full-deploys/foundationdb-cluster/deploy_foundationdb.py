"""
FoundationDB Cluster Deployment

Deploys a 5-node FoundationDB cluster with:
- 3 coordinator nodes (nodes 1-3) for quorum
- 5 storage nodes (all nodes)
- Triple redundancy mode

Usage:
    pyinfra inventories/docker.py deploy_foundationdb.py
"""

from os import path

from pyinfra import host, local
from pyinfra.operations import apt

# Update apt cache (with 1 hour cache time to avoid unnecessary updates)
apt.packages(
    name="Update apt cache",
    packages=["wget"],
    cache_time=3600,
    update=True,
)

# Install FoundationDB packages
local.include(
    filename=path.join("tasks", "install.py"),
)

# Configure FoundationDB (config files, cluster file, service)
local.include(
    filename=path.join("tasks", "configure.py"),
)

# Bootstrap cluster (only on the designated bootstrap node)
if host.data.get("is_bootstrap_node"):
    local.include(
        filename=path.join("tasks", "bootstrap.py"),
    )
