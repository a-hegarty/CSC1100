import os
import sys
import secrets
import hashlib
import math

size = 16

salt = os.urandom(size) # generated salt, passed to Salt.txt
iv = os.urandom(size) # generated IV, passed to IV.txt

pass_file = 'Password.txt'
with open(pass_file) as f:
    password = f.read()

password = password.encode() # encode defaults to UTF-8

# hash p||s 250x using SHA-256 from hashlib
#AES_key = hashlib.sha256([p_con_s], usedforsecurity=True)

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

print(password)