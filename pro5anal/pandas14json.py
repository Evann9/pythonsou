# JSON 자료 : XML에 비해 경량. 배열 개념만 있으면 처리 가능
import json


dict = {'name':'tom', 'age':25, 'score':['90','80','88']}   # dict type
print(dict, type(dict))

print('\n json 인코딩 : dict -> str -------')  # json encoding
str_val = json.dumps(dict)
str_val = json.dumps(dict, indent=4)    # 들여쓰기
print(str_val, type(str_val))        #  <class 'str'>
# print(str_val['name'])  # TypeError: string indices must be integers, not 'str'
print(str_val[0:20])  # 문자열 관련 함수만 사용 가능

print('\n json 디코딩 : str -> dict ------')  # json decoding
dict_val = json.loads(str_val)
print(dict_val, type(dict_val))      #  <class 'dict'>
print(dict_val['name'])

for k in dict_val.keys():
    print(k)

for v in dict_val.values():
    print(v)

print('\n서울시 제공 도서관 정보 JSON 샘플 자료 5개 읽기')
import urllib.request as req
import pandas as pd

url = "http://openapi.seoul.go.kr:8088/sample/json/SeoulLibraryTimeInfo/1/5/"
plainText = req.urlopen(url).read().decode('utf-8')
# print(plainText, type(plainText))   # <class 'str'>

jsonData = json.loads(plainText)
# print(jsonData, type(jsonData))   # <class 'dict'>
print(jsonData['SeoulLibraryTimeInfo']['row'][0]['LBRRY_NAME'])

# dict의 get() 사용
print()
libData = jsonData.get('SeoulLibraryTimeInfo').get('row')
# print(libData)
name = libData[0].get('LBRRY_NAME')
print(name)

print()
datas = []
for ele in libData:
    name = ele.get('LBRRY_NAME')
    tel = ele.get('TEL_NO')
    addr = ele.get('ADRES')
    print(name,' ' , tel, ' ' , addr)
    datas.append([name, tel, addr])

import pandas as pd
df = pd.DataFrame(datas, columns=['도서관명', '전화번호', '주소'])
print(df)


