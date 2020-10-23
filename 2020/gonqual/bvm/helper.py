# push 0, pop 1, read_io 2, write_io 3, alloc 4, free 5, 
# read_mem 6, write_mem 7, nop 8, halt 9, add 10, mul 11
inst = ['🍴', '🍿', '🍦', '🍨', '🥣', '😋', '🥢', '🥄', '🥤', '👋', '🍇', '🍉']
digit = ['🍞', '🥐', '🥖', '🥨', '🥯', '🥞', '🍪', '🍰', '🥧', '🍮']


def make10():
    return inst[0] + digit[1] + inst[0] + digit[9] + inst[10]

def makenum(n):
    s = str(n)
    res = ""
    res += inst[0]
    res += digit[int(s[0])]
    s = s[1:]
    for i in s:
        res += inst[0]
        res += make10()
        res += inst[11]
        res += inst[0]
        res += digit[int(i)]
        res += inst[10]
    return res

print(make10())
#print(makenum(1000)+inst[4]+digit[0])
#print(inst[0]+digit[3]+inst[0]+digit[2]+inst[0]+digit[1])
#print(inst[4]+digit[0]+inst[4]+digit[1]+inst[4]+digit[2])
#print(inst[7]+digit[0]+digit[0]+inst[7]+digit[1]+digit[0]+inst[7]+digit[2]+digit[0])

#for i in range(1, 8):
#    print(inst[5]+digit[i], end="")
print("")