#!/usr/bin/python

from flask import Flask, render_template, request, session
from bs4 import BeautifulSoup
from html_table_parser import parser_functions
import re
import requests
from elasticsearch import Elasticsearch
import sys
import pandas as pd
import numpy as np

from df import sort
from es import csv_to_df
from new_prediction import sentiment_predict
from new import update
import settings

settings.init()
es_host = "http://localhost:9200"

app = Flask(__name__)
  
@app.route('/post/', methods = ['POST'])
def post():
    temp = request.form['text']
    score = sentiment_predict(temp)

    if(score>0.5):
        return render_template("good.html")
    else:
        return render_template("bad.html")

@app.route('/review/')
def review():
    return render_template("review.html")


@app.route('/Ranking/')
def Ranking():
    df= csv_to_df()
    df = sort(df, '총점')
    return render_template('Ranking.html',  tables=[df.to_html()], titles=df.columns.values)

@app.route('/ready')
def ready():
    return render_template("ready.html")

@app.route('/Updating/')
def Updating():
    update()
    return "수고하셨습니다, 뒤로 가기를 눌러주세요"

@app.route('/hello/')
def hello():
    return render_template("project.html")

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == "__main__":
  app.run()


