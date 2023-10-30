import os
import numpy as np
from keras.models import load_model
from PIL import Image
from fastapi import FastAPI, UploadFile, File
import tensorflow as tf

app = FastAPI()


def model_processing(file):
    """
    Predicting probability of AP-ROP
    """
    model_cnn = load_model('modelCNN.h5', compile=False)
    model_cnn.compile()
    image = Image.open(file)
    img_array = np.array(image)
    prediction = model_cnn.predict(
        tf.reshape(img_array, [1, 480, 640, 3]))
    probability: float = round(float(prediction[0][0]), 5)
    if probability > 0.7:
        text = f'\n{probability * 100}% вероятность ЗАРН\nВысокая вероятность ЗАРН, требуется проверка!\n________________________________________'
    else:
        text = f'\n{probability * 100}% вероятность ЗАРН\n________________________________________'
    return text

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    messages = {}
    try:
        contents = file.file.read()
        res_folder = os.path.join('res', file.filename)
        with open(res_folder, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    try:
        result = model_processing(res_folder)
        return {"message": result}
    except Exception:
        return {"message": "There was an error processing the file"}

