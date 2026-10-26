import os
import sys
import secrets
import hashlib

size = 16

salt = os.urandom(size)
print(salt)