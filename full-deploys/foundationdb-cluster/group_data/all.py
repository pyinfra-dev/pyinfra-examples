fdb_version = "7.3.61"
fdb_port = 4500
fdb_coordinators = [
    f"pyinfra-example-foundationdb-node-1.pyinfra-examples-foundationdb-cluster:{fdb_port + 1}",
    f"pyinfra-example-foundationdb-node-2.pyinfra-examples-foundationdb-cluster:{fdb_port + 1}",
    f"pyinfra-example-foundationdb-node-3.pyinfra-examples-foundationdb-cluster:{fdb_port + 1}",
]

fdb_cluster_name = "docker"
fdb_cluster_id = "pyinfra123456789"  # Random cluster identifier
fdb_redundancy_mode = "triple"
fdb_storage_engine = "ssd-redwood-1"
