# Example: Deploy functions

Groups of operations can be defined within a Python function that can be re-used. These can be called directly on the command line.

```sh
# Run deploy functions
pyinfra @docker/ubuntu:22.04 deploy.install_base_packages
pyinfra @docker/ubuntu:22.04 deploy.setup_nginx

# Run the combined, undecorated function
pyinfra @docker/ubuntu:22.04 deploy.deploy_server
```
