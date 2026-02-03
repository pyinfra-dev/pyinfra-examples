"""
FoundationDB cluster bootstrap tasks.
Initializes the cluster configuration (runs only on bootstrap node).
"""

import json

from pyinfra import host
from pyinfra.operations import python, server


def bootstrap_cluster():
    """
    Initialize the FoundationDB cluster if not already configured.
    """

    # Note: this command will take a while to execute because it has to timeout trying to get the
    # status, I have yet to find a quick way to do this check.
    check_status = server.shell(
        name="Check cluster status",
        commands="fdbcli --no-status --exec 'status json' || true",
    )

    status_json = json.loads(check_status.stdout)
    status_client = status_json.get("client", {})

    # Note this is, so far, the best way I can tell to determine if FDB cluster is bootstrapped,
    # despite that for production I'd recommend any configure new commands are executed by hand.
    if (
        status_client.get("coordinators", {}).get("quorum_reachable") is True
        and status_client.get("database_status", {}).get("available") is False
    ):
        redundancy_mode = host.data.fdb_redundancy_mode
        storage_engine = host.data.fdb_storage_engine
        server.shell(
            name="Configure cluster",
            commands=f"fdbcli --no-status --exec 'configure new {redundancy_mode} {storage_engine}'",
        )


# Use python.call to execute the bootstrap function at runtime
# This ensures proper state checking during deployment
python.call(
    name="Bootstrap FoundationDB cluster",
    function=bootstrap_cluster,
)
