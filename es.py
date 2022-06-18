#!/usr/bin/python
import pandas as pd 
from elasticsearch import Elasticsearch

data = {'국가' : [], '도시': [], '최근검색량': [], '물가': [], '기후':[], '교통':[], '치안':[], '총점':[]}

es_host="http://localhost:9200"
es= Elasticsearch(es_host)

def make_index(es,index_name):
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        es.indices.create(index=index_name)

def input_data(n):
    for i in range(0,int(n)):
        country,city=input("국가와 도시 이름을 입력: ").split()
        searches, prices,weather,traffic,safety=map(int,input("최근검색량, 물가, 기후, 교통, 치안 입력 : ").split())
        total=searches+prices+weather+traffic+safety

        data_to_insert = {'국가' : country,'도시': city, '최근검색량': searches, '물가': prices, '기후' : weather, '교통' : traffic, '치안': safety,'총점':total}
        
        res=es.index(index='cities',document=data_to_insert)

def delete_data(element):
    es.indices.delete(index='cities',body={"query":{'match':{'도시':element}}})

def find_data(element):
    results = es.search(index='cities', body={"query":{'match':{'도시':element}}})
    for result in results['hits']['hits']:
        print(result['_source'])


make_index(es,'cities')


while 1:
    number=int(input('1 : 입력, 2 : 삭제, 3: 검색, 4: 종료\n'))
    if number==1:
        n=input('데이터 베이스에 추가할 개수를 입력하세요 : ')
        input_data(n)
    elif number==2:
        element=input('삭제할 것을 입력하세요 : ')
        delete_data(element)
    elif number==3:
        element=input('검색할 것을 입력하세요 : ')
        find_data(element)
    elif number==4:
        break
        


