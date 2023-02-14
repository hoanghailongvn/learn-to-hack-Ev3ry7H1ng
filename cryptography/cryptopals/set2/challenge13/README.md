# **[set 2 - challenge 13](https://cryptopals.com/sets/2/challenges/13): ECB cut-and-paste**

Write a k=v parsing routine, as if for a structured cookie. The routine should take:

```url
foo=bar&baz=qux&zap=zazzle
```

... and produce:

```map
{
  foo: 'bar',
  baz: 'qux',
  zap: 'zazzle'
}
```

(you know, the object; I don't care if you convert it to JSON).

Now write a function that encodes a user profile in that format, given an email address. You should have something like:

```python
profile_for("foo@bar.com")
```

... and it should produce:

```map
{
  email: 'foo@bar.com',
  uid: 10,
  role: 'user'
}
```

... encoded as:

```url
email=foo@bar.com&uid=10&role=user
```

Your "profile_for" function should not allow encoding metacharacters (& and =). Eat them, quote them, whatever you want to do, but don't let people set their email address to "foo@bar.com&role=admin".

Now, two more easy functions. Generate a random AES key, then:

A. Encrypt the encoded user profile under the key; "provide" that to the "attacker".
B. Decrypt the encoded user profile and parse it.
Using only the user input to profile_for() (as an oracle to generate "valid" ciphertexts) and the ciphertexts themselves, make a role=admin profile.

## Analysis

The above operations are similar to how a server manages and manipulates user cookies:

1. the first time the client connects to the server, send an email address
2. server generate cookie: `email=foo@bar.com&uid=10&role=user`
3. server encrypt this cookie string and send it back to the client
4. every time the client comes back, it sends that encrypted cookie with every request. Depends on that, the server can authenticate the client

Our mission is login to server as admin

## server function

- cookie2dict: extract cookie to dict
  - lambda generate anonymous functions: [document](https://julien.danjou.info/python-functional-programming-lambda/)
  - map() execute lambda function with each item.

    ```python
    def cookie2dict(s: str) -> dict:
        return dict(map(lambda x: x.split('='), s.strip('&').split('&')))
    ```

- dict2cookie:

    ```python
    def dict2cookie(d: dict) -> str:
        return '&'.join(map('='.join, d.items()))
    ```

- profile_for:
  - 1. generate dict
  - 2. from dict encode to cookie

    ```python
    def profile_for(email: str):
        return dict2cookie({
            'email': email.replace('&', '').replace('=', ''),
            'uid': str(10),
            'role': 'user'
        })
    ```

- encrypt:

    ```python
    def AES_encrypt(encoded_cookie):
        cryptor = AES.new(consistent_but_unknown_key, AES.MODE_ECB)
        ciphertext = cryptor.encrypt(pkcs7(encoded_cookie, blocksize))
        return ciphertext
    ```

- decrypt:

    ```python
    def AES_decrypt_and_parse(encrypted_cookie: bytes) -> dict:
        cryptor = AES.new(consistent_but_unknown_key, AES.MODE_ECB)
        encoded_cookie = pkcs7_unpadding(cryptor.decrypt(encrypted_cookie))

        return cookie2dict(encoded_cookie.decode())
    ```

- put it all together, we have recv_encrypted_cookie_for function on the server-side:

    ```python
    def recv_encrypted_cookie_for(email: str) -> bytes:
        cookie = profile_for(email)
        encrypted_cookie = AES_encrypt(bytes(cookie, 'ascii'))
        return encrypted_cookie
    ```

## Analysis phase 2

What do we, the attackers, know:

- cookies is encrypted by aes ebc
- consistent key
- padding: pkcs7
- blocksize: 16
- cookie before encrypting format: 'email=our@email.com&uid=10&role=user'

## Idea

still that security issue of ECB mode, two identical plaintext blocks - two identical ciphertext blocks. We don't know the key, but we know which ciphertext corresponds to which plaintext.

`attacker-controlled` position is position that we can inject our input to the encrypt function:

```url
'email=|attacker-controlled|&uid=10&role=user'
```

idea: choose an `attacker-controlled` so that when we receive the encrypted cookies, we swap blocks and send them back to the server, server decrypts that, and the string `role=admin` appear.

## Solution

input:

```text
'aaaaaaaaaa' + 'admin' + '\x0b'*0x0b + 'aaa':
```

cookie generated by server:

```text
block1 = 'email=aaaaaaaaaa'
block2 = 'admin' + '\x0b'*0x0b
block3 = 'aaa&uid=10&role=
block4 = 'user' + '\x0c'*0x0c
```

- '\x0b'*0x0b in block 2: is padding pkcs7 manually created by attacker
- '\x0c'*0x0c ở block 4: is padding pkcs7 generated by server

If we swap block 2 and block 4:

```text
block1 = 'email=aaaaaaaaaa'
block4 = 'user' + '\x0c'*0x0c
block3 = 'aaa&uid=10&role=
block2 = 'admin' + '\x0b'*0x0b
```

- `role=admin` appear
- valid padding pkcs7

Python code:

```python
def crack():
    email = 'aaaaaaaaaa' + 'admin' + '\x0b'*0x0b + 'aaa'

    encrypted_cookie = recv_encrypted_cookie_for(email)
    encrypted_cookie_block16 = [encrypted_cookie[i:i+blocksize] for i in range(0, len(encrypted_cookie), blocksize)]

    fake_encrypted_cookie = encrypted_cookie_block16[0] + encrypted_cookie_block16[3] + \
                            encrypted_cookie_block16[2] + encrypted_cookie_block16[1]

    profile = AES_decrypt_and_parse(fake_encrypted_cookie)
    print(profile)
```

result:

```python
{'email': 'aaaaaaaaaauser\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0caaa', 'uid': '10', 'role': 'admin'}
```

Source code: [here](./challenge13.py)

## References

- lambda: <https://julien.danjou.info/python-functional-programming-lambda/>
- map(): <https://www.w3schools.com/python/ref_func_map.asp>