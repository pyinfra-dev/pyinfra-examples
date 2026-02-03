"""
FoundationDB configuration tasks.
Manages config files, cluster file, and service state.
"""

from io import StringIO

from pyinfra import host
from pyinfra.operations import files, systemd

# Build the cluster file connection string
# Format: description:id@coordinator1,coordinator2,coordinator3
cluster_description = host.data.fdb_cluster_name
cluster_id = host.data.fdb_cluster_id
coordinators = ",".join(host.data.fdb_coordinators)
cluster_string = f"{cluster_description}:{cluster_id}@{coordinators}"

# Ensure data directory exists with correct permissions
files.directory(
    name="Ensure FDB data directory exists",
    path="/var/lib/foundationdb/data",
    user="foundationdb",
    group="foundationdb",
    mode="0755",
    present=True,
)

# Ensure log directory exists with correct permissions
files.directory(
    name="Ensure FDB log directory exists",
    path="/var/log/foundationdb",
    user="foundationdb",
    group="foundationdb",
    mode="0755",
    present=True,
)

# Deploy foundationdb.conf from template
config_changed = files.template(
    name="Deploy foundationdb.conf",
    src="templates/foundationdb.conf.j2",
    dest="/etc/foundationdb/foundationdb.conf",
    user="root",
    group="root",
    mode="0644",
    fdb_port=host.data.fdb_port,
    is_coordinator=host.data.get("is_coordinator", False),
)

# Deploy cluster file
cluster_file_changed = files.put(
    name="Deploy fdb.cluster file",
    src=StringIO(cluster_string),
    dest="/etc/foundationdb/fdb.cluster",
    user="foundationdb",
    group="foundationdb",
    mode="0644",
)

# Ensure service is enabled and started
systemd.service(
    name="Enable and start foundationdb service",
    service="foundationdb",
    running=True,
    enabled=True,
)

# Restart service if config changed
systemd.service(
    name="Restart foundationdb if config changed",
    service="foundationdb",
    restarted=True,
    _if=lambda: config_changed.did_change() or cluster_file_changed.did_change(),
)
