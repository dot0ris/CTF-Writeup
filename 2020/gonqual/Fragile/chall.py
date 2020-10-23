#!/usr/bin/env python3
from random import choice
from config import keys
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

SIZE = 32

with open('pt', 'rb') as f:
    pt = pad(f.read(), SIZE)

ct = b''
chunks = [pt[SIZE * i:SIZE * (i + 1)] for i in range(len(pt) // SIZE)]
for chunk in chunks:
    c1 = DES.new(choice(keys), DES.MODE_ECB)
    c2 = DES.new(choice(keys), DES.MODE_ECB)
    ct += c2.encrypt(c1.encrypt(chunk))

with open('ct', 'wb') as f:
    f.write(ct)