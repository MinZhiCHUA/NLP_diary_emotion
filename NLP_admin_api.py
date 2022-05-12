# from .NLP_API_SQL import st
from numpy import datetime_as_string
import streamlit as st
import pandas as pd
import pickle
import matplotlib.pylab as plt
import datetime as dt


def run_query(query, conn):
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def app(conn):

    filename = 'SGD_model.sav'

    data = run_query("SELECT * from df_user_emotion_diary_csv;", conn)
    df_data_diary = pd.DataFrame(data, columns=['user_id','text', 'date'])

    y_all_test = df_data_diary['text']

    filename = 'SGD_model.sav'
    model = pickle.load(open(filename, 'rb'))
    y_pred = model.predict(y_all_test)

    df_data_diary['Predicted_Emotion'] = y_pred




    data = run_query("SELECT * from df_user_info_csv;", conn)
    df_data_user = pd.DataFrame(data, columns=['user_id','user_name', 'first_name', 'last_name', 'email_add'])

    st.title('Welcome to Admin page')
    

    with st.sidebar.form(key ='Form1'):
        st.write("User's Information Management", )
        input_username1 = st.text_input("Username", "Enter a username")    
        select_func = st.radio('What would you like to do?', ('Create New', 'Modify', 'Delete'))

        apply_button = st.form_submit_button(label = 'Apply')
        st.write("User Database", )
        all_info = st.form_submit_button(label = "All User")

        input_username2 = st.text_input("Just this user", "Enter a username")  
        apply_button2 = st.form_submit_button(label = "Display")

    with st.sidebar.form(key ='Form2'):
        st.write("Users' Emotion Diaries", )

        format = 'MMM DD'  # format output
        start_date = dt.date(year=2022,month=4,day=9)
        end_date = dt.datetime.now().date()
        max_days = end_date-start_date

        values = st.slider('Select a range of dates', start_date, end_date , (start_date, end_date), format=format)

        # values = st.slider('Select a range of dates',min_value=start_date, value=end_date ,max_value=end_date, format=format)
        btn_diary_all = st.form_submit_button(label = 'Display Emotion Diary for all users')
        input_username_diary = st.text_input("Display Emotion Diary for this user:", "Enter a username")  
        btn_diary_user = st.form_submit_button(label = "Show")

        # btn_diary_range = st.form_submit_button(label = 'Display Emotion Diary for all users within a date range')

    date_to_display = pd.date_range(values[0],values[1])
    list_date_str = []
    for i in range(0,len(date_to_display)):
        if int(date_to_display[i].month)<10:
            if int(date_to_display[i].day)<10:
                list_date_str.append(str(date_to_display[i].year)+'-0'+str(date_to_display[i].month)+'-0'+str(date_to_display[i].day))
            else: 
                list_date_str.append(str(date_to_display[i].year)+'-0'+str(date_to_display[i].month)+'-'+str(date_to_display[i].day))
        else:
            if int(date_to_display[i].day)<10:
                list_date_str.append(str(date_to_display[i].year)+'-'+str(date_to_display[i].month)+'-0'+str(date_to_display[i].day))
            else:
                list_date_str.append(str(date_to_display[i].year)+'-'+str(date_to_display[i].month)+'-'+str(date_to_display[i].day))

    if all_info:
        st.subheader('User Database')
        st.dataframe(df_data_user)

    if apply_button2:
        st.subheader('Emotion Diary for '+input_username2)
        st.dataframe(df_data_user.loc[df_data_user['user_name']==input_username2])


    if btn_diary_all:
        
        df_data_diary_range = df_data_diary[df_data_diary['date'].isin(list_date_str)]

        st.subheader('Emotion Diary for all Users')

        mood_count = df_data_diary_range['Predicted_Emotion'].value_counts()

        df_mood_count = pd.DataFrame({
            'Emotion': mood_count.index,
            'Emotion_count': mood_count.values
        })

        fig1, ax1 = plt.subplots() 
        ax1.pie(df_mood_count['Emotion_count'], labels=df_mood_count['Emotion'], autopct='%1.1f%%')


        c1, c2 = st.columns(2)
        c1.dataframe(df_data_diary_range)
        c2.pyplot(fig1)

    if btn_diary_user:

        user_id = df_data_user['user_id'].loc[df_data_user['user_name'] == input_username_diary].values
        df_user_diary = df_data_diary.loc[df_data_diary['user_id'] == user_id[0]]
    
        df_user_diary_range = df_user_diary[df_user_diary['date'].isin(list_date_str)]

        mood_count_user = df_user_diary_range['Predicted_Emotion'].value_counts()
        df_mood_count_user = pd.DataFrame({
            'Emotion': mood_count_user.index,
            'Emotion_count': mood_count_user.values
        })
        fig2, ax2 = plt.subplots() 

        ax2.pie(df_mood_count_user['Emotion_count'], labels=df_mood_count_user['Emotion'], autopct='%1.1f%%')

        st.subheader('Emotion Diary for '+input_username_diary)
        # print(st.session_state.display_u_name)


        c1, c2 = st.columns(2)
        c1.dataframe(df_user_diary_range)
        c2.pyplot(fig2)