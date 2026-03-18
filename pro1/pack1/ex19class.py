# oop(객체 중심 프로그래밍 가능): 새로운 타입 생성, 포함, 상속, 다형성 등을 구사할 수 있음.
# class(설계도)로 인스턴스 해서 객체를 생성(별도의 이름 공간을 갖음)
# 객체는 멤버필드(변수)와 메소드로 구성
# 자바와 달리 접근 지정자가 없다. 메소드 오버로딩 없다.
# 모듈의 멤버 : 변수, 명령문, 함수, 모듈, 클래스
print('뭔가를 하다가 객체 만들기')

class TestClass:            # class는 새로운 타입을 만드는 것
    aa = 1  # 멤버필드(변수). 현재 클래스 내에서 전역 (필요시)

    def __init__(self):            # 특별한 메소드
        print('생성자: 객체 생성시 가장 먼저 1회만 호출 - 초기화 담당')

    def __del__(self):                                # 필요시
        print('소멸자: 프로그램 종료시 자동실행. 마무리 작업')

    def printMsg(self):         # 일반 메소드
        name = '한국인'           # 지역변수: printMsg 에서만 유효
        print(name)

print(TestClass)
test = TestClass()      # 객체 생성
print('test객체의 멤버 aa: ',test.aa)
# method call
test.printMsg()           # 1. Bound Method call
TestClass.printMsg(test)  # 2. UnBound Method call
print(type(1))
print(type(1.0))
print(type(test))        # <class '__main__.TestClass'>
print(id(test))
print(id(TestClass))
test2 = TestClass()
print(id(test2))
