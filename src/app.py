import logging
import time
import uuid

from src.config.config_manager import ConfigManager
from src.integration.camera_interaction import CameraInteraction

capture = CameraInteraction()
config_manager = ConfigManager()
set_id = uuid.uuid4().__str__()

while True:
    logging.debug("Triggering camera to take pictures.")
    capture.trigger_pictures(config_manager.get('trigger_photo_url'))
    logging.debug("Downloading picture into the given folder.")
    folder = config_manager.get('photo_folder') + set_id + "/" + str(int(time.time())) + '/'
    capture.create_folder(folder)
    capture.download_picture(config_manager.get('photo_download_url'), folder)
    time.sleep(config_manager.get('photo_interval_seconds'))
