# This is a sample Python script.
import requests
from requests import get, post
from json import loads
import urllib.request

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# ip = "192.168.1.83"
# port = "80"

class camera_interaction:
    """
    With the methods in ths class a Micasense multispectral camera can be accessed.
    """

    def get_status(self):
        response = requests.get('http://192.168.1.83:80/status')
        print(response.status_code)


    def trigger_pictures(self):
        picture = requests.get('http://192.168.1.83:80/capture?preview=true')
        print(picture.status_code)
        print(picture.content)

    def download_picture(self):
        path = "http://192.168.1.83/files"

        # Finds the last set
        Sets = get(path)
        SetsArray = loads(Sets.text)
        allSetNames = SetsArray['directories']
        print(f'{"Number of Sets:"} \t {len(allSetNames)}')
        lastSet = allSetNames[-1]
        print(f'{"Last Set:"} \t {lastSet}')

        # Finds the last subset
        setPath = path + '/' + lastSet
        print(setPath)
        Subsets = get(setPath)
        SubsetsArray = loads(Subsets.text)
        # print(SubsetsArray)
        allSubsetNames = SubsetsArray['directories']
        # print(allSubsetNames)
        print(f'{"Number of Subsets:"} \t {len(allSubsetNames)}')
        lastSubset = allSubsetNames[-1]
        print(f'{"Last Subset:"} \t {lastSubset}')

        # Finds the last image
        subsetPath = setPath + '/' + lastSubset
        print(subsetPath)
        Images = get(subsetPath)
        ImagesArray = loads(Images.text)
        # print(ImagesArray)
        allImages = ImagesArray['files']
        # allImageNames = allImages['name']
        # print(allImageNames)
        print(f'{"Number of Images:"} \t {len(allImages)}')
        lastImage = allImages[-1]
        lastImage = lastImage['name']
        print(f'{"Last Image:"} \t {lastImage}')
        lastCapPref = lastImage[0:8]
        numBands = int(lastImage[-5])
        print(f'{"Last Capture Prefix:"} \t {lastCapPref}')
        print(f'{"Number of Bands:"} \t {numBands}')

        i = 1
        while i <= numBands:
            imgPath = subsetPath + '/' + lastCapPref + '_' + str(i) + '.tif'
            print(imgPath)
            #Download of pictures
            img_name = lastCapPref + '_' + str(i) + '.tif'
            localPath = 'C:/Users/id496854/Documents/MicaSense_Integration/Pictures/' + img_name
            urllib.request.urlretrieve(imgPath, localPath)

            i += 1