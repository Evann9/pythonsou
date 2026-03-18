class ElecProduct:
    volume = 0

    def volumeControl(self):
        # print(volume)
        pass

class ElctTv(ElecProduct):
    def volumeControl(self, volume):
        self.volume = volume
        print(f'Tv volume: {self.volume}')

class ElctRadio(ElecProduct):
    def volumeControl(self, volume):
        sori = volume
        self.sori = sori
        print(f'Radio volume: {self.sori}')

product = ElecProduct()
tv = ElctTv()
product = tv
product.volumeControl(100)
radio = ElctRadio()
product = radio
product.volumeControl(14)
