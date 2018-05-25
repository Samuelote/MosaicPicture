from urllib.request import urlopen
import cv2
import numpy as np
from pathlib import Path
import json


# Returns list of [average_blue_val, average_green_val, average_red_val] from image.
def findAveragePixel(img):
    if(len(img) > 0):
        avg = [int(img[:, :, i].mean()) for i in range(img.shape[-1])]
        return(avg)


# Creates a filename for a given image using the average values of blue, red, and green.
def createLabel(img, directory):
    bgrVals = findAveragePixel(img)
    label = directory + "/" + format(bgrVals[0], '03d') + format(bgrVals[1], '03d') + format(bgrVals[2], '03d') + ".jpg"
    return label


# Downsamples image.
# Creates label based off of the average BGR Value of the sample.
# Writes the file to image_data directory.
def storeImage(img, directory):
    img = cv2.resize(img, (20,20))
    img_lab = createLabel(img, directory)
    my_file = Path(img_lab)
    if not my_file.exists():
        cv2.imwrite(img_lab,img)
        print("writing image:", img_lab)
    else:
        print("Image file already exists for", img_lab)


# Returns a list of image URLs from flickr.
# Takes a parameter for the API search.

# STILL NEEDS FUNCTIONALITY FOR QUANTITY!!!

def get_urls(search_text, quantity):
    ############################################################ Enter your own key in here. ###################################################################

    api_key = str(open("./apiKey").read()) # This should open a local file, so we don't have to keep removing our private key before pushing.
    url = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=' + api_key + '&text=' + search_text + '&sort=date-posted-desc&per_page=500&format=json&nojsoncallback=1'

    obj = urlopen(url).read().decode('utf-8')
    json_obj = json.loads(obj)
    image_url_list = []

    for item in json_obj['photos']['photo']:
        image_url = 'https://farm{}.staticflickr.com/{}/{}_{}.jpg'.format(item['farm'], item['server'], item['id'], item['secret'])
        image_url_list.append(image_url)

    return image_url_list


# Takes the URL of an image as a parameter.
# Reads the image with OpenCV.
# Stores image into specified directory.
def download_pictures(url_list):
    for url in url_list:
        resp = urlopen(url)
        img = np.asarray(bytearray(resp.read()), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        directory = "image_data/20x20"
        storeImage(img, directory)


def main():
    # Fill this list with generic terms to search their database with. There will likely be 500 images (maximum) for each term you put in this list.
    # An example is shown below... Beware that I stopped this about halfway through at around 50 minutes in.
    search_terms = ['gun', 'car', 'fun']
    for term in search_terms:
        print("Searching " + term + "...")
        image_urls = get_urls(term, 10)
        download_pictures(image_urls)


if __name__ == "__main__":
    main()
