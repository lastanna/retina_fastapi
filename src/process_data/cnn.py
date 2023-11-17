import os
import numpy as np
import logging
from keras.models import load_model
from PIL import Image
import tensorflow as tf
from src.core.config import app_settings
from src.core.logger import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def model_processing(file: str) -> float:
    """
    Predicting probability of AP-ROP
    """
    print(app_settings.models_path)
    try:
        model_file = os.path.join(app_settings.models_path, 'modelCNN.h5')
        model_cnn = load_model(model_file, compile=False)
        model_cnn.compile()
        image = Image.open(file)
        img_array = np.array(image)
        prediction = model_cnn.predict(
            tf.reshape(img_array, [1, 480, 640, 3]))
        probability: float = round(float(prediction[0][0]), 5)
        return probability
    except Exception as exc:
        logger.error(exc)




