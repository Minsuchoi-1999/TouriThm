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
from es import csv_to_df, find_data
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

@app.route('/post3/', methods = ['POST'])
def post3():
    text = request.form.get('검색')
    locallist = find_data(text)
    value1 = locallist['국가']
    value2 = locallist['수도']
    value3 = locallist['치안']
    value4 = locallist['물가']
    value5 = locallist['최근검색량']
    value6 = locallist['교통']
    value7 = locallist['총점']
    return render_template("search.html", value1= value1, value2 = value2, value3 = value3, value4 = value4, value5 = value5, value6 = value6, value7 = value7)

@app.route('/post2/', methods = ['POST'])
def post2():
    df=csv_to_df()
    selected1 =''
    selected2 =''
    if(request.form.get('design1')):
        selected1 = '국가'
    elif(request.form.get('design2')):
        selected1 = '수도'
    elif(request.form.get('design3')):
        selected1 = '치안'
    elif(request.form.get('design4')):
        selected1 = '물가'
    elif(request.form.get('design5')):
        selected1 = '검색량'
    elif(request.form.get('design6')):
        selected1 = '교통'
    elif(request.form.get('design7')):
        selected1 = '총점'
    if(request.form.get('function1')):
        selected2 = '오름차순'
    elif(request.form.get('function2')):
        selected2 = '내림차순'
                     
    df = sort(df, selected1, selected2)
    return render_template('Ranking.html', tables=[df.to_html()], titles=df.columns.values)
@app.route('/review/')
def review():
    return render_template("review.html")


@app.route('/Ranking/')
def Ranking():
    df= csv_to_df()
    df = sort(df, '총점','오름차순')
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


