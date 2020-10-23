from pwn import *
import hashlib

#context.log_level = "DEBUG"

HASH_DIFFICULTY = 22
CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def PoW(nonce, diff):
    while True:
        fail = False
        s = "".join(random.sample(CHARSET, 10))
        h = hashlib.md5()
        h.update((s + nonce).encode())
        md = h.digest()

        for i in range(HASH_DIFFICULTY):
            byte_idx = i // 8
            bit_idx = 7 - i % 8

            if ord(md[byte_idx]) & (1 << bit_idx):
                fail = True
                break

        if fail : continue
        else : return s

# base address of code section
CODE_BASE = 0x400000

def code_patch(bin_list, patch_byte, addr):
    for i in range(len(patch_byte)):
        bin_list[addr - CODE_BASE + i] = patch_byte[i]

IP = "127.0.0.1"
PORT = 13202

with open("./mms", "rb") as f:
    orig_bin = f.read()

bin_byte_list = list(orig_bin)

#this patch first byte of main into ret :)
code_patch(bin_byte_list, "\xc3", 0x40119B)

with open("./mms_patch", "wb") as f:
    f.write("".join(bin_byte_list))

p = remote(IP, PORT)

#solve PoW
l = p.recvline()
nonce, diff = l.split()[11], int(l.split()[14])
p.sendline(PoW(nonce, diff))
p.recvline()

#send patched binary
p.recvuntil(":")
p.send("".join(bin_byte_list))

p.interactive()



