from pwn import *

DEBUG = True
if DEBUG:
    p = process(['./buffetvm', 'emoji'])
else:
    p = remote('remote16.goatskin.kr', 63650)
context.log_level = 'debug'

p.interactive()