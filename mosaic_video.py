from urllib.request import urlopen
import json
import cv2
import time
import numpy as np
import re
import time
import os
from pathlib import Path
from bisect import bisect_left

start_time = time.time()

# Size of replaced image square segment (SEGMENT_SIZE x SEGMENT_SIZE)
SEGMENT_SIZE = 5

class pictureGenerator:

    def __init__(self, chosen_img):
        self.chosen_img = chosen_img
        self.localImg = ''
        self.filenames = ''
        self.gray_bgrs = []
        self.grays = []
        self.replacement_size = SEGMENT_SIZE

        # Initialize output image to completely black picture
        self.output_image = cv2.imread('./image_data/test_20x20/000.000_000.000_000.000_000.000.jpg')


    def start(self):
        self.local_image()

        self.get_image_filenames()

        # Builds a list of the bgr values of images in image_data
        for filename in self.filenames:
            self.gray_bgrs.append(self.filename_to_gray_BGR(filename))

        self.build_grays()
        self.loop_local_img()
        print("finished in", time.time() - start_time, "seconds")

        # cv2.imwrite('greek_200.jpg', self.output_image)
        # cv2.imshow('image', self.output_image)
        # cv2.waitKey(0)

    # Returns all image filenames from image_data/*x*/
    def get_image_filenames(self):
        self.filenames = sorted(os.listdir('./image_data/test_20x20/'))


    # Converts filename to a list of BGR values
    def filename_to_BGR(self, filename):
        filename = filename[:-4]
        return [int(filename[0:3]), int(filename[3:6]), int(filename[6:9])]

    def filename_to_gray_BGR(self, filename):
        filename = filename[:-4]
        return([float(filename[0:7]), float(filename[8:15]), float(filename[16:23]), float(filename[24:31])])

    # Converts BGR list to filename
    def BGR_to_filename(self, BGR_List):
        filename = format(BGR_List[0], '03d') + format(BGR_List[1], '03d') + format(BGR_List[2], '03d') + '.jpg'
        return filename

    def loop_local_img(self):
        img = self.localImg

        # Basically this loop is iterating by 20. But as you may see
        # line 45, this syntax: " self.localImg[i:i+20,j:j+20] " includes  every pixel
        # between those 20 pixel spans. I hope that makes sense...

        total_steps = self.output_image.shape[0] * self.output_image.shape[1] / 400
        print("total steps:", total_steps)
        step = 1

        for i in range(0,img.shape[0], self.replacement_size):
            for j in range(0, img.shape[1], self.replacement_size):

                # finds average pixel for every 20x20 square of local image
                bgr_section = self.findAveragePixel_GRGB(self.localImg[i:i+self.replacement_size,j:j+self.replacement_size])

                # reads in the image from image_data with the best match for average BGR values
                best_match_index = self.find_best_match(bgr_section)
                # match_filename = self.BGR_to_filename(self.gray_bgrs[best_match_index])
                # match_filename = format(self.gray_vals[best_match_index], '05.1f') + '_' + self.filenames[i])
                match_filename = self.filenames[best_match_index]
                readPic = cv2.imread('./image_data/test_20x20/' + match_filename)
                # print(match_filename)

                # self.localImg[i:i + 20, j:j + 20] = readPic
                self.output_image[int(i* 20 / self.replacement_size):int((i* 20 / self.replacement_size) + 20), int(j* 20 / self.replacement_size):int((j* 20 / self.replacement_size) + 20)] = readPic

                progress_percentage = step * 100 / total_steps
                # print(progress_percentage / 100)
                if step % 10 == 0:
                    # os.system('clear')
                    # print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
                    print('{:05.2f} % finished'.format(progress_percentage))
                step += 1

    def find_best_match(self, image_gbgr):
        lowest_error = 255 * 255 * 3
        lowest_error_index = 0

        # Bisection method to find best middle index for image search
        # Search is based off of the average grayscale value i.e. brightness
        mid_index = bisect_left(self.grays, float(image_gbgr[0]))

        index_range = 1000

        if mid_index < index_range:
            low_index = 0
        else:
            low_index = mid_index - index_range

        if mid_index >= (len(self.gray_bgrs) - index_range):
            high_index = len(self.gray_bgrs) - 1
        else:
            high_index = mid_index + index_range

        for index in range(low_index, high_index + 1):
            error = 0
            for i in range(1,4):
                error += pow(abs(float(image_gbgr[i]) - self.gray_bgrs[index][i]), 2)
            if error < lowest_error:
                lowest_error = error
                lowest_error_index = index
        return lowest_error_index

    ## Calculates the average RGB value of img argument
    def findAveragePixel(self, img):
        if(len(img) > 0):
            avg = [format(int(img[:, :, i].mean()), '03d') for i in range(img.shape[-1])]
            return(avg)

    ## Calculates the average RGB values of img argument and places a grayscale value in front
    def findAveragePixel_GRGB(self, img):
        if(len(img) > 0):
            avg = [format(float(img[:, :, i].mean()), '07.3f') for i in range(img.shape[-1])]
            gray = float(avg[0]) + float(avg[1]) + float(avg[2]) / 3
            avg.insert(0, format(gray, '07.3f'))
            return(avg)

    def build_grays(self):
        for gbgr in self.gray_bgrs:
            self.grays.append(float(gbgr[0]))


    # resizes local image
    def local_image(self):
        # resp = cv2.imread(self.chosen_img)
        resp = self.chosen_img
        height = resp.shape[0]
        width = resp.shape[1]
        while(height % self.replacement_size != 0):
            height = height - 1
        while(width % self.replacement_size != 0):
            width = width - 1
        resp = cv2.resize(resp, (width, height))

        self.localImg = resp
        self.output_image = cv2.resize(self.output_image, (int(width * 20 / self.replacement_size), int(height * 20 / self.replacement_size)))

def main():
    # link a path to a local photo here before running
    # generator = pictureGenerator('greek.jpg')
    # generator.start()
    # cv2.imshow('image', generator.output_image)
    # cv2.waitKey(0)

    cap = cv2.VideoCapture('SampleVideo.mp4')

    # Check if camera opened successfully
    if (cap.isOpened()== False):
      print("Error opening video stream or file")

    width = int(cap.get(3))
    height = int(cap.get(4))

    while(height % SEGMENT_SIZE != 0):
        height = height - 1
    while(width % SEGMENT_SIZE != 0):
        width = width - 1

    frame_width = int(width * 20 / SEGMENT_SIZE)
    frame_height = int(height * 20 / SEGMENT_SIZE)


    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter('SampleOut_5.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

    frame_count = 0

    while(cap.isOpened()):
    # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            generator = pictureGenerator(frame)
            generator.start()

            out.write(generator.output_image)

            print("frame_count:", frame_count)
            frame_count = frame_count + 1
        else:
            break

    # When everything done, release the video capture object
    cap.release()
    out.release()

if __name__ == "__main__":
    main()
    os.system('say "your program has finished"')
