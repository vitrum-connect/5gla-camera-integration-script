import logging
import unittest

from src.integration.api_integration_service import ApiIntegrationService


class ImageSequenceSendingTest(unittest.TestCase):
    micasense_image_channels = ['BLUE', 'GREEN', 'RED', 'RED_EDGE', 'NIR']

    @unittest.skip("Skip this test as it requires the camera to be connected to the network.")
    def test_send_image_sequence_to_api(self):
        api_integration_service = ApiIntegrationService()
        base64_encoded_images = self._read_all_images_as_base64_encoded_strings_from_files()
        self.assertEqual(5, len(base64_encoded_images))
        transaction_id = 'a5ee8a7208a2'
        camera_id = 'a58de346188f1236'
        for channel, base64_encoded_image in base64_encoded_images.items():
            logging.info(f"Sending image for channel: {channel}")
            self.assertTrue(api_integration_service.send_image(transaction_id=('%s' % transaction_id),
                                                               camera_id=camera_id,
                                                               channel=channel,
                                                               images=[base64_encoded_image]))

    @staticmethod
    def _read_all_images_as_base64_encoded_strings_from_files():
        base74_encoded_images = {}
        for i in range(0, 5):
            image_name = f"base64_encoded_drone_image_{i + 1}.txt"
            logging.info(f"Reading image: {image_name}")
            base64_encoded_image = ImageSequenceSendingTest._read_base64_encoded_image(image_name)
            base74_encoded_images[ImageSequenceSendingTest.micasense_image_channels[i]] = base64_encoded_image
        return base74_encoded_images

    @staticmethod
    def _read_base64_encoded_image(image_name):
        # Show the current directory
        import os
        logging.info(f"Current directory: {os.getcwd()}")
        with open(f'data/encoded_image_set/{image_name}', 'r') as file:
            return file.read()
