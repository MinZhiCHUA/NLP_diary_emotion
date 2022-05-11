import streamlit as st

def app():
    st.title('Welcome to User page')
    st. write('User User User User User User User User User')

    x = st.slider('x')  # 👈 this is a widget
    st.write(x, 'squared is', x * x)