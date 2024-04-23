import base64
import logging
import time

import requests

from src.config.config_manager import ConfigManager


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
        url = config_manager.get_env('API_URL') + config_manager.get('api_version_endpoint')
        headers = {'X-API-Key': config_manager.get_env('API_KEY')}
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return True
        else:
            logging.error(f"API is not available. Status code: {response.status_code}")
            logging.error(f"The response from the service was: {response.text}")
            return False

    def send_image(self, transaction_id, drone_id, channel, images):
        """
        Send images to API.

        :param transaction_id: The ID of the transaction.
        :param drone_id: The ID of the drone.
        :param channel: The channel to send the images.
        :param images: A list of images to send.
        :return: True if the images were successfully sent, False otherwise.

        """
        max_retries = ConfigManager().get('max_retries')
        for i in range(max_retries):
            if self._send_image(transaction_id, drone_id, channel, images):
                return True
            else:
                logging.info(f"Retrying to send image. Attempt {i + 1}/{max_retries}")
                retry_delay_seconds = ConfigManager().get('retry_delay_seconds')
                logging.info(f"Sleeping for {retry_delay_seconds} seconds.")
                time.sleep(retry_delay_seconds)

    def _send_image(self, transaction_id, drone_id, channel, images):
        """
        Send an image to the API server for processing.

        :param transaction_id: The ID of the transaction.
        :param drone_id: The ID of the drone.
        :param channel: The communication channel used for sending the images.
        :param images: A list of images to be sent.
        :return: True if the image is successfully sent, False otherwise.
        """
        config_manager = ConfigManager()
        url = config_manager.get_env('API_URL') + config_manager.get('api_image_endpoint')
        headers = {'X-API-Key': config_manager.get_env('API_KEY')}
        data = {
            'transactionId': transaction_id,
            'droneId': drone_id,
            'images': self._process_images(channel, images)
        }
        response = requests.post(url=url, headers=headers, json=data)
        if response.status_code == 201:
            return True
        else:
            logging.error(f"Looks like the image was not transferred correctly. Status code: {response.status_code}")
            logging.error(f"The response from the service was: {response.text}")
            return False

    @staticmethod
    def begin_transaction(drone_id, transaction_id):
        """
        :param drone_id: The ID of the drone to begin the transaction.
        :param transaction_id: The ID of the transaction to begin.
        :return: Returns True if the transaction was successfully ended. Returns False otherwise.
        """
        config_manager = ConfigManager()
        url = config_manager.get_env('API_URL') + config_manager.get('api_begin_transaction_endpoint')
        url = url.replace('@drone_id', drone_id)
        url = url.replace('@transaction_id', transaction_id)
        headers = {'X-API-Key': config_manager.get_env('API_KEY'), 'Content-Type': 'application/json'}
        response = requests.post(url=url, headers=headers)
        if response.status_code == 201:
            return True
        else:
            logging.error(
                f"Looks like we are not able to begin the transaction. The status code was {response.status_code}")
            logging.error(f"The response from the service was: {response.text}")
            return False

    def send_device_position(self, drone_id, transaction_id, latitude, longitude):
        """
        :param drone_id: The ID of the drone.
        :param transaction_id: The ID of the transaction.
        :param latitude: The latitude of the drone.
        :param longitude: The longitude of the drone.
        :return: True if the GPS position was successfully sent, False otherwise.
        """
        config_manager = ConfigManager()
        url = config_manager.get_env('API_URL') + config_manager.get('api_device_position_endpoint')
        url = url.replace('@drone_id', drone_id)
        url = url.replace('@transaction_id', transaction_id)
        headers = {'X-API-Key': config_manager.get_env('API_KEY'), 'Content-Type': 'application/json',
                   'Authorization': self._get_authorization_token()}
        data = {
            'latitude': latitude,
            'longitude': longitude
        }
        response = requests.post(url=url, headers=headers, json=data)
        if response.status_code == 201:
            return True
        else:
            logging.error(
                f"Looks like the GPS position was not transferred correctly. Status code: {response.status_code}")
            logging.error(f"The response from the service was: {response.text}")
            return False

    @staticmethod
    def _get_authorization_token():
        config_manager = ConfigManager()
        tenantAndAccessToken = config_manager.get_env('TENANT') + ':' + config_manager.get_env('TENANT_ACCESS_TOKEN')
        return 'Basic ' + base64.b64encode(tenantAndAccessToken.encode()).decode()

    @staticmethod
    def _process_images(channel, images):
        processed_images = []
        for image in images:
            processed_images.append({
                'micaSenseChannel': channel,
                'base64Image': image
            })
        return processed_images
