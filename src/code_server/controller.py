"""
code_server

Copyrights 2025 by Albert Weichselbraun. All rights reserved.
"""

import logging
import sys
from pathlib import Path

from flask import Flask, request, redirect
from code_server.util.authorize import is_authorized
from code_server.util.config import load_config
from code_server.util.nginx import nginx_config_parser
from code_server.util.port import PortManager

app = Flask(__name__)
CONFIG = load_config()

file_handler = logging.FileHandler("controller.log")
file_handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

nginx_port_url_mapping = nginx_config_parser(Path(CONFIG["paths"]["nginx_config"]))
if not nginx_port_url_mapping:
    print("Empty nginx_port_url_mapping - cannot start.")
    sys.exit(-1)

user_port_mapping = {}
port_manager = PortManager()


@app.route("/create")
def create():
    # check: instance available => redirect
    # otherwise: wait & schedule for creation
    global user_port_mapping
    global nginx_port_url_mapping

    moodle_course_id = request.args.get("m", "")
    instance_type = request.args.get("t", "")
    user_id = request.args.get("u", "")
    user_email = request.args.get("e", "")
    if not user_id.isdigit() or not moodle_course_id.isdigit():
        return "Invalid request detected.", 400

    if not is_authorized(
        request.args.get("k"),
        CONFIG["security"]["secret"][instance_type],
        moodle_course_id,
    ):
        return f"Invalid request key detected.", 400

    pairing = (user_id, instance_type)
    # redirect, if the instance has already been created
    if not pairing in user_port_mapping:
        user_port_mapping[pairing] = port_manager.get_next_port(instance_type)
        app.logger.info(
            f"Binding user {user_email} ({user_id}) to port {user_port_mapping[pairing]}."
        )

    port = user_port_mapping[pairing]
    return redirect(nginx_port_url_mapping[port])


if __name__ == "__main__":
    app.run(port=5000)
