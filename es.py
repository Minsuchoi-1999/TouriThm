#!/usr/bin/python
import pandas as pd 
from elasticsearch import Elasticsearch

#data = {'국가' : [], '도시': [], '최근검색량': [], '물가': [], '기후':[], '교통':[], '치안':[], '총점':[]}


def make_index(es, index_name):
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        es.indices.create(index=index_name)

def input_data(database):
    es_host="http://localhost:9200"
    es=Elasticsearch(es_host)
    make_index(es,'cities')
    for data in database:
        print(data)
        country= data[0]
        city= data[1]
        safety= data[2]
        gpa = data[3]
        search = data[4]
        traffic = data[5]

        data_to_insert = {'국가' : country,'수도': city,'치안' : safety, '물가' : gpa, '최근검색량': search, '교통' : traffic}
        
        res=es.index(index='cities',document=data_to_insert)

def delete_data(element):
    es.indices.delete(index='cities',body={"query":{'match':{'도시':element}}})

def find_data(element):
    results = es.search(index='cities', body={"query":{'match':{'도시':element}}})
    for result in results['hits']['hits']:
        print(result['_source'])

#while 1:
#    number=int(input('1 : 입력, 2 : 삭제, 3: 검색, 4: 종료\n'))
#    if number==1:
#        n=input('데이터 베이스에 추가할 개수를 입력하세요 : ')
#        input_data(n)
#    elif number==2:
#        element=input('삭제할 것을 입력하세요 : ')
#        delete_data(element)
#    elif number==3:
#        element=input('검색할 것을 입력하세요 : ')
#        find_data(element)
#    elif number==4:
#        break
        
if __name__ == "__main__":
    totallist = [['한국', '서울', '안전', '1', '2', '3'],['미국', '워싱턴', '안전', '1', '2', '3']]
    input_data(totallist)

