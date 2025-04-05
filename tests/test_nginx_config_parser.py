#!/usr/bin/env python3

from pathlib import Path
from code_server.util.nginx import nginx_config_parser

NGINX_CONFIG = Path(__file__).parent / "data/nginx-forwards.conf"


def test_config_parser():
    config_list = nginx_config_parser(NGINX_CONFIG)
    assert len(config_list) == 100

    for port, path in config_list.items():
        print(path, port)
        assert "/c/" in path or "/e/" in path
        if "/c/" in path:
            assert 9000 <= port <= 9050
        elif "/e/" in path:
            assert 9500 <= port <= 9550
