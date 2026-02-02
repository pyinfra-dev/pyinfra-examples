from pyinfra.api import deploy
from pyinfra.operations import apt, files, server


@deploy("Install common base packages")
def install_base_packages():
    apt.packages(
        name="Install base packages",
        packages=["dstat", "iftop"],
        update=True,
        cache_time=3600,
    )


@deploy("Setup nginx server")
def setup_nginx():
    apt.packages(
        name="Install nginx",
        packages=["nginx"],
        update=True,
        cache_time=3600,
    )

    remove_default_config = files.file(
        name="Remove nginx default config",
        path="/etc/nginx/nginx.conf",
        present=False,
    )

    server.service(
        name="Reload nginx",
        service="nginx",
        reloaded=True,
        _if=remove_default_config.did_change,
    )


def deploy_server():
    install_base_packages()
    setup_nginx()
