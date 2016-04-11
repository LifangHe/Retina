from sys import getsizeof
from scipy.misc import imresize
import numpy as np
import h5py

with h5py.File('vmcv.h5', 'a') as cv:
    dataset_names = cv.keys()
    num_datasets = len(dataset_names)
    print num_datasets
    done = False
    while done == False:
        with h5py.File('big2set.h5', 'a') as vb:
            numsets = vb.attrs.__getitem__('numsets')
            print('STARTING set', numsets)
            start = numsets*500
            stop = start + 500
            if numsets == num_datasets/500:
                stop = start + 41496%500
                done = True
            keys = dataset_names[start:stop]
            orgkey = str(keys)
            primed_array = np.array(cv.get(keys[0]))
            height,_,_ = primed_array.shape
            if height != 450:
                primed_array = imresize(primed_array,(450,600,3))
            primed_array = np.expand_dims(primed_array, axis=0)
            keys.pop(0)

            for key in keys:
                appendarray = np.array(cv.get(key))
                height,_,_ = appendarray.shape
                if height != 450:
                    print height, 'resize'
                    appendarray = imresize(appendarray,(450,600,3))
                appendarray = np.expand_dims(appendarray, axis=0)
                print 'primed_array',primed_array.shape,'appendshape', appendarray.shape
                primed_array = np.append(primed_array,appendarray,axis=0)
                print getsizeof(primed_array)/1e6, 'MB'
        with h5py.File('big2set.h5', 'a') as vb:
                vb.attrs.__setitem__('jpgkey'+ str(numsets),orgkey)
                vb.create_dataset('images'+ str(numsets),data=primed_array,compression="gzip",compression_opts=9)
                print('SAVED', numsets)
                if done == False:
                    vb.attrs.__setitem__('numsets',numsets+1)

print 'SUCCESS vmc data into big array'
