# [JWT - Revoked token](https://www.root-me.org/en/Challenges/Web-Server/JWT-Revoked-token)

## Solutions

- Đọc code và test thử thấy thấy:
  - đăng nhập thành công sẽ cho một cái jwt:
    - jwt được đưa vào blacklist trước khi gửi cho mình
    - có hsd là 3 phút sau đó
    - khi hết hsd thì jwt.decode() và @jwt_required đều thất bại, token được cho ra khỏi blacklist
  - vào trang admin, thử gửi 3 loại jwt trong header:
    - jwt mới nhận được: thông báo revoked
    - jwt sau 3 phút: thông báo expired
    - jwt sai: thông báo invalid

- Bruteforce để tìm secret không được

- Chú ý dòng 62.:

```python
access_token = request.headers.get("Authorization").split()[1]
```

- việc kiểm tra token có ở trong `blacklist` chỉ xảy ra với phần tử `[1]` của header `Authorization`
- mà ta có thể gửi nhiều token cùng 1 dòng header `Authorization` ([Stack over flow](https://stackoverflow.com/questions/29282578/multiple-http-authorization-headers))

- => Tạo một HTTP request với header `Authorization: token1, token2`, trong đó:
  - `token1` là một token đã expired: để không còn ở trong `blacklist`
  - `token2` là một token hợp lệ vẫn còn hsd: để vượt qua kiểm tra token `@jwt_required`

Kết quả:

```json
{"Congratzzzz!!!_flag:":"Do_n0t_r3v0ke_3nc0d3dTokenz_Mam3ne-Us3_th3_JTI_f1eld"}
```

## Questions

- Vì sao trong flag lại nhắc đến JTI?
  - Search google lời giải bài này, mọi người làm cách khác: [link](https://thanhlocpanda.wordpress.com/2021/03/01/jwt-revoke-explotation-rootme-challenge/)

## References

- <https://stackoverflow.com/questions/29282578/multiple-http-authorization-headers>
