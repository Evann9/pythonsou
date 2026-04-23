# deque : 양 쪽 끝에서 삽입과 삭제가 모두 가능한 자료구조
# 놀이공원 우선 탑승 + 일반 대기줄

from collections import deque

dq = deque()
print('놀이기구 대기 시작')

# 일반인으 뒤쪽으로 들어옴(Queue처럼)
dq.append('철수')
dq.append('영희')
dq.append('민수')
print('일반 대기 : ', list(dq))
print()

# 우선 탑승 - 철수 앞으로 (지수) 
dq.appendleft('VIP지수')
print('우선 탑승 : ', list(dq))
print()

# 놀이기구에 탑승
person = dq.popleft()
print(f'{person} 탑승')
print('현재 대기줄 상태 : ', list(dq))
print()

# 줄 맨 뒷사람 줄서기 포기
person = dq.pop()
print(f'{person} 포기')
print('현재 대기줄 상태 : ', list(dq))
print()