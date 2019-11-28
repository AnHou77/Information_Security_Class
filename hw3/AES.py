import numpy as np
import sys
from PIL import Image
from Crypto.Cipher import AES

ppmPic = './myppm.ppm'
pic = sys.argv[1]
method = sys.argv[2]
func = sys.argv[3]
# image_input = Image.open('./penguin.png')
image_input = Image.open('./'+ pic)

img_byte = image_input.convert('RGB').tobytes()
size = image_input.size

def AES_encrypt(text):
    key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x00'
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(text)
    return ciphertext

def AES_decrypt(text):
    key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x00'
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(text)
    return plaintext
 
def ECB_encrypt(input_byte):
    encrypt_size = len(input_byte)
    encrypt_byte = b''
    for i in range(0, encrypt_size, 16):
        if(i + 16 <= encrypt_size):
            plaintext = input_byte[i:i+16]
        else:
            plaintext = input_byte[i:encrypt_size]
            for j in range(16 - len(plaintext)):
                plaintext += b'\x00'
        if i == 0:
            encrypt_byte = AES_encrypt(plaintext)
        else:
            encrypt_byte += AES_encrypt(plaintext)
    img = Image.frombytes("RGB",size,encrypt_byte)
    #img.save('./penguin_encrypt.png')
    img.save('./ECB_encrypt.png')
    return encrypt_byte

def ECB_decrypt(input_byte):
    decrypt_byte = b''
    decrypt_size = len(input_byte)

    for i in range(0, decrypt_size, 16):
        if(i + 16 <= decrypt_size):
            ciphertext = input_byte[i:i+16]
        else:
            ciphertext = input_byte[i:decrypt_size]
            for j in range(16 - len(ciphertext)):
                ciphertext += b'\x00'
        if i == 0:
            decrypt_byte = AES_decrypt(ciphertext)
        else:
            decrypt_byte += AES_decrypt(ciphertext)
    img = Image.frombytes("RGB",size,decrypt_byte)
    #img.save('./penguin_decrypt.png')
    img.save('./ECB_decrypt.png')
    return decrypt_byte

def xor(a,b):
    int_a = int.from_bytes(a,sys.byteorder)
    int_b = int.from_bytes(b,sys.byteorder)
    int_concat = int_a ^ int_b
    return int_concat.to_bytes(len(a),sys.byteorder)

def CBC_encrypt(input_byte):
    encrypt_size = len(input_byte)
    encrypt_byte = b''
    IV = b'\xFF\xFE\xFD\xFC\xFB\xFA\xF9\xF8\xF7\xF6\xF5\xF4\xF3\xF2\xF1\xF0'
    next_state = b''
    for i in range(0, encrypt_size, 16):
        if(i + 16 <= encrypt_size):
            plaintext = input_byte[i:i+16]
        else:
            plaintext = input_byte[i:encrypt_size]
            for j in range(16 - len(plaintext)):
                plaintext += b'\x00'
        if i == 0:
            plaintext = xor(plaintext, IV)
            encrypt_byte = AES_encrypt(plaintext)
            next_state = encrypt_byte
        else:
            plaintext = xor(plaintext, next_state)
            next_state = AES_encrypt(plaintext)
            encrypt_byte += next_state
    img = Image.frombytes("RGB",size,encrypt_byte)
    #img.save('./penguin_encrypt.png')
    img.save('./CBC_encrypt.png')
    return encrypt_byte

def CBC_decrypt(input_byte):
    decrypt_size = len(input_byte)
    decrypt_byte = b''
    IV = b'\xFF\xFE\xFD\xFC\xFB\xFA\xF9\xF8\xF7\xF6\xF5\xF4\xF3\xF2\xF1\xF0'
    next_state = b''
    for i in range(0, decrypt_size, 16):
        if(i + 16 <= decrypt_size):
            ciphertext = input_byte[i:i+16]
        else:
            ciphertext = input_byte[i:decrypt_size]
            for j in range(16 - len(ciphertext)):
                ciphertext += b'\x00'
        if i == 0:
            encrypt_byte = AES_decrypt(ciphertext)
            encrypt_byte = xor(encrypt_byte, IV)
            next_state = ciphertext
        else:
            encrypt = AES_decrypt(ciphertext)
            encrypt_byte += xor(encrypt, next_state)
            next_state = ciphertext
    img = Image.frombytes("RGB",size,encrypt_byte)
    #img.save('./penguin_encrypt.png')
    img.save('./CBC_decrypt.png')
    return encrypt_byte

if method == 'ECB':
    if func == 'e':
        ECB_encrypt(img_byte)
        print('Encrypt sucessful! (ECB)')
    elif func == 'd':
        ECB_decrypt(img_byte)
        print('Decrypt sucessful! (ECB)')
    else:
        print('Command is not avalible!')
elif method == 'CBC':
    if func == 'e':
        CBC_encrypt(img_byte)
        print('Encrypt sucessful! (CBC)')
    elif func == 'd':
        CBC_decrypt(img_byte)
        print('Decrypt sucessful! (CBC)')
    else:
        print('Command is not avalible!')
else:
    print('Command is not avalible!')
