import streamlit as st
import pandas as pd
import numpy as no
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

from PIL import Image
from multiapp import MultiApp
import psycopg2

import NLP_admin_api
import NLP_user_api


st.write("""

# Emotion Diary Prediction App


This app predicts the emotion of a user based on their Emotion Diary. 

""")

image = Image.open("img/wordcloud.png") 

st.image(image=image)

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from mytable;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
