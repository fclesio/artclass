import io
import numpy as np
import tensorflow as tf
from PIL import Image
from opyrator.components.types import FileContent
from pydantic import BaseModel, Field
from tensorflow import keras

model = keras.models.load_model('../models/baseline_v0_02.h5')

class_names = ['bronze', 'ceramic', 'copper', 'earthenware', 'etching',
               'faience', 'glass', 'gold', 'graphite', 'ink', 'iron',
               'ivory', 'limestone', 'linen', 'marble', 'on_canvas', 'porcelain',
               'pottery', 'print', 'salted_paper', 'silk', 'silver',
               'steel', 'stone', 'terracotta', 'watercolor', 'wool']


class ImageInput(BaseModel):
    image_file: FileContent = Field(
        ...,
        mime_type="image/png",
        description="Upload a image to the model",
    )


class PredictionMessageOutput(BaseModel):
    message: str


def artwork_medium_classification(input: ImageInput) -> PredictionMessageOutput:
    image = Image.open(io.BytesIO(input.image_file.as_bytes()))
    image = image.convert('RGB')
    img_resized = image.resize((256, 256))
    input_arr = keras.preprocessing.image.img_to_array(img_resized)
    image_array_batch = tf.expand_dims(input_arr, 0)
    prediction = model.predict(image_array_batch)
    score = tf.nn.softmax(prediction[0])
    return PredictionMessageOutput(message=f"This image most likely belongs to {class_names[np.argmax(score)]} with a {round(100 * np.max(score), 2)} % confidence.")
