import cPickle
import gzip
import os
import sys
import timeit
import numpy
import theano
import theano.tensor as T
from PIL import Image

mnistdata = gzip.open('mnist.pkl.gz', 'rb')
train_set, valid_set, test_set = cPickle.load(mnistdata)
print train_set[0].shape
#(50000,784), 28*28 = 784
print train_set[1].shape
#(50000,)
print train_set[1][:10]
#[5 0 4 1 9 2 1 3 1 4]
#below shows how to reconstruct an numpy array to an RGB image
print type(train_set[0][0])
a = numpy.reshape(train_set[0][0],(28,28))
print a.shape
b = numpy.ones((3,28,28))
b[:3,:,:] = a*255
b=b.transpose(1, 2, 0)
print b.shape
# (28, 28, 3)
b = b.astype(numpy.uint8)
b = Image.fromarray(b,"RGB")
b.save('b.jpg')
