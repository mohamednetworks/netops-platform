from pathlib import Path

import yaml


def load_config(path: str = "configs/network.yml") -> dict:
    config_path = Path(path)

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("Configuration must be a YAML mapping")

    return config
