import streamlit as st
import base64
import time
import wikipedia

st.set_page_config(layout="wide")

LOGO_IMAGE = "logo.png"
PAGE_TITLE = "Wikipedia QnA"
st.markdown(
    """
    <style>
    .container {
        display: flex;
    }
    .logo-text {
        font-weight:700 !important;
        font-size:40px !important;
    }
    .logo-img {
        float:right;
        margin-right:20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}" width=70 height=70>
        <p class="logo-text">{PAGE_TITLE}</p>
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)

with col1:
    wiki_URL = st.text_input('Enter the URL of the wikipedia article to analyze.', 'https://en.wikipedia.org/wiki/Legume')
    # st.button('Load URL', on_click=None)
    st.components.v1.iframe(src=wiki_URL, width=None, height=550, scrolling=True)

with col2:
    question = st.text_input('Ask a question - What, Why, How, When?', 'What are legumes rich in?')
    # st.button("Find Answer", on_click=None)
    with st.spinner('Finding answer...'):
        html_answers = wikipedia.get_html_answers(question, wiki_URL, 3)
    
    st.components.v1.html(html=html_answers, width=None, height=550, scrolling=True)