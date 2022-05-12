import streamlit as st
import pandas as pd
import numpy as no
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

from PIL import Image
import psycopg2

import NLP_admin_api
import NLP_user_api

def main():
    st.write("""

    # Emotion Diary Prediction App


    This app predicts the emotion of a user based on their Emotion Diary. 

    """)

    image = Image.open("img/wordcloud.png") 

    st.image(image=image)

    conn = init_connection()

    def run_query(query):
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    rows = run_query("SELECT * from df_user_info_csv;")


    st.table(data=rows)

    def check_password():

        def password_entered():
            
            if (
                st.session_state["username"] in st.secrets["passwords"]
                and st.session_state["password"]
                == st.secrets["passwords"][st.session_state["username"]]
            ):
                st.session_state["password_correct"] = True
                
                del st.session_state["password"]  # don't store username + password
                # del st.session_state["username"]
                if st.session_state["username"] == 'admin':
                    st.session_state["isadmin"] = True
                else:
                    st.session_state["isadmin"] = False
            else:
                st.session_state["password_correct"] = False

        if "password_correct" not in st.session_state:
            # First run, show inputs for username + password.
            st.text_input("Username", on_change=password_entered, key="username")
            st.text_input(
                "Password", type="password", on_change=password_entered, key="password"
            )
            return False
        elif not st.session_state["password_correct"]:
            # Password not correct, show input + error.
            st.text_input("Username", on_change=password_entered, key="username")
            st.text_input(
                "Password", type="password", on_change=password_entered, key="password"
            )
            st.error("😕 User not known or password incorrect")
            return False
        else:
            # Password correct.
            return True

    if check_password():
        
        if st.session_state["isadmin"] == True:
            NLP_admin_api.app(conn)
        else:
            NLP_user_api.app(conn)


def init_connection():
    return psycopg2.connect(**st.secrets["herokudatabase"])

if __name__ == '__main__':
    main()
