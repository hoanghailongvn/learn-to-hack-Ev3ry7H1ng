# [JWT attacks](https://portswigger.net/web-security/jwt)

## Lab

- apprentice:
  - [1. JWT authentication bypass via unverified signature](./lab/1.%20JWT%20authentication%20bypass%20via%20unverified%20signat.md)
  - [2. JWT authentication bypass via flawed signature](./lab/2.%20JWT%20authentication%20bypass%20via%20flawed%20signature.md)
- practitioner:
  - [3. JWT authentication bypass via weak signing key](./lab/3.%20JWT%20authentication%20bypass%20via%20weak%20signing%20key.md)
  - [4. JWT authentication bypass via jwk header inject](./lab/4.%20JWT%20authentication%20bypass%20via%20jwk%20header%20inject.md)
  - [5. JWT authentication bypass via jku header inject](./lab/5.%20JWT%20authentication%20bypass%20via%20jku%20header%20inject.md)
  - [6. JWT authentication bypass via kid header path traversal](./lab/6.%20JWT%20authentication%20bypass%20via%20kid%20header%20path%20traversal.md)
- expert:
  - [7. JWT authentication bypass via algorithm confusion](./lab/7.%20JWT%20authentication%20bypass%20via%20algorithm%20confusion.md)
  - [8. JWT authentication bypass via algorithm confusion with no exposed key](./lab/8.%20JWT%20authentication%20bypass%20via%20algorithm%20confusion%20with%20no%20exposed%20key.md)

## Detect JWT

use burpsuite's extension called jwt editor, in HTTP history, any request that contains jwt will be green:
![detect.png](./img/detect.png)

## Exploit

1. server do not verify signature:

    - catch a request to account page contains jwt
    - use burp's jwt editor
    - directly edit jwt's body part
    - send to server

    - [lab](./lab/1.%20JWT%20authentication%20bypass%20via%20unverified%20signat.md)

2. server accept none alg:

    - catch a request to account page contains jwt
    - use burp's jwt editor
    - choose "attack" -> "none" Signing algorithm
    - send to server

    - [lab](./lab/2.%20JWT%20authentication%20bypass%20via%20flawed%20signature.md)

3. weak symmetric key:
    - catch a jwt
    - use hashcat to bruteforce:

    ```bash
    ┌──(kali㉿kali)-[~/Desktop/exam-preparation]
    └─$ hashcat -a 0 -m 16500 eyJraWQiOiJiNWM2MmM5ZS05YWZkLTQ0ODItODkwYy0zZTM2Y2YyNmUyOTAiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsInN1YiI6IndpZW5lciIsImV4cCI6MTY3MzMzMTcwNH0.uogTd4jaZZ5TxcovgRcegXA2gq208kLTgXxv_Gh3DZ0 ./jwt/jwt.secrets.list 

    ┌──(kali㉿kali)-[~/Desktop/exam-preparation]
    └─$ hashcat -a 0 -m 16500 eyJraWQiOiJiNWM2MmM5ZS05YWZkLTQ0ODItODkwYy0zZTM2Y2YyNmUyOTAiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsInN1YiI6IndpZW5lciIsImV4cCI6MTY3MzMzMTcwNH0.uogTd4jaZZ5TxcovgRcegXA2gq208kLTgXxv_Gh3DZ0 ./jwt/jwt.secrets.list --show
    eyJraWQiOiJiNWM2MmM5ZS05YWZkLTQ0ODItODkwYy0zZTM2Y2YyNmUyOTAiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsInN1YiI6IndpZW5lciIsImV4cCI6MTY3MzMzMTcwNH0.uogTd4jaZZ5TxcovgRcegXA2gq208kLTgXxv_Gh3DZ0:secret1
    ```

    - base64 encode key
    - generate new symmetric key using jwt editor, replace "k" with b64decoded key
    - edit jwt's body, sign with new generated key
    - send

    - [lab](./lab/3.%20JWT%20authentication%20bypass%20via%20weak%20signing%20key.md)

4. server trusted on the "jwk" header, which contains key and can be added or modified on client-side:
    - catch a request to account page contains jwt
    - use burp's jwt editor
    - generate new RSA key
    - copy key to header:

    ```json
    {
        "kid": "2b02f383-bc32-45ff-8067-8079b70b90e8",
        "typ": "JWT",
        "alg": "RS256",
        "jwk": {
            "p": "-m6TGEZy1OEuMUc9D8ws1FTtAyaD2OVpGBDauMOIVmbRKFkkaHfAR-qk7A1szo-VtW4mZ3vkD-9bGRNQ7ttEFhaPz1iArG0gveJTcdliLoaGxL9aVEWlXF6wJtKcn9HPaPxQzMWmrEOr1g4yb8yUmrWZeCiGATSYgjKvVEwULuE",
            ...
            "e": "AQAB",
            "kid": "2b02f383-bc32-45ff-8067-8079b70b90e8",
            ...
        }
    }
    ```

    - edit jwt's body
    - sign jwt, choose "update alg, type, kid" to automatically update the kid in the header to be the same as the kid in the newly created rsa key.
    - send

    - [lab](./lab/4.%20JWT%20authentication%20bypass%20via%20jwk%20header%20inject.md)

5. server trusted on the "jwu" header, which contains url to key and can be added or modified on client-side:
    - catch a request to account page contains jwt
    - generate new rsa key using burp's jwt editor
    - save newly created rsa key to exploit server (portswigger lab) or pipedream
    - update "jku":

    ```json
    {
        "jku": "https://exploit-0ad2000e040deae3c19c3e2201550079.exploit-server.net/exploit",
        "kid": "5bf6df89-b3ec-45f5-817c-44136956a075",
        "typ": "JWT",
        "alg": "RS256"
    }
    ```

    - update jwt's body
    - sign jwt, choose "update alg, type, kid" to automatically update the kid in the header to be the same as the kid in the newly created rsa key.
    - send

    - [lab](./lab/5.%20JWT%20authentication%20bypass%20via%20jku%20header%20inject.md)

6. "kid" is vulnerable to path traversal
    - catch a request to account page contains jwt
    - generate new symmetric key using burp's jwt editor, replace "k" with base64_encode('\x00') = "AA=="
    - edit jwt's body
    - try different "kid":
      - "../../../../dev/null"
      - "../../../../../dev/null"
      - ...
    - sign
    - send

7. algorithm confusion with exposed key:
    - get public rsa key from `/jwks.json` or `/.well-known/jwks.json`
    - generate new rsa key, paste the JWK obtained from server, save.
    - select copy public key as pem
    - then base64 encode
    - generate new symmetric key, replace "k" with base64 encoded value
    - edit jwt's body
    - change "alg" from RS256 to HS256
    - sign with symmetric key
    - send

    - [lab](./lab/7.%20JWT%20authentication%20bypass%20via%20algorithm%20confusion.md)

8. algorithm confusion with no exposed key:
    - try to get 2 different jwt
    - we can calculate public key:

    ```bash
    docker run --rm -it portswigger/sig2n <token1> <token2>
    ```

    - same as 7
    - [lab](./lab/8.%20JWT%20authentication%20bypass%20via%20algorithm%20confusion%20with%20no%20exposed%20key.md)
