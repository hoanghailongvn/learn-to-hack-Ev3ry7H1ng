# [HTTP Host header attacks](https://portswigger.net/web-security/host-header)

## Labs

- apprentice:
  - [1. Basic password reset poisoning](./lab/1.%20Basic%20password%20reset%20poisoning.md)
  - [2. Host header authentication bypass](./lab/2.%20Host%20header%20authentication%20bypass.md)

- practitioner:
  - [3. Web cache poisoning via ambiguous requests](./lab/3.%20Web%20cache%20poisoning%20via%20ambiguous%20requests.md)
  - [4. Routing-based SSRF](./lab/4.%20Routing-based%20SSRF.md)

## Checklist

1. arbitrary `Host` header:

    - exploit-server
    - localhost
    - collaborator

2. duplicate `Host` header:

    - frontend: upper server
    - backend: below server
    - or vice versa

3. flawed request parsing:

    ```http
    GET https://id.web-security-academy.net HTTP/1.1
    Host: localhost:6566
    ```

4. connection state attack:
create a group:

    - first request:

    ```http
    GET / HTTP/1.1
    Host: id.web-security-academy.net
    Connection: keep-alive
    ```

    - second request:

    ```http
    GET / HTTP/1.1
    Host: localhost:6566
    Connection: keep-alive
    ```

    - send group (single connection)

5. use the Param Miner extension's "Guess headers" function to automatically probe for supported headers

    - X-Forwarded-Host
    - X-Host
    - X-Forwarded-Server
    - X-HTTP-Host-Override
    - Forwarded
