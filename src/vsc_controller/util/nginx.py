import re

from collections import namedtuple
from pathlib import Path
from typing import List

EXTRACT_RE = re.compile(r"location\s+(/[\w/-]+)\s+{[^}]+?proxy_pass\s+http://[\d\.]+:(\d+)/")


def nginx_config_parser(config_file: Path) -> List[CodeServer]:
    config = config_file.read_text()
    return {int(port): path for path, port in EXTRACT_RE.findall(config)}

