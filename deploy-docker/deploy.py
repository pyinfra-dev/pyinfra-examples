from pyinfra import host, config
from pyinfra import local, logger
from pyinfra.operations import apt, files, server as operations_server
from pyinfra.facts import deb, server as facts_server
from io import StringIO
import json

# host.data._shell_executable = "bash"

fact_deb_arch = host.get_fact(deb.DebArch)
fact_linux_distribution = host.get_fact(facts_server.LinuxDistribution)

"""defaults/main.yml"""

# Edition can be one of: 'ce' (Community Edition) or 'ee' (Enterprise Edition).
docker_edition = "ce"
docker_packages = [
    f"docker-{docker_edition}",
    f"docker-{docker_edition}-cli",
    f"docker-{docker_edition}-rootless-extras",
    "containerd.io",
    "docker-buildx-plugin",
]
docker_packages_state = True

distribution = fact_linux_distribution["name"].strip()
distribution_release = fact_linux_distribution["release_meta"]["CODENAME"].strip()

# Service options.
docker_service_manage = True
docker_service_state = "started"
docker_service_enabled = True
docker_service_start_command = ""  # TODO: 'Docker service ExecStart command' not yet implemented.
docker_restart_handler_state = "restarted"

# Docker Compose Plugin options.
docker_install_compose_plugin = True
docker_compose_package = "docker-compose-plugin"
docker_compose_package_state = "present"

# Docker Compose options.
docker_install_compose = True
docker_compose_version = "v2.32.1"
docker_compose_arch = fact_deb_arch
docker_compose_url = f"https://github.com/docker/compose/releases/download/{docker_compose_version}/docker-compose-linux-{docker_compose_arch}"
docker_compose_path = "/usr/local/bin/docker-compose"

# Enable repo setup
docker_add_repo = True

# Docker repo URL.
docker_repo_url = "https://download.docker.com/linux"

# Used only for Debian/Ubuntu/Pop!_OS/Linux Mint. Switch 'stable' to 'nightly' if needed.
docker_apt_release_channel = "stable"
# docker_apt_ansible_distribution is a workaround for Ubuntu variants which can't be identified as such by Ansible,
# and is only necessary until Docker officially supports them.
docker_apt_ansible_distribution = f"{'ubuntu' if distribution in ['Pop!_OS', 'Linux Mint'] else distribution}"
# docker_apt_repo_url can be changed if you need to point at an internal mirror or cache.
docker_apt_repo_url = f"{docker_repo_url}/{docker_apt_ansible_distribution.lower()}"
docker_apt_gpg_key = f"{docker_repo_url}/{docker_apt_ansible_distribution.lower()}/gpg"
docker_apt_filename = "docker"

# Used only for RedHat/CentOS/Fedora.
docker_yum_repo_url = f"{docker_repo_url}/{'fedora' if distribution == 'Fedora' else 'rhel' if distribution == 'RedHat' else 'centos'}/docker-{docker_edition}.repo"
docker_yum_repo_enable_test = "0"
docker_yum_gpg_key = f"{docker_repo_url}/{'fedora' if distribution == 'Fedora' else 'rhel' if distribution == 'RedHat' else 'centos'}/gpg"

# A list of users who will be added to the docker group.
docker_users = ["map"]

# Docker daemon options as a dict
docker_daemon_options = {
    "debug": True,
}

if distribution == "Alpine":  # vars/Alpine.yml
    docker_packages = ["docker"]
    docker_compose_package = "docker-cli-compose"
elif distribution == "Archlinux":  # vars/Archlinux.yml
    docker_packages = ["docker"]
    docker_compose_package = "docker-compose"
elif distribution in ["Debian", "Ubuntu"]:  # vars/Debian.yml",
    docker_obsolete_packages = [
        "docker",
        "docker.io",
        "docker-engine",
        "docker-doc",
        "docker-compose",
        "docker-compose-v2",
        "podman-docker",
        "containerd",
        "runc",
    ]
elif distribution == "RedHat":  # vars/RedHat.yml
    docker_obsolete_packages = [
        "docker",
        "docker-client",
        "docker-client-latest",
        "docker-common",
        "docker-latest",
        "docker-latest-logrotate",
        "docker-logrotate",
        "docker-engine",
    ]
