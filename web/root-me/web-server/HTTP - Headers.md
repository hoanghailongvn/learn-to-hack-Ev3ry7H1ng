# [HTTP - Headers](https://www.root-me.org/en/Challenges/Web-Server/HTTP-Headers)

## Solutions

- Dùng burp suite:
  - Quan sát http response thấy có header lạ `Header-RootMe-Admin: none`
  - Thêm header này vào request và send

Kết quả:

- password xuất hiện ở response: `HeadersMayBeUseful`
