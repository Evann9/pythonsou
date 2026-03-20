import xml.etree.ElementTree as etree

xmlfile = etree.parse("my.xml")
print(xmlfile, type(xmlfile))
root = xmlfile.getroot()
print(root.tag)
print(root[0].tag)  # root 요소의 0번째 요소명(노드명) 얻기
print(root[0][0].tag)
# ...
print()
myname = root.find("item").find("name").text
mytel = root.find("item").find("tel").text
print(myname + '  ' + mytel)

print('\n--- 기상청 제공 XML 자료 읽기----------')
import requests

url = "https://www.kma.go.kr/XML/weather/sfc_web_map.xml"
header = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=header)
res.raise_for_status()
print(res.text, type(res.text))  # XML 자료가 문자열로 출력됨
root = etree.fromstring(res.text)
print(root)  # <Element '{current}current' at 0x00000240242A3830>

# {current} namespace 제거
for elem in root.iter():
    if '}' in elem.tag:
        elem.tag = elem.tag.split('}', 1)[1]   # '}'을 기준으로 잘라 태그명만 남김
# {current}weather -> weather
weather = root.find("weather")
year = weather.find("year")
month = weather.find("month")
day = weather.find("day")
hour = weather.find("hour")

print(f"{year}년 {month}월 {day}일 {hour}시")

# 각 지역(local tag) 순회
for local in weather.findall("local"):
    name = local.text.strip()  # 태그 안의 텍스트
    ta = local.get("ta")     # local 요소(엘리먼트)의 ta 속성값
    print(f"{name} 지역 온도는 {ta}")