from code_server.util.config import load_config
from code_server.util.podman import start_code_server, stop_code_server

CONFIG = load_config()

for port in range(CONFIG.ports.c.start, CONFIG.ports.c.stop + 1):
    stop_code_server(port)
