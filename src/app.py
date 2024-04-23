import logging
import time
import uuid

from src.config.config_manager import ConfigManager
from src.integration.api_integration_service import ApiIntegrationService
from src.integration.camera_integration_service import CameraIntegrationService
from src.integration.drone_integration_service import DroneIntegrationService

config_manager = ConfigManager()
camera_integration_service = CameraIntegrationService()
drone_integration_service = DroneIntegrationService()
api_integration_service = ApiIntegrationService()
transaction_id = uuid.uuid4().__str__()

if config_manager.get_env_or_default('INTEGRATION_TEST', False):
    logging.info("Integration test mode is enabled.")
else:
    if not api_integration_service.check_availability():
        logging.error("API is not available.")
    else:
        logging.info("API is available, starting the process.")
        api_integration_service.begin_transaction(drone_id=config_manager.get('drone_id'),
                                                  transaction_id=transaction_id)
        while drone_integration_service.still_has_power():
            logging.debug("Triggering camera to take pictures.")
            camera_integration_service.trigger_pictures(config_manager.get('trigger_photo_url'))
            logging.debug("Downloading picture into the given folder.")
            folder = config_manager.get_env('WORKING_DIR') + config_manager.get(
                'photo_folder') + transaction_id + "/" + str(
                int(time.time())) + '/'
            camera_integration_service.create_folder(folder)
            camera_integration_service.download_picture(config_manager.get('photo_download_url'), folder)
            camera_integration_service.send_pictures_via_api(drone_id=config_manager.get('drone_id'),
                                                             transaction_id=transaction_id,
                                                             folder=folder)
            camera_integration_service.s
            time.sleep(config_manager.get('photo_interval_seconds'))
