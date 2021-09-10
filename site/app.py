from __future__ import division, print_function

import os
import tensorflow as tf
import numpy as np
from pydub import AudioSegment
import pickle
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import openl3
import soundfile as sf
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, Normalizer, MinMaxScaler
from sklearn.pipeline import make_pipeline
import warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = Flask(__name__)

id2label = {
    0: "anger",
    1: "disgust",
    2: "fear",
    3: "joy",
    4: "neutral",
    5: "sadness",
    6: "surprise",
}
label2id = {value: key for key, value in id2label.items()}
classes = list(id2label.values())

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model_openl3 = openl3.models.load_audio_embedding_model(input_repr="mel256", content_type="env", embedding_size=512)

MODEL_PATH = os.path.join(os.getcwd(), 'model.pkl')
with open('model.pkl', 'rb') as f:
    clf = pickle.load(f)


def get_embed_openl3(path):
    if (path.split(".")[-1] != "wav"):
        sound = AudioSegment.from_mp3(path)
        new_path = path[:-4]+".wav"
        sound.export(new_path, format="wav")
        audio, sr = sf.read(new_path)
        os.remove(new_path)
    else:
        audio, sr = sf.read(path)
    os.remove(path)
    emb, _ = openl3.get_audio_embedding(audio, sr, model=model_openl3, hop_size=0.5)
    return emb


def predict_emotion(audio_path, clf):
    emb = get_embed_openl3(audio_path)
    count = emb.shape[0]
    preds = clf.predict_proba(emb)
    preds = np.sum(preds, axis=0) / count
    pred_class = str(np.argmax(preds))
    preds = [round(i,4) for i in preds]
    print(emb.shape,preds,pred_class)
    return {
        "pred": pred_class,
        "prob": [f"{classes[0]} : {preds[0]}", f"{classes[1]} : {preds[1]}", f"{classes[2]} : {preds[2]}",
                 f"{classes[3]} : {preds[3]}", f"{classes[4]} : {preds[4]}", f"{classes[5]} : {preds[5]}",
                 f"{classes[6]} : {preds[6]}"]
    }


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/predict', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        f = request.files["thefile"]
        if f:
            filename = secure_filename(f.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(filepath)
            result = predict_emotion(filepath, clf)
        else:
            result = {"pred": "null"}
        return result
    return None


if __name__ == '__main__':
    app.run(debug=False,use_reloader=False)
