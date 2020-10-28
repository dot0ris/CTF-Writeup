from pwn import *

DEBUG = True
if DEBUG:
    p = process(['./sparc-1'])
else:
    p = remote('flu.xxx', 2020)
context.log_level = 'debug'

addr = int(p.recvline(), 16)

p.interactive()