import os
import pathlib
import typing as tp

import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
config_path = BASE_DIR / "config" / "config.yaml"


def parse_config(config_path: str = config_path) -> dict[str, tp.Any]:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    config["database"]["user"] = os.environ.get("POSTGRES_USER", config["database"]["user"])
    config["database"]["password"] = os.environ.get("POSTGRES_PASSWORD", config["database"]["password"])
    config["database"]["host"] = os.environ.get("POSTGRES_HOST", config["database"]["host"])
    config["database"]["port"] = os.environ.get("POSTGRES_PORT", config["database"]["port"])
    config["database"]["database"] = os.environ.get("POSTGRES_DB", config["database"]["database"])

    config["bot"]["access_token"] = os.environ.get("ACCESS_TOKEN", config["bot"]["access_token"])
    config["bot"]["group_id"] = os.environ.get("GROUP_ID", config["bot"]["group_id"])

    config["game"]["timeout"] = os.environ.get("TIMEOUT", config["bot"]["timeout"])

    return config
