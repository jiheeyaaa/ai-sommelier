import streamlit as st

st.markdown("""
<style>
    div:has(> [data-testid="stImage"]) {
        width: 100% !important;
        max-width: 100% !important;
    }

    [data-testid="stImage"] img {
        width: 150px !important;
        margin: 0 auto !important;
    }
    .txtWrap {
        width:600px;
        margin:0 auto;
    }
</style>
""", unsafe_allow_html=True)

st.image("static/logo.svg")
st.markdown("""
    <div class='txtWrap'>
        <h3>당신의 특별한 순간을 위한 와인을 찾아드립니다.</h3>
        <ul>
            <li>와인을 처음 만나는 설렘도, 깊이 있는 여운도 여기에서 시작됩니다.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)


