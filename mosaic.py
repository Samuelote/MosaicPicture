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

    def __init__(self, chosen_img):
        self.chosen_img = chosen_img
        self.localImg = ''
        self.i = 0
        self.filenames = ''
        self.bgrs = []


    def start(self):
        self.local_image()
        print("start", time.time() - start_time, "seconds to run")

        self.get_image_filenames()

        # Builds a list of the bgr values of images in image_data
        for filename in self.filenames:
            self.bgrs.append(self.filename_to_BGR(filename))

        self.loop_local_img()
        print("finished", time.time() - start_time, "seconds to run")

        cv2.imwrite('greek_L2.jpg', self.localImg)
        cv2.imshow('image', self.localImg)
        cv2.waitKey(0)

    # Returns all image filenames from image_data/*x*/
    def get_image_filenames(self):
        self.filenames = os.listdir('./image_data/20x20/')

    # Converts filename to a list of BGR values
    def filename_to_BGR(self, filename):
        filename = filename[:-4]
        return [int(filename[0:3]), int(filename[3:6]), int(filename[6:9])]

    # Converts BGR list to filename
    def BGR_to_filename(self, BGR_List):
        filename = format(BGR_List[0], '03d') + format(BGR_List[1], '03d') + format(BGR_List[2], '03d') + '.jpg'
        return filename

    def loop_local_img(self):
        img = self.localImg

        # Basically this loop is iterating by 20. But as you may see
        # line 45, this syntax: " self.localImg[i:i+20,j:j+20] " includes  every pixel
        # between those 20 pixel spans. I hope that makes sense...

        total_steps = img.shape[0] * img.shape[1] / 400
        print("total steps:", total_steps)
        step = 1

        for i in range(0,img.shape[0], 20):
            for j in range(0, img.shape[1], 20):

                # finds average pixel for every 20x20 square of local image
                bgr_section = self.findAveragePixel(self.localImg[i:i+20,j:j+20])

                # reads in the image from image_data with the best match for average BGR values
                best_match_index = self.find_best_match(bgr_section)
                match_filename = self.BGR_to_filename(self.bgrs[best_match_index])
                readPic = cv2.imread('./image_data/20x20/' + match_filename)

                self.localImg[i:i + 20, j:j + 20] = readPic

                progress_percentage = step * 100 / total_steps
                print('{:05.2f} % finished'.format(progress_percentage))
                step += 1

    def find_best_match(self, image_bgr):
        lowest_error = 255 * 3
        lowest_error_index = 0
        for index in range(len(self.bgrs)):
            error = 0
            for i in range(3):
                error += pow(abs(int(image_bgr[i]) - self.bgrs[index][i]), 2)
            # print("error[" + str(index) + "]:", error)
            if error < lowest_error:
                lowest_error = error
                lowest_error_index = index
        # print("lowest error:", lowest_error)
        # print("at index:", lowest_error_index)
        return lowest_error_index

    ## Calculates the average RGB value of img argument
    def findAveragePixel(self, img):
        if(len(img) > 0):
            avg = [format(int(img[:, :, i].mean()), '03d') for i in range(img.shape[-1])]
            return(avg)



    # resizes local image
    def local_image(self):
        resp = cv2.imread(self.chosen_img)
        height = resp.shape[0]
        width = resp.shape[1]
        while(height % 20 != 0):
            height = height - 1
        while(width % 20 != 0):
            width = width - 1
        resp = cv2.resize(resp, (width, height))

        self.localImg = resp


def main():
    # link a path to a local photo here before running
    generator = pictureGenerator('greek.jpg')
    # generator.start()
    generator.local_image()



if __name__ == "__main__":
    main()
