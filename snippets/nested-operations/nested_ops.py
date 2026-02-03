import requests
from pyinfra.operations import apt, python, server

# Install some service X...
apt.packages(...)


def register_device():
    get_idx = server.shell(commands="get identifier from service X")

    # Save the service X identifier in some external system
    requests.post("", get_idx.stdout)


python.call(function=register_device)
