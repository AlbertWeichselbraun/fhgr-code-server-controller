#!/usr/bin/env python3

from pathlib import Path
from uuid import uuid4

from jinja2 import Template

TEMPLATE_PATH = Path(__file__).parent.parent / "src/code_server/templates/nginx.conf"


template = Template(TEMPLATE_PATH.read_text())

MAX_CLIENTS = 50
CONFIG_GROUPS = {
    "c": 9000,
    "e": 9500,
}

for prefix, start_port in CONFIG_GROUPS.items():
    for port in range(start_port, start_port + MAX_CLIENTS):
        cfg = template.render(prefix=prefix, port=port, uuid=str(uuid4()))
        print(cfg)
