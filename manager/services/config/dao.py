import json
from pathlib import Path


def read_config_from_file(config_file: Path):
    if config_file.exists() and config_file.is_file():
        return json.loads(
            config_file.read_text()
        )
    else:
        return {}


def write_config_to_file(config: dict, file: Path):
    print(config)
    file.write_text(
        json.dumps(
            config
        )
    )
