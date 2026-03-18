# class 다중상속

class Animal:
    def move(self):
        pass

class Dog(Animal):
    def name(self):
        print('개')

    def move(self):
        pass

class Cat(Animal):
    def name(self):
        print('고양이')

    def move(self):
        pass

class Wolf(Dog, Cat):
    pass

class Fox(Cat, Dog):

    def move(self):
        pass

    def foxMethod(self):
        print('Fox 고유 메소드')
