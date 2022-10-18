import streamlit as st
from PIL import Image
import base64
import wikipedia

st.set_page_config(
    page_title="Wikipedia QnA",
    page_icon=Image.open("logo.png"),
    layout="wide",
)

app_heading_css = """
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
    """
app_heading_html = app_heading_css + f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open("logo.png", "rb").read()).decode()}" width=70 height=70>
        <p class="logo-text">{"Wikipedia QnA"}</p>
    </div>
    """

st.markdown(
    app_heading_html,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)

with col1:
    wiki_URL = st.text_input('Enter the URL of the wikipedia article to analyze.', value="", placeholder='https://en.wikipedia.org/wiki/Legume')
    if wiki_URL is not None and wiki_URL != "":
        st.components.v1.iframe(src=wiki_URL, width=None, height=550, scrolling=True)

with col2:
    question = st.text_input('Ask a question - What, Why, How, When?', value="", placeholder='What are legumes rich in?')
    with st.spinner('Finding answer...'):
        if question is not None and question != "":
            html_answers = wikipedia.get_html_answers(question, wiki_URL, 3)
            st.components.v1.html(html=html_answers, width=None, height=550, scrolling=True)