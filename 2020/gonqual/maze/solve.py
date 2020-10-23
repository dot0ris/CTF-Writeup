from pwn import *

DEBUG = True
if DEBUG:
    p = process(['./maze'])
else:
    p = remote('REMOTE_ADDR', 1337)
context.log_level = 'debug'

p.interactive()