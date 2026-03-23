import xml.etree.ElementTree as etree

# etree.parse: XML 파일을 파싱하여 ElementTree 객체 생성
xmlfile = etree.parse("my.xml")
print(xmlfile, type(xmlfile))

root = xmlfile.getroot() # getroot: XML의 최상위 요소(루트 노드) 가져오기
print(root.tag)
print(root[0].tag)  # root 요소의 0번째 요소명(노드명) 얻기
print(root[0][0].tag)
# ...
print()

myname = root.find("item").find("name").text # find: 특정 태그를 찾아 해당 요소 반환, .text: 텍스트 내용 추출
mytel = root.find("item").find("tel").text   # find().find(): 계층 구조를 따라 하위 요소 탐색
print(myname + '  ' + mytel)

print('\n--- 기상청 제공 XML 자료 읽기----------')
import requests

url = "https://www.kma.go.kr/XML/weather/sfc_web_map.xml"
header = {"User-Agent": "Mozilla/5.0"}

# requests.get: 해당 URL로 HTTP GET 요청을 보냄
res = requests.get(url, headers=header)
res.raise_for_status() # raise_for_status: 200 OK가 아닐 경우 에러 발생
print(res.text, type(res.text))  # XML 자료가 문자열로 출력됨

root = etree.fromstring(res.text) # fromstring: XML 형식의 문자열을 파싱하여 요소 객체로 변환
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

# findall: 매칭되는 모든 하위 요소를 리스트로 반환하여 순회
for local in weather.findall("local"):
    name = local.text.strip()  # 태그 안의 텍스트
    ta = local.get("ta")     # local 요소(엘리먼트)의 ta 속성값
    print(f"{name} 지역 온도는 {ta}")