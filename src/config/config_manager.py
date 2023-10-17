import os
from pathlib import Path

import yaml


class ConfigManager:

    def __init__(self):
        self._config_path = Path(__file__).parent / 'config' / 'config.yaml'
        self._config = self._load_config()

    def _load_config(self):
        """
        Load configuration from a YAML file.

        :return: A dictionary containing the configuration data.
        """
        with open(self._config_path, 'r') as config_file:
            return yaml.safe_load(config_file)

    def get(self, key):
        """

        :param key: The key representing the configuration value to fetch from the `config.yaml` file.
        :return: The value corresponding to the provided key.

        """
        value = self._config.get(key)
        if value is None:
            raise KeyError(f"Key '{key}' has not been found in `config.yaml`.")
        return value

    @staticmethod
    def get_env(key):
        """
        :param key: The key of the environment variable to retrieve.
        :return: The value of the specified environment variable.

        """
        value = os.environ.get(key)
        if value is None:
            raise KeyError(f"Key '{key}' has not been found in environment variables.")
        return value
