from pathlib import Path

import yaml


class ConfigManager:

    def __init__(self):
        self._config_path = Path(__file__).parent / 'config' / 'config.yaml'
        self._config = self._load_config()

    def _load_config(self):
        with open(self._config_path, 'r') as config_file:
            return yaml.safe_load(config_file)

    def get(self, key):
        value = self._config.get(key)
        if value is None:
            raise KeyError(f"Key '{key}' has not been found in `config.yaml`.")
        return value
