import streamlit as st

st.title('와인 추천 서비스')

main_page = st.Page('main.py', title='main_page', icon='🏠')
login_page = st.Page('login.py', title='login_page', icon='🔐')
chat_page = st.Page('chat.py', title='chat_page', icon='💬')

pages = st.navigation([main_page, login_page, chat_page])

pages.run()
