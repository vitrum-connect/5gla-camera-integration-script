import unittest
import uuid

from src.config.config_manager import ConfigManager
from src.integration.camera_integration_service import CameraIntegrationService


class CameraPositionLoggingTest(unittest.TestCase):

    @unittest.skip("Skip this test as it requires the camera to be connected to the network.")
    def test_given_camera_position_when_logging_the_camera_position_should_be_logged(self):
        camera_integration_service = CameraIntegrationService()
        config_manager = ConfigManager()
        transaction_id = uuid.uuid4().__str__()
        camera_position_has_been_send_successfully = camera_integration_service.send_camera_position_via_api(
            drone_id=config_manager.get('drone_id'),
            transaction_id=transaction_id)
        self.assertTrue(camera_position_has_been_send_successfully)
