# [HTTP - POST](https://www.root-me.org/en/Challenges/Web-Server/HTTP-POST)

## Solutions

- Đọc html source code ta thấy:
  - Khi ấn vào nút `Give a try` thì javascript sẽ sinh ra một số ngẫu nhiên trong khoảng 1000001 và gửi giá trị này trong POST request body.
- Dùng burp suite thay đổi request body parameters:
  - `score=1000000&generate=Give+a+try%21`

Kết quả:

- Flag xuất hiện trong response: `H7tp_h4s_N0_s3Cr37S_F0r_y0U`
