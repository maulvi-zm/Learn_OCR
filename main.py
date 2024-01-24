# -*- coding: utf-8 -*-
from src import im_folder
import cv2
import os
import src

def resize_img_byW(width, img):
    # Define the desired width or height
    desired_width = width  # You can set your desired width
    # Calculate the corresponding height to maintain the aspect ratio
    aspect_ratio = img.shape[1] / img.shape[0] #lebar/tinggi
    desired_height = int(desired_width / aspect_ratio)
    # Resize the image
    return cv2.resize(img, (desired_width, desired_height), interpolation=cv2.INTER_LINEAR)
def resize_img_byH(height, img):
    # Define the desired height or height
    desired_height = height  # You can set your desired height
    # Calculate the corresponding height to maintain the aspect ratio
    aspect_ratio = img.shape[1] / img.shape[0]
    desired_width = int(aspect_ratio*desired_height)
    # Resize the image
    return cv2.resize(img, (desired_width, desired_height), interpolation=cv2.INTER_LINEAR)



file = input("Masukkan nama file:")
path = os.path.join(im_folder, file)
print("Masukkan tipe file\n1. Video\n2. Gambar")
code = int(input())
if (code == 1) :
    video = cv2.VideoCapture(path)
    cv2.startWindowThread()
    cv2.namedWindow('output')
    cv2.moveWindow('output', 500, 30)
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            rects = src.process(frame)
            frame = src.draw(rects, frame)
            cv2.imshow('output', frame)
            cv2.waitKey(1)
    video.release()
else:
    try:
        raw_img = cv2.imread(path)
        if raw_img is None:
            raise FileNotFoundError(f"Tidak dapat membaca gambar dari path: {path}")
        if(raw_img.shape[0]>raw_img.shape[1]):
            img = resize_img_byH(500, raw_img)
        else:
            img = resize_img_byW(500, raw_img)
        rects = src.process(img)
        print("")
        print(len(rects))
        image = src.draw(rects, img, debug=True)
        cv2.imshow('output', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except FileNotFoundError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")
    