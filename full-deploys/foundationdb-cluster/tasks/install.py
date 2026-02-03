"""
FoundationDB package installation tasks.
Downloads and installs FDB .deb packages from GitHub releases.
"""

from pyinfra import host
from pyinfra.facts.server import Arch
from pyinfra.operations import apt, files, server

fdb_version = host.data.fdb_version
fdb_base_url = f"https://github.com/apple/foundationdb/releases/download/{fdb_version}"
arch = host.get_fact(Arch)
if arch == "x86_64":
    arch = "amd64"

# Download FDB packages
files.download(
    name="Download foundationdb-clients package",
    src=f"{fdb_base_url}/foundationdb-clients_{fdb_version}-1_{arch}.deb",
    dest=f"/tmp/foundationdb-clients_{fdb_version}-1_{arch}.deb",
)

files.download(
    name="Download foundationdb-server package",
    src=f"{fdb_base_url}/foundationdb-server_{fdb_version}-1_{arch}.deb",
    dest=f"/tmp/foundationdb-server_{fdb_version}-1_{arch}.deb",
)

# Install packages (clients first, then server)
apt.deb(
    name="Install foundationdb-clients",
    src=f"/tmp/foundationdb-clients_{fdb_version}-1_{arch}.deb",
)

apt.deb(
    name="Install foundationdb-server",
    src=f"/tmp/foundationdb-server_{fdb_version}-1_{arch}.deb",
)
