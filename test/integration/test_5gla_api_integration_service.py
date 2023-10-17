import unittest

from src.integration.api_integration_service import ApiIntegrationService


class ApiIntegrationServiceTest(unittest.TestCase):

    def test_given_running_api_when_checking_availability_then_should_return_true(self):
        api_integration_service = ApiIntegrationService()
        self.assertTrue(api_integration_service.check_availability())

    def test_given_running_api_when_sending_image_then_should_return_true(self):
        api_integration_service = ApiIntegrationService()
        self.assertTrue(
            api_integration_service.send_image(2, 4, 'BLUE', [self._read_base64_encoded_image_as_string_from_file()]))

    def test_given_running_api_when_sending_multiple_images_then_should_return_true(self):
        api_integration_service = ApiIntegrationService()
        self.assertTrue(
            api_integration_service.send_image(2, 4, 'BLUE', [self._read_base64_encoded_image_as_string_from_file(),
                                                              self._read_base64_encoded_image_as_string_from_file()]))

    @staticmethod
    def _read_base64_encoded_image_as_string_from_file():
        with open('test/integration/data/base64_drone_image.txt', 'r') as file:
            return file.read()
