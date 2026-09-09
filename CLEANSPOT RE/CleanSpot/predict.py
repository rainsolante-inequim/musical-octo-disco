import os
import cv2
import numpy as np
import tensorflow as tf

IMAGE_SIZE = 180
MODEL_PATH = os.path.join("model", "cleanspot_model.keras")
CLASS_PATH = os.path.join("model", "classes.txt")

model = None
class_names = []


def load_model_files():
    global model, class_names

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "ML model not found. Run train_model.py first."
        )

    model = tf.keras.models.load_model(MODEL_PATH)

    if not os.path.exists(CLASS_PATH):
        raise FileNotFoundError(
            "classes.txt not found. Run train_model.py first."
        )

    with open(CLASS_PATH, "r", encoding="utf-8") as file:
        class_names = [line.strip() for line in file if line.strip()]


def predict_waste(image_path):
    if model is None:
        load_model_files()

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("OpenCV could not read the image.")

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
    image = image.astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)

    predictions = model.predict(image, verbose=0)[0]
    index = int(np.argmax(predictions))

    return class_names[index], float(predictions[index])
