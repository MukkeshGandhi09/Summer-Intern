import tensorflow as tf 

n1=tf.constant(3.0)
n2=tf.constant(4.0)
c=n1*n2

sess= tf.Session()

fw=tf.summary.FileWriter("/home/predator/Desktop/graph",sess.graph)

with tf.Session() as sess :
	o=sess.run(c)
	print(o)			
