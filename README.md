# pyinfra Examples

A set of documented & tested pyinfra deploys.

## Full Deploys

These are complete examples along with Docker test containers (acting as servers accessible via SSH)
and scripts to execute them. These deploys are all tested as part of CI.

### [`python-web-app`](./full-deploys/python-web-app)

Simple: deploys two servers: one database and one web running a Python app fetched using Git.

### [`foundationdb-cluster`](./full-deploys/foundationdb-cluster)

Advanced: sets up a five node FoundationDB cluster from scratch. Uses runtime callbacks to bootstrap.

## Snippets

Shorter collections of code snippets that don't always function on their own but demonstrate various
parts of pyinfra functionality.

### [`deploy-functions`](./snippets/deploy-functions)

Shows how to execute Python functions as operations directly from the CLI.

### [`inventory-functions`](./snippets/inventory-functions)

Look at using Python functions, and external packages, to generate inventory.

### [`nested-operations`](./snippets/nested-operations)

Execute operations using output or results of other operations.
