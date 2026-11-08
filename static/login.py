import streamlit as st

st.subheader('🔐 로그인')

id = st.text_input('id', key='id')
pw = st.text_input('pw', key='pw', type='password')
btn = st.button(
    "로그인",
    disabled=not id or not pw
)

