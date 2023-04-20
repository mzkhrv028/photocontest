import typing as tp
import pathlib
import yaml


BASE_DIR = pathlib.Path(__file__).parent.parent.parent
config_path = BASE_DIR / "config" / "config.yaml"


def parse_config(config_path: str = config_path) -> dict[str, tp.Any]:
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    return raw_config
