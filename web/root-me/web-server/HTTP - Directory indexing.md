# [HTTP - Directory indexing](https://www.root-me.org/en/Challenges/Web-Server/HTTP-Directory-indexing)

## Solutions

- Đọc HTML source code thấy dòng comment `<!-- include("admin/pass.html") -->`
- Truy cập vào directory `admin/`, ta thấy được cây thư mục
- Tìm tòi trong cây thư mục này, ta thấy mật khẩu lưu ở `http://challenge01.root-me.org/web-serveur/ch4/admin/backup/admin.txt`: `LINUX`

## References

- <https://www.ibm.com/docs/en/snips/4.6.0?topic=categories-directory-indexing-attacks>
