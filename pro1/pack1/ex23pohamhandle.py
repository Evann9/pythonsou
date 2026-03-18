# 어딘가에서 필요한 부품 핸들 클래스 작성
class PohamHandle:
    quantity = 0 # 핸들 회전량     -> 멤버필드 없으면 각각의 값을 가짐

    def left_turn(self, quantity):
        self.quantity = quantity
        return '좌회전'
    
    def right_turn(self, quantity):
        self.quantity = quantity
        return '우회전'
    