elif distribution == "Suse":  # vars/Suse.yml
    docker_obsolete_packages = [
        "docker-engine",
        "docker.io",
        "docker-ce",
        "docker-ce-cli",
        "docker-buildx-plugin",
        "docker-ce-rootless-extras",
        "containerd.io",
    ]
    docker_packages = [
        "docker",
        "containerd",
        "runc",
    ]
    docker_suse_release = ""  # TODO: get Suse release
    docker_zypper_repo_url = (
        f"https://download.opensuse.org/repositories/Virtualization:/containers/{docker_suse_release}/"
    )

    docker_add_repo = True


def setup_Debian():
    """tasks/setup_Debian.yml"""

    ########## Ensure apt key is not present in trusted.gpg.d ##########
    # - name: Ensure apt key is not present in trusted.gpg.d
    #   ansible.builtin.file:
    #     path: /etc/apt/trusted.gpg.d/docker.asc
    #     state: absent

    files.file(
        name="Ensure apt key is not present in trusted.gpg.d",
        path="/etc/apt/trusted.gpg.d/docker.asc",
        present=False,
    )

    ########## Ensure old apt source list is not present in /etc/apt/sources.list.d ##########
    # - name: Ensure old apt source list is not present in /etc/apt/sources.list.d
    #   ansible.builtin.file:
    #     path: "/etc/apt/sources.list.d/download_docker_com_linux_{{ docker_apt_ansible_distribution | lower }}.list"
    #     state: absent

    files.file(
        name="Ensure old apt source list is not present in /etc/apt/sources.list.d",
        path=f"/etc/apt/sources.list.d/download_docker_com_linux_{docker_apt_ansible_distribution.lower()}.list",
        present=False,
    )

    ########## Ensure old versions of Docker are not installed. ##########
    # # See https://docs.docker.com/engine/install/debian/#uninstall-old-versions
    # - name: Ensure old versions of Docker are not installed.
    #   ansible.builtin.package:
    #     name: "{{ docker_obsolete_packages }}"
    #     state: absent

    apt.packages(
        name="Ensure old versions of Docker are not installed.",
        packages=docker_obsolete_packages,
        present=False,
    )

    ########## Ensure legacy repo file is not present. ##########
    # - name: Ensure legacy repo file is not present.
    #   ansible.builtin.file:
    #     path: "/etc/apt/sources.list.d/docker.list"
    #     state: absent

    files.file(
        name="Ensure legacy repo file is not present.",
        path="/etc/apt/sources.list.d/docker.list",
        present=False,
    )

    ########## Ensure dependencies are installed. ##########
    # - name: Ensure dependencies are installed.
    #   ansible.builtin.apt:
    #     name:
    #       - ca-certificates
    #       - python3-debian
    #     state: present

    apt.packages(
        name="Ensure dependencies are installed.",
        packages=["ca-certificates", "python3-debian"],
        present=True,
    )

    ########## Add or remove Docker repository. ##########
    # - name: Add or remove Docker repository.
    #   ansible.builtin.deb822_repository:
    #     name: "{{ docker_apt_filename }}"
    #     types: deb
    #     uris: "{{ docker_apt_repo_url }}"
    #     suites: "{{ ansible_facts.distribution_release }}"
    #     components: "{{ docker_apt_release_channel }}"
    #     signed_by: "{{ docker_apt_gpg_key }}"
    #     state: "{{ 'present' if docker_add_repo | bool else 'absent' }}"
    #   notify: apt update

    files.download(
        name=f"Download",
        src="https://download.docker.com/linux/ubuntu/gpg",
        dest="/etc/apt/keyrings/docker.asc",
    )
    apt.sources_file(
        name="Add or remove Docker repository.",
        filename="docker",
        types="deb",
        uris=docker_apt_repo_url,
        suites=distribution_release,
        components=docker_apt_release_channel,
        architectures=docker_compose_arch,
        signed_by="/etc/apt/keyrings/docker.asc",  # docker_apt_gpg_key,
        present=True if docker_add_repo else False,
    )

    ########## Ensure handlers are notified immediately to update the apt cache. ##########
    # - name: Ensure handlers are notified immediately to update the apt cache.
    #   ansible.builtin.meta: flush_handlers

    # TODO: Is something like "flush_handles" with PyInfra necessary?


