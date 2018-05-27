import os
import cv2


def findAveragePixel(img):
    if(len(img) > 0):
        avg = [float(img[:, :, i].mean()) for i in range(img.shape[-1])]
        return(avg)




class data_cleaner():
    def __init__(self):
        self.filenames = []
        self.gray_filenames = []
        self.gray_vals = []
        self.bgrs = []

    # Returns all image filenames from image_data/*x*/
    def get_image_filenames(self):
        self.filenames = os.listdir('./image_data/20x20/')

    def check_lengths(self):
        for filename in self.filenames:
            if len(filename) != 13:
                print("check_lengths:",filename)

    # Converts filename to a list of BGR values
    def filename_to_BGR(self, filename):
        filename = filename[:-4]
        return [int(filename[0:3]), int(filename[3:6]), int(filename[6:9])]

    def create_bgrs(self):
        for filename in self.filenames:
            self.bgrs.append(self.filename_to_BGR(filename))

    def create_gray_values(self):
        for bgr in self.bgrs:
            self.gray_vals.append((bgr[0] + bgr[1] + bgr[2]) / 3)

    def create_gray_labels(self):
        for i in range(len(self.gray_vals)):
            self.gray_filenames.append(format(self.gray_vals[i], '07.3f') + '_' + self.filenames[i])
            # print(self.gray_filenames[i])

    def create_gray_label(self, filename):
        print("original:", filename)
        filename = format(self.gray_vals[i], '07.3f') + '_' + filename
        print("gray:", filename)
        return filename

    def build_gray_files(self):
        for i in range(len(self.filenames)):
            img = cv2.imread('./image_data/20x20/' + self.filenames[i])
            label = self.createLabel(img, './image_data/test_20x20')
            print("writing", label)
            cv2.imwrite(label, img)

    def createLabel(self, img, directory):
        bgrVals = findAveragePixel(img)
        label = format(bgrVals[0], '07.3f') + '_' + format(bgrVals[1], '07.3f') + '_' + format(bgrVals[2], '07.3f') + ".jpg"
        gray_val = (bgrVals[0] + bgrVals[1] + bgrVals[2]) / 3
        label = format(gray_val, '07.3f') + '_' + label
        label = directory + '/' + label
        return label



clean = data_cleaner()
clean.get_image_filenames()
clean.create_bgrs()
clean.create_gray_values()
# clean.create_gray_labels()
clean.build_gray_files()
