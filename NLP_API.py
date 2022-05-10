import streamlit as st
import pandas as pd
import numpy as no
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

from PIL import Image

st.write("""

# Emotion Diary Prediction App


This app predicts the emotion of a user based on their Emotion Diary. 

""")

image = Image.open("img/wordcloud.png") 

st.image(image=image)