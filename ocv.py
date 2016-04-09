import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import h5py

filelist = [ f for f in os.listdir(r"vmc/") if f.endswith('.jpg') ]

for filename in filelist:

    with h5py.File('cv.h5', 'a') as cv:

        img=mpimg.imread(r"vmc/"+ filename)

        cv.create_dataset(filename,data=img,compression="gzip",compression_opts=9)

        print 'success', filename
