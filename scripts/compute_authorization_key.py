#!/usr/bin/env python3

from vsc_controller.util.authorize import get_authorization_key
from vsc_controller.util.config import load_config

CONFIG = load_config()


course_id = input("Moodle course ID to authorized:")
print(
    "Authorization Code: "
    + get_authorization_key(CONFIG["security"]["secret"], course_id)
)
