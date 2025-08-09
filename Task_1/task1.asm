org 100h                 ; .COM starts at 100h

section .data
a     db 5
b     db 7
c     db 3
msg   db 'Result: $'

section .text
start:
    ; AL = b - c + a
    mov al, [b]
    sub al, [c]
    add al, [a]

    ; print "Result: "
    mov ah, 09h
    mov dx, msg
    int 21h

    ; print one-digit result (0..9)
    add al, '0'
    mov dl, al
    mov ah, 02h
    int 21h

    ; exit to DOS
    mov ah, 4Ch
    xor al, al
    int 21h
