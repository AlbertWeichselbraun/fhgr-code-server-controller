"""
Verify and create authorizations.
"""

import base64

from hashlib import sha256


def get_authorization_key(secret: str, moodle_course_id: str) -> str:
    hash_bytes = sha256(f"{secret}:{moodle_course_id}".encode("utf8")).digest()
    return base64.urlsafe_b64encode(hash_bytes).decode("utf8")[:10]


def is_authorized(key: str, secret: str, moodle_course_id: str) -> bool:
    return key == get_authorization_key(secret, moodle_course_id)
