import os
import numpy as np
import tensorflow as tf
from PIL import Image
import streamlit as st
import time
from tensorflow import keras

ROOT_DIR = os.getcwd()

model = keras.models.load_model(ROOT_DIR + '/models/baseline_v0_04.h5')

class_names = ['bronze', 'ceramic', 'copper', 'earthenware', 'etching',
               'faience', 'glass', 'gold', 'graphite', 'ink', 'iron',
               'ivory', 'limestone', 'linen', 'marble', 'on_canvas', 'porcelain',
               'pottery', 'print', 'salted_paper', 'silk', 'silver',
               'steel', 'stone', 'terracotta', 'watercolor', 'wool']


def predict(image_file):
    image = image_file
    image = image.convert('RGB')
    img_resized = image.resize((256, 256))
    input_arr = keras.preprocessing.image.img_to_array(img_resized)
    image_array_batch = tf.expand_dims(input_arr, 0)
    prediction = model.predict(image_array_batch)
    score = tf.nn.softmax(prediction[0])
    predicted_class = class_names[np.argmax(score)]
    predicted_score = round(100 * np.max(score), 2)
    return predicted_class, predicted_score


st.title("Artwork Image Classification App")
st.write("This is a simple image classification web app to predict the medium of an Artwork")
st.write('\n')

image = Image.open('images/Perseo-con-la-testa-di-Medusa.png')
show = st.image(image, use_column_width=True)

st.sidebar.title("Upload Image")

uploaded_file = st.sidebar.file_uploader(" ", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    uploaded_image = Image.open(uploaded_file)
    show.image(uploaded_image, 'Uploaded Image', use_column_width=True)


st.sidebar.write('\n')
if st.sidebar.button("Click Here to Classify"):

    if uploaded_file is None:
        st.sidebar.write("Please upload an image to classify")

    else:
        with st.spinner('Classifying...'):
            predicted_class, predicted_score = predict(uploaded_image)
            time.sleep(2)
            st.success('Image classified with success!')

        st.sidebar.header("Algorithm Predicts: ")
        st.sidebar.write(f"This image most likely belongs to medium \"{predicted_class}\"", '\n')
        st.sidebar.write(f"Prediction confidence across 27 classes: {predicted_score}%", '\n')