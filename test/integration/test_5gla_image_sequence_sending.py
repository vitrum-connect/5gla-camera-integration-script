import logging
import unittest

from app.integration.api_integration_service import ApiIntegrationService


class ImageSequenceSendingTest(unittest.TestCase):
    micasense_image_channels = ['BLUE', 'GREEN', 'RED', 'RED_EDGE', 'NIR']

    def test_send_image_sequence_to_api(self):
        api_integration_service = ApiIntegrationService()
        base64_encoded_images = self._read_all_images_as_base64_encoded_strings_from_files()
        self.assertEqual(5, len(base64_encoded_images))
        transaction_id = '693197e0-eea3-432c-8cff-a5ee8a7208a2'
        drone_id = '6f394286-5c51-49ff-ba98-a58de346188f'
        for channel, base64_encoded_image in base64_encoded_images.items():
            logging.info(f"Sending image for channel: {channel}")
            self.assertTrue(api_integration_service.send_image(transaction_id=('%s' % transaction_id),
                                                               drone_id=drone_id,
                                                               channel=channel,
                                                               images=[base64_encoded_image]))
        self.assertTrue(api_integration_service.end_transaction(transaction_id=transaction_id))

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
        with open(f'./data/encoded_image_set/{image_name}', 'r') as file:
            return file.read()
