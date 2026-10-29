import os
import sys
import secrets
import hashlib
import math

size = 16

salt = os.urandom(size) # generated salt, passed to Salt.txt
iv = os.urandom(size) # generated IV, passed to IV.txt

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
    return y


# function to convert power to binary
def Binary(a):
    bin = ""
    while a > 0:
        bin = str(a % 2) + bin
        a //= 2
    return bin

Mod_expo(255, 65537, 0xbec6a8f10c13bfdcaf255ff5fef28f9c2349ade9e99a38841ad797d4dce43e7de880e2745093243fe86e56b347b2222ec5f75060630a2c153750c77a2c7e9e89fe21abdd852b59930a804cbbed11855ce9f16ffc5e1f85eab423b4521d4c03ff45814acaa69bfc65c162cf11f59f4abca489ff8ca1232d65a2c3a0516b5d0ced)