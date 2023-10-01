import os
import pathlib
import typing as tp

import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
config_path = BASE_DIR / "config" / "config.yaml"


def parse_config(config_path: str = config_path) -> dict[str, tp.Any]:
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    raw_config["database"]["user"] = os.environ.get("POSTGRES_USERNAME", raw_config["database"]["user"])
    raw_config["database"]["password"] = os.environ.get("POSTGRES_PASSWORD", raw_config["database"]["password"])
    raw_config["database"]["host"] = os.environ.get("POSTGRES_HOST", raw_config["database"]["host"])
    raw_config["database"]["port"] = os.environ.get("POSTGRES_PORT", raw_config["database"]["port"])

    return raw_config
