from pwn import *

DEBUG = True
if DEBUG:
    p = process(['./ld-2.32.so', './buffetvm', 'emoji'], env={'LD_PRELOAD':'./libc-2.32.so'})
else:
    p = remote('remote16.goatskin.kr', 63650)
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

gdb.attach(p)

p.interactive()