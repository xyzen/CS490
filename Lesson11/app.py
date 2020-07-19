from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_uploads import configure_uploads, IMAGES, UploadSet
import os
import numpy as np
import cv2


# CODE FOR APP

app = Flask(__name__, static_folder="/home/pi/Desktop/obj-detect-web/static")
app.config['SECRET_KEY'] = "clishmaclaver"
app.config['UPLOADED_IMAGES_DEST'] = "static"

images = UploadSet("images", IMAGES)
configure_uploads(app, images)

class ObjDetectForm(FlaskForm):
    image = FileField("image")

@app.route("/", methods=["GET", "POST"])
def home():
    form = ObjDetectForm()
    if form.validate_on_submit():
        filename = images.save(form.image.data)
        detected = obj_detect("./static/"+filename)
        filename = "result_" + filename
        cv2.imwrite("./static/"+filename, detected)
        return render_template("index.html", form=form, result=filename)
    return render_template("index.html", form=form, result="intro.jpg")

@app.route("/about")
def about():
    return "A simple Flask project for object detection"


# CODE FOR OBJECT DETECTION

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("./obj-detect/MobileNetSSD_deploy.prototxt.txt", "./obj-detect/MobileNetSSD_deploy.caffemodel")

def obj_detect(path):
    image = cv2.imread(path)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()
    for i in np.arange(0, detections.shape[2]):
	    confidence = detections[0, 0, i, 2]
	    if confidence > 0.2:
		    idx = int(detections[0, 0, i, 1])
		    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		    (startX, startY, endX, endY) = box.astype("int")
		    label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
		    print("[INFO] {}".format(label))
		    cv2.rectangle(image, (startX, startY), (endX, endY),COLORS[idx], 2)
		    y = startY - 15 if startY - 15 > 15 else startY + 15
		    cv2.putText(image, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
    return image

if __name__ == "__main__":
    app.run()
