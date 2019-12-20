from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
import keras
import tensorflow as tf
import pickle
# import time
import numpy as np


# keras.backend.clear_session()
labels = pickle.load(open('model/label.kece', 'rb'))
labels = labels.classes_
model = pickle.load(open('model/model.kece', 'rb'))
graph = tf.get_default_graph()
IMAGE_SIZE = (256, 256)


black_list = [
    'Pepper__bell___healthy',
    'Pepper__bell___Bacterial_spot',
    'Potato___healthy',
    'Potato___Late_blight'
]


def detect(image):
    with graph.as_default():
        img = prepare_image(image)
        predicts = model.predict(img)
        normalized = np.argmax(predicts, axis=1)
        predicts_name = []
        for i in normalized:
            predicts_name.append(labels[i])
        predict_name = predicts_name[0]

        blacked = predict_name in black_list

        # print('Probability')
        # print(normalized)
        # time.de

        if blacked:
            print('========== BLACKED CATCHED ========')
            predict_name = 'Tomato_Bacterial_spot'

        return {
            'predict': normalized.tolist()[0],
            # 'predict_name': predicts_name
            'predict_name': predict_name
        }

def prepare_image(img):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(IMAGE_SIZE)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = imagenet_utils.preprocess_input(img)

    return img
