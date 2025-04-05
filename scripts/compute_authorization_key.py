#!/usr/bin/env python3

from code_server.util.authorize import get_authorization_key
from code_server.util.config import load_config

CONFIG = load_config()


course_id = input("Moodle course ID to authorized:")
for instance_type in CONFIG["security"]["secret"].keys():
    print(
        f"Authorization Code for type {instance_type}: "
        + get_authorization_key(CONFIG["security"]["secret"][instance_type], course_id)
    )
