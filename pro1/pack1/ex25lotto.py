import random

class LottoBall:
    def __init__(self, num):
        self.num = num

class LottoMachine:
    def __init__(self):
        self.ballList = []
        for i in range(1,46):
            self.ballList.append(LottoBall(i))   # 클래스의 포함관계

    def selectBalls(self):
        # for a in range(45):
        #     print(self.ballList[a].num, end= ' ')
        # print('-------')
        random.shuffle(self.ballList)   # 번호 섞기
        # for a in range(45):
        #     print(self.ballList[a].num, end= ' ')
        return self.ballList[0:6]  #슬라이싱

class LottoUI:
    def __init__(self):
        self.machine = LottoMachine()  # 포함관계

    def playLotto(self):
        input('로또를 시작하려면 enter키를 누르세요')
        selectedBalls = self.machine.selectBalls()
        for ball in selectedBalls:
            print('%d'%(ball.num))

if __name__ == '__main__':
#     # machine = LottoMachine()
#     # print(machine.selectBalls())

    # lot = LottoUI()
    # lot.playLotto()
    LottoUI().playLotto()

