class Car:         # 클래스는 대문자로 시작
    handle = 1        # 멤버 앞 + , - 
    speed = 0

    def __init__(self, name, speed):
        self.name = name    # 현재 객체의 name에게 name(지역변수) 인자값 치환
        self.speed = speed

    def showData(self):
        km = "킬로미터"
        msg = '속도:' + str(self.speed) + km
        return msg
    
    def printHandle(self):
        return self.handle      # 클래스 내에 변수를 불러올때 self가 꼭 있어야함.

print(Car.handle)  # 원형(prototype) 클래스의 멤버 호출
car1 = Car('tom', 10)   # 생성자 호출 후 객체 생성 (인스턴스화)
print('car1 객체 주소:' , car1)
print('car1:', car1.name,' ', car1.speed, car1.handle)
car1.color = '파랑'
print('car1.color: ', car1.color)

car2 = Car('john', 20)
print('car2 객체 주소:' , car2)
print('car2:',car2.name,' ', car2.speed, car2.handle)
# print(Car.color, ' ', car2.color)  # color는 Car1만 가지고 있는 고유한 특성임
print(Car, car1, car2)
print(id(Car), id(car1), id(car2))
print(car1.__dict__)        # __dict__: 각 객체의 특성을 확인할 수 있는 메소드
print(car2.__dict__)

print()
print('----메소드-----------')
print('car1 speed : ' ,car1.showData())  # ()안에 Car1이 자동으로 들어감
print('car2 speed : ' ,car2.showData())  # ()안에 Car2이 자동으로 들어감
car1.speed = 80
car2.speed = 110
print('car1 speed : ' ,car1.showData())  # ()안에 Car1이 자동으로 들어감
print('car2 speed : ' ,car2.showData())  # ()안에 Car2이 자동으로 들어감

print('car1 handle : ' ,car1.printHandle())  # ()안에 Car1이 자동으로 들어감
print('car2 handle : ' ,car2.printHandle())  # ()안에 Car2이 자동으로 들어감