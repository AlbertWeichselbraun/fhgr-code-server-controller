#!/usr/bin/env python3

from code_server.util.config import load_config
from code_server.util.podman import stop_code_server

CONFIG = load_config()

for instance_type in CONFIG["ports"].keys():
    for port in range(
        CONFIG["ports"][instance_type]["start"], CONFIG["ports"][instance_type]["end"]
    ):
        print(f"Stopping server of type {instance_type} on port {port}.")
        stop_code_server(port)
