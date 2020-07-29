import pandas as pd
import numpy as np
import librosa
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical

# PREPROCESSING

# extracts and returns MFCC spectrogram
def extract_features(file_name):
    max_pad_len = 174
    try:
        audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast') 
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        pad_width = max_pad_len - mfccs.shape[1]
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
        print(mfccs.shape)

    except Exception as e:
        print("Error encountered while parsing file: ", file_name)
        return None 
     
    return mfccs

dataset_path = "E:/Documents/CS490/Lesson12/UrbanSound8k/audio/"

metadata = pd.read_csv("E:/Documents/CS490/Lesson12/UrbanSound8k/metadata/UrbanSound8k.csv")

features = []

classes = set()

# extract MFCC spectrogram from all sound files
for ndx, row in metadata.iterrows():
	filename = os.path.join(
		os.path.abspath(dataset_path),
		"fold" + str(row["fold"]),
	    str(row["slice_file_name"])
	    )
	class_label = row["class"]
	classes.add(class_label)
	data = extract_features(filename)
	features.append([data, class_label])

# convert to pandas dataframe
featuresdf = pd.DataFrame(features, columns=['feature', 'class_label'])

print(classes)

X = np.array(featuresdf.feature.tolist())
y = np.array(featuresdf.class_label.tolist())

print(X.shape)
print(y.shape)

le = LabelEncoder()
yy = to_categorical(le.fit_transform(y))

print(yy.shape)

x_train, x_test, y_train, y_test = train_test_split(X, yy, test_size=0.2, random_state=42)

np.save("./preprocessed/x_train.npy", x_train)
np.save("./preprocessed/x_test.npy", x_test)
np.save("./preprocessed/y_train.npy", y_train)
np.save("./preprocessed/y_test.npy", y_test)
np.save("./preprocessed/yy.npy", yy)
np.save("./preprocessed/classes.npy", le.classes_)