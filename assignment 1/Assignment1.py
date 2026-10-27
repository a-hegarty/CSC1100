import os
import sys
import secrets
import hashlib
import math

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


# read generated salt from salt.txt
salt_file = "Salt.txt"
with open(salt_file, mode="rb") as f:
    salt = f.read()

# read generated IV from IV.txt
iv_file = "IV.txt"
with open(iv_file, mode="rb") as f:
    iv = f.read()

#Read chosen password from Password.txt
#And encode with UTF-8
pass_file = 'Password.txt'
with open(pass_file, mode="rb") as f:
    password = f.read()

#concatenate password || salt
p_con_s = b''.join([password, salt])

# hash p||s 250x using SHA-256 from hashlib
AES_key = Hash_func(p_con_s, 250)


print(AES_key)