# -*- coding: utf-8 -*-
"""Cats and Dogs

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YXszi2TbGLVcBBQt55FbKyph6K872lNE
"""

import tensorflow as tf
import numpy as np
import cv2 
import os
import random


##Parameters required for the model##
data_path='/home/predator/data'
height=100
width=100
all_classes = os.listdir(data_path)
number_of_classes = len(all_classes)
color_channels=3
epochs=10
batch_size=10
batch_counter=0
model_save_name='/home/predator/checkpoints'
images_ph=tf.placeholder(tf.float32,shape=[None,width,height,color_channels],name="input_image")
labels_ph=tf.placeholder(tf.float32,shape=[None,number_of_classes])
print("Initialised Completed")

class utils:
    image_count = []
    count_buffer=[]
    class_buffer=all_classes[:]
    def __init__(self):
        self.image_count = []
        self.count_buffer = []
        for i in os.walk(data_path):
            if len(i[2]):
                self.image_count.append(len(i[2]))
        self.count_buffer=self.image_count[:]

    # processing images into arrays and dispatch as batches whenever called.
    def batch_dispatch(self,batch_size=batch_size):
        global batch_counter
        if sum(self.count_buffer):

            class_name = random.choice(self.class_buffer)
            choice_index = all_classes.index(class_name)
            choice_count = self.count_buffer[choice_index]
            if choice_count==0:
                class_name=all_classes[self.count_buffer.index(max(self.count_buffer))]
                choice_index = all_classes.index(class_name)
                choice_count = self.count_buffer[choice_index]

            slicer=batch_size if batch_size<choice_count else choice_count
            img_ind=self.image_count[choice_index]-choice_count
            indices=[img_ind,img_ind+slicer]
            images = self.generate_images(class_name,indices)
            labels = self.generate_labels(class_name,slicer)

            self.count_buffer[choice_index]=self.count_buffer[choice_index]-slicer
        else:
            images,labels=(None,)*2
        return images, labels

    #gives one hot for the respective labels
    def generate_labels(self,class_name,number_of_samples):
        one_hot_labels=[0]*number_of_classes
        one_hot_labels[all_classes.index(class_name)]=1
        one_hot_labels=[one_hot_labels]*number_of_samples
        #one_hot_labels=tf.one_hot(indices=[all_classes.index(class_name)]*number_of_samples,depth=number_of_classes)
        return one_hot_labels

    # image operations
    def generate_images(self,class_name,indices):
        batch_images=[]
        choice_folder=os.path.join(data_path,class_name)
        selected_images=os.listdir(choice_folder)[indices[0]:indices[1]]
        for image in selected_images:
            img=cv2.imread(os.path.join(choice_folder,image))
            batch_images.append(img)
        return batch_images



"""::::Model Architecture Defintions:::"""

def add_weights(shape):
        return tf.Variable(tf.truncated_normal(shape=shape, stddev=0.05))

def add_biases(shape):
        return tf.Variable(tf.constant(0.05, shape=shape))

def conv_layer(layer, kernel, input_shape, output_shape, stride_size):
        weights = add_weights([kernel, kernel, input_shape, output_shape])
        biases = add_biases([output_shape])
        stride = [1, stride_size, stride_size, 1]
        layer = tf.nn.conv2d(layer, weights, strides=stride, padding='SAME') + biases
        return layer

def pooling_layer(layer, kernel_size, stride_size):
        kernel = [1, kernel_size, kernel_size, 1]
        stride = [1, stride_size, stride_size, 1]
        return tf.nn.max_pool(layer, ksize=kernel, strides=stride, padding='SAME')

def flattening_layer(layer):
        input_size = layer.get_shape().as_list()
        new_size = input_size[-1] * input_size[-2] * input_size[-3]
        return tf.reshape(layer, [-1, new_size]),new_size

def fully_connected_layer(layer, input_shape, output_shape):
        weights = add_weights([input_shape, output_shape])
        biases = add_biases([output_shape])
        layer = tf.matmul(layer,weights) + biases
        return layer

def activation_layer(layer):
        return tf.nn.relu(layer)

""":::MODEL ARCHITECTURE:::"""

network=conv_layer(images_ph,5,3,16,1)
network=pooling_layer(network,5,2)
network=activation_layer(network)
network=conv_layer(network,4,16,32,1)
network=pooling_layer(network,4,2)
network=activation_layer(network)
network=conv_layer(network,3,32,64,1)
network=pooling_layer(network,3,2)
network=activation_layer(network)
network,features=flattening_layer(network)
network=fully_connected_layer(network,features,1024)
network=activation_layer(network)
network=fully_connected_layer(network,1024,2)

print("\n Network Architecture has been defined")

""":::Training Loop:::"""

def trainer(network,no_of_images):
	print("\nTraining Started")
	cross_entropy=tf.nn.softmax_cross_entropy_with_logits_v2(logits=network,labels=labels_ph)
	cost=tf.reduce_mean(cross_entropy)
	tf.summary.scalar("cost", cost)

	optimizer=tf.train.AdamOptimizer().minimize(cost)
	#print(optimizer+"\n")
	with tf.Session() as sess:
		print("\nSession Initialised")
		sess.run(tf.global_variables_initializer())
		writer = tf.summary.FileWriter(model_save_name, graph=tf.get_default_graph())
		merged = tf.summary.merge_all()
		saver = tf.train.Saver(max_to_keep=4)
		counter=0
		for epoch in range(epochs):
			print("\n Epoch Started")
			tools = utils()
			for batch in range(int(number_of_images / batch_size)):
				print("\nBATCH Processeing started")
				counter+=1
				images, labels = tools.batch_dispatch()
				if images == None:
					break
			#	print("\nPRINTING ERROR")
				loss,summary = sess.run([cost,merged], feed_dict={images_ph: images, labels_ph: labels})
				print('loss', loss)
				sess.run(optimizer, feed_dict={images_ph: images, labels_ph: labels})

				print('Epoch number ', epoch, 'batch', batch, 'complete')
				writer.add_summary(summary,counter)
			saver.save(sess, model_save_name)


if __name__=="__main__":
	#global network
	print("\nMAIN FUNCTION HAS BEEN ENTERED")
	tools=utils()
	number_of_images = sum([len(files) for r, d, files in os.walk("/home/predator/data")])
	trainer(network,number_of_images)
	print("\n---------------------------Training Over---------------------------")
