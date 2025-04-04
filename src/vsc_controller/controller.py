"""
code-server
controller.py

Copyrights 2025 by Albert Weichselbraun. All rights reserved.
"""
import time

from collections import deque
from hashlib import sha256
from pathlib import Path
from shutil import copytree
from threading import Thread

from flask import Flask, request, render_template 
from lib.config import load_config
from lib.nginx import nginx_config_parser
from lib.port import PortManager

app = Flask(__name__)
CONFIG = load_config()

nginx_port_url_mapping = nginx_config_parser(
        Path(CONFIG['paths']['nginx_config'])
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
    config_dir = f"{CONFIG['paths']['instance_dir']}.{user_id}"
    copytree(CONFIG['paths']['instance_template'], config_dir, dir_exist_ok=True)

    # create docker container
    docker_cmd = render_template('docker.sh', config_dir=config_dir, port=_port)
    subprocess.run(docker_cmd, shell=True, check=True, capture_output=True, text=True)


@app.route("/create")
def create():
    # check: instance available => redirect
    # otherwise: wait & schedule for creation
    global user_mapping
    global nginx_port_url_mapping

    moodle_course_id = request.args.get('m')
    instance_type = request.args.get('t')
    user_id = request.args.get('u')
    if not user_id.isdigit() or not moodle_course_id.isdigit():
        return "Invalid request detected.", 400

    key = request.args.get('k')
    reference = sha256(f"{CONFIG['security']['secret']}:{moodle_course_id}".encode("utf8")).hexdigest()[:16]
    if key != reference:
        return f"Invalid request key detected.", 400

    pairing = (user_id, instance_type) 
    # redirect, if the instance has already been created
    if not pairing in user_mapping:
        setup_code_server(user_id, instance_type)

    port = user_mapping[pairing]
    return redirect(nginx_port_url_mapping[port])


if __name__ == '__main__':
    app.run(debug=True, port=5000)
