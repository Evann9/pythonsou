# BeautifulSoup 객체를 이용한 웹 문서 처리
import requests
from bs4 import BeautifulSoup

baseurl = "https://www.naver.com"
headers = {"User-Agent": "Mozilla/5.0"}  # 필수적으로 들어가야 인식 가능

source = requests.get(baseurl, headers=headers)
print(source, type(source))  #  <Response [200]> <class 'requests.models.Response'>
print(source.status_code)  # 200
# print(source.text, type(source.text))  # 페이지 소스 불러오기
# print(source.content)  # 이진데이터로 변경해서 불러옴

conv_data = BeautifulSoup(source.text , 'lxml')
# print(conv_data, type(conv_data))  # <class 'bs4.BeautifulSoup'>

for atag in conv_data.find_all('a'):
    href = atag.get('href')
    title = atag.get_text(strip=True)
    if title :
        print(href)
        print(title)
        print('-------------')
