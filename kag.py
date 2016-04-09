import numpy as np
import urllib
import cv2
import funk
import pickle
import h5py

jpeg_url = pickle.load( open( "retinadictall.p", "rb" ) )
jpeg_keys = jpeg_url.keys()

for key in jpeg_keys:

        with h5py.File('kag.h5', 'a') as kag:

            img = funk.url_to_numpy(jpeg_url[key])

            kag.create_dataset(key,data=img,compression="gzip",compression_opts=9)

            print 'success', key
