import pyimgur
import requests
import os, shutil


def echoimage(URL):
    im = pyimgur.Imgur(os.environ['IMGUR_CID'])
    #url can be sent directly but i wanted to test the temp directory's usage
    response = requests.get(URL)
    if response.status_code == 200:
        with open("temp/echoim.jpg", 'wb') as f:
            f.write(response.content)
    uploaded_image = im.upload_image("temp/echoim.jpg", title="twilwhatbot")
    return uploaded_image.link

def clean(path = 'temp/', log = False):
    for file in os.listdir(path):
        if file == '.gitkeep':
            continue
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    if log == True:
        return '\n'.join(os.listdir(path))

def sudoku(URL):
    im = pyimgur.Imgur(os.environ['IMGUR_CID'])
    response = requests.get(URL)
    if response.status_code == 200:
        with open("temp/sudoku.jpg", 'wb') as f:
            f.write(response.content)
    cropped, squares, digits = croppedsquaredigits('temp/sudoku.jpg')
    frame = numonim(cropped, squares, digits)
    cv2.imwrite('temp/solvedsudoku.jpg',frame)
    uploaded_image = im.upload_image("temp/solvedsudoku.jpg", title="twilwhatbot")
    return uploaded_image.link

if __name__ == '__main__':
    print(clean(log =True))
