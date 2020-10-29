from typing import Any
import yaml
from .helper import get_absolute_path


class Configuration:
    DEFAULT_CONFIG_FILE_PATH = "configuration.yaml"

    def __init__(self):
        self._config: dict = None
        self._init_config()

    def _init_config(self, config_file=DEFAULT_CONFIG_FILE_PATH) -> None:
        self._config = Configuration._load_yaml(get_absolute_path(config_file))

    @staticmethod
    def _load_yaml(path: str) -> dict:
        with open(path, 'r') as stream:
            return yaml.safe_load(stream)
            #return yaml.load(stream, Loader=yaml.UnsafeLoader)

    def get(self, key: str) -> Any:
        return self._config[key]
