import unittest

from app.integration.api_integration_service import ApiIntegrationService


class ApiIntegrationServiceTest(unittest.TestCase):

    def test_given_running_api_when_checking_availability_then_should_return_true(self):
        api_integration_service = ApiIntegrationService()
        self.assertTrue(api_integration_service.check_availability())
