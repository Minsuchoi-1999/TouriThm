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

    


