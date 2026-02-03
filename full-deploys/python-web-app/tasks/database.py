from pyinfra.operations import apt, files, mysql, systemd

apt.packages(
    name="Install mariadb-server",
    packages=["mariadb-server"],
    update=True,
    cache_time=3600,
)

files.line(
    name="Set mariadb bind-address",
    path="/etc/mysql/mariadb.conf.d/50-server.cnf",
    line="bind-address",
    replace="bind-address = 0.0.0.0",
)

systemd.service(
    service="mysql",
    running=True,
    enabled=True,
)

mysql.user(
    name="Create database role",
    user="python-app",
    user_hostname="%",
)

mysql.database(
    name="Create database",
    database="python_app",
    user="python-app",
    user_hostname="%",
)
