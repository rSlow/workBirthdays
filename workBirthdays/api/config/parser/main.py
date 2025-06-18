from adaptix import Retort

from workBirthdays.core.config.models.paths import Paths
from workBirthdays.core.config.parser.config_file_reader import read_config_yaml
from workBirthdays.core.config.parser.main import load_base_config
from ..models import ApiAppConfig
from ..models.api import ApiConfig


def load_config(paths: Paths, retort: Retort) -> ApiAppConfig:
    config_dct = read_config_yaml(paths)

    return ApiAppConfig.from_base(
        base=load_base_config(config_dct, paths, retort),
        api=retort.load(config_dct["api"], ApiConfig),
    )
