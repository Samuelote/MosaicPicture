import os

class data_cleaner():
    def __init__(self):
        self.filenames = []

    # Returns all image filenames from image_data/*x*/
    def get_image_filenames(self):
        self.filenames = os.listdir('./image_data/20x20/')

    def check_lengths(self):
        for filename in self.filenames:
            if len(filename) != 13:
                print(filename)

clean = data_cleaner()
clean.get_image_filenames()
clean.check_lengths()
