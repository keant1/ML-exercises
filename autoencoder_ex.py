import tensorflow as tf
import numpy as np

import input_data

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
samples = mnist.train.images



def DAE(lr):
    input = samples

    in_dim = input.shape[1]
    out_dim = in_dim
    h_dim = 700
    h2_dim = 500
    encoding_matrices=[]
    biases=[]

    targets_train = input

    x = tf.placeholder(dtype='float',shape=[None,in_dim],name='x')

    maxval_ih = tf.sqrt(6.0/(in_dim+h_dim))
    maxval_ho = tf.sqrt(6.0/(out_dim+h_dim))

    w=tf.Variable(tf.random_uniform(shape=[in_dim,h_dim],minval=-maxval_ih,maxval=maxval_ih,dtype='float'),name='w1')
    w2=tf.Variable(tf.random_uniform(shape=[h_dim,h2_dim],minval=-maxval_ih,maxval=maxval_ih,dtype='float'),name='w2')
    b=tf.Variable(tf.random_uniform(shape=[h_dim],minval=-0.01,maxval=0.01,dtype='float'),name='b1')
    b2=tf.Variable(tf.random_uniform(shape=[h2_dim],minval=-0.01,maxval=0.01,dtype='float'),name='b2')
    batchSize = 10000
    sess = tf.InteractiveSession()

    targets = tf.placeholder(dtype='float',shape=[None,out_dim],name='targets')
    

    l2 = tf.nn.tanh(tf.matmul(x,w) + b)
    l3 = tf.nn.tanh(tf.matmul(l2, w2)+b2)
    l5 = tf.nn.tanh(tf.matmul(l3-b2, tf.transpose(w2)))
    l6 = tf.nn.tanh(tf.matmul(l5-b, tf.transpose(w)))
    cost3 = tf.nn.l2_loss(targets - l6)
    cost3 = tf.reduce_mean(cost3)/60000
    train_op = tf.train.AdamOptimizer(lr).minimize(cost3)
    sess.run(tf.initialize_all_variables())
    for i in range(0,10):
        print i
        for batch in range (0,input.shape[0],batchSize):
            batch_end = min(input.shape[0],batch+batchSize) + 1
            train_op.run(feed_dict={x:input[batch:batch_end],targets:targets_train[batch:batch_end]})
            c3 = cost3.eval(feed_dict={x:input[batch:batch_end],targets:targets_train[batch:batch_end]})
        print c3
    return c3



lr = 0.001
print lr
print DAE(lr)