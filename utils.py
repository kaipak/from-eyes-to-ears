from google.colab import files
import os
import glob
import cv2

def upload_file():
    print("Provide a test image")
    img = files.upload()
    list_of_files = glob.glob('./*') # * means all if need specific format then *.csv
    img_file = max(list_of_files, key=os.path.getctime)
    img = cvs.imread(img_file)
    return (img, img_file)
