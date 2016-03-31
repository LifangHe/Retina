from scipy.misc import imresize
import matplotlib.image as mpimg
import numpy as np
import pickle
import h5py
import os.path
import sys

dataname = 'load_reload.h5'
#path = r'/scratch/users/carsonl/retina/VMC/'
path = r'/Users/carsonlam/Desktop/VMC/'

if os.path.exists(path):
    print('path detected')
else:
    print('No path detected')
    sys.exit()

image_text = pickle.load(open("image_text2.p","rb"))
imagecount = len(image_text)
print('list size of image text',imagecount)

# check if data exists
if not os.path.isfile(dataname):
    print('create new datasets')
    FOB = h5py.File(dataname, 'a')
    imset = FOB.create_dataset(
    "images",(imagecount,450,600,3),maxshape=(None,450,600,3),compression="gzip",compression_opts=9, dtype='uint8')
    laset = FOB.create_dataset("labels",(imagecount,4),maxshape=(None,4),compression="gzip",compression_opts=4)
    FOB.attrs.create('count',0)

else:
    FOB = h5py.File(dataname, 'a')
    imset = FOB['images']
    laset = FOB['labels']
    print("existing file object opened ",FOB.attrs.__getitem__('count'),' existing entries')

numimages,_,_,_ = imset.shape
numlabels,_ = laset.shape
numin = numim = FOB.attrs.__getitem__('count')

def insert(path, key):
    img = mpimg.imread(path+key)
    height,_,_ = img.shape
    if height > 450:
        img = imresize(img,(450,600,3))
    return img

if numlabels != numimages:
    print('examples dont match labels',numlabels,numimages)
else:
    print('match',numlabels,numimages,numin)

    for i in range(numin,imagecount+1):
        FOB.attrs.__setitem__('count',i + 1)
        for key, value in image_text[i].iteritems():
            if "Unable" in value or "unreadable" in value:
                 try:
                    imset[i] = insert(path,key)
                    laset[i] = np.array([1,0,0,0])
                 except:
                    pass
            elif "Severe" in value or "Significant retinopathy found" in value:
                 try:
                    imset[i] = insert(path,key)
                    laset[i] = np.array([0,1,0,0])
                 except:
                    pass
            elif "Mild" in value or "Minimal" in value:
                 try:
                    imset[i] = insert(path,key)
                    laset[i] = np.array([0,0,1,0])
                 except:
                    pass
            elif "No retinopathy found" in value:
                 try:
                    imset[i] = insert(path,key)
                    laset[i] = np.array([0,0,0,1])
                 except:
                    pass
            else:
                FOB.attrs.__setitem__('count',i - 1 )


        print('count', FOB.attrs.__getitem__('count'))

        if i%10 == 0:

            FOB.close()
            FOB = h5py.File(dataname, 'a')
            imset = FOB['images']
            laset = FOB['labels']
            v = FOB['images'][0]
            print("File Saved with ",FOB.attrs.__getitem__('count'),' entries')


FOB.close()
print('end size',sys.getsizeof(dataname))
