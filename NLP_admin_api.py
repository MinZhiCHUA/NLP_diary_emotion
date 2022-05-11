# from .NLP_API_SQL import st
import streamlit as st
import pandas as pd
# from NLP_API_SQL import conn


# def run_query(query):
#         with conn.cursor() as cur:
#             cur.execute(query)
#             return cur.fetchall()

def app(conn):
    st.title('Welcome to Admin page')


    def run_query(query):
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    rows = run_query("SELECT * from df_user_info_csv;")

    df_row = pd.DataFrame(rows, columns=['user_id','user_name', 'first_name', 'last_name', 'email_add'])

    st.dataframe(data=df_row)

    st.button('Display Emotion diary')
    st.button('Add new User')

    # Add a selectbox to the sidebar:
    add_selectbox = st.sidebar.selectbox(
        'Menu',
        ('Add/delete/rename user', 'Display emotion Diary', 'Mobile phone')
    )
    




    

    # rows = run_query("SELECT * from df_user_info_csv;")