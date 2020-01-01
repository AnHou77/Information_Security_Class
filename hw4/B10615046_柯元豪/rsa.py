# B10615046 柯元豪

import numpy as np
import random
import sys

# Extended gcd 目的為找出 a mod b 的反元素
def gcd_ext(a, b):
    if b == 0:
        return 1, 0
    else:
        xx, yy = gcd_ext(b, a % b)
        x = yy
        y = xx - (a // b) * yy
        return x, y

# 產生 n bits 大數
def proBin(n):
    prime = []
    prime.append('1')
    for i in range(n - 2):
        c = random.choice(['0', '1'])
        prime.append(c)
    prime.append('1')
    p = int(''.join(prime), 2)
    return p


# 產生 n bits 大質數
def proPrime(n):
# 通過檢測符合的就return 不符的就重新產生大數
    p = proBin(n)
    while (True):
        if (MillerRabin(p)):
            return p
        p = proBin(n)


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

# 中國餘式定理
def CRT(p, q, d, c):
    # xp
    xdp = d % (p - 1)
    xp = square_multiply(xdp, c, p)
    # xq
    xdq = d % (q - 1)
    xq = square_multiply(xdq, c, q)
    # t = pinv mod q
    t = gcd_ext(p,q)[0]
    # u = (xq - xp)t mod q
    u = ((xq - xp) * t) % q
    # x = xp + pu
    x = xp + p * u
    return x

# 產生public key與private key
def proKey(p, q):
    n = p * q
    phy = (p - 1) * (q - 1)  # Euler 函數
    e = 65537

    # d * e ≡ 1 mod phy(n)
    d = gcd_ext(e, phy)[0]

    # 回傳public key與private key
    # (n, e) & (d)
    return n, e, d

# 用傳入的plaintext 同時做加解密
def RSA(bits, plaintext):
    # initial
    p = proPrime(bits)
    q = proPrime(bits)
    n, e, d = proKey(p,q)
    print('\n -----------------------initial----------------------- \n')
    print('p:', p)
    print('\nq:', q)
    print('\ne:', e)
    print('\nd:', d)

    # Encrypt 因e較小 使用square and multiply來做
    ciphertext = square_multiply(e, plaintext, n)
    
    # Decrypt 因d極大 因此透過CRT來做解密
    plaintext = CRT(p, q, d, ciphertext)
    
    return ciphertext , plaintext

# main function

bit = int(sys.argv[1])
inputtext = sys.argv[2]

# 將輸入的str轉成int 因funtion接的型態為int
inputtext = bytes(inputtext, encoding='utf8')
length = len(inputtext)
plaintext_int = int.from_bytes(inputtext, byteorder='big')
# 做 RSA 加解密 得ciphertext與plaintext
ciphertext, plaintext = RSA(bit, plaintext_int)

# 由於RSA做完回傳的型態也是int 因此要將解密結果轉回str 才能確認是否與輸入的plaintext相同
plaintext = plaintext.to_bytes(length, byteorder="big")
plaintext = str(plaintext, encoding='utf-8')    

print('\n -----------------------result----------------------- \n')
print('Encrypt -> Ciphertext: ', ciphertext)
print('\nDecrypt -> Plaintext: ', plaintext)
