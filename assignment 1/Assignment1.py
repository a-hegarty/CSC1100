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
    print(f"number -> {base} || power -> {power} || modulus -> {modulus} || result -> {y}")


# function to convert power to binary
def Binary(a):
    bin = ""
    while a > 0:
        bin = str(a % 2) + bin
        a //= 2
    return bin

Mod_expo(123, 5, 511) # test, expected value 359
Mod_expo(2, 37, 77) # test, expected value 51
Mod_expo(51, 13, 77) # test, expected value 2