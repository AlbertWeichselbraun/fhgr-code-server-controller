import yaml
from pathlib import Path

CONFIG_FILES = (Path('/etc/code-server.yaml'), 
                Path('~/.code-server.yaml').expanduser(),
                Path(__file__).parent.parent.parent / 'code-server.yaml')


def load_config():
    """Load the configuration file."""
    for path in CONFIG_FILES:
        if path.exists():
            config_path = path
            break   

    with open(config_path) as f:
        return yaml.safe_load(f)
