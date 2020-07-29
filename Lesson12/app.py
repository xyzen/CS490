from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_uploads import configure_uploads, AUDIO, UploadSet
import os
import numpy as np
import librosa
from tensorflow import keras
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder

# Load model and label encoder
model = keras.models.load_model("./saved_models/weights.best.basic_cnn.hdf5")
le = LabelEncoder()
le.classes_ = np.load("./saved_models/classes.npy")

# data dims
num_rows = 40
num_columns = 174
num_channels = 1

# CODE FOR FLASK APP

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), "static"))
app.config['SECRET_KEY'] = "clishmaclaver"
app.config['UPLOADED_AUDIOSET_DEST'] = "static"

audioset = UploadSet("audioset", AUDIO)
configure_uploads(app, audioset)

class AudioClassifyForm(FlaskForm):
    audio = FileField("audio")

@app.route("/", methods=["GET", "POST"])
def home():
    form = AudioClassifyForm()
    if form.validate_on_submit():
        filename = audioset.save(form.audio.data)
        filename = os.path.join(os.getcwd(), "static", filename)
        features = extract_features(filename)
        features = features.reshape(40, 174, 1)
        status = print_prediction(filename)
        return render_template("index.html", form=form, status=status)
    return render_template("index.html", form=form, status="")

@app.route("/about")
def about():
    return "A simple Flask project for audio classification"

# CODE FOR AUDIO CLASSIFICATION

# print predictions
def print_prediction(file_name):
    status = []
    prediction_feature = extract_features(file_name) 
    prediction_feature = prediction_feature.reshape(1, num_rows, num_columns, num_channels)

    predicted_vector = np.argmax(model.predict(prediction_feature), axis=-1)
    predicted_class = le.inverse_transform(predicted_vector)
    status.append("The predicted class is: " + str(predicted_class[0]))

    predicted_proba_vector = model.predict(prediction_feature) 
    predicted_proba = predicted_proba_vector[0]
    for i in range(len(predicted_proba)): 
        category = le.inverse_transform(np.array([i]))
        string = category[0] + ": " + format(predicted_proba[i], '.32f')
        status.append(string)
    return status

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
        print(e)
        return None 
     
    return mfccs

if __name__ == "__main__":
	app.run()