# 메소드 오버라이딩(= 재정의)
# 부모애서 정의된 메소드를 자식이 동일명의 메소드로 내용만 변경해 사용
# 부모 메소드의 기능을 대체 하는 새로운 기능
# 동작의 구체화(공통 틀은 부모가, 실제 행동은 자식) 실현
# polymorphism(다형성) - 같은 메소드이나 객체에 따라 다른 기능을 수행
# 확장, 유지보수에 도움 - 부모 코드는 유지한 채 자식 코드만 변경

class Parent:
    def printData(self):
        pass

class Child1(Parent):
    def abc():
        print('Chlid1 고유 메소드')

    def printData(self):   # 메소드 오버라이딩
        a = 5 + 6
        #...
        print('Child1에서 printData 재정의')

class Child2(Parent):
    def printData(self):   # 메소드 오버라이딩
        print('Chlid2에서 printData override')
        msg = '부모와 동일 메소드 명이나 내용은 다르다'
        print(msg)

c1 = Child1()
c1.printData()
print()
c2 = Child2()
c2.printData()
print('\n ----다형성---')     # 권장 
par = Parent()
par = c1
par.printData()
print()
par = c2
par.printData()
print('--------------')    # 권장 X
imsi = c1
imsi.printData()
imsi = c2
imsi.printData()


