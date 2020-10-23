#!/usr/bin/env python3
from string import ascii_letters
from random import randint, choice
from signal import alarm
from math import factorial
import native

OPCODE = {i: op for i, op in enumerate(
    ['a1', 'plus', 'minus', 'bitAnd', 'bitOr',
     'bitXor', 'a7', 'rightShift', 'leftShift', 'oob',
     'a11', 'a12', 'a13', 'a14'])}

class TPU:
    def run(e, b, a=[]):
        alarm(5)
        e.i = 0                     # index
        e.c = 0                     # count
        e.r = [0] * 8               # calculation result
        e.a = bytes(a)              # bytes([a, b]), from random
        e.o = []                    # output
        e.m = bytearray(8)
        e.b = bytes.fromhex(b)      # bytes(hexval), from user
        e.h = len(e.b)
        e.z = True
        while e.i != e.h:
            getattr(e, OPCODE[e.b[e.i]])()
            e.i += 1
            e.c += 1
        alarm(0)
        print(e.m)
        return e.o

    def e(e):                       # ret input[++i]
        e.i += 1
        return e.b[e.i]

    def a1(e):
        e.r[e.e()] = e.e()
        print(e.r)

    def plus(e):
        if e.z:
            e.r[e.e()] = e.r[e.e()] + e.r[e.e()] & 0xFF
        else:
            e.r[e.e()] = native.plus(e.r[e.e()], e.r[e.e()])
        print(e.r)

    def minus(e):
        if e.z:
            e.r[e.e()] = e.r[e.e()] - e.r[e.e()] & 0xFF
        else:
            e.r[e.e()] = native.minus(e.r[e.e()], e.r[e.e()])
        print(e.r)

    def bitAnd(e):
        if e.z:
            e.r[e.e()] = e.r[e.e()] & e.r[e.e()]
        else:
            e.r[e.e()] = native.bitAnd(e.r[e.e()], e.r[e.e()])
        print(e.r)

    def bitOr(e):
        if e.z:
            e.r[e.e()] = e.r[e.e()] | e.r[e.e()]
        else:
            e.r[e.e()] = native.bitOr(e.r[e.e()], e.r[e.e()])
        print(e.r)

    def bitXor(e):
        if e.z:
            e.r[e.e()] = e.r[e.e()] ^ e.r[e.e()]
        else:
            e.r[e.e()] = native.bitXor(e.r[e.e()], e.r[e.e()])
        print(e.r)

    def a7(e):
        i = e.e()
        e.r[i] = -e.r[i]
        print(e.r)

    def rightShift(e):
        if e.z:
            e.r[e.e()] = e.r[e.e()] >> e.r[e.e()] & 0xFF
        else:
            e.r[e.e()] = native.rightShift(e.r[e.e()], e.r[e.e()])
        print(e.r)

    def leftShift(e):
        if e.z:
            e.r[e.e()] = e.r[e.e()] << e.r[e.e()] & 0xFF
        else:
            e.r[e.e()] = native.leftShift(e.r[e.e()], e.r[e.e()])
        print(e.r)

    def oob(e):
        m = e.e()           # b[1]
        s = e.e()           # b[2]
        d = e.e()           # b[3]
        if e.z:
            if m == 0:e.r[d] = e.a[s]
            if m == 1:e.r[d] = e.m[s]
            if m == 2:e.r[e.r[d]] = e.m[s]
            if m == 3:e.r[d] = e.m[e.r[s]]
            if m == 4:e.m[d] = e.r[s]
            if m == 5:e.m[e.r[d]] = e.r[s]
            if m == 6:e.m[d] = e.r[e.m[s]]
        else:
            native.oob(e, m, s, d)
        print(e.r)

    def a11(e):
        e.i = e.r[e.e()] - 1
        print(e.r)

    def a12(e):
        if e.r[e.e()]:e.e()
        else:e.i = e.r[e.e()] - 1
        print(e.r)

    def a13(e):
        e.o.append(e.r[e.e()])
        e.c = 0
        print(e.r)

    def a14(e):
        e.z ^= True
        print(e.r)

tpu = TPU()

"""
code = input('chall 1 : ')
for i in range(20):
    a = randint(0, 100)
    b = randint(0, 100)
    assert a + b == tpu.run(code, [a, b])[0]
"""

# code = input('chall 2 : ')
'''
code = '002003'
code+='000504'
code+='000105'
code+='09000001'
code+='03010302'
code+='07020402'
code+='08020502'
code += '02050202'
code += '08020402'
code += '010102000c00'

code += '002003'
code+='000504'
code+='000105'
code+='09000101'
code+='03010302'
code+='07020402'
code+='08020502'
code += '02050202'
code += '08020402'
code += '010102000c00'

code += '002003'
code+='000504'
code+='000105'
code+='09000201'
code+='03010302'
code+='07020402'
code+='08020502'
code += '02050202'
code += '08020402'
code += '010102000c00'

code += '002003'
code+='000504'
code+='000105'
code+='09000301'
code+='03010302'
code+='07020402'
code+='08020502'
code += '02050202'
code += '08020402'
code += '010102000c00'

code += '002003'
code+='000504'
code+='000105'
code+='09000401'
code+='03010302'
code+='07020402'
code+='08020502'
code += '02050202'
code += '08020402'
code += '010102000c00'

code += '002003'
code+='000504'
code+='000105'
code+='09000501'
code+='03010302'
code+='07020402'
code+='08020502'
code += '02050202'
code += '08020402'
code += '010102000c00'

code += '002003'
code+='000504'
code+='000105'
code+='09000601'
code+='03010302'
code+='07020402'
code+='08020502'
code += '02050202'
code += '08020402'
code += '010102000c00'

for i in range(1):
    # word = ''.join(choice(ascii_letters) for _ in range(7))
    word = 'abcdABD'
    print(''.join(chr(_) for _ in tpu.run(code, word.encode())))
    #assert word.swapcase() == ''.join(chr(_) for _ in tpu.run(code, word.encode()))

exit()
'''
chall3 = ""
chall3 += "09000601"
chall3 += "09000702"
chall3 += "000103"


#code = input('chall 3 : ')
for i in range(20):
    a = randint(0, 15)
    b = randint(0, 15)
    assert a * b == tpu.run(chall3, [a, b])[0]

exit()

code = input('chall 4 : ')
args = []
total = 0
for i in range(10):
    args.append(randint(0, 10))
    if total % 2:
        total = total + factorial(args[-1]) & 0xff
    else:
        total = total + sum(range(args[-1] + 1)) & 0xff
result = tpu.run(code, args)
if total == result[0]:
    print('good job. now, you can do anything!')
else:
    print('try harder!')
    exit(0)

while True:
    code = input('code : ')
    print(tpu.run(code))