#!/usr/bin/python
import pandas as pd 

#data = {'나라' : ['한국', '일본'], '이름': ['서울', '도쿄'], '물가': [80,70], '치안': [90,80], '총점':[170,150]}
#df = pd.DataFrame(data=data)

#n=input('추가할 도시의 개수를 입력하세요 : ')

#for i in range(0,int(n)):
#    country,city=input("나라와 도시 이름을 입력: ").split()
#    prices,safety=map(int,input("물가, 치안 입력 : ").split())
#    total=prices+safety
#
#    data_to_insert = {'나라' : country,'이름': city, '물가': prices,'치안': safety,'총점':total}
#    df = df.append(data_to_insert, ignore_index=True)
    

def sort(datas):
    df=pd.DataFrame(datas,columns = ['국가', '수도', '치안', '물가', '검색량', '교통', '총점'])
    value=input('정렬할 기준 입력: 0.국가/ 1.수도/ 2.치안/ 3.물가/ 4.검색량/ 5.교통 /6 총점')
    sorted=df.sort_values(by=value,ascending=False)
    print(sorted.head())
    sorted=df.sort_values(by=value,ascending=True)
    print(sorted.head())

if __name__ == "__main__":
    print()
