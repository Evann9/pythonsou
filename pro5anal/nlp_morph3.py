# 웹(동아일보)에서 특정 단어 관련 문서들 검색 후 명사만 추출
# 워드클라우드 그리기
# pip install simplejson
# pip install pytagcloud

from bs4 import BeautifulSoup
from urllib.parse import quote
import urllib.request
from konlpy.tag import Okt
from collections import Counter  # 단어수를 카운트 하는 라이브러리
import matplotlib.pyplot as plt
import koreanize_matplotlib
import pytagcloud
import numpy as np  
import matplotlib.image as mpimg
import webbrowser

# keyword = input("검색어: ")
# print(quote(keyword))
keyword = '춘분'

target_url = "https://www.donga.com/news/search?query=" + quote(keyword)
headers = {'User-Agent': 'Mozilla/5.0'}
source_code = urllib.request.urlopen(target_url)
# print(source_code)
soup = BeautifulSoup(source_code, 'lxml', from_encoding='utf-8')
# print(soup)

msg = ""

for title in soup.find_all("h4", class_="tlt"):
    title_link = title.find('a')
    # print(title_link)
    article_url = title_link['href']
    # print(article_url)
    
    try:
        source_article = urllib.request.urlopen(article_url)
        soup2 = BeautifulSoup(source_article, 'lxml', from_encoding='utf-8')
        # print(soup2)
        contents = soup2.select('div.article_txt')
        # print(contents)
        for imsi in contents:
            item = str(imsi.find_all(string=True))
            msg += item
            

    except Exception as e:
        pass

    # 형태소 분석 후 명사 추출
    okt=Okt()
    nouns = okt.nouns(msg)
    result = []

    for imsi in nouns:
        if len(imsi) > 1:
            result.append(imsi)
    print(result)
    
    # 워드 클라우드 작성
    taglist = pytagcloud.make_tags(tag, maxsize=100)
    print(taglist)
