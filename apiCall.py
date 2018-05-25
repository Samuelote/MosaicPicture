from urllib.request import urlopen
import json
import cv2
import time
import numpy as np
import re
import time
import os
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
        self.replace()
        cv2.imshow('image', self.localImg)
        cv2.waitKey(0)


    # resizes local image
    def local_image(self, chosen_img):
        resp = cv2.imread(chosen_img)
        # height = int(int(resp.shape[0])/2)
        # width = int(int(resp.shape[1])/2)
        # resizedImg = cv2.resize(resp, (width, height))
        self.localImg = resp


    def loadImages(self):
        path, dirs, images = next(os.walk('./image_data/20x20'))
        for pic in images:
            self.imageBank.append(pic)


    # This replaces the existing pixels of the root image with 20x20px flickr images
    def replace(self):
        requiredIterations = ((self.localImg.shape[0]*1920))/200
        print("replace start", time.time() - start_time, "seconds to run")
        for j in range(0,len(self.imageBank)-1):
            iter = self.imageBank[j]
            readPic = cv2.imread('./image_data/20x20/'+iter)
            raw = str(iter[:-4]);
            rgb = raw[0]+raw[1]+raw[2]+','+raw[3]+raw[4]+raw[5]+','+raw[6]+raw[7]+raw[8]
            coords = self.findPixelMatch(rgb)
            if coords != 'No Match Found':
                self.i += 1;
                yaxis = int(coords[1])
                xaxis = int(coords[0])
                self.localImg[xaxis:xaxis+20, yaxis:yaxis+20] = readPic
        print("replace done", time.time() - start_time, "seconds to run")

        #     # else:
        #     #     if (j < len(self.imageBank)-100):
        #     #         self.imageBank.pop(j)
        #     #         j -= 1
        #
        # print(self.i, requiredIterations, '   banksize: ', len(self.imageBank))
        # if (self.i < requiredIterations):
        #     self.replace()
        # else:


    # Pretty self-explanatory. Once the flickr image is analyzed for average RGB, it is put into here to find
    # the closest match (if any) of our localImage
    def findPixelMatch(self, rgb):
        img = self.localImg
        b2 = int(rgb[0]+rgb[1]+rgb[2])
        g2 = int(rgb[4]+rgb[5]+rgb[6])
        r2 = int(rgb[8]+rgb[9]+rgb[10])
        for i in range(0,img.shape[0]-30, 20):
            for j in range(0, img.shape[1]-30, 20):
                b = int(img[i, j, 0])
                g = int(img[i, j, 1])
                r = int(img[i, j, 2])
                if ((r <= r2+3 and r >= r2-3) and (g <= g2+3 and g >= g2-3) and (b <= b2+3 and b >= b2-3) and self.checkForCoords(i, j) == False):
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