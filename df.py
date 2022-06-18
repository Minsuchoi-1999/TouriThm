#!/usr/bin/python
import pandas as pd 
from elasticsearch import Elasticsearch

data = {'국가' : [], '도시': [], '최근검색량': [], '물가': [], '기후':[], '교통':[], '치안':[], '총점':[]}
df = pd.DataFrame(data=data)

es_host="http://localhost:9200"
es= Elasticsearch(es_host)

def input_data(n):
    for i in range(0,int(n)):
        country,city=input("국가와 도시 이름을 입력: ").split()
        searches, prices,weather,traffic,safety=map(int,input("최근검색량, 물가, 기후, 교통, 치안 입력 : ").split())
        total=searches+prices+weather+traffic+safety

        data_to_insert = {'국가' : country,'도시': city, '최근검색량': searches, '물가': prices, '기후' : weather, '교통' : traffic, '치안': safety,'총점':total}
        df.append(data_to_insert, ignore_index=True)

        res=es.index(index='cities',document=data_to_insert)
        print(res)

def print_df(value):
    sorted_df=df.sort_values(by=value,ascending=False)
    print(sorted_df.head())


n=input('데이터 베이스에 추가할 개수를 입력하세요 : ')
input_data(n)





results = es.search(index='cities', body={"query":{'match':{'국가':'중국'}}})
for result in results['hits']['hits']:
    print(result['_source'])