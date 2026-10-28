import os
import sys
import secrets
import hashlib
import math

# function hashes input b, n times
def Hash_func(b, n):
    for _ in range(n):
        b = hashlib.sha256(b).hexdigest().encode()
    return b
    
# modular exponentiation function via GeeksforGeeks
def Mod_expo(base, power, modulus):
    # power = Binary(power)
    y = 1
    while power >= 1:
        if power % 2 == 1: # if exponent is odd
            y = (y * base) % modulus
            power -= 1
        else: # if exponent is even
            base = (base * base) % modulus
            power //= 2
    # print(f"number -> {base} || power -> {power} || modulus -> {modulus} || result -> {y}")
    return y


# function to convert power to binary
def Binary(a):
    bin = ""
    while a > 0:
        bin = str(a % 2) + bin
        a //= 2
    return bin

# function will encrypt file bin using AES key and initial Vector
def CBC_Encrypt(plain_txt, key, in_vec):
    blocks = [Pad_Block(plain_txt)]
    cipher = ""

# function will split message into blocks
# first blocks will be 16 bytes long
# next block is any remaining bytes to be padded
# final block is the length of the message in hexadecimal
def Split_Message(message):
    blocks = [] 

    #length of the block is multiplied by 8 to give the lenght of the message in bits
    #length will be in bytes otherwise
    length_block = hex(len(message) * 8).encode()
    for i in range(0, len(message), 16):
        blocks.append(message[i: i + 16])
    blocks.append(length_block)
    return blocks

def Pad_Block(message):
    # 128 bits is 16 bytes
    # hence mod 16
    pad_len = 16 - len(message) % 16
    if pad_len % 16 == 0:
        return message
    else:
        padded_data = (b'\\0x00' * pad_len)
        return message + padded_data

# read generated salt from salt.txt
salt_file = "Salt.txt"
with open(salt_file, mode="rb") as f:
    salt = f.read()

# read generated IV from IV.txt
iv_file = "IV.txt"
with open(iv_file, mode="rb") as f:
    iv = f.read()

#Read chosen password from Password.txt
pass_file = 'Password.txt'
with open(pass_file, mode="rb") as f:
    password = f.read()

#concatenate password || salt
p_con_s = b''.join([password, salt])

# hash p||s 250x using SHA-256 from hashlib
AES_key = Hash_func(p_con_s, 250)

test_message = b"12345678901234567890"

blocks = Split_Message(test_message)
print(blocks)