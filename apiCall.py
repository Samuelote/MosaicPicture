from urllib.request import urlopen
import json
import cv2
import time
import numpy as np
import re



class pictureGenerator:

    def __init__(self, localImg):
        self.localImg = cv2.imread(localImg)
        self.occupiedCoords = []
        self.i = 0
        self.imageBank = []


    def localImage(self):
        # self.findRGB(img)
        for i in range(0,img.shape[0]):
            for j in range(0, img.shape[1]):
                b = int(img[i, j, 0])
                g = int(img[i, j, 1])
                r = int(img[i, j, 2])
                print(r, b, g)

        # height = int(int(img.shape[0])/1.3)
        # width = int(int(img.shape[1])/1.3)
        # resizedImg = cv2.resize(img, (width, height))
        # cv2.imshow('image', resizedImg)
        # cv2.waitKey(0)
        # print(img.shape)

    def loadImages(self):
        urlList = ["https://www.flickr.com/search/?text=solid%20colors&color_codes=e",
                   "https://www.flickr.com/search/?text=solid%20colors&color_codes=d",
                   "https://www.flickr.com/search/?text=solid%20colors&color_codes=a",
                   "https://www.flickr.com/search/?text=solid%20colors&color_codes=9",
                   "https://www.flickr.com/search/?text=solid%20colors&color_codes=8",
                   "https://www.flickr.com/search/?text=solid%20colors&color_codes=7",
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
        for item in urlList:
            photo = urlopen(item)
            html = photo.read().decode('utf-8')
            pattern = re.compile("(\/\/c1.staticflickr.com\/.+\.jpg)", re.UNICODE)
            for m in pattern.findall(html):
                self.i += 20
                url = 'http:' + m
                resp = urlopen(url)
                img = np.asarray(bytearray(resp.read()), dtype="uint8")
                img = cv2.imdecode(img, cv2.IMREAD_COLOR)
                resizedImg = cv2.resize(img, (20, 20))
                self.imageBank.append(resizedImg)


    def start(self):
        self.loadImages()
        print('now fires replace')
        self.replace()


    def replace(self):

        for iter in self.imageBank:
            coords = self.findPixelMatch(self.findAveragePixel(iter))
            if coords != 'No Match Found':
                self.i += 2
                yaxis = int(coords[1])
                xaxis = int(coords[0])
                self.localImg[xaxis:xaxis+20, yaxis:yaxis+20] = iter

        if self.i <= (self.localImg.shape[0]*self.localImg.shape[1])/200: self.replace()
        else:
            print(self.i, (self.localImg.shape[0]*self.localImg.shape[1])/200)
            cv2.imshow('image', self.localImg)
            cv2.waitKey(0)

    def findPixelMatch(self, rgb):
        # print(rgb)
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

    def findAveragePixel(self, img):
        if(len(img) > 0):
            avg = [int(img[:, :, i].mean()) for i in range(img.shape[-1])]
            return(avg)

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
    generator = pictureGenerator('/home/samuel/Pictures/erin.png')
    generator.start()




if __name__ == "__main__":
    main()

            # Working API CALL and stuff but I maxed out my calls for now


            # resp = urlopen(url)
            # img = np.asarray(bytearray(resp.read()), dtype="uint8")
            # img = cv2.imdecode(img, cv2.IMREAD_COLOR)
            # resizedImg = cv2.resize(img, (width, height))