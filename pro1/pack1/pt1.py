class coffee_bean:
    def __init__(self, name, roast, acidity):
        self.name = name
        self.roast = roast
        self.acidity = acidity

    def describe(self):
        print(f"이 원두는 '{self.name}'이며, {self.roast} 로스팅에 {self.acidity} 산미를 가졌습니다.")

bean1 = coffee_bean("pike_place", "middle", "low")
bean2 = coffee_bean('veranda', 'little', 'high')
bean3 = coffee_bean('Yirgacheffe', 'middle', 'middle')

my_beans = [bean1, bean2, bean3]

for bean in my_beans:
    bean.describe()