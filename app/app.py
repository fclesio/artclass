import io
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from PIL import Image
from io import BytesIO
from opyrator.components.types import FileContent
from pydantic import BaseModel, Field
from tensorflow import keras
import cv2

# Load pretrained model
model = keras.models.load_model('/Users/flavioclesio/Documents/github/capivara/app/models/baseline_v0_01.h5')

class_names = ['bronze', 'ceramic', 'copper', 'earthenware', 'etching',
               'faience', 'glass', 'gold', 'graphite', 'ink', 'iron',
               'ivory', 'limestone', 'linen', 'marble', 'on_canvas', 'porcelain',
               'pottery', 'print', 'salted_paper', 'silk', 'silver',
               'steel', 'stone', 'terracotta', 'watercolor', 'wool']


class ImageSuperResolutionInput(BaseModel):
    image_file: FileContent = Field(
        ...,
        mime_type="image/png",
        description="Upload a image to the model",
    )

"""
class ImageSuperResolutionOutput(BaseModel):
    upscaled_image_file: FileContent = Field(
        ...,
        mime_type="image/png",
        description="Upscaled image via super resolution model.",
    )
"""


class ImageSuperResolutionOutput(BaseModel):
    message: str


def image_super_resolution(input: ImageSuperResolutionInput) -> ImageSuperResolutionOutput:

    image = Image.open(io.BytesIO(input.image_file.as_bytes()))

    image = image.convert('RGB')

    img_resized = image.resize((256, 256))

    input_arr = keras.preprocessing.image.img_to_array(img_resized)

    print(type(input_arr))

    print(input_arr.shape)

    #image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #image_resized = cv2.resize(image_rgb, (256, 256))
    #img_np_array = np.array(image)
    #img_np_array = np.array(Image.open(io.BytesIO(input.image_file.as_bytes())))
    #img__ = Image.open(io.BytesIO(input.image_file.as_bytes()))
    #img = Image.open(io.BytesIO(input.image_file.as_bytes()))
    #img_io = io.BytesIO(input.image_file.as_bytes())
    #img_raw = input.image_file





    #image_transformed = keras.preprocessing.image.load_img(
    #    img__, target_size=(256, 256))

    #image_array = keras.preprocessing.image.img_to_array(image_transformed)

    image_array_batch = tf.expand_dims(input_arr, 0)

    prediction = model.predict(image_array_batch)

    score = tf.nn.softmax(prediction[0])

    print(prediction)
    print(score)

    return ImageSuperResolutionOutput(message=f"This image most likely belongs to {class_names[np.argmax(score)]} with a {round(100 * np.max(score), 2)} % confidence.")
