import numpy as np
import urllib
import cv2


#takes the URL of an image and turns into a numpy array representation of the image
def url_to_numpy(url):

    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image
