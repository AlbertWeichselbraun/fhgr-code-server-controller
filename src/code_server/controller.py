"""
code-server
controller.py

Copyrights 2025 by Albert Weichselbraun. All rights reserved.

TODO:
    - use different keys for different instance types
"""
import os
import subprocess

from pathlib import Path
from shutil import copytree

from flask import Flask, request, render_template, redirect
from code_server.util.authorize import is_authorized
from code_server.util.config import load_config
from code_server.util.nginx import nginx_config_parser
from code_server.util.port import PortManager

app = Flask(__name__)
UID = os.getuid()
GID = os.getgid()
CONFIG = load_config()

nginx_port_url_mapping = nginx_config_parser(Path(CONFIG['paths']['nginx_config']))
if not nginx_port_url_mapping:
    logger.error("Empty nginx_port_url_mapping - cannot start.")
    import sys
    sys.exit(-1)

user_port_mapping = {}
port_manager = PortManager()


def setup_code_server(user_id, instance_type):
    """
    Creates a new server instance for the given numerical user_id.
    """
    global port_manager
    global user_port_mapping

    port = port_manager.get_next_port(instance_type)
    user_port_mapping[(user_id, instance_type)] = port

    # setup working directory
    config_dir = Path(f"{CONFIG['paths']['instance_dir']}.{user_id}")
    if config_dir.exists():
        from shutil import rmtree
        rmtree(config_dir)
    copytree(CONFIG['paths']['instance_template'], config_dir, dirs_exist_ok=True)

    # create docker container
    docker_cmd = render_template('docker.sh', config_dir=config_dir, port=port, 
                                 sudo_password=CONFIG['security']['suid_pwd'], uid=UID, gid=GID)
    result = subprocess.run(docker_cmd.split(), check=True, capture_output=True, text=True)


@app.route("/create")
def create():
    # check: instance available => redirect
    # otherwise: wait & schedule for creation
    global user_port_mapping
    global nginx_port_url_mapping

    moodle_course_id = request.args.get('m')
    instance_type = request.args.get('t')
    user_id = request.args.get('u')
    if not user_id.isdigit() or not moodle_course_id.isdigit():
        return "Invalid request detected.", 400

    if not is_authorized(request.args.get('k'), CONFIG['security']['secret'][instance_type], moodle_course_id):
        return f"Invalid request key detected.", 400

    pairing = (user_id, instance_type) 
    # redirect, if the instance has already been created
    if not pairing in user_port_mapping:
        setup_code_server(user_id, instance_type)

    port = user_port_mapping[pairing]
    return redirect(nginx_port_url_mapping[port])


if __name__ == '__main__':
    app.run(debug=True, port=5000)
