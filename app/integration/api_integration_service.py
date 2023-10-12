import logging

import requests

from app.config.config_manager import ConfigManager


class ApiIntegrationService:
    """
    The `ApiIntegrationService` class provides methods to interact with the 5GLA API.
    """

    @staticmethod
    def check_availability():
        """
        Checks the availability of the 5GLA API.
            """
        config_manager = ConfigManager()
        url = config_manager.get('api_url') + config_manager.get('api_version_endpoint')
        headers = {'X-API-Key': config_manager.get_env('API_KEY')}
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return True
        else:
            logging.error(f"API is not available. Status code: {response.status_code}")
            return False
