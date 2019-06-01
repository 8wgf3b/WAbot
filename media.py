import pyimgur
import requests

def echoimage(URL):
    im = pyimgur.Imgur(os.environ['IMGUR_CID'])
    #url can be sent directly but i wanted to test the temp directory's usage
    response = requests.get(url)
    if response.status_code == 200:
        with open("temp/echoim.jpg", 'wb') as f:
            f.write(response.content)
    uploaded_image = im.upload_image(url="temp/echoim.jpg", title="Uploaded with PyImgur")
    return uploaded_image.link
