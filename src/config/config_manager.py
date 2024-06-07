import logging
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

    @staticmethod
    def get_env_or_default(key, default):
        """
        :param key: The key of the environment variable to retrieve.
        :param default: The default value to return if the key is not found.
        :return: The value of the specified environment variable.

        """
        value = os.environ.get(key, default)
        return value

    def set_log_level_from_config(self):
        """
        Set the log level from the configuration file.

        :return: None

        """
        root_level = self.get('log_level')
        logging.basicConfig(level=root_level)
        logging.log(logging.getLevelName(root_level), "Root logger has been set to the level: " + root_level)
        for key, value in self._config.items():
            if key.startswith('log_level'):
                logger_declaration = key.split('.')
                if len(logger_declaration) != 2:
                    logging.debug(f"Skipping key: {key} as it does not follow the logger declaration format.")
                    continue
                else:
                    logger = logger_declaration[1]
                    logging.getLogger(logger).setLevel(value)
                    logging.info(f"Log level for {logger} has been set to {value}.")
