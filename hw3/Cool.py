from PIL import Image
from Crypto.Cipher import AES
import os
import sys


# transform ppm image to BYTES unit
def bytes_from_file(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break


# PNG > PNG
class CoolTransform:
    def __init__(self, inp, result, key, IV):

        # 先把輸入圖片轉成ppm
        self.inputImage = Image.open('./' + inp)  # img (source)
        self.inputImage.save('./ppmtemp.ppm')
        # 分割成BYTE
        self.ppmArray = [i for i in bytes_from_file('./ppmtemp.ppm')]
        os.remove('./ppmtemp.ppm')
        # 設定參數
        self.key = bytes.fromhex(key)
        self.IV = bytes.fromhex(IV)
        self.result = result
        # ppm標頭 單位 byte
        self.ppmHeader = []
        # 1 block = 16 byte
        self.blockArray = []
        self.resultBlockArray = []
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def coolpreProcess(self):
        i = 0;
        # 分離 header & pixel
        for b in range(0, len(self.ppmArray)):
            if self.ppmArray[b] == 10:
                i += 1
            if i == 3:
                self.ppmHeader = self.ppmArray[0:b + 1]
                self.ppmArray = self.ppmArray[b + 1:-1]
                break
        # 補byte
        while len(self.ppmArray) % 16 != 0:
            self.ppmArray.append(0)
        # 分割成block
        for i in range(0, len(self.ppmArray), 16):
            self.blockArray.append(bytes(self.ppmArray[i: i + 16]))

    def coolEncode(self):
        self.coolpreProcess()

        # XOR WITH 10101010 OR 01010101
        for i in range(0, len(self.blockArray)):
            fixed = bytes.fromhex('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            if i % 2 != 0:
                fixed = bytes.fromhex('55555555555555555555555555555555')
            self.blockArray[i] = self.bytexor(self.blockArray[i], fixed)
        _IV = self.IV
        for i in range(0, len(self.blockArray)):
            self.resultBlockArray.append(self.bytexor(_IV, self.blockArray[i]))
            self.resultBlockArray[i] = self.cipher.encrypt(self.resultBlockArray[i])
            _IV = self.resultBlockArray[i][8:16] + self.resultBlockArray[i][0:8]
        with open('./tempResult.ppm', "wb") as f:
            f.write(bytes(self.ppmHeader))
            for i in self.resultBlockArray:
                f.write(i)
        tp = Image.open('./tempResult.ppm')  # img (source)
        tp.save('./' + self.result, 'png')
        os.remove('./tempResult.ppm')

    def coolDecode(self):
        self.coolpreProcess()
        _IV = self.IV
        for i in range(0, len(self.blockArray)):
            fixed = bytes.fromhex('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            if i % 2 != 0:
                fixed = bytes.fromhex('55555555555555555555555555555555')
            self.resultBlockArray.append(self.cipher.decrypt(self.blockArray[i]))
            if i > 0:
                _IV = self.blockArray[i - 1][8:16] + self.blockArray[i - 1][0:8]
            self.resultBlockArray[i] = self.bytexor(self.resultBlockArray[i], _IV)
            self.resultBlockArray[i] = self.bytexor(self.resultBlockArray[i], fixed)
        with open('./tempResult.ppm', "wb") as f:
            f.write(bytes(self.ppmHeader))
            for i in self.resultBlockArray:
                f.write(i)
        tp = Image.open('./tempResult.ppm')  # img (source)
        tp.save('./' + self.result, 'png')
        os.remove('./tempResult.ppm')

    def bytexor(self, a, b):
        return bytes([_a ^ _b for _a, _b in zip(a, b)])


ikey = '96c0832dab2b35ee5bf265ce403fc073'
iIV = '29b4937dfe7d83e08f117c5259a9c972'

if len(sys.argv) == 4:
    x = CoolTransform(sys.argv[1], sys.argv[2], ikey, iIV)
    # decode
    print(sys.argv[1],' >>> ', sys.argv[2])
    if (sys.argv[3] == 'd'):
        print('decode..')
        x.coolDecode()
    # encode
    elif (sys.argv[3] == 'e'):
        print('encode..')
        x.coolEncode()
