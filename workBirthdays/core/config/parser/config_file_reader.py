import yaml

from ..models.paths import Paths


def read_config_yaml(paths: Paths) -> dict:
    with (paths.config_path / "config.yml").open("r") as f:
        return yaml.safe_load(f)
