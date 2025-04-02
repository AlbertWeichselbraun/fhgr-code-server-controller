#!/usr/bin/env python3

from pathlib import Path
from vsc_controller.util.nginx import nginx_config_parser, CodeServer

NGINX_CONFIG = Path(__file__).parent / "data/nginx-forwards.conf"

def test_config_parser():
    config_list = nginx_config_parser(NGINX_CONFIG)
    assert len(config_list) == 100

    for path, port in config_list:
        print(path, port)
        assert '/c/' in path or '/e/' in path
        if '/c/' in path:
            assert port >= 9000 and port <= 9050
        elif '/e/' in path:
            assert port >= 9500 and port <= 9550
