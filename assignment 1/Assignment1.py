import os
import sys
import secrets
import hashlib

size = 16

salt = os.urandom(size) # generated salt, passed to Salt.txt
iv = os.urandom(size) # generated IV, passed to IV.txt

# modular exponentiation function
def Mod_expo(num, power, modulus):
    print(f"number -> {num} || power -> {power} || modulus -> {modulus}")


# function to convert power to binary
def Binary(a):
    bin = ""
    while a > 0:
        bin = str(a % 2) + bin
        a //= 2
    print(f"dec -> {a} || bin -> {bin}")

Binary(39)
Mod_expo(123, 5, 511) # test, expected value 359
Mod_expo(2, 37, 77) # test, expected value 51
Mod_expo(51, 13, 77) # test, expected value 2