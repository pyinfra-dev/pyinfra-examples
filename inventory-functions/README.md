# Example: Inventory Functions

Like operations inventories can also be defined using Python functions. This brings incredible flexibility allowing you to pull data from external systems using Python's package ecosystem to generate pyinfra inventories. The `inventory.py` contains a triaival example of this which can be executed like so:

```sh
pyinfra inventory.make_docker_inventory exec uptime
```

There are no restrictions on what the function itself does, so you can call basically anything Python packages provide access to. Some ideas:

+ load inventory from AWS/Hetzner/DigitalOcean APIs
+ pull in secrets from a vault or password store
