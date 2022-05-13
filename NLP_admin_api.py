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

def run_query_insert(conn,query,data):
    with conn.cursor() as cur:
        cur.execute(query,data)
        conn.commit()
        return "succeed"

def func_create_user_first(df_data_user,conn, input_user):
    input_firstname = st.text_input("First Name:", "")  
    input_lastname = st.text_input("Last Name:", "")  
    input_email = st.text_input("Email:", "")  
    btn_create_user = st.button(label = "Create New User")

    if btn_create_user:
        input_id = int(df_data_user['user_id'].max()+1)

        q = 'INSERT INTO df_user_info_csv(user_id,user_name,first_name,last_name,email_add) VALUES (%s,%s,%s,%s,%s);'
        data = (int(input_id),input_user,input_firstname,input_lastname,input_email)

        run_query_insert(conn,q,data)
        st.write('User profile for '+input_user+" is created")
        st.session_state['create_new_user'] = False
        # return False


def func_modify_user(conn, modify_userid,modify_username,modify_firstname,modify_lastname,modify_emailadd):
    st.session_state['create_new_user'] = False
    st.session_state['modify_new_user'] = True
    
    input_modify_firstname = st.text_input("First Name:", str(modify_firstname))  
    input_modify_lastname = st.text_input("Last Name:", str(modify_lastname))  
    input_modify_email = st.text_input("Email:", str(modify_emailadd))  

    btn_modify_user = st.button(label = "Modify user profile")

    if btn_modify_user:

        q2 = "UPDATE df_user_info_csv SET first_name=%s, last_name=%s,email_add=%s WHERE user_name=%s;"
        data2 = input_modify_firstname,input_modify_lastname,input_modify_email,modify_username

        run_query_insert(conn,q2,data2)
        st.write('User profile for '+modify_username+" is modified")

        st.session_state['modify_new_user'] = False


def func_delete_user(conn, delete_username):
    q3 = 'DELETE FROM df_user_info_csv WHERE "user_name"=%s;'
    data3 = (delete_username,)
    # print(delete_username)
    run_query_insert(conn,q3,data3)
    st.write('User profile for '+delete_username+" is deleted")

    st.session_state['modify_new_user'] = False
    

def init():
    # Initialization
    if 'create_new_user' not in st.session_state:
        st.session_state['create_new_user'] = False

    if 'modify_new_user' not in st.session_state:
        st.session_state['modify_new_user'] = False
    
    if 'delete_new_user' not in st.session_state:
        st.session_state['delete_new_user'] = False

def app(conn):

    
    filename = 'SGD_model.sav'

    # st.write(st.session_state)
    init()
    # st.write(st.session_state)

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

        existing_user = str(df_data_user['user_name'])

    # Create a new user
    if apply_button and select_func=='Create New':
        st.session_state['delete_new_user'] = False
        st.session_state['modify_new_user'] = False

        st.subheader('Creating a new user')
        
        if  input_username1 in existing_user:
            st.error("😕 Error! This user already exists")
        else:
            # st.write(st.session_state)
            st.session_state['create_new_user'] = True
    
    if st.session_state['create_new_user'] == True:
        st.session_state['delete_new_user'] = False
        st.session_state['modify_new_user'] = False
        func_create_user_first(df_data_user,conn, input_username1)

    # Modify an existing user
    if apply_button and select_func=='Modify':    
        st.session_state['create_new_user'] = False
        st.session_state['delete_new_user'] = False 
        st.subheader('Modify a user')

        if  input_username1 not in existing_user:
            st.error("😕 Error! This user does not exists in the database")
            st.subheader('All Users in database')
            st.dataframe(df_data_user)
            st.session_state['create_new_user'] = False
        else:
            # st.write(st.session_state)
            st.session_state['modify_new_user'] = True

    if st.session_state['modify_new_user'] == True:

        st.session_state['create_new_user'] = False
        st.session_state['delete_new_user'] = False
        
        st.subheader('Please make the changes in '+input_username1)
        user_profile = df_data_user.loc[df_data_user['user_name']==input_username1]

        modify_userid = int(user_profile.user_id.iloc[0])
        modify_username = str(user_profile.user_name.iloc[0])
        modify_firstname = str(user_profile.first_name.iloc[0])
        modify_lastname = str(user_profile.last_name.iloc[0])
        modify_emailadd = str(user_profile.email_add.iloc[0])

        func_modify_user(conn, modify_userid,modify_username,modify_firstname,modify_lastname,modify_emailadd)


    # Remove an existing user
    if apply_button and select_func=='Delete':
        st.session_state['create_new_user'] = False
        st.session_state['modify_new_user'] = False
        

        st.subheader('Delete a user')

        if  input_username1 not in existing_user:
            st.error("😕 Error! This user does not exists in the database")
            st.subheader('All Users in database')
            st.dataframe(df_data_user)
        else:
            # st.write(st.session_state)
            st.session_state['delete_new_user'] = True


    if st.session_state['delete_new_user'] == True:

        st.session_state['create_new_user'] = False
        st.session_state['modify_new_user'] = False

        user_profile = df_data_user.loc[df_data_user['user_name']==input_username1]
        st.dataframe(user_profile)

        st.subheader('Are you sure that you want to delete this user?')

        c1,c2 = st.columns(2)
        delete_yes = c1.button(label='Yes')
        delete_no = c2.button(label='No')

        if delete_yes:
            func_delete_user(conn,input_username1)

        if delete_no:
            st.write('Delete canceled')


    if all_info:
        st.session_state['create_new_user'] = False
        st.session_state['modify_new_user'] = False
        st.session_state['delete_new_user'] = False

        st.subheader('User Database')
        st.dataframe(df_data_user)

    if apply_button2:
        st.session_state['create_new_user'] = False
        st.session_state['modify_new_user'] = False
        st.session_state['delete_new_user'] = False

        st.subheader('User profile for '+input_username2)
        st.dataframe(df_data_user.loc[df_data_user['user_name']==input_username2])

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




    if btn_diary_all:
        st.session_state['create_new_user'] = False
        st.session_state['modify_new_user'] = False
        st.session_state['delete_new_user'] = False

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
        st.session_state['create_new_user'] = False
        st.session_state['modify_new_user'] = False
        st.session_state['delete_new_user'] = False

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