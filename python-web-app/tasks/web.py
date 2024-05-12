from pyinfra.operations import files, git, pip, server, systemd

server.user(
    name="Create python-app user",
    user="python-app",
)

git.repo(
    name="Clone the app repository",
    src="https://github.com/Fizzadar/Flask-Web-App-Tutorial.git",
    dest="/opt/flask-web-app",
    branch="main",
)

pip.packages(
    name="install pip packages",
    requirements="/opt/flask-web-app/requirements.txt",
)

generate_unit = files.template(
    name="Generate systemd unit",
    src="templates/python-app.j2.service",
    dest="/etc/systemd/system/python-app.service",
)

systemd.service(
    name="Start & enable python-app.service",
    service="python-app.service",
    running=True,
    enabled=True,
    # If we change the systemd unit, restart it (if running already)
    restarted=generate_unit.will_change,
    # If we change the systemd unit run daemon-reload before handling the service
    daemon_reload=generate_unit.will_change,
)
