import logging
import time
import uuid

from src.config.config_manager import ConfigManager
from src.integration.camera_interaction import trigger_pictures, create_folder, download_picture, send_pictures_via_api

config_manager = ConfigManager()
set_id = uuid.uuid4().__str__()

while True:
    logging.debug("Triggering camera to take pictures.")
    trigger_pictures(config_manager.get('trigger_photo_url'))
    logging.debug("Downloading picture into the given folder.")
    folder = config_manager.get('photo_folder') + set_id + "/" + str(int(time.time())) + '/'
    create_folder(folder)
    download_picture(config_manager.get('photo_download_url'), folder)
    send_pictures_via_api(folder)
    time.sleep(config_manager.get('photo_interval_seconds'))
