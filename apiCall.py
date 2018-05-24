from urllib.request import urlopen
import json
import cv2
import time
import numpy as np
import re
import time
start_time = time.time()

# I'm stupid and just realized that things aren't supposed to be camel cased in Python. My JS mind fkd me up. So that'll change soon.

class pictureGenerator:

    def __init__(self, chosenImg):
        self.chosenImg = chosenImg
        self.localImg = ''
        self.occupiedCoords = []
        self.i = 0
        self.imageBank = []


    def start(self):
        self.local_image(self.chosenImg)
        self.loadImages()
        print("loadImages took", time.time() - start_time, "seconds to run")
        self.replace()


    # resizes local image
    def local_image(self, localImg):
        resp = cv2.imread(localImg)
        # height = int(int(resp.shape[0])/2)
        # width = int(int(resp.shape[1])/2)
        # resizedImg = cv2.resize(resp, (width, height))
        self.localImg = resp


    def loadImages(self):

        # My List of URL's for web-scraping

        # Comment all out except one if you wanna see it run in any sort of timely manner

        urlList = ["https://www.flickr.com/search/?text=solid%20colors&color_codes=e",
                   # "https://www.flickr.com/search/?text=solid%20colors&color_codes=d",
                   # "https://www.flickr.com/search/?text=solid%20colors&color_codes=a",
                   # "https://www.flickr.com/search/?text=solid%20colors&color_codes=9",
                   # "https://www.flickr.com/search/?text=solid%20colors&color_codes=8",
                   # "https://www.flickr.com/search/?text=solid%20colors&color_codes=7",
                   # "https://www.flickr.com/search/?text=solid%20colors&color_codes=6",
                   # "https://www.flickr.com/search/?text=solid%20colors&color_codes=5",
                   # "https://www.flickr.com/search/?text=solid%20colors&color_codes=3",
                   # "https://www.flickr.com/search/?text=solid%20colors&color_codes=4",
                   # "https://www.flickr.com/search/?text=solid%20colors&color_codes=1",
                   # "https://www.flickr.com/search/?text=solid%20colors&color_codes=0",
                   # "https://www.flickr.com/photos/",
                   # "https://www.flickr.com/search/?text=solid%20colors&color_codes=2",
                   # "https://www.flickr.com/search/?text=solid%20colors&color_codes=b",
                   # "https://www.flickr.com/groups/44124468667@N01/pool/"
                   ]

        # regex for finding each jpg. Pushes those found jpgs to self.imageBank

        for item in urlList:
            photo = urlopen(item)
            html = photo.read().decode('utf-8')
            print(html)
            pattern = re.compile("(\/\/c1.staticflickr.com\/.+\.jpg)", re.UNICODE)
            # for m in pattern.findall(html):
            #     self.i += 20
            #     url = 'http:' + m
            #     resp = urlopen(url)
            #     img = np.asarray(bytearray(resp.read()), dtype="uint8")
            #     img = cv2.imdecode(img, cv2.IMREAD_COLOR)
            #     resizedImg = cv2.resize(img, (20, 20))
            #     self.imageBank.append(resizedImg)


    # This replaces the existing pixels of the root image with 20x20px flickr images
    def replace(self):
        for iter in self.imageBank:
            coords = self.findPixelMatch(self.findAveragePixel(iter))
            if coords != 'No Match Found':
                self.i += 1
                yaxis = int(coords[1])
                xaxis = int(coords[0])
                self.localImg[xaxis:xaxis+20, yaxis:yaxis+20] = iter

        print("Everything else took", time.time() - start_time, "seconds to run")
        cv2.imshow('image', self.localImg)
        cv2.waitKey(0)



    ## Calculates the average RGB value of img argument
    def findAveragePixel(self, img):
        if(len(img) > 0):
            avg = [int(img[:, :, i].mean()) for i in range(img.shape[-1])]
            return(avg)


    # Pretty self-explanatory. Once the flickr image is analyzed for average RGB, it is put into here to find
    # the closest match (if any) of our localImage
    def findPixelMatch(self, rgb):
        img = self.localImg
        for i in range(0,img.shape[0]-30, 20):
            for j in range(0, img.shape[1]-30, 20):
                b = int(img[i, j, 0])
                g = int(img[i, j, 1])
                r = int(img[i, j, 2])
                if ((r <= rgb[0]+5 and r >= rgb[0]-5) and (g <= rgb[1]+5 and g >= rgb[1]-5) and (b <= rgb[2]+5 and b >= rgb[2]-5) and self.checkForCoords(i, j) == False):
                    self.occupiedCoords.append([i,j])
                    return (i, j)
        return ('No Match Found')

    # This makes sure we don't overwrite already filled in pixels with other flickr images
    def checkForCoords(self, i, j):
        bool = None
        for z in range(0, 20):
            for t in range(0, 20):
                if ([i+z, j+t] in self.occupiedCoords) or ([i-z, j-t] in self.occupiedCoords):
                    # print(i,j)
                    bool = True
                else:
                    bool = False
        return bool




def main():
    # link a path to a local photo here before running
    generator = pictureGenerator('/home/samuel/Pictures/erin.png')
    generator.start()




if __name__ == "__main__":
    main()