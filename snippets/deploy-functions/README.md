# Example: Deploy Functions

Groups of operations can be defined within a Python function that can be re-used. These can be called directly on the command line. Any functions can be called, including ones with with `@deploy` and `@operation` decorators.

```sh
# Run deploy functions
pyinfra @docker/ubuntu:22.04 deploy.install_base_packages
pyinfra @docker/ubuntu:22.04 deploy.setup_nginx

# Run the combined, undecorated function
pyinfra @docker/ubuntu:22.04 deploy.deploy_server
```

## Why use the `@deploy` decorator at all?

The `@deploy` decorator is designed for packages as a way to wrap groups of operations together. It also serves as a great way to group and name your own operation code into re-usable functions just like this example.
