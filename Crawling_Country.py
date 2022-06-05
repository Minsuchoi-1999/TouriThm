import requests
from bs4 import BeautifulSoup
from html_table_parser import parser_functions
import pandas as pd
import re
import numpy as np
from openpyxl import Workbook
import warnings

countrySearch = requests.get("https://www.0404.go.kr/dev/country.mofa?idx=&hash=&chkvalue=no2&stext=&group_idx=&alert_level=0")
country = BeautifulSoup(countrySearch.text, "html.parser")
countryData = country.find('div', 'country_stage_box')
countryData = countryData.find_all('a')

with warnings.catch_warnings(record=True):
    warnings.simplefilter("always")
    df = pd.read_excel('국내총생산_20220605154742.xlsx', engine = 'openpyxl')


for j in countryData:
    word = j.get_text()
    print(word)
    if(word == '가이아나공화국'):
        word = '가이아나'
    elif(word == '나우루'):
        print('야렌')
    elif(word == '니우에'):
        print('알로피아')
    elif(word == '마이크로네시아'):
         word = '미크로네시아'
    elif(word == '마카오(중국)'):
        word = '마카오'
        print("마카오")
    elif(word == '쿡제도'):
        print('아바루아')
    elif(word == '홍콩(중국)'):
        print('홍콩')
    elif(word == '싱가포르'):
        print('싱가포르')
    elif(word == '모나코'):
        print('모나코')
    else :
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + word +'+수도'
        CapitalSearch = requests.get(url)
        Capital = BeautifulSoup(CapitalSearch.text, "html.parser")
        Capitaldata = Capital.find("dl", "info_naflag").find('a')
        print(Capitaldata.get_text())

    if(word == '남수단'):
        print(12000)
    elif(word == '니우에' or word == '쿡제도'):
        word = '뉴질랜드'
        dfnew = df[df['국가'] == word];
        if(dfnew[2020].values[0] != '-'):
            gdp = dfnew[2020].values[0]
        elif(dfnew['2019'].values[0] != '-'):
            gdp = dfnew['2019'].values[0]
        else:
            gdp = dfnew[2018].values[0]
        print(gdp)
    elif(word == '대만'):
        print(759104)
    elif(word == '모리타니아'):
        print(7779)
    elif(word == '베네수엘라'):
        print(48600)
    elif(word == '보스니아헤르체고비나'):
        print(19790)
    elif(word == '사이프러스'):
        print(23800)
    elif(word == '시리아'):
        print(40400)
    elif(word == '에리트레아'):
         print(2065)
    elif(word == '코소보'):
        print(8810)
    elif(word == '팔레스타인'):
        print(15560)
    elif(word == '호주'):
        word = '오스트레일리아'
        dfnew = df[df['국가'] == word];
        if(dfnew[2020].values[0] != '-'):
            gdp = dfnew[2020].values[0]
        elif(dfnew['2019'].values[0] != '-'):
            gdp = dfnew['2019'].values[0]
        else:
            gdp = dfnew[2018].values[0]
        print(gdp)
    elif(word == '홍콩(중국)'):
        word = '홍콩'
        dfnew = df[df['국가'] == word];
        if(dfnew[2020].values[0] != '-'):
            gdp = dfnew[2020].values[0]
        elif(dfnew['2019'].values[0] != '-'):
            gdp = dfnew['2019'].values[0]
        else:
            gdp = dfnew[2018].values[0]
        print(gdp)
        
    else:
        dfnew = df[df['국가'] == word];
        if(dfnew[2020].values[0] != '-'):
            gdp = dfnew[2020].values[0]
        elif(dfnew['2019'].values[0] != '-'):
            gdp = dfnew['2019'].values[0]
        else:
            gdp = dfnew[2018].values[0]
        print(gdp)


    quantityOfSearchUrl = 'http://n-keyword.com/?keyword=' + word
    QOSSearch = requests.get(quantityOfSearchUrl)
    QOS = BeautifulSoup(QOSSearch.text, "html.parser")
    QOSdata1 = QOS.find_all("p", "pcCount")
    QOSdata2 = QOS.find_all("p", "mobileCount")
    QOSSUM = int(QOSdata1[1].get_text().replace(',','')) + int(QOSdata2[1].get_text().replace(',',''))
    print(QOSSUM)
    


