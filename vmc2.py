from scipy.misc import imresize
import matplotlib.image as mpimg
import numpy as np
import pickle
import gzip
import sys


image_text = pickle.load(open("image_text2.p","rb"))
imagecount = len(image_text)
print('list size of image text',imagecount)

#restore the object
numpycom = np.load('img_one.npz')
print(type(numpycom))
imgarray = numpycom['imgarray']
onehot = numpycom['onehot']

numimages,_,_,_ = imgarray.shape
numlabels,_ = onehot.shape
#path = r'/Users/carsonlam/Desktop/VMC/'
path = r'/scratch/users/carsonl/retina/VMC/'

def imginsert(images, path, key):
    img = mpimg.imread(path+key)
    height,_,_ = img.shape
    if height > 450:
        img = imresize(img,(450,600,3))
    return np.append(images,np.expand_dims(img, axis=0),axis=0)

if numlabels != numimages:
    print('examples dont match labels',numlabels,numimages)
else:
    print('match',numlabels,numimages)
    for i in range(numlabels,imagecount+1):
        for key, value in image_text[i].iteritems():
            if "Unable" in value or "unreadable" in value:
                 try:
                        imgarray = imginsert(imgarray, path, key)
                        onehot = np.append(onehot,np.asarray([1,0,0,0]).reshape(1,4),axis=0)
                 except:
                    pass
            elif "Severe" in value or "Significant retinopathy found" in value:
                 try:
                        imgarray = imginsert(imgarray, path, key)
                        onehot = np.append(onehot,np.asarray([0,1,0,0]).reshape(1,4),axis=0)
                 except:
                    pass
            elif "Mild" in value or "Minimal" in value:
                 try:
                        imgarray = imginsert(imgarray, path, key)
                        onehot = np.append(onehot,np.asarray([0,0,1,0]).reshape(1,4),axis=0)
                 except:
                    pass
            elif "No retinopathy found" in value:
                 try:
                        imgarray = imginsert(imgarray, path, key)
                        onehot = np.append(onehot,np.asarray([0,0,0,1]).reshape(1,4),axis=0)
                 except:
                    pass

        if i%20 == 0:
            np.savez_compressed('img_one.npz', imgarray=imgarray, onehot=onehot)
            print(sys.getsizeof('img_one.npz'))
            print(imgarray.shape,onehot.shape)

np.savez_compressed('img_one.npz', imgarray=imgarray, onehot=onehot)
