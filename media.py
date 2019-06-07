import pyimgur
import requests
import os, shutil
import cv2
import numpy as np
from utils.preprocess import isolate

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
    response = requests.get(URL)
    if response.status_code == 200:
        with open("temp/sudoku.jpg", 'wb') as f:
            f.write(response.content)
    orig = cv2.imread('temp/sudoku.jpg')
    frame = isolate(orig)
    cv2.imwrite('temp/solvedsudoku.jpg',frame)
    uploaded_image = im.upload_image("temp/solvedsudoku.jpg", title="twilwhatbot")
    return uploaded_image.link
