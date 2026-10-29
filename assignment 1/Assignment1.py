import sys
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# function hashes input b, n times
def Hash_func(b, n):

    # data = hashlib.sha256() # produces 512 bit key, which causes error when encrypting in ECB mode
    data = hashlib.md5() # produces 256 bit key as required by project specifications & ECB mode limitations
    for _ in range(n):
        data.update(b)
    return data.hexdigest()

#Right to left modular exponentiation function
def Right_left_Mod_expo(base, power, modulo):
    y = 1

    # convert exponent to Binary
    power = Binary(power)
    for i in range(0, len(power)):

        # if the bit is set
        if power[i] == "1":
            y = (y * base) % modulo

        # the base is squared for all new bits after checlking if set
        base = (base ** 2) % modulo
    return y

# function to convert power to binary
def Binary(a):
    bin = ""
    while a > 0:
        bin = str(a % 2) + bin
        a //= 2
    return bin

# function encrypts a given input using AES encryption and Key
# modified from python Cryptography library documentation
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

    # if no padding is necessary
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
# password = d1edb39ab2b21d57
pass_file = "Password_hex.txt"
with open(pass_file, mode="rb") as f:
    password = f.read()

#concatenate password || salt
p_con_s = b''.join([password, salt])

# hash p||s 250x using SHA-256 from hashlib
AES_key = Hash_func(p_con_s, 250).encode()

ciphertext = CBC_Chain(plaintext, AES_key, init_vector)
print(ciphertext)