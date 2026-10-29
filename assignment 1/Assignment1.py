import sys
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# function hashes input b, n times
def Hash_func(b, n):
    # data = hashlib.sha256() # produces 512 bit key, which causes error when encrypting in ECB mode
    data = hashlib.md5() # produces 256 bit key as required by project specifications
    for _ in range(n):
        data.update(b)
    return data.hexdigest()

#Right to left modular exponentiation function
def Right_left_Mod_expo(base, power, modulo):
    y = 1
    power = Binary(power)[::-1] # reveses the string for right-to left exponentiation
    for i in range(0, len(power)):
        # if the bit is set
        if power[i] == "1":
            y = (y * base) % modulo
        # the base is squared for all new bits
        base = (base ** 2) % modulo
    return y

# function to convert power to binary
def Binary(a):
    bin = ""
    while a > 0:
        bin = str(a % 2) + bin
        a //= 2
    return str(bin)

# function encrypts a given input using AES encryption and Key
def AES_encrypt(key, input):
   e = Cipher(algorithm=algorithms.AES(key), 
                    mode=modes.ECB(), 
                    backend=default_backend)
   encryptor = e.encryptor()
   em = encryptor.update(input)
   return em

# function will encrypt file bin using AES key and initial Vector
def CBC_Chain(plain_txt, key, in_vec):
    blocks = Split_Message(plain_txt)
    cipher_txt = b''

    #xor initial vector with the first block
    input = bytes( a ^ b for a, b in zip(in_vec, blocks[0]))

    #pass key and input to AES function
    cipher = AES_encrypt(key, input)

    #ciphertext becomes the current ciphertext + encryption of the previous block
    cipher_txt += cipher

    #for all remaining blocks
    for b in range(1, len(blocks)):

        # xor next block with the encryption of the previous block
        input = bytes( a ^ b for a, b in zip(cipher, blocks[b]))
        cipher = AES_encrypt(key, input)
        cipher_txt += cipher

    return cipher_txt
    
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
        # add padding if needed, then append to list blocks
        b = Pad_Block(message[i: i+ 16])
        blocks.append(b)
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

#---------------------------------------------------------

stdin = sys.argv[1]

plaintext = stdin.encode()

# read generated salt from salt.txt
salt_file = "Salt.txt"
with open(salt_file, mode="rb") as f:
    salt = f.read()

# read generated IV from IV.txt
iv_file = "IV.txt"
with open(iv_file, mode="rb") as f:
    init_vector = f.read()

#Read chosen password from Password_hex.txt
# password = b'd1edb39ab2b21d57'
pass_file = "Password_hex.txt"
with open(pass_file, mode="rb") as f:
    password = f.read()

#concatenate password || salt
p_con_s = b''.join([password, salt])

# hash p||s 250x using SHA-256 from hashlib
AES_key = Hash_func(p_con_s, 250).encode()

ciphertext = CBC_Chain(plaintext, AES_key, init_vector)
print(ciphertext)

pass_hex = "0x" + password.decode()
pass_hex = int(pass_hex, 16)


E = 65537

N='0xbec6a8f10c13bfdcaf255ff5fef28f9c2349ade9e99a38841ad797d4dce43e7de880e2745093243fe86e56b347b2222ec5f75060630a2c153750c77a2c7e9e89fe21abdd852b59930a804cbbed11855ce9f16ffc5e1f85eab423b4521d4c03ff45814acaa69bfc65c162cf11f59f4abca489ff8ca1232d65a2c3a0516b5d0ced'

N = int(N, 16)

