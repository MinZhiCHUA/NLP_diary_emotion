import streamlit as st
import pandas as pd
from datetime import date

def run_query_user(conn,query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def run_query_insert(conn,query,data):
    with conn.cursor() as cur:
        cur.execute(query,data)
        conn.commit()
        return "succeed"
def run_query_user2(conn,query,data):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

db_user = "df_user_info_csv"
db_diary = "df_user_emotion_diary_csv"
#df_user_info = pd.DataFrame(columns=['user_id', 'user_name', 'first_name', 'last_name','email_add'])

def app(conn):

    # with st.sidebar.form(key ='Form1'):  
    #     select = st.selectbox('Choose an option',('New entry', 'Modify', 'Delete'))
    #     display_all = st.form_submit_button("Click to read Diary")
    #     display_date = st.date_input("Select a date")
    #     display_date_button = st.form_submit_button("Click to read your diary at a specific date") 
    

    #save user_name
    if 'username' not in st.session_state:
        pass
    else:
        st.session_state["user"] = st.session_state["username"]


    #get the user info
    user_info = run_query_user(conn,"SELECT * from df_user_info_csv;")
    df_user_info = pd.DataFrame(user_info,columns=['user_id', 'user_name', 'first_name', 'last_name','email_add'])

    user_id = df_user_info[df_user_info['user_name']==st.session_state['user']]['user_id'].values[0]
    user_fn = df_user_info[df_user_info['user_name']==st.session_state['user']]['first_name'].values[0]
    user_ln = df_user_info[df_user_info['user_name']==st.session_state['user']]['last_name'].values[0]
    
    
    # diary of that specific user   
    rows = run_query_user(conn,"SELECT * from df_user_emotion_diary_csv;")
    df_diary = pd.DataFrame(rows,columns=['user_id', 'text', 'date'])
    df_user = df_diary[df_diary["user_id"]==int(user_id)]
    df_date = df_user[df_user["date"]==str(date.today())]

    
    st.title(f'Welcome to your diary {user_fn}')

    #-----------row 1-------------------
    a1, a2 = st.columns(2)
    with a1:     
        #textbox for add a niew diary
        st.markdown("### Write your mood")
        st.text_input(" ",key="mood")


        if st.button(label='Add your mood to your diary'):
            # aller chercher les infos du patient
            m = st.session_state["mood"]
            d = date.today()
            q = 'INSERT INTO df_user_emotion_diary_csv(user_id,text,date) VALUES (%s,%s,%s);'
            data = (int(user_id),m,d)
            run_query_insert(conn,q,data)
            st.write("You have write in your diary")


    with a2:
        st.markdown("### Modify your text")
        se = list()
        for r in df_date["text"]:
            se.append(r[0:min(20,len(r))])
        rad = st.radio("select the one your want to modify",se)
        
        modify = st.text_input(f'"{rad}" will be changed to :')
        if st.button("Apply"):
            # delete 
            q2 = 'DELETE FROM df_user_emotion_diary_csv WHERE "text" = %s;'
            data2 = (rad,)
            run_query_insert(conn,q2,data2)
            # add the new message
            q = 'INSERT INTO df_user_emotion_diary_csv(user_id,text,date) VALUES (%s,%s,%s);'
            data = (int(user_id),modify,date.today())
            run_query_insert(conn,q,data)
            st.write("Diary update")

    # with a3:
    #     st.text_input("Text to delete",key="to_del")
    #     if st.button(label='del your mood'):
    #         q2 = 'DELETE FROM df_user_emotion_diary_csv WHERE "text" = %s;'
    #         data2 = (st.session_state["to_del"],)
    #         run_query_insert(conn,q2,data2)


#--------------------row 2------------------------
    #st.markdown("### Your diary for today")
    st.markdown("<h1 style='text-align: center; color: black;'>Your diary for today</h1>", unsafe_allow_html=True)
    st.dataframe(df_date["text"])

#------------------row 3----------------------    
    b1, b2 = st.columns(2)    
    with b1:
        st.markdown("### Your diary")
        display_all = st.button("Read your diary")
        if display_all:
            st.dataframe(df_user[["text","date"]])
    
    with b2:
        st.markdown("### Day to day diary ")
        display_date = st.date_input("Select a date")
        display_date_button = st.button("Click to read your diary at a specific date")
        if display_date_button:
            st.dataframe(df_user[df_user["date"]==str(display_date)][["text","date"]])









    # if st.button("Modify text"):
    #     i=0
    #     for r in df_date["text"]:
            
    #         modify_text = st.text_input(r[0:min(10,len(r))])
    #         if st.button("Apply",key=f"{i}"):
    #             print(modify_text)
    #             st.write(modify_text)
    #         i+=1

    


