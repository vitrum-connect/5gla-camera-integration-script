import unittest

from src.config.config_manager import ConfigManager


class ConfigManagerTest(unittest.TestCase):
    def test_given_valid_config_path_when_loading_the_config_the_configmanager_should_have_values(self):
        config_manager = ConfigManager()
        version = config_manager.get('version')
        self.assertEqual(version, "1.0.0")

    def test_given_invalid_config_path_when_loading_the_config_the_configmanager_should_raise_keyerror(self):
        config_manager = ConfigManager()
        with self.assertRaises(KeyError):
            config_manager.get('invalid_key')
