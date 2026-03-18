/*
gcc flag-shop.c -o flag-shop -D_FORTIFY_SOURCE=0

balance=0x0000555555558010
name=0x7fffffffdcd1
hex(name-balance)
'0x2aaaaaaa5cc1'
*/

#include <stdio.h>
#include <stdlib.h>

int balance = 100;

int main()
{   
    char name[32];
    char voucher[32];

    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);

    printf("Welcome to the flag shop! Flags are currently on sale for only $13371337.");

    // get name
    printf("\n> Enter your name (max length 31): ");
    scanf("%31s",name);

    // welcome user
    printf("\nWelcome, ");
    printf(name);
    printf(". Your balance is currently $%d.", balance);

    // get voucher code
    printf("\n> Please input a voucher code (max length 31): ");
    scanf("%31s",voucher);

    // return voucher error (TODO: add voucher code validation)
    printf("[ERROR] Invalid voucher code: ");
    printf(voucher);
    
    // check if balance is sufficient to purchase the flag
    if (balance >= 13371337) {
        printf("\n\nCongratulations, here's the flag: ");
        system("cat flag.txt");
    } else {
        printf("\n\nUnfortunately, you are too broke to purchase the flag.");
    }

    return 0;
}
