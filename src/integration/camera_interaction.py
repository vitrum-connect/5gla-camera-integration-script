# This is a sample Python script.
import requests
from requests import get
from json import loads
import urllib.request

from src.integration.api_integration_service import ApiIntegrationService

"""
With these methods a Micasense multispectral camera can be accessed.
Standard config Ethernet access:
PC: IP: 192.168.1.40/24 Gateway:192.168.1.83
CameraIP: 192.168.1.83
"""


class CameraInteraction:

    def get_status(self, ip):
        #response = requests.get('http://192.168.1.83:80/status')
        response = requests.get(ip)
        print(response.status_code)
        return response.status_code

    def trigger_pictures(self, ip):
        #picture = requests.get('http://192.168.1.83:80/capture?preview=true')
        picture = requests.get(ip)
        print(picture.status_code)
        print(picture.content)

    def download_picture(self, ip, save):
        #path = "http://192.168.1.83/files"
        path = ip
        # Finds the last set
        sets = get(path)
        sets_array = loads(sets.text)
        all_set_names = sets_array['directories']
        print(f'{"Number of sets:"} \t {len(all_set_names)}')
        last_set = all_set_names[-1]
        print(f'{"Last Set:"} \t {last_set}')

        # Finds the last subset
        set_path = path + '/' + last_set
        print(set_path)
        subsets = get(set_path)
        subsets_array = loads(subsets.text)
        # print(subsets_array)
        all_subset_names = subsets_array['directories']
        # print(all_subset_names)
        print(f'{"Number of subsets:"} \t {len(all_subset_names)}')
        last_subset = all_subset_names[-1]
        print(f'{"Last Subset:"} \t {last_subset}')

        # Finds the last image
        subset_path = set_path + '/' + last_subset
        print(subset_path)
        images = get(subset_path)
        images_array = loads(images.text)
        # print(images_array)
        all_images = images_array['files']
        # allImageNames = all_images['name']
        # print(allImageNames)
        print(f'{"Number of images:"} \t {len(all_images)}')
        last_image = all_images[-1]
        last_image = last_image['name']
        print(f'{"Last Image:"} \t {last_image}')
        last_cap_pref = last_image[0:8]
        num_bands = int(last_image[-5])
        print(f'{"Last Capture Prefix:"} \t {last_cap_pref}')
        print(f'{"Number of Bands:"} \t {num_bands}')

        i = 1
        while i <= num_bands:
            img_path = subset_path + '/' + last_cap_pref + '_' + str(i) + '.tif'
            print(img_path)
            # Download of pictures
            img_name = last_cap_pref + '_' + str(i) + '.tif'
            #local_path = 'C:/Users/id496854/Documents/MicaSense_Integration/Pictures/' + img_name
            local_path = save + img_name
            urllib.request.urlretrieve(img_path, local_path)

            i += 1

    def send_pictures_via_api(self):
        api_integration_service = ApiIntegrationService()

        api_integration_service.check_availability()


capture = CameraInteraction()
capture.trigger_pictures('http://192.168.1.83:80/capture?preview=true')
capture.download_picture("http://192.168.1.83/files", 'C:/Users/id496854/Documents/MicaSense_Integration/Pictures/')

