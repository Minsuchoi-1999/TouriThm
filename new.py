#!/usr/bin/python

import requests
from bs4 import BeautifulSoup, NavigableString
from html_table_parser import parser_functions
import pandas as pd
import re
import numpy as np
from openpyxl import Workbook
import warnings
import concurrent.futures
import multiprocessing
from transformers import pipeline
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from df import sort 
from es import input_data, make_index

totallist = []
worldlist = []
MAXsize = 0
current = 0

def translator(word):
    trans_Url = 'https://www.google.com/search?q='+ word +' 영어로'
    trans = requests.get(trans_Url)
    tra = BeautifulSoup(trans.text, "html.parser")
    transporation_information = tra.find('div', id = "lrtl-translation-text")
    try:
        Englishword = transporation_information.get_text()
    except AttributeError:
        print("죄송합니다. 알 수 없는 오류가 발생하였습니다. 다시 시도해주세요")
    return Englishword

def collectingCountry():
    countrySearch = requests.get("https://www.0404.go.kr/dev/country.mofa?idx=&hash=&chkvalue=no2&stext=&group_idx=&alert_level=0")
    country = BeautifulSoup(countrySearch.text, "html.parser")
    overallData = country.find('div', 'country_stage_box')
    overallData = overallData.find_all('li')
    return overallData

def collectingCapital(word):
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + word +'+수도'
    CapitalSearch = requests.get(url)
    Capital = BeautifulSoup(CapitalSearch.text, "html.parser")
    Capitaldata = Capital.find("dl", "info_naflag").find('a')
    return Capitaldata.get_text()

def collectSearchNum(word):
    quantityOfSearchUrl = 'http://n-keyword.com/?keyword=' + word
    QOSSearch = requests.get(quantityOfSearchUrl)
    QOS = BeautifulSoup(QOSSearch.text, "html.parser")
    QOSdata1 = QOS.find_all("p", "pcCount")
    QOSdata2 = QOS.find_all("p", "mobileCount")
    QOSSUM = int(QOSdata1[1].get_text().replace(',','')) + int(QOSdata2[1].get_text().replace(',',''))
    return QOSSUM

def collectTransportation(Englishword, grade):
    transportation_Url = 'https://en.wikivoyage.org/wiki/'+ Englishword
    transportation = requests.get(transportation_Url)
    trp = BeautifulSoup(transportation.text, "html.parser")
    transporation_information = trp.find('span', id = "Get_around").parent.next_siblings
    s=""
    count = 0
    total = 0
    for i in transporation_information :
        if(not isinstance(i, NavigableString)):
            s+=i.get_text()
    score = sia.polarity_scores(s)
    if grade == "여행유의":
        weight = 1
    elif grade == "여행자제":
        weight = 0.8
    elif grade == "출국권고":
        weight = 0.75
    elif grade == "여행금지":
        weight = 0.7
    elif grade == "특별여행주의보":
        weight = 0.8

    return round((score['pos']-score['neg'])*weight*100, 1)

