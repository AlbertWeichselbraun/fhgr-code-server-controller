"""
controller.py

Copyrights 2025 by Albert Weichselbraun. All rights reserved.
"""

from flask import Flask, request, render_template 

from collections import deque
from hashlib import sha256
from pathlib import Path
from shutil import copytree


app = Flask(__name__)

SECRET = "7c46e02d-bb8a-4e41-a044-1e3675992117"

INSTANCE_DIR_TEMPLATE = "/home/albert/tmp/prog/config.template"
INSTANCE_DIR = "/home/albert/tmp/prog/config.template"

user_mapping = {}
instance_creation_queue = deque(list)

def create_server_instance():
    """
    Creates a new server instance for the given numerical user_id.
    """
    global user_mapping
    global instance_creation_queue

    while instance_creation_queue:
        user_id = instance_creation_queue.popleft()
        config_dir = f"{INSTANCE_DIR}.{user_id}"

        # copy the template directory to the users individual working directory
        copytree(INSTANCE_DIR_TEMPLATE, config_dir, dir_exist_ok=True)

        # user the jinja engine to create the docker exec call
        docker_command = render_template('docker.sh', config_dir=config_dir, port=config_port)


@app.route("/create")
def create_flask_instance():
    # check: instance available => redirect
    # otherwise: wait & schedule for creation
    global user_mapping
    global instance_creation_queue

    moodle_course_id = request.args.get('m')
    instance_type = request.args.get('t')
    user_id = request.args.get('u')
    if not user_id.isdigit() or not moodle_course_id.isdigit():
        return "Invalid request detected", 400
    key = request.args.get('k')

    reference = sha256(f"{SECRET}:{moodle_course_id}".encode("utf8")).hexdigest()[:16]
    if key != reference:
        return f"Invalid request key detected", 400

    if user_id in user_mapping:
        target_url = user_mapping[user_id]
        return f"Redirecting to URL '{target_url}'.", 301

    # create a new flask instance
    key = (user_id, instance_type) 
    if not (user_id, instance_type) in instance_creation_queue:
        instance_creation_queue.append(


    return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)


