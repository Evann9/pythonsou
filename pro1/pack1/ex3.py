# 기본 자료형 : int, float, bool, complex
# 묶음 자료형 : str, list, tuple, set, dicy

#1) str : 문자열 묶음 자료형. 순서O, 수정X 
s = 'sequence'
print(s, id(s))
print('길이: ',len(s))
print(s[0], s[2])
print('길이: ',s.find('e'),s.find('e',3),s.rfind('e'))  # 문자열 관련함 find('문자',몇번째부터)
#인덱싱 / 슬라이싱
print(s[5])    # 인덱싱 - 변수명[순서], index는 0부터 출발
print(s[2:5])    # 슬라이싱[시작점,미만] 
print(s[:], ' ', s[0:len(s)],s[::1]) 
print(s[0:7:2])
print(s[-1], ' ', s[-4:-1:1])
print(s)
s= 'sequenc'  # 수정X, 변경
print(s,id(s))
s= 'bequenc'
print(s, id(s))

print('-------------')
#2) List : 다양한 종류의 자료 묶음형. 순서O, 수정O, 중복O
a = [1,2,3]
print(a, a[0],a[0:2])
b = [10, a, 10, 20.5, True, '문자열']
print(b, ' ' , b[1], ' ', b[1][0])
print()
family = ['엄마', '아빠', '나','여동생']
print(id(family))
family.append('남동생')    # 추가
print(id(family))
family.remove('나')        # 삭제 
family.insert(0,'할머니')  # 삽입
family.extend(['삼촌', '고모', '조카']) # 추가
family += ['이모']         # 추가
print(family)
print(family.index('아빠'))
print('엄마' in family, '나' in family)

family.remove('아빠')   #값에 의한 삭제
del family[2]
print(family)

print()
kbs = ['123', '34', '234']
kbs.sort()   #문자열 정렬
print(kbs)

mbc = [123, 34 , 234]
#mbc.sort()              #숫자 정렬 (ascending sort, 오름)
mbc.sort(reverse=True)   #숫자 정렬 (decending, 내림)
print(mbc)

sbs = [123, 34, 234]
ytn = sorted(sbs)
print(sbs)
print(ytn)
print()
name = ['tom', 'james', 'oscar']
name2 = name
print(name)
print(name2)

import copy 
name3 = copy.deepcopy(name)
print(name3)

name[0] = '길동'
print(name)
print(name2)
print(name3)

print('------------')
#3) tuple : 리스트와 유사. 읽기 전용, 수정X
t = (1,2,3,4)
t = 1,2,3,4    # 위와 동일
print(t,type(t))
#k = (1)
k = (1,)
print(k, type(k))
print(t[0],' ', t[0:2])
#t[0] = 77  #'tuple' object does not support item assignment

imsi = list(t)
imsi[0] = 77
t = tuple(imsi)
print(t)

print('--------------')
#4) set : 순서X, 중복X, 수정O
ss = {1,2,1,3}
print(ss)
ss2 = {3,4}
print(ss.union(ss2))                 # 합집합 
print(ss.intersection(ss2))          # 교집합
print(ss - ss2, ss | ss2, ss & ss2)  # 차, 합, 교집합
#print(ss[0]) # TypeError: 'set' object is not subscriptable

ss.update({6,7})
print(ss)
ss.discard(7)  #값 삭제
ss.discard(7)  #값 없으면 해당 값 패스
ss.remove(6)  #값 삭제
#ss.remove(6)  # 값이 없으면 에러 발생
print(ss)

li = ['aa', 'aa', 'bb', 'cc', 'aa']
print(li)
imsi = set(li)
li = list(imsi)
print(li)

print('-------------')
#5) dict : 사전 자료형 {'키': 값} 형ㅌ
# 방법1
mydic = dict(k1 = 1, k2 = 'ok', k3 = 123.4)
print(mydic,type(mydic))

# 방법2
dic = {'파이썬':'뱀', '자바':'커피', '인사':'안녕'}
print(dic)
print(len(dic))
print(dic['자바'])
ff = dic.get('자바')
print(ff)

# print(dic['커피']) # key로 찾는것
# print(dic[0])  # 인덱싱X
dic['금요일'] = '와우'   # 추가
print(dic)
del dic['인사']
print(dic)
print(dic.keys())
print(dic.values())























