# -*- coding: utf-8 -*-
"""open-lab-endsem.ipynb

Automatically generated by Colaboratory.

Original file is located at (for testing purposes)
    https://colab.research.google.com/drive/1PouihWWeJX7V-g7OHHf3N-rw5NU7lrr2

Github repo link : https://github.com/Mahe-git2hub/openlab-copy2endsem.git
"""

# Commented out IPython magic to ensure Python compatibility.
# %%bash
# mkdir openlab
# cp /content/drive/'My Drive'/'end sem_openlab' -r /content/openlab/
# ls


# from flask_ngrok import run_with_ngrok
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

import spacy
from spacy.matcher import PhraseMatcher
from spacy import displacy

# try:
nlp = spacy.load('en_core_web_sm')
# except Exception:
#     import en_core_web_sm
#     nlp = en_core_web_sm.load()

from collections import Counter
from db_creator import Login, SQLAlchemy
from pprint import pprint

from pathlib import Path
import os
from bs4 import BeautifulSoup
import requests
import re
from flask import Flask, render_template, request, flash, redirect, url_for, session, g
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import socket
import pickle

import nltk
import threading
from nltk.corpus import stopwords

# nltk.download('stopwords')

link1 = 'https://www.thehindu.com/news/national/centre-may-raise-loan-to-pay-shortfall-of-gst-compensation-amount' \
        '/article31329841.ece?homepage=true '
link2 = 'https://www.thehindu.com/news/national/several-union-ministers-officials-return-to-work-at-ministries' \
        '/article31329079.ece?homepage=true '
link3 = 'https://www.thehindu.com/news/national/plea-to-bring-back-to-punjab-stranded-sikh-pilgrims/article31329103' \
        '.ece?homepage=true '

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.secret_key = 'mahesh'
# run_with_ngrok(app)

print('Socket : \t', socket.gethostbyname(socket.getfqdn(socket.gethostname())))

stop_words = set(stopwords.words("english"))
new_stopwords = ['Hindu', 'Subscribe Now', 'free trial', 'Subscription', 'Subscribe']
stop_words = stop_words.union(new_stopwords)

url = None
urlop = None


engine = create_engine('sqlite:///namma_db.db')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
# db = SQLAlchemy(app=app)
# db.create_all()


@app.route('/url_to_string/<url_to_scrape>', methods=['POST'])
def url_to_string(url_to_scrape):
    res = requests.get(url_to_scrape)
    html = res.text
    soup = BeautifulSoup(html, 'html5lib')
    for script in soup(["script", "style", 'aside']):
        script.extract()
    return " ".join(re.split(r'[\n\t]+', soup.get_text()))


def string_to_nlp(s: str):
    matcher = PhraseMatcher(nlp.vocab)
    states = ['Andhra Pradesh',
              'Arunachal Pradesh',
              'Assam',
              'Bihar',
              'Chhattisgarh',
              'Goa',
              'Gujarat',
              'Haryana',
              'Himachal Pradesh',
              'Jharkhand',
              'Karnataka',
              'Kerala',
              'Madhya Pradesh',
              'Maharashtra',
              'Manipur',
              'Meghalaya',
              'Mizoram',
              'Nagaland',
              'Odisha',
              'Punjab',
              'Rajasthan',
              'Sikkim',
              'Tamil Nadu',
              'Telangana',
              'Tripura',
              'Uttar Pradesh',
              'Uttarakhand',
              'West Bengal',
              'Andaman and Nicobar',
              'Chandigarh',
              'Dadra Nagar ',
              'Haveli ',
              'Daman ',
              'Diu',
              'Delhi',
              'Jammu and Kashmir',
              'Ladakh',
              'Lakshadweep',
              'Puducherry']
    # Only run nlp.make_doc to speed things up
    patterns = [nlp.make_doc(text) for text in states]
    matcher.add("Indian State", None, *patterns)
    return nlp(s)


art = url_to_string(link2)
article = nlp(art)
print(article.ents)
print(string_to_nlp(art).ents)

print(len(string_to_nlp(url_to_string(link3))))

labels = [x.label_ for x in article.ents]
print(Counter(labels))

items = [x.text for x in article.ents]
print(Counter(items).most_common(15))

print('\n\n if below works there is no pblm with sents of nlp')
sentences = [x for x in article.sents]
# any sentence can be selected randomly
sent_num = 10
print(sentences[sent_num], '\n\n')


# sentence and its dependencies
@app.route('/pos', defaults={'sent_nums': 10})
@app.route('/pos/<int:sent_nums>', methods=['GET'])
def PartsofSpeech(sent_nums=10):
    pos_article = pickle.load(open("vocab and nlp Obj.pickle", "rb"))
    sentences_pos = [x for x in pos_article.sents]
    # any sentence can be selected randomly default is 10
    svg = displacy.render(nlp(str(sentences_pos[sent_nums])), style='dep', jupyter=False, options={'distance': 70})
    output_path = Path(os.path.join("./", "sentence.svg"))
    output_path.open('w', encoding="utf-8").write(svg)
    # sentence and its dependencies
    return redirect(url_for('NER'))


@app.route('/NER', methods=['GET'])
def NER():
    # ner_article = g.nlp_content
    ner_article = pickle.load(open("vocab and nlp Obj.pickle", "rb"))
    ner_obj = displacy.render(ner_article, style='ent', jupyter=False, page=True)
    with open('templates/display.html', 'wb') as f:
        f.write(bytes(ner_obj, encoding='utf-8'))
    return render_template('display.html')


#
# doc1 = nlp("This is a sentence.")
# doc2 = nlp("This is another sentence.")
# html = displacy.render([doc1, doc2], style="dep", page=True)
#
# # pprint(html)


# displacy.render(ner_article, jupyter=True, style='ent')
#
# doc1 = nlp("This is a sentence.")
# doc2 = nlp("This is another sentence.")
# html = displacy.render([doc1, doc2], style="dep", page=True)


def wc(wc_article):
    wordcloud = WordCloud(width=8000, height=8000, background_color='white', min_font_size=10,
                          stopwords=stop_words).generate(wc_article)
    plt.figure(figsize=(20, 28), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('wordcloud.png', dpi='figure')
    plt.show()


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pass')
        # print(Login.query.filter_by(name='Mahesh').all())
        # db_session.query(Login).filter_by(name="Mahesh").first()
        if username == 'Mahesh' and password == 'WE':
            return redirect(url_for('display'))
        else:
            return render_template('error.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        return redirect('login')


@app.route('/display', methods=['GET', 'POST'])
def display():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        global url
        try:
            url = request.form.get('News article URL')
        except ConnectionError:
            return render_template('error.html')
        except requests.exceptions.ConnectionError:
            return render_template('error.html')
        print(url)
        string_content_url = url_to_string(str(url))
        nlp_content = string_to_nlp(string_content_url)
        print('nlp content: ', nlp_content)
        pickle.dump(nlp_content, open("vocab and nlp Obj.pickle", "wb"))

        # return redirect(url_for('NER'))
        return redirect(url_for('PartsofSpeech', sent_nums=input('Enter the number of sentences\t')))


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    if request.method == 'GET':
        return redirect(url_for('login'), code=302)


if __name__ == '__main__':
    print("Use the following links if don't have any :\n", link1, '\n', link2, '\n', link3)
    app.run(debug=True)
    print(' For running worldcloud open word.py ....')
