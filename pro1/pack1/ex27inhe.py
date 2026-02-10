# 상속 : 자원의 재활용울 목적으로 특정 클래스의 멤버(속성과 필드)를 가져다 쓰는것
# 코드 재사용
# 확장성 - 기존 클래스에 새 기능을 추가한 새로운 클래스 생성
# 구조적 설계 - 공통개념은 부모 클래스, 구체적 내용은 자식 클래스에서 구현
# 다형성 구사 - 메소드 오버라이딩

class Animal:   # 동물들이 가져야할 공통 속성과 행위 선언
    age = 1
    def __init__(self):
        print('Animal 생성자')
    def move(self):
        print('움직이는 생물')

class Dog:
    def __init__(self):
        print('Dog 생성자')
    
    def my(self):
        print('댕댕이라고 해요')

class Dog(Animal):      # 상속 - Animal :부모, 조상, super, parent, Dog: 자식, 자손, 파생, sub, child
    def __init__(self):
        print('Dog 생성자')
    
    def my(self):
        print('댕댕이라고 해요')


dog1 = Dog()
dog1.my()
dog1.move()
print('age: ', dog1.age)
print()
dog2 = Dog()
dog2.my()
dog2.move()
print()

class Horse(Animal):     # 상속
    pass

horse1  = Horse() 
horse1.move()


