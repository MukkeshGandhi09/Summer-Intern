import tensorflow as tf
from tensorflow import keras

class mycallback(tf.keras.callbacks.Callback):
	def on_epoch_end(self,epoch,log={}):
		if(log.get('loss')<1.4):
			print("ACCURACY DETERMINED HAS BEEN REACHED")
			self.model.stop_training=True

callbacks=mycallback()
mnist= tf.keras.datasets.fashion_mnist
(train_images,train_labels),(test_images,test_labels)=mnist.load_data()

train_images=train_images/255
test_images=test_images/255

model= tf.keras.models.Sequential([tf.keras.layers.Flatten(),
								   tf.keras.layers.Dense(128,activation= tf.nn.relu),
								   tf.keras.layers.Dense(128,activation=tf.nn.relu),
								   tf.keras.layers.Dense(10,activation=tf.nn.softmax)])
model.compile(optimizer=tf.train.AdamOptimizer(),loss='sparse_categorical_crossentropy')
model.fit(train_images,train_labels,epochs=10, callbacks=[callbacks])


print("TESTING:::")
print(model.evaluate(test_images,test_labels))


