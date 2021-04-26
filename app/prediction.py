from tensorflow import keras
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

model = keras.models.load_model('/Users/flavioclesio/Documents/github/capivara/app/models/baseline_v0_01.h5')

class_names = ['bronze', 'ceramic', 'copper', 'earthenware', 'etching',
               'faience', 'glass', 'gold', 'graphite', 'ink', 'iron',
               'ivory', 'limestone', 'linen', 'marble', 'on_canvas', 'porcelain',
               'pottery', 'print', 'salted_paper', 'silk', 'silver',
               'steel', 'stone', 'terracotta', 'watercolor', 'wool']


def predict(image_path, model=model):
    image_transformed = keras.preprocessing.image.load_img(
        image_path, target_size=(256, 256))

    image_array = keras.preprocessing.image.img_to_array(image_transformed)
    image_array_batch = tf.expand_dims(image_array, 0)

    prediction = model.predict(image_array_batch)
    score = tf.nn.softmax(prediction[0])

    print(
        f"This image most likely belongs to {class_names[np.argmax(score)]} with a {round(100 * np.max(score), 2)} % confidence.")

    image_display = mpimg.imread(image_path)
    image_plot = plt.imshow(image_display)
    plt.show()

    print("open image via bytes")

    from PIL import Image
    import io

    image_file = image_path

    np.array(Image.open(io.BytesIO(input.image_file.as_bytes())))


image = 'app/bronze.png'

predict(image)