def collectEverything(j):
    locallist = []
    word = j.find('a').get_text()
    locallist.append(word)
    print(word)
    if(word == '가이아나공화국'):
        word = '가이아나'
        capital = '가이아나'
    elif(word == '나우루'):
        capital ='야렌'
    elif(word == '니우에'):
        capital = '알로피아'
    elif(word == '마이크로네시아'):
        capital = '미크로네시아'
        word = '미크로네시아'
    elif(word == '마카오(중국)'):
        word = '마카오'
        capital = "마카오"
    elif(word == '쿡제도'):
        capital = '아바루아'
    elif(word == '홍콩(중국)'):
        capital = '홍콩'
    elif(word == '싱가포르'):
        capital = '싱가포르'
    elif(word == '모나코'):
        capital='모나코'
    elif(word == '대만(중국)'):
        capital = '대만'
        word = '대만'
    else :
        capital = collectingCapital(word)
    locallist.append(capital)

    safety = j.find_all('strong')
    safetylist = []
    for k in safety:
        grade = k.find("img")['alt']
        safetylist.append(grade)
    locallist.append(safetylist)

    if(word == '남수단'):
        gdp = 12000
    elif(word == '니우에' or word == '쿡제도'):
        word = '뉴질랜드'
        dfnew = df[df['국가'] == word];
        if(dfnew[2020].values[0] != '-'):
            gdp = dfnew[2020].values[0]
        elif(dfnew['2019'].values[0] != '-'):
            gdp = dfnew['2019'].values[0]
        else:
            gdp = dfnew[2018].values[0]

    elif(word == '대만'):
        gdp = 759104
    elif(word == '모리타니아'):
        gdp = 7779
    elif(word == '베네수엘라'):
        gdp = 48600
    elif(word == '보스니아헤르체고비나'):
        gdp =19790
    elif(word == '사이프러스'):
        gdp=23800
    elif(word == '시리아'):
        gdp=40400
    elif(word == '에리트레아'):
        gdp=2065
    elif(word == '코소보'):
        gdp=8810
    elif(word == '팔레스타인'):
        gdp=15560
    elif(word == '호주'):
        word = '오스트레일리아'
        dfnew = df[df['국가'] == word];
        if(dfnew[2020].values[0] != '-'):
            gdp = dfnew[2020].values[0]
        elif(dfnew['2019'].values[0] != '-'):
            gdp = dfnew['2019'].values[0]
        else:
            gdp = dfnew[2018].values[0]
    elif(word == '홍콩(중국)'):
        word = '홍콩'
        dfnew = df[df['국가'] == word];
        if(dfnew[2020].values[0] != '-'):
            gdp = dfnew[2020].values[0]
        elif(dfnew['2019'].values[0] != '-'):
            gdp = dfnew['2019'].values[0]
        else:
            gdp = dfnew[2018].values[0]
    else:
        dfnew = df[df['국가'] == word];
        if(dfnew[2020].values[0] != '-'):
            gdp = dfnew[2020].values[0]
        elif(dfnew['2019'].values[0] != '-'):
            gdp = dfnew['2019'].values[0]
        else:
            gdp = dfnew[2018].values[0]
    locallist.append(gdp)


    locallist.append(collectSearchNum(word))

    if(word == "북마케도니아"):
        Englishword = "North Macedonia"
    elif(word =="브루나이"):
        Englishword = "Brunei"
    elif(word =="시에라리온"):
        Englishword = "Republic of Sierra Leone"
    elif(word =="앤티가바부다"):
        Englishword = "Antigua and Barbuda"
    elif(word == "도미니카연방"):
        Englishword = "Commonwealth of Dominica"
    elif(word == "아일랜드"):
        Englishword = "Ireland"
    elif(word == "트리니다드토바고"):
        Englishword = "Republic of Trinidad and Tobago"
    elif(word == '몰디브'):
        Englishword = "Maldives"
    elif word == "부탄" :
        Englishword = "Bhutan"
    elif word == "세인트루시아" :
        Englishword = "Saint Lucia"
    elif word == "세인트빈센트그레나딘" :
        Englishword = "Saint_Vincent_and_the_Grenadines"
    elif word == "수단" :
        Englishword = "Sudan"
    elif word == "수리남" :
        Englishword = "Suriname"
    elif word == "슬로베니아" :
        Englishword = "Slovenia"
    elif word == "영국" :
        Englishword = "United Kingdom"
    elif word == "이란" :
        Englishword = "Iran"
    elif word == "조지아" :
        Englishword = "Georgia_(country)"
    elif word == "카타르":
        Englishword = "Qatar"
    elif word == "콜롬비아":
        Englishword = "Colombia" 
    elif word == "콩고":
        Englishword = "Republic_of_the_Congo"
    elif word == "피지":
        Englishword = "Fiji"
    elif word == "가이아나":
        Englishword = "Guyana"
    elif word == "기니비사우":
        Englishword = "Guinea-Bissau" 
    else:
        Englishword = translator(word)
   
    locallist.append(collectTransportation(Englishword, grade))
    if(len(locallist) <6):
        print(locallist)
    totallist.append(locallist)
    worldlist.append(word)

with warnings.catch_warnings(record=True):
    warnings.simplefilter("always")
    df = pd.read_excel('국내총생산_20220605154742.xlsx', engine = 'openpyxl')

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

overallData = collectingCountry()

print("조금만 기다려주세요, 업데이트 중 입니다")
print(str(current) + '/' +str(MAXsize))

with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    for j in overallData:
        print(str(current)+'/197:'+ str(round((current/197*100),1)) +'%',end='==')
        MAXsize+=1
        current+=1
        collectEverything(j)
#        t.start()
#        threads.append(t)

input_data(totallist)

#while(True):
#    sort(totallist)
