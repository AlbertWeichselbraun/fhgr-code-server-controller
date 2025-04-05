import os
import subprocess
from pathlib import Path
from shutil import copytree, rmtree

from jinja2 import Template
from code_server.util.config import load_config

CONFIG = load_config()
UID = os.getuid()
GID = os.getgid()
DOCKER_TEMPLATE = Template(
    (Path(__file__).parent.parent / "templates" / "podman.sh").read_text()
)


def start_code_server(port):
    """
    Creates a new server instance for the given port.
    """
    # setup working directory
    instance_dir = Path(f"{CONFIG['paths']['instance_dir']}.{port}")
    copytree(CONFIG["paths"]["instance_template"], instance_dir, dirs_exist_ok=False)

    # create docker container
    docker_cmd = DOCKER_TEMPLATE.render(
        config_dir=instance_dir,
        port=port,
        sudo_password=CONFIG["container"]["suid_pwd"],
        hosts=CONFIG["container"]["hosts_file"],
        resolv=CONFIG["container"]["resolv_file"],
        uid=UID,
        gid=GID,
    )
    print(docker_cmd)
    result = subprocess.run(docker_cmd.split())


def stop_code_server(port):
    """
    Stops the code server instance for the given port.
    """
    instance_dir = Path(f"{CONFIG['paths']['instance_dir']}.{port}")
    result = subprocess.run(
        ["podman", "stop", f"fhgr-code-server-{port}"],
    )
    if instance_dir.exists():
        rmtree(instance_dir)
