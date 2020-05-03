from google.colab import files
import os
import glob

def upload_file:
    print("Provide a test image")
    test_img = files.upload()
    list_of_files = glob.glob('./*') # * means all if need specific format then *.csv
    test_img = max(list_of_files, key=os.path.getctime)
    return test_img
