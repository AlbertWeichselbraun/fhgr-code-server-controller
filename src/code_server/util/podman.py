import os
import subprocess
from pathlib import Path
from shutil import copytree, rmtree

from jinja2 import Template
from code_server.util.config import load_config

CONFIG = load_config()
UID = os.getuid()
GID = os.getgid()
DOCKER_TEMPLATE = Template(Path(__file__).parent.parent / "templates" / "podman.sh")


def start_code_server(port):
    """
    Creates a new server instance for the given port.
    """
    # setup working directory
    instance_dir = Path(f"{CONFIG['paths']['instance_dir']}.{port}")
    copytree(CONFIG["paths"]["instance_template"], instance_dir, dirs_exist_ok=True)

    # create docker container
    docker_cmd = DOCKER_TEMPLATE.render(
        config_dir=instance_dir,
        port=port,
        sudo_password=CONFIG["security"]["suid_pwd"],
        uid=UID,
        gid=GID,
    )
    result = subprocess.run(
        docker_cmd.split(), check=True, capture_output=True, text=True
    )
    print(result)


def stop_code_server(port):
    """
    Stops the code server instance for the given port.
    """
    instance_dir = Path(f"{CONFIG['paths']['instance_dir']}.{port}")
    result = subprocess.run(
        ["docker", "stop", f"fhgr-code-server-{port}"],
        check=True,
        capture_output=True,
        text=True,
    )
    print(result)
    if instance_dir.exists():
        rmtree(instance_dir)
