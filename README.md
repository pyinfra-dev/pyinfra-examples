# pyinfra Examples

A set of documented & tested pyinfra deploys.

## Getting started

This repository is self-hosted with [uv](https://docs.astral.sh/uv/) — no global pyinfra install required. After installing uv:

```sh
# Create the virtualenv and install the pinned pyinfra version from uv.lock
uv sync

# Run pyinfra via uv (picks up the locked pyinfra automatically)
uv run pyinfra --version
```

All example commands below can be prefixed with `uv run` — e.g. `uv run pyinfra inventories/docker.py deploy.py`.

## Complete Deploys

### [`python-web-app`](./python-web-app)

Simple: deploys two servers: one database and one web running a Python app fetched using Git.

## Specific Features

### [`deploy-functions`](./deploy-functions)

Shows how to execute Python functions as operations directly from the CLI.

### [`inventory-functions`](./inventory-functions)

Look at using Python functions, and external packages, to generate inventory.
