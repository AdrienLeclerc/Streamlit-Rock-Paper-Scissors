import streamlit as st
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image, ImageOps
import numpy as np

def teachable_machine_classification(img, file):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = tf.keras.models.load_model(file)

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = img
    # image = Image.open(img_name).convert('RGB')
    # image = cv2.imread(image)

    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    #print(prediction)
    return np.argmax(prediction)

st.image("https://i.imgur.com/CikgsKT.png")
st.title("Pierre, Feuille, Ciseaux : Image Classification avec Teachable Machine de Google !")
st.markdown("Plus d'information sur Teachable Machine par ici : [Teachable Machine](https://teachablemachine.withgoogle.com)", unsafe_allow_html = True)
st.markdown("Base de donnée Kaggle utilisée pour entrainer le modèle : [Base de donnée](https://www.kaggle.com/drgfreeman/rockpaperscissors)", unsafe_allow_html = True)
st.header("Normal X Ray Vs Pneumonia X Ray")
st.text("Upload a X Ray to detect it is normal or has pneumonia")
# file upload and handling logic
uploaded_file = st.file_uploader("Choose a X Ray Image")


if uploaded_file is not None:
    
    image = Image.open(uploaded_file).convert('RGB')
#image = Image.open(img_name).convert('RGB')

    st.image(image, caption='Uploaded a X Ray IMage.', use_column_width=True)
    
    st.write("")
    
    st.write("Classifying a X Ray Image - Normal Vs Pneumonia.........hold tight")
    
    label = teachable_machine_classification(image,'keras_model.h5')
    
    if label == 0:
        st.write("Roche")
        
    elif label == 1:
        st.write("Papier")
        
    else : 
        st.write("Sciseaux")
