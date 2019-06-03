# -*- coding: utf-8 -*-
"""Working CNN_MNIST

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZVGclRNAI-MnpZFOZ8rHhs5iNBu7nKKl
"""

import tensorflow as tf
from future import *
import tensorflow_datasets as tfds
import math
import matplotlib as plt
import numpy as np

""":::MNIST-CNN Tensorflow implementation:::

Network Architecture

    Convolution, Filter shape:(5,5,6), Stride=1, Padding=’SAME’
    Max pooling (2x2), Window shape:(2,2), Stride=2, Padding=’Same’
    ReLU
    Convolution, Filter shape:(5,5,16), Stride=1, Padding=’SAME’
    Max pooling (2x2), Window shape:(2,2), Stride=2, Padding=’Same’
    ReLU
    Fully Connected Layer (128)
    ReLU
    Fully Connected Layer (10)
    Softmax
"""

import matplotlib.pyplot as plt
import numpy as np
import time
import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data
data=input_data.read_data_sets('data/MNIST/',one_hot=True)

x= tf.placeholder(tf.float32,shape=[None,28*28],name='X')
x_img=tf.reshape(x,[-1,28,28,1])

y_true=tf.placeholder(tf.float32,shape=[None,10],name='Y')
y_true_cls=tf.argmax(y_true,dimension=1)


def new_convolution_layer (input,num_input_channel,filter_size,num_filter,name):
  with tf.variable_scope(name) as scope:
    shape=[filter_size,filter_size,num_input_channel,num_filter]
    weights=tf.Variable(tf.truncated_normal(shape,stddev=0.05))
    #biases=tf.Variable(tf.constant(0.05, shape = num_filter))
    layer= tf.nn.conv2d(input=input,filter=weights,strides=[1,1,1,1],padding='SAME')
    #layer+=biases
    return layer,weights

def new_pool_layer(input,name):
  with tf.variable_scope(name) as scope:
    layer=tf.nn.max_pool(value=input,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
    return layer

def new_relu_layer(input,name):
  with tf.variable_scope(name) as scope:
    layer=tf.nn.relu(input)
    return layer

def new_fc_layer(input,num_inputs,num_outputs,name):
  with tf.variable_scope(name) as scope:
    weights=tf.Variable(tf.truncated_normal([num_inputs,num_outputs],stddev=0.05))
    #biases=tf.Variable(tf.constant(0.05,shape=num_outputs))
    layer=tf.matmul(input,weights)
    return layer

conv1_output,weights_conv1=new_convolution_layer(input=x_img,num_input_channel=1,filter_size=5,num_filter=6,name="conv_layer1")
max1_output=new_pool_layer(input=conv1_output,name='maxpool_layer1')
relu1_output=new_relu_layer(input=max1_output,name='relu_layer1')
conv2_ouput,weights_conv2=new_convolution_layer(input=relu1_output,num_input_channel=6,filter_size=5,num_filter=16,name='conv_layer2')
max2_output=new_pool_layer(input=conv2_ouput,name='maxpool_layer2')
relu2_output=new_relu_layer(input=max2_output,name='relu_layer2')
num_features=relu2_output.get_shape()[1:4].num_elements()
layer_flat=tf.reshape(relu2_output,[-1,num_features])
fc1_output=new_fc_layer(input=layer_flat,num_inputs=num_features,num_outputs=128,name='fc_layer1')
relu3_output=new_relu_layer(input=fc1_output,name='relu_layer3')
fc2_output=new_fc_layer(input=relu3_output,num_inputs=128,num_outputs=10,name='fc_layer2')
with tf.variable_scope("Softmax"):
  y_pred=tf.nn.softmax(fc2_output)
  y_pred_class=tf.argmax(y_pred,dimension=1)

with tf.variable_scope('entropy'):
  crossentropy=tf.nn.softmax_cross_entropy_with_logits(logits=fc2_output,labels=y_true)
  cost = tf.reduce_mean(crossentropy)

with tf.variable_scope('optimiser'):
  optimizer=tf.train.AdamOptimizer(learning_rate=1e-4).minimize(cost)

with tf.name_scope("accuracy"):
    correct_prediction = tf.equal(y_pred_class, y_true_cls)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

writer = tf.summary.FileWriter("Training_FileWriter/")
writer1 = tf.summary.FileWriter("Validation_FileWriter/")


# Add the cost and accuracy to summary
tf.summary.scalar('loss', cost)
tf.summary.scalar('accuracy', accuracy)

# Merge all summaries together
merged_summary = tf.summary.merge_all()

num_epochs = 100
batch_size = 100

with tf.Session() as sess:
    # Initialize all variables
    sess.run(tf.global_variables_initializer())
    
    # Add the model graph to TensorBoard
    writer.add_graph(sess.graph)
    
    # Loop over number of epochs
    for epoch in range(num_epochs):
        
        start_time = time.time()
        train_accuracy = 0
        
        for batch in range(0, int(len(data.train.labels)/batch_size)):
            
            # Get a batch of images and labels
            x_batch, y_true_batch = data.train.next_batch(batch_size)
            
            # Put the batch into a dict with the proper names for placeholder variables
            feed_dict_train = {x: x_batch, y_true: y_true_batch}
            
            # Run the optimizer using this batch of training data.
            sess.run(optimizer, feed_dict=feed_dict_train)
            
            # Calculate the accuracy on the batch of training data
            train_accuracy += sess.run(accuracy, feed_dict=feed_dict_train)
            
            # Generate summary with the current batch of data and write to file
            summ = sess.run(merged_summary, feed_dict=feed_dict_train)
            writer.add_summary(summ, epoch*int(len(data.train.labels)/batch_size) + batch)
        
          
        train_accuracy /= int(len(data.train.labels)/batch_size)
        
        # Generate summary and validate the model on the entire validation set
        summ, vali_accuracy = sess.run([merged_summary, accuracy], feed_dict={x:data.validation.images, y_true:data.validation.labels})
        writer1.add_summary(summ, epoch)
        

        end_time = time.time()
        
        print("Epoch "+str(epoch+1)+" completed : Time usage "+str(int(end_time-start_time))+" seconds")
        print("\tAccuracy:")
        print ("\t- Training Accuracy:\t{}".format(train_accuracy))
        print ("\t- Validation Accuracy:\t{}".format(vali_accuracy))