# **net2**
## Source code
```
#include "../common/common.c"

#define NAME "net2"
#define UID 997
#define GID 997
#define PORT 2997

void run()
{
  unsigned int quad[4];
  int i;
  unsigned int result, wanted;

  result = 0;
  for(i = 0; i < 4; i++) {
      quad[i] = random();
      result += quad[i];

      if(write(0, &(quad[i]), sizeof(result)) != sizeof(result)) {
          errx(1, ":(\n");
      }
  }

  if(read(0, &wanted, sizeof(result)) != sizeof(result)) {
      errx(1, ":<\n");
  }


  if(result == wanted) {
      printf("you added them correctly\n");
  } else {
      printf("sorry, try again. invalid\n");
  }
}

int main(int argc, char **argv, char **envp)
{
  int fd;
  char *username;

  /* Run the process as a daemon */
  background_process(NAME, UID, GID); 
  
  /* Wait for socket activity and return */
  fd = serve_forever(PORT);

  /* Set the client socket to STDIN, STDOUT, and STDERR */
  set_io(fd);

  /* Don't do this :> */
  srandom(time(NULL));

  run();
}
```

## Tools
- gdb
- python
- netcat

## Phân tích source code
run(): 
  - Tạo 4 số ngẫu nhiên
  - Tương tự như net1, server sẽ gửi từng số cho client nhưng là từng bytes và ghép lại thành string.
  - Nhận một số từ client và so sánh với tổng 4 số ngẫu nhiên trên.

mục tiêu:
  - Gửi cho server số = tổng 4 số ngẫu nhiên

## Final
Viết python script:
```
#!/usr/bin/env python

import socket
import struct

if __name__ == "__main__":
        s = socket.socket()
        s.connect(("127.0.0.1", 2997))

        result = 0
        for i in range(4):
                data = s.recv(1024)
                temp = "0x"
                for c in reversed(data):
                        temp += c.encode('hex')
                print "temp:", temp

                result += int(temp, 0)
        
        # Gửi cho server tổng 4 số nhận được nhưng dưới dạng hexa little endian
        s.send(str(struct.pack("I", result)))

        data = s.recv(1024)
        print(data)

        s.close()
~                 
```

Kết quả:
```
user@protostar:/tmp$ python ./script.py 
temp: 0x21e84225
temp: 0x021d39fa
temp: 0x57d3cd06
temp: 0x7fafaa81
you added them correctly
```

# References