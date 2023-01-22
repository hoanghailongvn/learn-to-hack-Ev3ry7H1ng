# [HTTP - Improper redirect](https://www.root-me.org/en/Challenges/Web-Server/HTTP-Improper-redirect)

## Solutions

- Truy cập vào `index.php`, sử dụng burp suite để đọc response:
  - Nhận được một response 302, tuy nhiên ở phần body vẫn có nội dung của file `index.php`
  - Trong đó xuất hiện flag: `ExecutionAfterRedirectIsBad`

## References

- <https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20Exploiting%20Improper%20Redirection%20in%20PHP%20Web%20Applications.pdf?_gl=1>
