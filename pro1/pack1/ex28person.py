# 상속

class Person:
    say = '난 사람이야'    # 접근권한 : public
    nai = '20'
    __msg = 'good : private 멤버'  #  접근권한 : private

    def __init__(self,nai):
        print('Person 생성자')
        self.nai = nai
    
    def printInfo(self):      # 접근권한 : public
        print(f'나이: {self.nai}, 이야기: {self.say}')

    def helloMethod(self):
        print('안녕')
        print('hello: ', self.say, self.nai, self.__msg)
        
print(Person.say, Person.nai)
# Person.printInfo()
per = Person('25')
per.printInfo()
per.helloMethod()

print('---' * 10)
class Employee(Person):
    subject = '근로자'    # Employee 만 가지는 특성
    say = '일하는 동물'   # Employee 만 가지는 특성

    def __init__(self):
        print('Employee 생성자')

    def printInfo(self):      # 접근권한 : public
        print('Employee 클래스의 printInfo 호출됨')
    
    def ePrintInfo(self):
        print(self.subject, self.say, self.nai)    # 클래스 변수를 찾고 없으면 부모 클래스로 감
        # print(self.__msg)    # __msg : private 멤버 => Person에서만 유효
        self.helloMethod()
        self.printInfo()
        print(super().say)  # super(). : 부모 클래스의 정보를 가져온다. (이전 클래스만 가능)
        super().printInfo()

emp = Employee()
print(emp.subject,emp.nai, emp.say)
print()
emp.ePrintInfo()

print('---' * 10)
class Worker(Person):
    def __init__(self, nai):
        print('Worker 생성자')
        super().__init__(nai)    # 부모클래스의 생성자를 호출함
    
    def wPrintInfo(self):
        print('Worker - wPrintInfo 처리')
        # self.printInfo()
        super().printInfo()

wor = Worker('30')
print(wor.say, wor.nai)
wor.wPrintInfo()

print('===' * 10)
class Programmer(Worker):
    def __init__(self, nai):
        print('Programmer 생성자')
        # super().__init__(nai)       # Bound call
        Worker.__init__(self, nai)   # UnBound call

    def pPrintInfo(self):
        print('Programmer - pPrintInfo 처리')

    def wPrintInfo(self):  # 부모 메소드와 동일 메소드 선언(상속에서만 나온다)
        print('Programmer에서 overriding')

pro = Programmer('35')
print(pro.say, pro.nai)
pro.pPrintInfo()
pro.wPrintInfo()

print('\n클래스 타입 확인')
a = 3; print(type(a))
print(type(pro))
print(type(wor))
print(Person.__bases__)
print(Employee.__bases__)
print(Worker.__bases__)
print(Programmer.__bases__)

