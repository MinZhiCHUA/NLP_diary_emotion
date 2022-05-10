import streamlit as st
import pandas as pd
import numpy as no
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

from PIL import Image

import NLP_admin_api
import NLP_user_api

st.write("""

# Emotion Diary Prediction App


This app predicts the emotion of a user based on their Emotion Diary. 

""")

image = Image.open("img/wordcloud.png") 

st.image(image=image)

PAGES = {
    "Admin_api": NLP_admin_api,
    "User_api": NLP_user_api
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()