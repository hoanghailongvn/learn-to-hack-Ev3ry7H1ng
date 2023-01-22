# [HTTP - IP restriction bypass](https://www.root-me.org/en/Challenges/Web-Server/HTTP-IP-restriction-bypass)

## Solutions

- Sử dụng burpsuite để thay đổi http request:
  - Thêm header `X-Forwarded-For: 192.168.1.2`
- Response có chứa password
