'''
alist = [('a', 0), ('b', 1), ('c', 2), ('d', 3), 
         ('e', 4), ('f', 5), ('g', 6), ('h', 7), 
         ('i', 8), ('j', 9), ('k', 10), ('l', 11), 
         ('m', 12), ('n', 13), ('o', 14), ('p', 15)]
'''

def ctoh(str):
    assert(len(str) == 16)
    return [ord(i) for i in str]

def shuf(csrc, cmask):
    src = ctoh(csrc)
    mask = ctoh(cmask)

    for i in range(16):
        if(mask[i] & 0x80):
            src[i] = 0
        else:
            idx = mask[i] & 0xf
            src[i] = src[idx]
    
    return src

def lz(c):
    h = ord(c)
    cnt = 8
    mask = 0x80
    for i in range(8):
        if(h & mask):
            break
        cnt += 1
        mask >>= 1
    return cnt

def pc(c):
    h = ord(c)
    cnt = 0
    mask = 1
    for i in range(8):
        if(h & mask):
            cnt += 1
        mask <<= 1
    return cnt

def second(c):
    return 

src = r"GoN{thisissample"
mask = "abcdefghijklmnop"
test = ["hpoldjnepjodecfd", "ejpopnblfdpeijdp", "cjobcjpdpnamjdbe", "fepefmmpjoefmpde"]

'''
for i in test:
    for j in i:
        print(hex(ord(j)-97), end=" ")
    print()
'''
'''
for i in test:
    for j in i:
        for k in range(3, 8):
            print(chr(0x10*k+(ord(j)-97)), end=" ")
        print()
    print("-----------------------")
'''
#print(hex(lz("G")), hex(pc("G")))

#ss = "E0 FF FB F8 CB FE F5 F9 F3 E7 CA E1 FC FD E6 CB".split(" ")
#ss = "F6 FD F8 F4 E4 EC CC F6 FB F8 E6 F8 FA F7 F4 E2".split(" ")
#ss = "F6 F0 CA E7 F1 F9 FA CB FF FB E7 F1 F8 CB E0 E0".split(" ")
ss = "FB E3 C9 F9 F5 FF FD F8 F3 CA E0 FC F1 E5 F0 E9".split(" ")
zz, cc = "t", 15
print(chr(int(ss[cc], 16) ^ (lz(zz) * 16) ^ pc(zz)))

#print([hex(i) for i in shuf(mask, src)])
#print([chr(i) for i in shuf(src, mask)])

GoN{SIMD_instruction_makes_this_binary_complicated_tell_intel_stop_making_these}
