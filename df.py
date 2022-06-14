#!/usr/bin/python
import pandas as pd 
data = {'나라' : ['한국', '일본'], '이름': ['서울', '도쿄'], '물가': [80,70], '치안': [90,80], '총점':[170,150]}
df = pd.DataFrame(data=data)

# 추가할 데이터 

n=input('추가할 도시의 개수를 입력하세요 : ')

for i in range(0,int(n)):
    country,city=input("나라와 도시 이름을 입력: ").split()
    mulga,chian=map(int,input("물가, 치안 입력 : ").split())
    jumsu=mulga+chian

    data_to_insert = {'나라' : country,'이름': city, '물가': mulga,'치안': chian,'총점':jumsu}
    df = df.append(data_to_insert, ignore_index=True)
    

value=input('정렬할 기준 입력 : ')
sorted=df.sort_values(by=value,ascending=False)
print(sorted.head())