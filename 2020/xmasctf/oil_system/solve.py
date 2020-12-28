from pwn import *

HOST, PORT = 'host4.dreamhack.games', 8764

example = '''
2 24 12
5 26 -9
8 28 3
11 30 -15
14 32 33
17 34 16
20 36 30
23 38 67
100 100 100
100 100 100
100 100 100
100 100 100
100 100 100
'''

p = remote(HOST, PORT)
context.log_level = 'debug'

p.sendlineafter('> ', '2')
p.sendlineafter('Name : ', 'qeqadq')
p.sendlineafter('Code : ', example)

p.sendlineafter('> ', '3')
p.sendlineafter('> ', '4')

p.interactive()
