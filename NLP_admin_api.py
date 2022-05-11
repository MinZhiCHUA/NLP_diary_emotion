# from .NLP_API_SQL import st
import streamlit as st
# from NLP_API_SQL import conn


# def run_query(query):
#         with conn.cursor() as cur:
#             cur.execute(query)
#             return cur.fetchall()

def app(conn):
    st.title('Welcome to Admin page')
    st. write('Admin admin admin admin admin admin admin admin admin')


    def run_query(query):
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    rows = run_query("SELECT * from df_user_emotion_diary_csv;")
    st.dataframe(data=rows)
    




    

    # rows = run_query("SELECT * from df_user_info_csv;")