# [SQL Truncation](https://www.root-me.org/en/Challenges/Web-Server/SQL-Truncation)

## Solutions

Source code trang register có phần html comment:

```sql
CREATE TABLE IF NOT EXISTS user(   
 id INT NOT NULL AUTO_INCREMENT,
    login VARCHAR(12),
    password CHAR(32),
    PRIMARY KEY (id));
```

=> Độ dài username là 12.

Đăng ký với credential `admin       a:long1234` => ok, vì ký tự a bị cắt bớt.

Đăng nhập admin với mật khẩu đã viết ở trên => Flag: `J41m3Qu4nD54Tr0nc`
