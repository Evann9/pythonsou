# stack : LIFO 구조

stack = [] # 파이썬의 List를 Stack처럼 사용
print('놀이공원 입장')
print()

# 놀이 기구 탈 때의 기록을 남김
stack.append('T-express 탑승') # PUSH
print('기록 : ', stack)

stack.append('바이킹 탑승')
print('기록 : ', stack)
# print(stack[1])  # 주의 : 파이썬의 List 기능 사용. Stack 기능 아님

stack.append('회전목마 탑승')
print('기록 : ', stack)
print()

# 가장 최근 기록 삭제
last_action = stack.pop()  # POP   주의 : pop(0), pop(1) 사용X - 개념 위반
print('마지막 기록 삭제 후 현재 기록 : ', stack)
print()

last_action = stack.pop()
print('마지막 기록 삭제 후 현재 기록 : ', stack)
print()

print('\n' + '--' * 20)
# LIFO를 class로 연습
class MyStack:
    def __init__(self, iterable=None):
        self._data = []  # __data : privite / _data : 내부저장소 임을 알림(가독성 높임), 기본문법X
        if iterable is not None:
            for x in iterable:
                self.push(x)

    def push(self, x):
        # 맨 위 (top)에 요소 추가(삽입)
        self._data.append(x)
        return x
    
    def pop(self):
        # 맨 위 (top)에 요소 제거
        if not self._data:
            raise IndexError('pop from empty stack')
        return self._data.pop()
    
    def is_empty(self):
        return not self._data  # 비어있을때 True 반환

    def __repr__(self):  # 파이썬 실행시(print) 자동 호출 되는 특별 메소드
        top_to_bottom = list(reversed(self._data))
        return f"Stack(top -> bottom {top_to_bottom})"


def demo1Func():
    s = MyStack()
    for item in ['A','B','C','D']:
        s.push(item)
        print(f"push {item} -> {s}")

    print('LIFO에 따라 하나씩 추출')
    while not s.is_empty():
        print(f"pop -> {s.pop()}")

def demo2Func(text : str) -> str:
    s = MyStack(text)
    out = [] # 뒤집힌 문자 기억
    while not s.is_empty():
        out.append(s.pop())
    return ''.join(out)

if __name__ == '__main__':
    demo1Func()
    print(demo2Func('Python is good'))
    print(demo2Func('나끝 제언'))
    print(demo2Func('다싶 고가집'))
    