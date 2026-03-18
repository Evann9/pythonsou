import re #정규표현식 지원 모듈 로딩

ss = "'1234 abc가나다abc_123555집에가나78요_6'python is fun'"
print(ss)
print(re.findall(r'123',ss))
print(re.findall(r'가나',ss))
print(re.findall(r'[0-9]',ss))
print(re.findall(r'[0-9]+',ss))
print(re.findall(r'[0-9]{2}',ss))
print(re.findall(r'[0-9]{2,3}',ss))
print(re.findall(r'[a-zA-Z]',ss))
print(re.findall(r'[가-힣]+',ss))
print(re.findall(r'\d+',ss))
print(re.findall(r'\D+',ss))
