# This is a sample Python script.
import logging
import os
import urllib.request
from json import loads

import requests
from requests import get


class CameraInteraction:
    """
    CameraInteraction class for handling interactions with a camera.

    Methods:
        - get_status(ip)
        - trigger_pictures(ip)
        - download_picture(ip, save)
        - send_pictures_via_api()
    """

    @staticmethod
    def trigger_pictures(ip):
        """
        :param ip: The IP address of the server from which to request the picture
        :return: None

        """
        picture = requests.get(ip)
        logging.info(f"Picture status: {picture.status_code}")
        logging.info(f"Picture content: {picture.content}")

    @staticmethod
    def download_picture(ip, save):
        """
        :param ip: The IP address of the server where the pictures are stored.
        :param save: The directory where the downloaded pictures will be saved.
        :return: None

        Downloads the latest picture from a server given its IP address and saves it to a specified directory.

        Example Usage:
        download_picture('192.168.0.1', 'C:/Pictures/')
        """
        path = ip
        sets = get(path)
        sets_array = loads(sets.text)
        all_set_names = sets_array['directories']
        logging.info(f"Number of sets: {len(all_set_names)}")
        last_set = all_set_names[-1]
        logging.info(f"Last Set: {last_set}")
        set_path = path + '/' + last_set
        subsets = get(set_path)
        subsets_array = loads(subsets.text)
        all_subset_names = subsets_array['directories']
        logging.debug(f"Number of subsets: {len(all_subset_names)}")
        last_subset = all_subset_names[-1]
        logging.debug(f"Last Subset: {last_subset}")
        subset_path = set_path + '/' + last_subset
        logging.debug(f"Subset Path: {subset_path}")
        images = get(subset_path)
        images_array = loads(images.text)
        all_images = images_array['files']
        logging.debug(f"Number of images: {len(all_images)}")
        last_image = all_images[-1]
        last_image = last_image['name']
        logging.debug(f"Last Image: {last_image}")
        last_cap_pref = last_image[0:8]
        num_bands = int(last_image[-5])
        logging.debug(f"Last Capture Prefix: {last_cap_pref}")
        logging.debug(f"Number of Bands: {num_bands}")

        i = 1
        while i <= num_bands:
            img_path = subset_path + '/' + last_cap_pref + '_' + str(i) + '.tif'
            print(img_path)
            img_name = last_cap_pref + '_' + str(i) + '.tif'
            local_path = save + img_name
            urllib.request.urlretrieve(img_path, local_path)
            i += 1

    @staticmethod
    def create_folder(folder):
        """
        :param folder: The folder to create.
        :return: None

        Creates a folder if it does not exist.

        Example Usage:
        create_folder('C:/Pictures/')
        """
        try:
            os.makedirs(folder)
        except FileExistsError:
            logging.info(f"Folder '{folder}' already exists.")
        except Exception as e:
            logging.error(f"An error occurred while creating the folder: {e}")
