#!/usr/bin/env python3

from code_server.util.config import load_config
from code_server.util.podman import start_code_server

CONFIG = load_config()

for port in range(CONFIG['ports']['c']['start'], CONFIG['ports']['c']['end'] + 1):
    print("Starting server for port {}".format(port))
    start_code_server(port)
