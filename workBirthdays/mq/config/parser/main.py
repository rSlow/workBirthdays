from adaptix import Retort

from workBirthdays.core.config import Paths
from workBirthdays.core.config.parser.config_file_reader import read_config_yaml
from workBirthdays.core.config.parser.main import load_base_config
from workBirthdays.mq.config.models.backend import ResultBackendConfig
from workBirthdays.mq.config.models.main import TaskiqAppConfig
from workBirthdays.mq.config.models.selenium import SeleniumConfig


def load_config(paths: Paths, retort: Retort):
    config_dct = read_config_yaml(paths)

    return TaskiqAppConfig.from_base(
        base=load_base_config(config_dct, paths, retort),
        result_backend=retort.load(config_dct["mq"]["backend"], ResultBackendConfig),
    )
