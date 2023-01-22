# [Javascript - Obfuscation 3](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Obfuscation-3)

## Solutions

- Sau khi ngồi phân tích hàm dechiffre(pass_enc) thì hàm này luôn trả về string `FAUX PASSWORD HAHA` với mọi `pass_enc`.
- Trong source code còn có một đoạn hex `\x35\x35\x2c\x35\x36\x2c\x35\x34\x2c\x37\x39\x2c\x31\x31\x35\x2c\x36\x39\x2c\x31\x31\x34\x2c\x31\x31\x36\x2c\x31\x30\x37\x2c\x34\x39\x2c\x35\x30`, thử decode đoạn này:

```bash
echo \x35\x35\x2c\x35\x36\x2c\x35\x34\x2c\x37\x39\x2c\x31\x31\x35\x2c\x36\x39\x2c\x31\x31\x34\x2c\x31\x31\x36\x2c\x31\x30\x37\x2c\x34\x39\x2c\x35\x30 | xxd -r -p
=> 55,56,54,79,115,69,114,116,107,49,50

echo $(printf '\\x%x' $(echo 55,56,54,79,115,69,114,116,107,49,50 | sed 's/,/ /g'))
=> 786OsErtk12
```

- Nhập `786OsErtk12` vào ô đáp án thấy ok.
