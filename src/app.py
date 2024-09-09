import logging
import threading
import time
import uuid

from src.config.config_manager import ConfigManager
from src.integration.api_integration_service import ApiIntegrationService
from src.integration.camera_integration_service import CameraIntegrationService
from src.integration.drone_integration_service import DroneIntegrationService

config_manager = ConfigManager()
config_manager.set_log_level_from_config()
camera_integration_service = CameraIntegrationService()
drone_integration_service = DroneIntegrationService()
api_integration_service = ApiIntegrationService()
transaction_id = uuid.uuid4().__str__()


def send_drone_position():
    if config_manager.get_env('ENABLE_IMAGE_SENDING'):
        while drone_integration_service.still_has_power():
            camera_integration_service.send_camera_position_via_api(drone_id=config_manager.get_env('CAMERA_ID'),
                                                                    transaction_id=transaction_id)
            time.sleep(int(config_manager.get_env('POSITION_SENDING_INTERVAL_IN_SECONDS')))
    else:
        logging.info("Position sending is disabled, skipping the process.")


def send_image_to_api():
    if config_manager.get_env('ENABLE_IMAGE_SENDING'):
        while drone_integration_service.still_has_power():
            camera_integration_service.trigger_pictures(config_manager.get('trigger_photo_url'))
            logging.debug("Downloading picture into the given folder.")
            folder = config_manager.get_env('WORKING_DIR') + config_manager.get(
                'photo_folder') + transaction_id + "/" + str(
                int(time.time())) + '/'
            camera_integration_service.create_folder(folder)
            camera_integration_service.download_picture(config_manager.get('photo_download_url'), folder)
            camera_integration_service.send_pictures_via_api(camera_id=config_manager.get_env('CAMERA_ID'),
                                                             transaction_id=transaction_id,
                                                             folder=folder)
            time.sleep(int(config_manager.get_env('IMAGE_SENDING_INTERVAL_IN_SECONDS')))
    else:
        logging.info("Image sending is disabled, skipping the process.")

def send_heartbeat():
    while drone_integration_service.still_has_power():
        api_integration_service.send_heartbeat(drone_id=config_manager.get_env('CAMERA_ID'))
        time.sleep(int(config_manager.get_env('HEARTBEAT_INTERVAL_IN_SECONDS')))


if config_manager.get_env_or_default('INTEGRATION_TEST', False):
    logging.info("Integration test mode is enabled.")
else:
    thread_for_image_sending = threading.Thread(target=send_image_to_api)
    thread_for_position_sending = threading.Thread(target=send_drone_position)#
    thread_for_heartbeat = threading.Thread(target=send_heartbeat)

    thread_for_image_sending.start()
    thread_for_position_sending.start()
    thread_for_heartbeat.start()

    logging.info("All threads are started, now waiting for them to finish.")

    thread_for_image_sending.join()
    thread_for_position_sending.join()
    thread_for_heartbeat.join()