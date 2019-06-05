import pyimgur
import requests
import os, shutil
import cv2
import numpy as np

def echoimage(URL):
    im = pyimgur.Imgur(os.environ['IMGUR_CID'])
    #url can be sent directly but i wanted to test the temp directory's usage
    response = requests.get(URL)
    if response.status_code == 200:
        with open("temp/echoim.jpg", 'wb') as f:
            f.write(response.content)
    uploaded_image = im.upload_image("temp/echoim.jpg", title="twilwhatbot")
    return uploaded_image.link

def clean(path = 'temp/'):
    for file in os.listdir(path):
        if file == '.gitkeep':
            continue
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def sudoku(URL):
        im = pyimgur.Imgur(os.environ['IMGUR_CID'])
        #url can be sent directly but i wanted to test the temp directory's usage
        response = requests.get(URL)
        if response.status_code == 200:
            with open("temp/sudoku.jpg", 'wb') as f:
                f.write(response.content)
        frame = cv2.imread('temp/sudoku.jpg')
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame,(7, 7), 0)
        frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        cv2.imwrite('temp/solvedsudoku.jpg',frame)
        uploaded_image = im.upload_image("temp/solvedsudoku.jpg", title="twilwhatbot")
        return uploaded_image.link
