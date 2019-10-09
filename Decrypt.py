import sys
import numpy as np
import math


#  B10615047 陳哲緯


class Decrypt:
    def __init__(self, way, key, text):
        self.way = way  # 方式
        self.key = key
        self.text = text  # Ciphertext
        self.result = ''  # OUTPUT result

    def run(self):
        if self.way == 'caesar':
            self.text = self.text.upper()
            for i in self.text:
                shift = (ord(i) - ord('A') - int(self.key) + 26) % 26  # 減掉key value 換成Plaintext
                ori = ord('A')
                ori += int(shift)
                self.result += chr(ori)
        if self.way == 'playfair':
            text = self.text.upper()
            self.key = self.key.upper()
            alp = "A B C D E F G H I K L M N O P Q R S T U V W X Y Z"
            alp = alp.split()
            mx = []  # 字符矩陣
            key = ''
            # 替換 J>I
            for i in self.key:
                if i == 'J':
                    key += 'I'
                else:
                    key += i
            kvalue = sorted(set(key), key=key.index)  # 刪除重複元素
            for i in kvalue:
                mx.append(i)  # key 轉換為 list
            for i in mx:
                alp = [a for a in alp if (a != i)]  # 建立字符矩陣
            mx += alp
            mx = np.array(mx)
            mx = mx.reshape(5, 5)  # 建立字符矩陣
            for i in range(0, len(text), 2):
                if text[i] == text[i + 1]:  # 如果字符重複相連 加入X
                    text = text[:i + 1] + 'X' + text[i + 1:]
            for i in range(0, len(text), 2):
                if text[i] == 'J':  # J 視為 I
                    left = np.where(mx == 'I')
                else:
                    left = np.where(mx == text[i])
                if i + 1 == len(text):
                    # 如果是奇數長度 補上X
                    right = np.where(mx == 'X')
                else:
                    if text[i + 1] == 'J':
                        # J視為I
                        left = np.where(mx == 'I')
                    else:
                        right = np.where(mx == text[i + 1])
                lrow = int(left[0])
                lcol = int(left[1])
                rrow = int(right[0])
                rcol = int(right[1])
                if lrow == rrow:
                    self.result += mx[lrow][int((lcol + 5 - 1) % 5)]
                    self.result += mx[rrow][int((rcol + 5 - 1) % 5)]
                elif left[1] == right[1]:
                    li = (lrow - 1 + 5) % 5
                    ri = (rrow - 1 + 5) % 5
                    self.result += mx[int(li)][lcol]
                    self.result += mx[int(ri)][rcol]
                else:
                    self.result += mx[lrow][rcol]
                    self.result += mx[rrow][lcol]

        if self.way == 'vernam':
            klen = len(self.key)
            text = self.text.upper()
            for i in range(0, len(text)):
                #  print(i, self.key[i], text[i], chr(ord('A') + (ord(self.key[i]) ^ ord(text[i]))))
                fix = (ord(self.key[i]) - ord('A')) ^ (ord(text[i]) - ord('A'))
                self.key += chr(ord('A') + fix)
            self.result += self.key[klen:]

        if self.way == 'row':
            # 計算出最大子字串長度
            klen = len(self.text) / len(self.key)
            klen = math.ceil(klen)
            fixn = len(self.text) % len(self.key)
            colsizedic = {}
            coltext = []
            # 建立 index對應子字串長度
            for i in range(0, len(self.key)):
                if i < fixn:
                    colsizedic[int(self.key[i])] = klen
                else:
                    colsizedic[int(self.key[i])] = klen - 1
            # 把密文分解成子字串
            for i in range(0, len(self.key)):
                coltext.append(self.text[0:int(colsizedic[int(i + 1)])])
                self.text = self.text[colsizedic[int(i + 1)]:]
            idx = 0
            # 還原原文
            for i in range(0, klen):
                for j in self.key:
                    if idx < colsizedic[int(j)]:
                        self.result += coltext[int(j) - 1][idx]
                    else:
                        continue
                idx += 1
        if self.way == 'rail_fence':
            text = self.text.upper()
            rowsize = int(self.key)
            colsize = len(self.text)
            fillmatrix = np.zeros((rowsize, colsize))
            i = 0
            j = 0
            sign = 0  # 0 down 1 up
            # 標記要填入字元的地方
            while i < rowsize and j < colsize:
                fillmatrix[i][j] = 1
                if i == (rowsize - 1):
                    sign = 1
                elif i == 0:
                    sign = 0
                if sign == 0:
                    i += 1
                    j += 1
                else:
                    i -= 1
                    j += 1
            # 填入字元
            for r in range(0, rowsize):
                for c in range(0, colsize):
                    if fillmatrix[r][c]:
                        fillmatrix[r][c] = ord(text[0])
                        text = text[1:]
            i = 0
            j = 0
            # 解密
            while i < rowsize and j < colsize:
                self.result += chr(int(fillmatrix[i][j]))
                if i == (rowsize - 1):
                    sign = 1
                elif i == 0:
                    sign = 0
                if sign == 0:
                    i += 1
                    j += 1
                else:
                    i -= 1
                    j += 1

    def output(self):
        print(self.result.lower())


if len(sys.argv) == 4:
    x = Decrypt(sys.argv[1], sys.argv[2], sys.argv[3])
    x.run()
    x.output()
