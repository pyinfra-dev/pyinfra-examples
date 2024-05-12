from os import path

from pyinfra import host, local
from pyinfra.operations import apt, files, git, pip, server, systemd

apt.packages(
    name="Install required apt packages",
    packages=["python3", "python3-dev", "python3-pip", "git"],
    update=True,
    cache_time=3600,
)


if host.data.get("is_database"):
    local.include(filename=path.join("tasks", "database.py"))


if host.data.get("is_web"):
    local.include(filename=path.join("tasks", "web.py"))
