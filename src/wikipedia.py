from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

from transformers import pipeline

def get_soup(url):
    # Page content from Website URL
    page = requests.get(url)
    
    # parse html content
    soup = BeautifulSoup(page.content , 'html.parser')

    return soup

def clean_paragraph(text):
    text = re.sub("\[\d+\]", "" , text)
    text = text.replace("[edit]", "")

    return text

def get_paragraph_text(p):
    paragraph_text = ''
    for tag in p.children:
        paragraph_text = paragraph_text + tag.text
    
    return paragraph_text

def get_wiki_extract(url):
    soup = get_soup(url) 
    headers = ['h1', 'h2', 'h3', 'h4']
    wiki_extract = []
    for tag in soup.find_all():
        if tag.name in headers and tag.text != 'Contents':
            # We try to find all paragraphs after it
            p = ''
            # loop through the next elements
            for ne in tag.next_elements:
                if ne.name == 'p':
                    p = p + get_paragraph_text(ne)
                if ne.name in headers:
                    break
            if p != '':
                section = [clean_paragraph(tag.text), tag.name, clean_paragraph(p)]
                wiki_extract.append(section)
        
    return wiki_extract

def get_answers(question, url):
    # question_answerer = pipeline("question-answering", model='../models/distilbert-base-cased-distilled-squad')
    # question_answerer = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')
    question_answerer = pipeline("question-answering", model='deepset/roberta-base-squad2')
    wiki_extract = get_wiki_extract(url)    
    answers = []
    for section in wiki_extract:
        result = question_answerer(question=question, context=section[2])
        answer = {'title': section[0], 'title_tag': section[1], 'paragraph': section[2], **result }
        answers.append(answer)

    return answers

def get_html_answers(question, url, top_n=3):
    answers = get_answers(question, url)
    df = pd.DataFrame(answers)
    n_sections = len(df)
    if n_sections <= top_n:
        df_answers = df.nlargest(n_sections, 'score')
    else:
        df_answers = df.nlargest(top_n, 'score')

    html_answers = ""
    for index, row in df_answers.iterrows():
        title = row['title']
        title_tag = row['title_tag']
        paragraph = row['paragraph']
        par_start = 0
        par_end = len(paragraph) - 1
        ans_start = row['start']
        ans_end = row['end']
        ans = row['answer']
        score = round(row['score'] * 100, 2)
        
        html_answer = f"""
        <p style="background-color: BlanchedAlmond">
            <span style="color: purple; font-weight: bold;">Answer: </span>
            <span>{ans}</span>
            <span style="color: purple; font-weight: bold;">Score: </span>
            <span>{score} %</span>
        </p>
        <{title_tag}>{title}</{title_tag}>
        <p>
            <span>{paragraph[par_start:ans_start-1]}</span>
            <span style="background-color: lightgreen;">{paragraph[ans_start:ans_end]}</span>
            <span>{paragraph[ans_end:par_end]}</span>
        </p>
        <br>
        """
        
        html_answers =  html_answers + html_answer

    return(html_answers)