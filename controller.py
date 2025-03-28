"""
controller.py

Copyrights 2025 by Albert Weichselbraun. All rights reserved.
"""

from flask import Flask, request, render_template 
from hashlib import sha256
from pathlib import Path
from shutil import copytree

app = Flask(__name__)

SECRET = "7c46e02d-bb8a-4e41-a044-1e3675992117"

INSTANCE_DIR_TEMPLATE = "/home/albert/tmp/prog/config.template"
INSTANCE_DIR = "/home/albert/tmp/prog/config.template"

user_mapping = {}

def create_server_instance(user_id):
    """
    Creates a new server instance for the given numerical user_id.
    """
    global user_mapping
    config_dir = f"{INSTANCE_DIR}.{user_id}"
    # copy the template directory to the users individual working directory
    copytree(INSTANCE_DIR_TEMPLATE, config_dir, dir_exist_ok=True)

    # user the jinja engine to create the docker exec call
    docker_command = render_template('docker.sh', config_dir=config_dir, port=config_port)




@app.route("/create")
def create_flask_instance():
    moodle_course_id = request.args.get('m')
    user_id = request.args.get('u')
    if not user_id.isdigit() or not moodle_course_id.isdigit():
        return "Invalid request detected", 400
    key = request.args.get('k')

    reference = sha256(f"{SECRET}:{moodle_course_id}".encode("utf8")).hexdigest()[:16]
    if key != reference:
        return f"Invalid request key detected", 400

    return "All good"


if __name__ == '__main__':
    app.run(debug=True, port=5000)


