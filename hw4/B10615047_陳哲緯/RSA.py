# b10615047 陳哲緯
import random
import sys


# 算最大公因
def gcd(num1, num2):
    if num1 < num2:
        num1, num2 = num2, num1
    else:
        pass
    while num2 != 0:
        num1, num2 = num2, num1 % num2
    return num1


# 測試質數
def rabin_miller(num):
    s = num - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1

    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            x = 0
            while v != (num - 1):
                if x == t - 1:
                    return False
                else:
                    x = x + 1
                    v = (v ** 2) % num
    return True


# 產生n bit 大數
def proBin(w):  # w表示產生位數
    rb = []
    rb.append('1')  # 最高位定為1
    for i in range(w - 2):
        c = random.choice(['0', '1'])
        rb.append(c)
    rb.append('1')  # 最低位定為1
    res = int(''.join(rb), 2)
    return res


# 產生N bit質數
def proN(n):
    while 1:
        p = proBin(n)
        for i in range(50):
            if rabin_miller(p):
                return p
            else:
                p += 2


# 化簡次方來快速mod
# x^n mod P =  (x*x)^(n/2) mod P = ((x*x)mod P)^(n/2) mod P
def SquareMod(x, n, p):
    if n == 0:
        return 1
    res = SquareMod((x * x) % p, n >> 1, p)
    if n & 1 != 0:
        res = (res * x) % p
    return res


# 中國餘式定理
def ChinaRemainderMod(base, exp, M, lexp, rexp):
    # m1
    lx = SquareMod(base, exp, lexp)
    a1 = lx
    M1 = M // lexp
    y1 = SquareMod(M1, lexp - 2, lexp)

    # m2
    rx = SquareMod(base, exp, rexp)
    a2 = rx
    M2 = M // rexp
    y2 = SquareMod(M2, rexp - 2, rexp)

    return (a1 * M1 * y1 + a2 * M2 * y2) % M


# 找出在a mod b 下的mod反元素
def ext_gcd(a, b):
    if b == 0:
        return 1, 0
    else:
        x1, y1 = ext_gcd(b, a % b)
        x = y1
        y = x1 - a // b * y1
        return x, y


def gen_key(p, q):
    n = p * q
    fy = (p - 1) * (q - 1)  # 歐拉函數
    e = 65537

    # 計算d
    x, y = ext_gcd(e, fy)
    while x < 0:
        x += fy
    d = x
    # pubkey & prikey
    return (n, e), (n, d)


class RSA:
    def __init__(self, nb):
        self.p = 0
        self.q = 0
        self.bit = nb

    def generate(self):
        # 產生亂數p q
        self.p = proN(self.bit)
        self.q = proN(self.bit)
        while self.p == self.q:
            self.p = proN(self.bit)
        # 產生公鑰私鑰
        a, b = gen_key(self.p, self.q)
        # 寫入檔案
        print(a[0], '\n', a[1], '\n', self.p, '\n', self.q, file=open('Private_Key15047.txt', 'w'))
        print(b[0], '\n', b[1], file=open('Public_Key15047.txt', 'w'))

    def encrypt(self, p):
        pub = []
        # 讀公鑰
        with open('Public_Key15047.txt', 'r') as f:
            pub.append(int(f.readline()))
            pub.append(int(f.readline()))
        return SquareMod(p, pub[1], pub[0])

    def decrypt(self, c):
        pri = []
        # 讀私鑰
        with open('Private_key15047.txt', 'r') as f:
            pri.append(int(f.readline()))
            pri.append(int(f.readline()))
            pri.append(int(f.readline()))
            pri.append(int(f.readline()))
        return ChinaRemainderMod(c, pri[1], pri[0], pri[2], pri[3])


# 設定系統最大遞迴次數
sys.setrecursionlimit(1000000)

if len(sys.argv) == 3:
    # 初始化: RSA.py {n bit} i
    if sys.argv[2] == 'i':
        rsa = RSA(int(sys.argv[1]))
        rsa.generate()
        print('initial state: ', sys.argv[1], 'bit finished')
    # 解碼: RSA.py {cypherfilename} d
    elif sys.argv[2] == 'd':
        rsa = RSA(0)
        cypherFile = sys.argv[1]
        p = ''
        with open(cypherFile, 'r') as f:
            i = f.readline()
            while i:
                p += chr(rsa.decrypt(int(i)))
                i = f.readline()
        print(p)
# 加密: RSA.py {message} {cypherflename} e
elif len(sys.argv) == 4 and sys.argv[3] == 'e':
    rsa = RSA(0)
    ptxt = sys.argv[1]
    pfile = sys.argv[2]
    with open(pfile, 'w') as f:
        for i in ptxt:
            c = rsa.encrypt(ord(i))
            f.write(str(c) + '\n')
    print('encrypt :', ptxt, ' to ', pfile, 'finished')
