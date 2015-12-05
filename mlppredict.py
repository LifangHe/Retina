import cPickle
import gzip
import os
import sys
import timeit
import numpy
import theano
import theano.tensor as T
from PIL import Image
from mlp import *

dataset='mnist.pkl.gz'
datasets = load_data(dataset)
test_set_x, test_set_y = datasets[2]
test_set_x = test_set_x.get_value()
input = test_set_x[:10]
params = cPickle.load(open('best_mlp_model.pkl'))
dataset='mnist.pkl.gz'
datasets = load_data(dataset)
test_set_x, test_set_y = datasets[2]
test_set_x = test_set_x.get_value()
input = test_set_x[:10]
params = cPickle.load(open('best_mlp_model.pkl'))

print params[0].ndim
print params[1].ndim
rng = numpy.random.RandomState(1234)
layer1 = HiddenLayer(
            input=input,
            rng = rng,
            n_in=28 * 28,
            n_out=500,
            W=params[0],
            b=params[1],
            activation=T.tanh
        )
p_y_given_x = T.nnet.softmax(T.dot(layer1.output, params[2]) + params[3])
y_pred = T.argmax(p_y_given_x, axis=1)
print y_pred.eval()
