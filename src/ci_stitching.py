#!/usr/bin/env python
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
from datetime import datetime

def stitch_video()

    print ('opencv version' + cv2.__version__)
    '''
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--images", type=str, required=True, help="path to input directory of images to stitch")
    # The path to the directory of input images to stitch.

    ap.add_argument("-o", "--output", type=str, required=True, help="path to the output image")
    # The path to the output image where the result will be saved.

    args = vars(ap.parse_args())
    '''
    img_dir = '/Users/hammer/Google Drive/VG research/REMOTE PHOTOGRAPHY/Stitching/car_stitching_test_IMG/VID_20200102_153326'
    output_dir = 'output_image/'
    # grab the paths to the input images and initialize our images list
    print("[INFO] loading images...")
    imagePaths = sorted(list(paths.list_images(img_dir)))
    batches = []
    modes = [cv2.Stitcher_PANORAMA, cv2.Stitcher_SCANS]


    # loop over the image paths, load each one, and add them to our
    # images to stitch list

    step = 3
    batch_size = 12
    start_at_batch = 2

    for i in range(0,len(imagePaths), batch_size):

        batches.append(imagePaths[i:i+batch_size])

    print ("total number of batch:"+ str(len(batches)))



    batch_count = 0
    for i in batches:
        print("[INFO] stitching images batch " + str(batch_count) + "...")
        images = [] #clean up the images container
        for j in i:
            if (batch_count >=start_at_batch):
                print('reading images:' + str(j) + '\n')
                image = cv2.imread(j)
                image2 = imutils.resize(image, width=400)
                #cv2.imwrite("/Users/hammer/Google Drive/VG research/REMOTE PHOTOGRAPHY/Stitching/car_stitching_test_IMG/TEST.jpg", image2)
                images.append(image2)


        ## initialize OpenCV's image stitcher object and then perform the image
        ## stitching

        stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create(modes[1])
        (status, stitched) = stitcher.stitch(images)

        ## if the status is '0', then OpenCV successfully performed image
        ## stitching
        now = datetime.now()

        if status == 0:
            ## write the output stitched image to disk
            #cv2.imwrite(output_dir+'stitched'+str(now.strftime("%H:%M:%S"))+'.jpg', stitched)
            cv2.imwrite(output_dir + 'stitched' + str(batch_count).zfill(3) + '.jpg', stitched)

            ## display the output stitched image to our screen
            #cv2.imshow("Stitched", stitched)
            #cv2.waitKey(0)

        ## otherwise the stitching failed, likely due to not enough keypoints)
        ## being detected
        else:
            print("[INFO] image stitching failed ({})".format(status)+"\n")

        batch_count +=1

def video_to_image(path, pixel_width):
    # taking pixels from each frame of video, and put append time to form an scan image


    

    pass



if __name__ == "__main__":
    print("Running main")