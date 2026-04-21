# LinearLit(선형구조 - Array, list) 연습
# 놀이공원 줄서기

# 연습1 = python 함수 사용
line = ['철수','영희','민수']
print('현재 줄 상태 : ', line)
print()

# 데이터 접근 - 인덱스를 사용(빠름)
print('맨 앞 사람 : ', line[0])
print('두번째 사람 : ', line[1])
print()

# 새치기(삽입)
line.insert(2, '지수')  # 민수는 다음 자리로 밀림
print('지수 삽입 후 현재 줄 상태 : ', line)
print()

# 줄에서 빠짐(삭제)
line.remove('영희')
print('영희 삭제 후 현재 줄 상태 : ', line)
print()

# 앞 사람부터 놀이기구 타기 - 첫번째 자료부터 빠져나감. 뒤 자료는 앞으로 이동
first_person = line.pop(0)  # pop(0) : 왼쪽 값 추출, pop() 오른쪽 값 추출
print('첫번째 사람 : ', first_person)
print('첫번째 사람 탑승 후 현재 줄 상태 : ', line)
print()

# 현재 남은 사람 번호와 함께 출력
for i, p in enumerate(line):
    print(f'{i+1}번째 사람 : {p}')
print("**" * 10)


# 연습 2 - python code 사용
line = ['철수','영희','민수']
print('현재 줄 상태 : ', line)
print()

# 데이터 접근 - 인덱스를 사용(빠름)
print('맨 앞 사람 : ', line[0])
print('두번째 사람 : ', line[1])
print()

# 중간에 새로운 사람이 삽입 : 철수 영희 민수에서 민수 앞에 끼워넣기
# index 2 위치에 지수 삽입 - 공간확보 -> 2 이후 뒤로 한 칸씩 이동 -> 값 대입
line.append(None)  # 새 데이터를 넣기 위해 리스트 끝에 빈 공간(None) 추가
for i in range(len(line) - 1, 2, -1):  
    line[i] = line[i-1]
line[2] = '지수' 
print('지수 삽입 후 현재 줄 상태 : ', line)
print()

# 줄에서 대기하던 영희가 빠져나감(삭제)
# 영희의 위치를 찾은 후 요소들을 앞으로 이동 
remove_index = None
for i in range(len(line)):
    if line[i] == '영희':
        remove_index = i
        break
# 앞으로 한 칸 씩 이동
for i in range(remove_index, len(line) - 1):
    line[i] = line[i+1]
line.pop() # 마지막 중복 데이터 제거
print('영희 삭제 후 현재 줄 상태 : ', line)

# 앞사람 부터 한명씩 놀이기구 타기
# 앞에서 부터 한 칸 씩 좌측으로 이동
first_person = line[0]
for i in range(0,len(line) - 1):
    line[i] = line[i+1]
line.pop()
print('첫번째 사람 탑승 후 현재 줄 상태 : ', line)
print()

# 현재 남은 사람 번호롸 함께 출력
for i, p in enumerate(line):
    print(f'{i+1}번째 사람 : {p}')
print()

# LinearList는 index로 즉시 접근 가능, 삽입/삭제 시 데이터 이동 발생(비용) - 비효율적