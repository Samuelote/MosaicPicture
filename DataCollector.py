from urllib.request import urlopen
import cv2
import time
import numpy as np
import re
import time
from pathlib import Path
start_time = time.time()

def findAveragePixel(img):
    if(len(img) > 0):
        avg = [int(img[:, :, i].mean()) for i in range(img.shape[-1])]
        return(avg)

def createLabel(img, directory):
    rgbVals = findAveragePixel(img)
    label = directory + "/" + format(rgbVals[0], '03d') + format(rgbVals[1], '03d') + format(rgbVals[2], '03d') + ".jpg"
    return label

# 1. Downsamples image
# 2. Creates label based off of the average RGB Value of the sample
# 3. Writes the file to image_data directory
def storeImage(img, directory):
    img = cv2.resize(img, (20,20))
    img_lab = createLabel(img, directory)
    my_file = Path(img_lab)
    if not my_file.exists():
        cv2.imwrite(img_lab,img)
        print("writing image:", img_lab)
    else:
        print("Image file already exists for", img_lab)

def loadImages():
# My List of URL's for web-scraping
# Comment all out except one if you wanna see it run in any sort of timely manner
    urlList = ["https://www.flickr.com/search/?text=solid%20colors&color_codes=a",
    "https://www.flickr.com/search/?text=solid%20colors&color_codes=g",
    "https://www.flickr.com/search/?text=solid%20colors&color_codes=h",
    "https://www.flickr.com/search/?text=solid%20colors&color_codes=i",
    "https://www.flickr.com/search/?text=solid%20colors&color_codes=j",
    "https://www.flickr.com/search/?text=solid%20colors&color_codes=7",
    "https://www.flickr.com/search/?text=solid%20colors&color_codes=6",
    "https://www.flickr.com/search/?text=solid%20colors&color_codes=5",
    "https://www.flickr.com/search/?text=solid%20colors&color_codes=3",
    "https://www.flickr.com/search/?text=solid%20colors&color_codes=4",
    "https://www.flickr.com/search/?text=solid%20colors&color_codes=1",
    "https://www.flickr.com/search/?text=solid%20colors&color_codes=0",
    "https://www.flickr.com/photos/",
    "https://www.flickr.com/search/?text=solid%20colors&color_codes=2",
    "https://www.flickr.com/search/?text=solid%20colors&color_codes=b",
    "https://www.flickr.com/groups/44124468667@N01/pool/"
    ]

# regex for finding each jpg. Writes those images down to the image_data directory
    for item in urlList:
        photo = urlopen(item)
        html = photo.read().decode('utf-8')
        pattern = re.compile("(\/\/c1.staticflickr.com\/.+\.jpg)", re.UNICODE)
        for m in pattern.findall(html):
            # self.i += 20
            url = 'http:' + m
            resp = urlopen(url)
            img = np.asarray(bytearray(resp.read()), dtype="uint8")
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)
            directory = "image_data/20x20"
            storeImage(img, directory)

def main():
    loadImages()

if __name__ == "__main__":
    main()
