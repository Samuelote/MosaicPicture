import cv2
import time
import os
from bisect import bisect_left

# Desired output image filename (WARNING: WILL OVERWRITE FILES!)
out_filename = 'out.jpg'

# Size of replaced image square segment (SEGMENT_SIZE x SEGMENT_SIZE)
SEGMENT_SIZE = 250

class mosaic_generator:

    def __init__(self, input_img, segment_size):
        self.input_image = input_img
        self.localImg = ''
        self.filenames = ''
        self.gray_bgrs = []
        self.grays = []
        self.replacement_size = segment_size
        self.start_time = 0

        # Initialize output image to completely black picture
        self.output_image = cv2.imread('./image_data/test_20x20/000.000_000.000_000.000_000.000.jpg')


    def start(self):
        self.start_time = time.time()
        self.prepare_image()
        self.get_image_data_filenames()

        # Builds a list of the [grayscale, b, g, r] values of images in image_data
        for filename in self.filenames:
            self.gray_bgrs.append(self.filename_to_GBGR(filename))

        self.build_grays()
        self.loop_local_img()
        if str(type(self.input_image)) == """<class 'str'>""":
            print("finished in", time.time() - self.start_time, "seconds")
            print('\n')
            print("To exit: Click image and press any key.")

            cv2.imwrite(out_filename, self.output_image)
            cv2.imshow('image', self.output_image)
            cv2.waitKey(0)

            print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
            print("Your image is stored as:", out_filename)

    # Returns all image filenames from image_data/*x*/
    def get_image_data_filenames(self):
        self.filenames = sorted(os.listdir('./image_data/test_20x20/'))


    # Converts a filename to a list of [gray, blue, green, red] values
    def filename_to_GBGR(self, filename):
        filename = filename[:-4]
        return([float(filename[0:7]), float(filename[8:15]), float(filename[16:23]), float(filename[24:31])])


    # Loops over input image
    # Breaks into segments of self.replacement_size
    # Replaces each segment with best-fitting image from database
    def loop_local_img(self):
        img = self.localImg

        # Stats for progress feedback
        total_steps = self.output_image.shape[0] * self.output_image.shape[1] / 400
        if str(type(self.input_image)) == """<class 'str'>""":
            print("Total number of segments to replace:", total_steps)
        step = 1

        # Loops through input image width-wise and height-wise with steps of self.replacement_size
        for i in range(0,img.shape[0], self.replacement_size):
            for j in range(0, img.shape[1], self.replacement_size):

                # Calculates average pixel for every segment of input image
                bgr_section = self.find_average_values_GRGB(self.localImg[i:i+self.replacement_size,j:j+self.replacement_size])

                # Reads in the image from image_data with the best match for average BGR values
                best_match_index = self.find_best_match(bgr_section)
                match_filename = self.filenames[best_match_index]
                readPic = cv2.imread('./image_data/test_20x20/' + match_filename)

                self.output_image[int(i* 20 / self.replacement_size):int((i* 20 / self.replacement_size) + 20), int(j* 20 / self.replacement_size):int((j* 20 / self.replacement_size) + 20)] = readPic

                # Display progress in terminal
                progress_percentage = step * 100 / total_steps
                if step % 10 == 0 and str(type(self.input_image)) == """<class 'str'>""":
                    os.system('clear')
                    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
                    print('{:05.2f} % finished'.format(progress_percentage))
                step += 1

    # Searches database and returns the index of the most-fitting image for given [gray,blue,green,red]
    def find_best_match(self, image_gbgr):
        lowest_error = 255 * 255 * 3
        lowest_error_index = 0

        # Bisection method to find best middle index for image search
        # Search is based off of the average grayscale value i.e. brightness
        mid_index = bisect_left(self.grays, float(image_gbgr[0]))


        # Searches within 1000 indeces of mid_index
        index_range = 1000

        if mid_index < index_range:
            low_index = 0
        else:
            low_index = mid_index - index_range

        if mid_index >= (len(self.gray_bgrs) - index_range):
            high_index = len(self.gray_bgrs) - 1
        else:
            high_index = mid_index + index_range

        # Minimizes sum of squares error
        for index in range(low_index, high_index + 1):
            error = 0
            for i in range(1,4):
                error += pow(abs(float(image_gbgr[i]) - self.gray_bgrs[index][i]), 2)
            if error < lowest_error:
                lowest_error = error
                lowest_error_index = index
        return lowest_error_index


    ## Calculates the average RGB values of img argument and places a grayscale value in front
    def find_average_values_GRGB(self, img):
        if(len(img) > 0):
            avg = [format(float(img[:, :, i].mean()), '07.3f') for i in range(img.shape[-1])]
            gray = float(avg[0]) + float(avg[1]) + float(avg[2]) / 3
            avg.insert(0, format(gray, '07.3f'))
            return(avg)


    # Initializes array of grayscale values
    def build_grays(self):
        for gbgr in self.gray_bgrs:
            self.grays.append(float(gbgr[0]))


    # Resizes local image
    def prepare_image(self):
        if str(type(self.input_image)) == """<class 'str'>""":
            resp = cv2.imread(self.input_image)
        else:
            resp = self.input_image
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
    generator = mosaic_generator('greek.jpg', SEGMENT_SIZE)
    generator.start()



if __name__ == "__main__":
    main()
