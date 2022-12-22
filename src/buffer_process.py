import os
import cv2
import imutils

def buffer_crop(img, x1, x2, y1, y2):

    w = int(img.shape[1])
    h = int(img.shape[0])

    #print(' h:'+ str(h)+'w: '+str(w)+' ' + str(int(h * y1))+':'+str(int(h * y2))+','+ str(int(w * x1))+':'+str(int(w * x2)))

    crop_img = img[int(h * y1):int(h * y2), int(w * x1):int(w * x2)]

    return crop_img


def buffer_append(main_img, new_img):
    im_v = cv2.vconcat([main_img, new_img])
    return im_v