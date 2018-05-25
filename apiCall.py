from urllib.request import urlopen
import json
import cv2
import time
import numpy as np
import re
import time
import os
from pathlib import Path

start_time = time.time()

# I'm stupid and just realized that things aren't supposed to be camel cased in Python. My JS mind fkd me up. So that'll change soon.

class pictureGenerator:

    def __init__(self, chosenImg):
        self.chosenImg = chosenImg
        self.localImg = ''
        self.i = 0


    def start(self):
        self.local_image(self.chosenImg)
        print("start", time.time() - start_time, "seconds to run")
        self.loop_local_img()
        print("finished", time.time() - start_time, "seconds to run")


        cv2.imshow('image', self.localImg)
        cv2.waitKey(0)


    def loop_local_img(self):
        img = self.localImg

        # Basically this loop is iterating by 20. But as you may see
        # line 45, this syntax: " self.localImg[i:i+20,j:j+20] " includes  every pixel
        # between those 20 pixel spans. I hope that makes sense...

        for i in range(0,img.shape[0], 20):
            for j in range(0, img.shape[1], 20):

                #finds average pixel for every 20x20 square of local image
                rgb = self.findAveragePixel(self.localImg[i:i+20,j:j+20])

                # converts the rgb to the formats of the files in our image_data directory
                fileFormat = ''.join(rgb)+'.jpg'

                # this is used to check if the file exists
                path = Path('./image_data/20x20/' + fileFormat)

                #this checks to see if file exists
                if path.is_file():
                    # reads each picture
                    readPic = cv2.imread('./image_data/20x20/' + fileFormat)

                    #assigns picture to correct coordinates of local image
                    self.localImg[i:i + 20, j:j + 20] = readPic
                    print('success')



    ## Calculates the average RGB value of img argument
    def findAveragePixel(self, img):
        if(len(img) > 0):
            avg = [format(int(img[:, :, i].mean()), '03d') for i in range(img.shape[-1])]
            return(avg)



    # resizes local image
    def local_image(self, chosen_img):
        resp = cv2.imread(chosen_img)
        # height = int(int(resp.shape[0])/2)
        # width = int(int(resp.shape[1])/2)
        # resizedImg = cv2.resize(resp, (width, height))
        self.localImg = resp


    # This replaces the existing pixels of the root image with 20x20px flickr images
    # def replace(self):
    #     requiredIterations = ((self.localImg.shape[0]*1920))/200
    #     print("replace start", time.time() - start_time, "seconds to run")
    #     for j in range(0,len(self.imageBank)-1):
    #         iter = self.imageBank[j]
    #         readPic = cv2.imread('./image_data/20x20/'+iter)
    #         raw = str(iter[:-4]);
    #         rgb = raw[0]+raw[1]+raw[2]+','+raw[3]+raw[4]+raw[5]+','+raw[6]+raw[7]+raw[8]
    #         coords = self.findPixelMatch(rgb)
    #         if coords != 'No Match Found':
    #             self.i += 1;
    #             yaxis = int(coords[1])
    #             xaxis = int(coords[0])
    #             self.localImg[xaxis:xaxis+20, yaxis:yaxis+20] = readPic
    #     print("replace done", time.time() - start_time, "seconds to run")
    #
    #     #     # else:
    #     #     #     if (j < len(self.imageBank)-100):
    #     #     #         self.imageBank.pop(j)
    #     #     #         j -= 1
    #     #
    #     # print(self.i, requiredIterations, '   banksize: ', len(self.imageBank))
    #     # if (self.i < requiredIterations):
    #     #     self.replace()
    #     # else:








def main():
    # link a path to a local photo here before running
    generator = pictureGenerator('/home/samuel/Pictures/erin.png')
    generator.start()




if __name__ == "__main__":
    main()