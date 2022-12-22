import os
import cv2
import imutils
import string
import buffer_process
import numpy as np
import math
from datetime import datetime


def f_name(j):
    tmp = (os.path.splitext(j))
    return tmp[0]

def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)

def write_frame(dir, f, start, end, step):
    ## Take a video, do something to it and write them onto local folder


    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    print('Reading: '+ dir +f)
    cap = cv2.VideoCapture(dir+f)

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    # Read until video is completed
    current_frame = 0
    print("Reading video success")

    while (cap.isOpened()):
        ## Capture frame-by-frame
        ret, frame = cap.read()
        os.makedirs(img_dir + f_name(f), mode=0o755, exist_ok=True)

        if ret == True:


            ## *********Process the image*********
            frame = buffer_process.buffer_crop(frame, 0, 1, 0.49, 0.51)

            img_name = f_name(f) + '.' + str(current_frame).zfill(4) + ".jpg"
            #print (img_dir + f_name(f) +'/'+ img_name)

            if (current_frame % step == 0 and current_frame >= start and current_frame <= end):

                ##export to a different folder 'img_dir' just for images

                s = cv2.imwrite(img_dir + f_name(f) +'/'+ img_name, frame)
                #print ('result ' + str(s))

            ## Press Q on keyboard to  exit
            current_frame = current_frame + 1
        ## Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()


def remove_frame(dir, f):
    print ('dir: '+dir+f_name(f))
    if os.path.exists(dir+f_name(f)):
        for path in os.listdir(dir+f_name(f)):
            full_path = os.path.join(dir+f_name(f), path)
            #print('fp: '+ full_path)
            if os.path.isfile(full_path):
                os.remove(full_path)
            else:
                break

def merge_frame(dir, f):

    img_merged = 255 * np.ones(shape=[20, 3840, 3], dtype=np.uint8)

    for path in sorted(os.listdir(dir + f_name(f))):
        full_path = os.path.join(dir + f_name(f), path)

        #print ("X: "+full_path)
        if os.path.isfile(full_path) and os.path.splitext(full_path)[-1] == ".jpg":
            #print (full_path)
            img = cv2.imread(full_path)
            #cv2.imshow("A", img)
            img_merged = cv2.vconcat([img_merged, img])

    cv2.imwrite(img_dir + '/merge_'+ f_name(f) +'.jpg', img_merged)
    #return img_merged



video_dir = "/Users/hammer/Google Drive/VG research/REMOTE PHOTOGRAPHY/Stitching/Test footage car/020120/"
img_dir = "/Users/hammer/Google Drive/VG research/REMOTE PHOTOGRAPHY/Stitching/car_stitching_test_IMG/"
vf = 'VID_20200102_153326.mp4'
step = 1

#create a list for all the video file
count = 0
now = datetime.now()
print('Starting time: '+ str(now.strftime("%H:%M:%S")))

for i in sorted(os.listdir(video_dir)):
    #print (os.path.splitext(i)[-1])
    #if os.path.splitext(i)[-1] == ".mp4" and count <= 40 and i == vf:
    if os.path.splitext(i)[-1] == ".mp4" and count <= 40:
        print (i)
        count = count +1
        remove_frame(img_dir, i)  # clean up the folder
        write_frame(video_dir, i, 0, 900, step)  # write cropped images onto the folder
        #merge_frame(img_dir, i)
count = 0

for i in sorted(os.listdir(video_dir)):

    if os.path.splitext(i)[-1] == ".mp4" and count <= 40:
        print('Start merging')
        merge_frame(img_dir, i)
        count = count + 1

now = datetime.now()

print('Finished time: '+ str(now.strftime("%H:%M:%S")))