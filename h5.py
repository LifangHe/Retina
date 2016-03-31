from scipy.misc import imresize
import matplotlib.image as mpimg
import numpy as np
import h5py
import time

def jpg_resize_numpy(path):
    imgnp = mpimg.imread(path)
    height,_,_ = imgnp.shape
    if height != 450:
        imgnp = imresize(imgnp,(450,600,3))
    return imgnp

#path = r'/Users/carsonlam/Desktop/VMC/'
path = r'/scratch/users/carsonl/retina/VMC/'
hdf5file = 'cycle1.h5'

with h5py.File(hdf5file, 'a') as FOB:
    done = int(FOB.attrs.__getitem__('count'))
    imagenames = np.array(FOB.get('imgnames'))

totalnum = imagenames.shape[0]

for imgcount in range(done,totalnum):
    with h5py.File(hdf5file, 'a') as FOB:
        fail_delay = int(FOB.attrs.__getitem__('fail_delay'))
        i = imgcount + fail_delay
        try:
            arrnum = str(int(np.floor(i/1000)))
            FOB.get('imgarray'+arrnum)[i%1000]=jpg_resize_numpy(path+imagenames[i])
            FOB.attrs.__setitem__('count',i + 1)
            print('image number ',imgcount,'placed in ',i,'skipped ',fail_delay)
        except:
            print( i , 'failed, iterating fail_protocol' )
            Fail = True
            while Fail == True:
                try:
                    fail_delay += 1
                    i = imgcount + fail_delay
                    arrnum = str(int(np.floor(i/1000)))
                    FOB.get('imgarray'+arrnum)[i%1000]=jpg_resize_numpy(path+imagenames[i])
                    FOB.attrs.__setitem__('count',i + 1)
                    print(time.ctime(),"fail everted skipped ahead to", imgcount + fail_delay ,arrnum, i%1000,'new count',i + 1,imagenames[i])
                    FOB.attrs.__setitem__('fail_delay', fail_delay)
                    Fail = False
                except:
                    print('try again, skip',i)
                    pass
            pass

print("SUCCESS!")
