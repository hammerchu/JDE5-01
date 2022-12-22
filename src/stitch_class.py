#!/usr/bin/python
import os
import cv2
import numpy as np


###
# Class to stitch video frame together 
#
###

class scan(object):

    def __init__(self):
        print("-------------------Init VG scan-------------------")

        self.frame_height = 20 # how many rows of pixel shall each frame be extracted
        self.step = 2


    def stitch(self, video):
        # 1. read through the video file
        # 2. extract rows of pixels and save in a tmp folder
        # 3. merge all the rows

        pass

    def buffer_crop(self, img, x1, x2, y1, y2):
        # extract and return pixels from an image

        w = int(img.shape[1])
        h = int(img.shape[0])

        if y1 < 1 and y2 < 1: # when y1 and y2 are percentage of the overall image height
            crop_img = img[int(h * y1):int(h * y2), int(w * x1):int(w * x2)]
        else: # when y1 and y2 are num of rows from the middle of image
            crop_img = img[int(h/2 - y1):int(h/2 + y2), int(w * x1):int(w * x2)]

        return crop_img



    def extract_frame(self, video, start, end, step):

        abs_path, dir_name, base_name = self.get_path(video)

        cap = cv2.VideoCapture(video)

        # Check if camera opened successfully
        if (cap.isOpened() == False):
            print("Error opening video stream or file")

        # Read until video is completed
        current_frame = 0
        print("Reading video success")

        os.makedirs(dir_name + '/'+ base_name, mode=0o755, exist_ok=True)

        while (cap.isOpened()):
            ## Capture frame-by-frame
            ret, frame = cap.read()
            

            if ret == True:

                # ## *********Process the image*********
                # frame = self.buffer_crop(frame, 0, 1, 0.49, 0.51)
                frame = self.buffer_crop(frame, 0, 1, self.frame_height/2, self.frame_height/2)

                img_name = base_name + '.' + str(current_frame).zfill(4) + ".jpg"

                if (current_frame % step == 0 and current_frame >= start and current_frame <= end):

                    ##export to a different folder 'img_dir' just for images

                    s = cv2.imwrite(dir_name + '/' + base_name + '/' + img_name, frame)
                    #print ('result ' + str(s))

                # Press Q on keyboard to  exit
                # print (current_frame)
                current_frame = current_frame + 1
            ## Break the loop
            else:
                break

        # When everything done, release the video capture object
        cap.release()

        dir_path = dir_name + '/' 
        base_name = base_name
        print(dir_path)
        print (base_name)
        return dir_path, base_name 

    def merge_frame(self, dir_path, base_name ):

        img_merged = 255 * np.ones(shape=[20, 3840, 3], dtype=np.uint8)

        for path in sorted(os.listdir(dir_path)):
            full_path = os.path.join(dir_path + base_name+'/'+ base_name, path)
            print(full_path)

            if os.path.isfile(full_path) and os.path.splitext(full_path)[-1] == ".jpg":
                print (full_path)
                img = cv2.imread(full_path)
                #cv2.imshow("A", img)
                img_merged = cv2.vconcat([img_merged, img])


        cv2.imwrite('../footage' + '/merge_'+ base_name +'.jpg', img_merged)

    def get_path(self, file):

        abs_path = os.path.abspath(file)
        base_name = os.path.basename(file).split(".")[0]
        dir_name =  os.path.dirname(file)

        return abs_path, dir_name, base_name
        
    

if __name__ == '__main__':

    print("running main")

    video_file = "../footage/VID_20200812_230216.mp4"

    node = scan()
    dir_path, base_name = node.extract_frame(video_file, 1, 10, 1)
    node.merge_frame(dir_path, base_name)

    # node.get_path(video_file)
