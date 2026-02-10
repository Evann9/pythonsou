from abc import *

class Employee(metaclass = ABCMeta):

    def __init__(self, irum, nai):
        self.irum = irum
        self.nai = nai

    @abstractmethod
    def pay(self):
        pass

    @abstractmethod
    def data_print(self):
        pass

    def irumnai_print(self):
        print('이름: ' + self.irum + '나이: ' + str(self.nai), end = ' ')

class Temporary(Employee):
    
    def __init__(self, irum, nai, lisu, lidang):
        Employee.__init__(self, irum, nai)
        self.lisu = lisu
        self.lidang = lidang
    
    def pay(self):
        return self.lisu * self.lidang  
    
    def data_print(self):
        super().irumnai_print()
        print(', 월급: ' + str(self.pay()))
        
t = Temporary('홍길동',25,20,15000)
t.data_print()

class Regular(Employee):

    def __init__(self, irum, nai, salary):
        Employee.__init__(self, irum, nai)
        self.salary = salary

    def pay(self):
        pass
    
    def data_print(self):
        super().irumnai_print()
        print(f', 급여액: {self.salary}')

r = Regular('한국인', 27, 3500000)
r.data_print()

# class Salesman(Regular):
#     def __init__(self, irum, nai salary, sales, commmission):
#         self.irum = irum
#         self.nai = nai
#         self.salary = salary
#         self.sales = sales
#         self.commission = commmission

#     def pay(self):
#         return self.salary + (self.sales * self.commission)
        

    
#     def data_print(self):
#         super().irumnai_print()
#         print(f', 수령액: {self.pay()}')

# s = Salesman('손오공', 29, 1200000, 5000000, 0.25)
# s.data_print()







