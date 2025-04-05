import re

from pathlib import Path
from typing import Dict

EXTRACT_RE = re.compile(r"location\s+(/[\w/-]+)\s+{[^}]+?proxy_pass\s+http://[\d\.]+:(\d+)/")


def nginx_config_parser(config_file: Path) -> Dict[int, str]:
    config = config_file.read_text()
    return {int(port): path for path, port in EXTRACT_RE.findall(config)}

