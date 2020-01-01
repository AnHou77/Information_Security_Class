# B10615046 柯元豪

import numpy as np
import random
import sys
from hashlib import sha1

# Extended gcd 目的為找出 a mod b 的反元素
def gcd_ext(a, b):
    if b == 0:
        return 1, 0
    else:
        xx, yy = gcd_ext(b, a % b)
        x = yy
        y = xx - (a // b) * yy
        return x, y


# 產生 n bits 質數
def proPrime(n):
# 通過檢測符合的就return 不符的就重新產生大數
    p = random.getrandbits(n)
    while (True):
        if (MillerRabin(p)):
            return p
        p = random.getrandbits(n)

# 檢測傳入的質數是真質數還是偽質數
def MillerRabin(p):
    a = random.randrange(2, p - 1)
    if ((p - 1) % 2 != 0):
        return False
    d = p - 1
    cnt = 0
    while (d % 2) == 0:
        d = d >> 1
        cnt += 1
    x = pow(a, d, p)
    if (x == 1 or x == p - 1):
        return True
    for i in range(cnt - 1):
        x = (x * x) % p
        if x == 1:
            return True
        elif x == p - 1:
            return False
    return False

# 透過降冪來加速mod
def square_multiply(exp,x,n):
    h = bin(exp)[2:].zfill(exp.bit_length())
    y = 1
    length = len(h)
    for i in range(length):
        y = (y ** 2) % n
        if h[i] == '1':
            y = (y * x) % n
    return y

def gen_key():
    q = proPrime(160)
    k = random.getrandbits(864)   #1024-160, (p-1) / q
    p = 0
    while True:
        p = q * k + 1
        if(MillerRabin(p)):
            break;
        k = random.getrandbits(864)
    h = 2
    alpha = square_multiply(k,h,p)
    d = random.randint(1,p - 1)
    beta = square_multiply(d,alpha,p)
    return((p,q,alpha,beta),d)

def gen_sign(publickey,privatekey,message):
    p = publickey[0]
    q = publickey[1]
    alpha = publickey[2]
    beta = publickey[3]
    d = privatekey
    ke = random.randint(1,p - 1)
    ke_inv = gcd_ext(ke,q)[0] # ke mod q的inv 用於求s
    r = square_multiply(ke,alpha,p) % q
    h = sha1()
    h.update(message.encode("utf-8"))
    h = int(h.hexdigest(), 16)
    s = ((h + d * r) * ke_inv) % q
    return r,s

def verify(r,s,publickey,message):
    p = publickey[0]
    q = publickey[1]
    alpha = publickey[2]
    beta = publickey[3]
    h = sha1()
    h.update(message.encode("utf-8"))
    h = int(h.hexdigest(), 16)
    w = gcd_ext(s,q)[0] # s mod q inv
    u1 = (w * h) % q
    u2 = (w * r) % q
    v = (square_multiply(u1,alpha,p) * square_multiply(u2,beta,p) % p) % q
    if v == r:
        return True
    return False

if __name__ == "__main__":
    mode = sys.argv[1]
    message = sys.argv[2]
    if mode == "-fullstep":
        # 因為全部寫一起比較輕鬆 只需看結果的話用這個操作應該足夠了
        g = gen_key()
        pubkey,prikey = g[0],g[1]
        r,s = gen_sign(pubkey,prikey,message)
        v = verify(r,s,pubkey,message)
        print("signature is: ", v)


    # 因為各個function都有獨立寫 所以之後可以用下方的code改成讀檔的方式來實作可互動的DSA


    # elif mode == "-keygen":
    #     # 用來產生公鑰和私鑰 這裡沒做讀檔的方式 因此只是簡單的呈現key
    #     g = gen_key()
    #     pubkey,prikey = g[0],g[1]
    #     print("p: ",pubkey[0])
    #     print("q: ",pubkey[1])
    #     print("alpha: ",pubkey[2])
    #     print("beta: ",pubkey[3])
    #     print("d: ",prikey)
    # elif mode == "-sign":
    #     # 因為沒有做成讀檔的方式 直接讀輸入的str還要把它轉bit code太長了
    #     # 所以這個mode暫不使用 用fullstep的mode取代
    #     pubkey = []
    #     pubkey.append(sys.argv[3])
    #     pubkey.append(sys.argv[4])
    #     pubkey.append(sys.argv[5])
    #     pubkey.append(sys.argv[6])
    #     prikey = sys.argv[7]
    #     r,s = gen_sign(pubkey,prikey,message)
    #     print("r: ", r)
    #     print("s: ", s)