def tasks_main():
    """tasks/main.yml"""

    ########## Load OS-specific vars. ##########
    # - name: Load OS-specific vars.
    #   include_vars: "{{ lookup('first_found', params) }}"
    #   vars:
    #     params:
    #       files:
    #         - '{{ansible_facts.distribution}}.yml'
    #         - '{{ansible_facts.os_family}}.yml'
    #         - main.yml
    #       paths:
    #         - 'vars'

    ########## include Seutp tasks ##########
    # - include_tasks: setup-RedHat.yml
    #   when: ansible_facts.os_family == 'RedHat'
    if distribution == "RedHat":
        # setup_RedHat()
        pass

    # - include_tasks: setup-Suse.yml
    #   when: ansible_facts.os_family == 'Suse'
    elif distribution == "Suse":
        # setup_Suse()
        pass

    # - include_tasks: setup-Debian.yml
    #   when: ansible_facts.os_family == 'Debian'
    elif distribution in ["Debian", "Ubuntu"]:
        setup_Debian()

    ########## Install Docker packages. ##########
    # - name: Install Docker packages.
    #   package:
    #     name: "{{ docker_packages }}"
    #     state: "{{ docker_packages_state }}"
    #   notify: restart docker
    #   ignore_errors: "{{ ansible_check_mode }}"
    #   when: "ansible_version.full is version_compare('2.12', '<') or ansible_facts.os_family not in ['RedHat', 'Debian']"

    # - name: Install Docker packages (with downgrade option).
    #   package:
    #     name: "{{ docker_packages }}"
    #     state: "{{ docker_packages_state }}"
    #     allow_downgrade: true
    #   notify: restart docker
    #   ignore_errors: "{{ ansible_check_mode }}"
    #   when: "ansible_version.full is version_compare('2.12', '>=') and ansible_facts.os_family in ['RedHat', 'Debian']"

    apt.packages(
        name=f"Install Docker packages. {docker_packages}",
        packages=docker_packages,
        present=docker_packages_state,
        update=True,
        allow_downgrades=True if distribution in ["Debian", "Ubuntu", "RedHat"] else False,
    )

    ########## Install docker-compose plugin. ##########
    # - name: Install docker-compose plugin.
    #   package:
    #     name: "{{ docker_compose_package }}"
    #     state: "{{ docker_compose_package }}"
    #   notify: restart docker
    #   ignore_errors: "{{ ansible_check_mode }}"
    #   when: "docker_install_compose_plugin | bool == true and (ansible_version.full is version_compare('2.12', '<') or ansible_facts.os_family not in ['RedHat', 'Debian', 'Suse'])"

    # - name: Install docker-compose-plugin (with downgrade option).
    #   package:
    #     name: "{{ docker_compose_package }}"
    #     state: "{{ docker_compose_package_state }}"
    #     allow_downgrade: true
    #   notify: restart docker
    #   ignore_errors: "{{ ansible_check_mode }}"
    #   when: "docker_install_compose_plugin | bool == true and ansible_version.full is version_compare('2.12', '>=') and ansible_facts.os_family in ['RedHat', 'Debian']"

    if docker_install_compose_plugin:
        apt.packages(
            name=f"Install '{docker_compose_package}'.",
            packages=docker_compose_package,
            present=docker_compose_package,
            update=True,
            allow_downgrades=True if distribution in ["Debian", "Ubuntu", "RedHat"] else False,
        )

    ########## Ensure /etc/docker/ directory exists. ##########
    # - name: Ensure /etc/docker/ directory exists.
    #   file:
    #     path: /etc/docker
    #     state: directory
    #     mode: 0755
    #   when: docker_daemon_options.keys() | length > 0

    files.directory(
        name="Ensure /etc/docker/ directory exists.",
        path="/etc/docker",
        mode="0755",
        present=True,
    )

    ########## Configure Docker daemon options. ##########
    # - name: Configure Docker daemon options.
    #   copy:
    #     content: "{{ docker_daemon_options | to_nice_json }}"
    #     dest: /etc/docker/daemon.json
    #     mode: 0644
    #   when: docker_daemon_options.keys() | length > 0
    #   notify: restart docker

    if docker_daemon_options:
        json_docker_daemon_options = json.dumps(docker_daemon_options, indent=4)
        files.put(
            name="Configure Docker daemon options.",
            src=StringIO(json_docker_daemon_options),
            dest="/etc/docker/daemon.json",
            mode="0644",
        )

    ########## Replace Docker service ExecStart command if configured. ##########
    # - name: Replace Docker service ExecStart command if configured.
    #   when: docker_service_start_command != ""
    #   notify: restart docker
    #   block:
    #     - name: Get Docker service status
    #       ansible.builtin.systemd_service:
    #         name: docker
    #       register: docker_service_status

    #     - name: Patch docker.service
    #       ansible.builtin.replace:
    #         path: "{{ docker_service_status.status['FragmentPath'] }}"
    #         regexp: "^ExecStart=.*$"
    #         replace: "ExecStart={{ docker_service_start_command }}"
    #       register: docker_service_patch

    #     - name: Reload systemd services
    #       service:
    #         daemon_reload: true
    #       when: docker_service_patch is changed

    # TODO: 'Docker service ExecStart command' not yet implemented.

    ########## Ensure Docker is started and enabled at boot. ##########
    # - name: Ensure Docker is started and enabled at boot.
    #   service:
    #     name: docker
    #     state: "{{ docker_service_state }}"
    #     enabled: "{{ docker_service_enabled }}"
    #   ignore_errors: "{{ ansible_check_mode }}"
    #   when: docker_service_manage | bool

    if docker_service_manage:
        operations_server.service(
            name="Ensure Docker is started and enabled at boot.",
            service="docker",
            enabled=docker_service_enabled,
        )

    ########## Ensure handlers are notified now to avoid firewall conflicts. ##########
    # - name: Ensure handlers are notified now to avoid firewall conflicts.
    #   meta: flush_handlers

    # TODO: Is something like "flush_handles" with PyInfra necessary?

    ########## include docker-compose.yml ##########
    # - include_tasks: docker-compose.yml
    #   when: docker_install_compose | bool

    ########## docker-compose.yml ##########
    # - name: Check current docker-compose version.
    #   command: "{{ docker_compose_path }} --version"
    #   register: docker_compose_vsn
    #   check_mode: false
    #   changed_when: false
    #   failed_when: false

    # - set_fact:
    #     docker_compose_current_version: "{{ docker_compose_vsn.stdout | regex_search('(\\d+(\\.\\d+)+)') }}"
    #   when: >
    #     docker_compose_vsn.stdout is defined
    #     and (docker_compose_vsn.stdout | length > 0)

    # - name: Delete existing docker-compose version if it's different.
    #   file:
    #     path: "{{ docker_compose_path }}"
    #     state: absent
    #   when: >
    #     docker_compose_current_version is defined
    #     and (docker_compose_version | regex_replace('v', '')) not in docker_compose_current_version

    # - name: Install Docker Compose (if configured).
    #   get_url:
    #     url: "{{ docker_compose_url }}"
    #     dest: "{{ docker_compose_path }}"
    #     mode: 0755
    #   when: >
    #     (docker_compose_current_version is not defined)
    #     or (docker_compose_current_version | length == 0)
    #     or (docker_compose_current_version is version((docker_compose_version | regex_replace('v', '')), '<'))

    # TODO: Check if necessary. Docker Desktop includes Docker Compose along with Docker Engine and Docker CLI.

    ########## Ensure docker users are added to the docker group. ##########
    # - name: Get docker group info using getent.
    #   getent:
    #     database: group
    #     key: docker
    #     split: ':'
    #   when: docker_users | length > 0

    # - name: Check if there are any users to add to the docker group.
    #   set_fact:
    #     at_least_one_user_to_modify: true
    #   when:
    #     - docker_users | length > 0
    #     - item not in ansible_facts.getent_group["docker"][2]
    #   with_items: "{{ docker_users }}"

    # - include_tasks: docker-users.yml
    #   when: at_least_one_user_to_modify is defined

    for user in docker_users:
        operations_server.user(
            name=f"Ensure user '{user}' is added to the 'docker' group.",
            user=user,
            group="docker",
        )


tasks_main()
