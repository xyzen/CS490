import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Convolution2D, Conv2D, MaxPooling2D, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
from datetime import datetime
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder

x_train = np.load("./preprocessed/x_train.npy")
y_train = np.load("./preprocessed/y_train.npy")
x_test = np.load("./preprocessed/x_test.npy")
y_test = np.load("./preprocessed/y_test.npy")
yy = np.load("./preprocessed/yy.npy")
le = LabelEncoder()
le.classes_ = np.load("./preprocessed/classes.npy")

# MODEL

num_rows = 40
num_columns = 174
num_channels = 1

x_train = x_train.reshape(x_train.shape[0], num_rows, num_columns, num_channels)
x_test = x_test.reshape(x_test.shape[0], num_rows, num_columns, num_channels)

num_labels = yy.shape[1]
filter_size = 2

def construct_model():
	# Construct model 
	model = Sequential()
	model.add(Conv2D(filters=16, kernel_size=2, input_shape=(num_rows, num_columns, num_channels), activation='relu'))
	model.add(MaxPooling2D(pool_size=2))
	model.add(Dropout(0.2))
	
	model.add(Conv2D(filters=32, kernel_size=2, activation='relu'))
	model.add(MaxPooling2D(pool_size=2))
	model.add(Dropout(0.2))
	
	model.add(Conv2D(filters=64, kernel_size=2, activation='relu'))
	model.add(MaxPooling2D(pool_size=2))
	model.add(Dropout(0.2))
	
	model.add(Conv2D(filters=128, kernel_size=2, activation='relu'))
	model.add(MaxPooling2D(pool_size=2))
	model.add(Dropout(0.2))
	model.add(GlobalAveragePooling2D())
	
	model.add(Dense(num_labels, activation='softmax'))
	
	# Compile the model
	model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam') 
	
	# Display model architecture summary 
	model.summary()

	model.save("./model.h5")

	return model


model = construct_model()

# TRAINING

num_epochs = 72
num_batch_size = 256

checkpointer = ModelCheckpoint(filepath='saved_models/weights.best.basic_cnn.hdf5', 
                               verbose=1, save_best_only=True)
start = datetime.now()

model.fit(x_train, y_train, batch_size=num_batch_size, epochs=num_epochs, validation_data=(x_test, y_test), callbacks=[checkpointer], verbose=1)


duration = datetime.now() - start
print("Training completed in time: ", duration)

# TESTING

# Evaluating the model on the training and testing set
score = model.evaluate(x_train, y_train, verbose=0)
print("Training Accuracy: ", score[1])

score = model.evaluate(x_test, y_test, verbose=0)
print("Testing Accuracy: ", score[1])