# [PHP - Loose Comparison](https://www.root-me.org/en/Challenges/Web-Server/PHP-Loose-Comparison#validation_challenge)

## Solutions

Phân tích source code:

```php
if($s.$r == $h) {
            print "Well done! Here is your flag: ".$flag;
        }
```

- $s: user input
- $r: random number
- $h: md5(user input)

Khai thác loose comparison "0e..." == "0e...": (dấu ... bao gồm toàn số)

- Nhập $s = "0e"
- Tìm trên google một input mà khi cho vào md5 thì output có dạng "0e...":
  - md5('QNKCDZO') = '0e830400451993494058024219903391'
  - => Nhập $h = 'QNKCDZO'

Kết quả: `Well done! Here is your flag: F34R_Th3_L0o5e_C0mP4r15On`

Flag: `F34R_Th3_L0o5e_C0mP4r15On`

## References

- <https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Type%20Juggling/README.md>
