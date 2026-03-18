kor = 100     # 모듈의 전역변수

def abc():
    print('모듈의 멤버 함수')


class My:
    kor = 80    # My 멤버 변수(필드)
    
    def abc(self):
        print('My 멤버 메소드')

    def show(self):
        # kor = 77 # 메소드 내 지역 변수
        print(kor)  # 지역 ->(없으면) 전역변수 값 출력
        print(self.kor)  # class 내 변수값
        self.abc()
        abc()

my = My()
my.show()
print()
print(My.kor)
tom = My()
print(tom.kor)
tom.kor = 88
print(tom.kor)

print()
oscar = My()
print(oscar.kor)