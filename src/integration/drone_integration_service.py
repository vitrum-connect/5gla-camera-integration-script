import logging


class DroneIntegrationService:
    """
    Class that provides services for drone integration.

    """
    @staticmethod
    def still_has_power():
        logging.debug("Checking if the drone still has power.")
        return True
