# Name: 柯元豪
# ID: B10615046
# Last Update: Dec 29, 2019
# Problem statement: Information_Security_Class_HW1

import sys
import numpy as np

Method = sys.argv[1]
key = sys.argv[2]
Plaintext = sys.argv[3]
# 字母字典 有的Function直接查表比較快
direction = np.array(
    ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
     'X', 'Y', 'Z'])


def caesar(text, k):
    ans = ""
    for i in text:
        find = np.where(direction == i)
        # 將此字母的index shift k
        search = int((find[0] + k) % 26)
        ans += direction[search]
    return ans


def play(text, k):
    # function一開始 先將text key中的'J'用'I'取代
    text.replace('J', 'I')
    k.replace('J', 'I')
    # 建一個5*5的矩陣
    matrix = np.array(np.random.rand(5, 5), dtype=str)
    # 判斷是否填入矩陣 若無 則不改變iterator
    flag = False
    r = 0
    c = 0
    # 先將 Key 不重複的字母放入矩陣
    for i in k:
        if not (matrix == i).any():
            matrix[r][c] = i
            flag = True
        if flag:
            if c != 4:
                c += 1
            else:
                c = 0
                r += 1
        flag = False
    # 後將剩餘字母依序填入矩陣
    for i in direction:
        if i != 'J':
            if not (matrix == i).any():
                matrix[r][c] = i
                flag = True
            if flag:
                if c != 4:
                    c += 1
                else:
                    c = 0
                    r += 1
            flag = False
    new = ''
    j = 0
    # 取出text中每個pair 放入新字串 若有重複則在中間插入'X' 若最後新產生的字串為基數 則在字串最後插入'X'
    for i in text:
        new += i
        j += 1
        if j % 2 == 0:
            if new[j - 1] == new[j - 2]:
                new = new[:j] + new[j - 1] + new[j + 1:]
                new = new[:(j - 1)] + 'X' + new[j:]
                j += 1
    if len(new) % 2 == 1:
        new += 'X'
    ans = ''
    # 找新字串中 每個pair 兩字母在矩陣中的位置
    # 在同一個row上 向右shift
    # 在同一個column上 向下shift
    # 其餘則用同一個row 和 另一方所在的column上的字取代
    for i in range(0, len(new), 2):
        a = [int(np.where(matrix == new[i])[0]), int(np.where(matrix == new[i])[1])]
        b = [int(np.where(matrix == new[i + 1])[0]), int(np.where(matrix == new[i + 1])[1])]
        if a[0] == b[0]:
            if a[1] != 4:
                ans += matrix[a[0]][a[1] + 1]
            else:
                ans += matrix[a[0]][0]
            if b[1] != 4:
                ans += matrix[b[0]][b[1] + 1]
            else:
                ans += matrix[b[0]][0]
        elif a[1] == b[1]:
            if a[0] != 4:
                ans += matrix[a[0] + 1][a[1]]
            else:
                ans += matrix[0][a[1]]
            if b[0] != 4:
                ans += matrix[b[0] + 1][b[1]]
            else:
                ans += matrix[0][b[1]]
        else:
            ans += matrix[a[0]][b[1]]
            ans += matrix[b[0]][a[1]]
    return ans


def auto(text, k):
    # 將Key和plaintext結合
    mix = k + text
    ans = ""
    # 將舊的plaintext與混和的字串做XOR 得出新字串
    for i in range(len(text)):
        search = int((np.where(direction == text[i]))[0] ^ np.where(direction == mix[i])[0])
        if search > 25:
            ans += chr(ord('Z') + (search - 25))
        else:
            ans += direction[search]
    return ans


def row(text, k):
    # 依key的長度建一個對應矩陣
    c = len(k)
    r = len(text)
    if r % c == 0:
        r = int(r / c)
    else:
        r = int(r / c) + 1
    matrix = np.array(np.random.rand(r, c), dtype=str)
    flag = False
    r = 0
    c = 0
    # 將plaintext依序填入表中
    for i in text:
        matrix[r][c] = i
        if c != (len(k) - 1):
            c += 1
            flag = False
        else:
            c = 0
            r += 1
            flag = True
    ans = ""
    if flag:
        r -= 1
    # 依key的順序取出column
    for i in range(len(k)):
        search = k.find(str(i + 1))
        for j in range(r + 1):
            ch = matrix[j][search]
            if len(ch) == 1:
                ans += ch
    return ans


def rail(text, k):
    # 建一個k維的籬笆
    fence = [[] for i in range(k)]
    j = 0
    flag = True
    # 依序接在對應的籬笆上
    # 判斷往下或往上走
    for i in range(len(text)):
        fence[j].append(text[i])
        if j == 0:
            flag = True
        elif j == (k - 1):
            flag = False
        if flag:
            j += 1
        else:
            j -= 1
    ans = ''
    # 從上而下取出籬笆上的字
    for i in fence:
        for j in i:
            ans += j
    return ans


cipher = ''
# 選擇對應function
if Method == 'caesar':
    cipher = caesar(str(Plaintext).upper(), int(key))
elif Method == 'playfair':
    cipher = play(str(Plaintext).upper(), str(key).upper())
elif Method == 'vernam':
    cipher = auto(str(Plaintext).upper(), str(key).upper())
elif Method == 'row':
    cipher = row(str(Plaintext).upper(), str(key))
elif Method == 'rail_fence':
    cipher = rail(str(Plaintext).upper(), int(key))
else:
    print('Please enter a legal function.')
print(cipher)
