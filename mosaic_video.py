import mosaic_gray as mos

import cv2
import os
SEGMENT_SIZE = 250

def main():

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
    out = cv2.VideoWriter('SampleOut_50.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

    frame_count = 0

    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            generator = mos.mosaic_generator(frame, SEGMENT_SIZE)
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
