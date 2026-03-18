# 여러개의 부품 객체를 조립해서 완성 차 생성
# 클래스의 포함 관계 사용 (자원의 재활용)
# 다른 클래스(객체)를 마치 자신의 멤버처럼 선언하고 사용  # 객체 = 개체 = object

from ex23pohamhandle import PohamHandle

class PohamCar:
    ternShowMessage = '정지'
    
    def __init__(self, ownerName):
        # ownerName = self.ownerName  -> 절대 금지
        self.ownerName = ownerName
        self.handle = PohamHandle()   # 클래스의 포함관계

    def turnHandle(self, q):
        if q > 0:
            self.ternShowMessage = self.handle.right_turn(q)    # 클래스의 포함관계
        elif q < 0:
            self.ternShowMessage = self.handle.left_turn(q)    # 클래스의 포함관계
        elif q == 0:
            self.ternShowMessage = '직진'

if __name__ == '__main__':
    tom = PohamCar('미스터 톰')
    tom.turnHandle(10)
    print(tom.ownerName + '의 회전량은 ' + tom.ternShowMessage + ' ' + str(tom.handle.quantity))


    john = PohamCar('미스터 존')
    john.turnHandle(-20)
    print(john.ownerName + '의 회전량은 ' + john.ternShowMessage + ' ' + str(john.handle.quantity))

    john.turnHandle(0)
    print(john.ownerName + '의 회전량은 ' + john.ternShowMessage + ' ' + str(john.handle.quantity))