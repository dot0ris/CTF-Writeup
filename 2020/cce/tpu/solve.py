from pwn import *

DEBUG = False
if DEBUG:
    p = process([''])
else:
    p = remote('52.79.129.93', 1337)
context.log_level = 'debug'

chall1 = "09000001"
chall1 += "09000102"
chall1 += "01010200"
chall1 += "0c00"

code = '002003'
code+='000504'
code+='000105'
code+='09000001'
code+='03010302'
code+='07020402'
code+='08020502'
code += '02050202'
code += '08020402'
code += '010102000c00'

code += '002003'
code+='000504'
code+='000105'
code+='09000101'
code+='03010302'
code+='07020402'
code+='08020502'
code += '02050202'
code += '08020402'
code += '010102000c00'

code += '002003'
code+='000504'
code+='000105'
code+='09000201'
code+='03010302'
code+='07020402'
code+='08020502'
code += '02050202'
code += '08020402'
code += '010102000c00'

code += '002003'
code+='000504'
code+='000105'
code+='09000301'
code+='03010302'
code+='07020402'
code+='08020502'
code += '02050202'
code += '08020402'
code += '010102000c00'

code += '002003'
code+='000504'
code+='000105'
code+='09000401'
code+='03010302'
code+='07020402'
code+='08020502'
code += '02050202'
code += '08020402'
code += '010102000c00'

code += '002003'
code+='000504'
code+='000105'
code+='09000501'
code+='03010302'
code+='07020402'
code+='08020502'
code += '02050202'
code += '08020402'
code += '010102000c00'

code += '002003'
code+='000504'
code+='000105'
code+='09000601'
code+='03010302'
code+='07020402'
code+='08020502'
code += '02050202'
code += '08020402'
code += '010102000c00'

p.sendlineafter("chall 1 : ", chall1)
p.sendlineafter("chall 2 : ", code)


p.interactive()