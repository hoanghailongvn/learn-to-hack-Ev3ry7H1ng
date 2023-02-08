# [Web cache poisoning](https://portswigger.net/web-security/web-cache-poisoning)

## Lab

- practitioner:
  - [1. Web cache poisoning with an unkeyed header](./lab/1.%20Web%20cache%20poisoning%20with%20an%20unkeyed%20header.md)
  - [2. Web cache poisoning with an unkeyed cookie](./lab/2.%20Web%20cache%20poisoning%20with%20an%20unkeyed%20cookie.md)
  - [3. Web cache poisoning with multiple headers](./lab/3.%20Web%20cache%20poisoning%20with%20multiple%20headers.md)
  - [4. Targeted web cache poisoning using an unknown header](./lab/4.%20Targeted%20web%20cache%20poisoning%20using%20an%20unknown%20header.md)
  - [5. Web cache poisoning via an unkeyed query string](./lab/5.%20Web%20cache%20poisoning%20via%20an%20unkeyed%20query%20string.md)
  - [6. Web cache poisoning via an unkeyed query parameter](./lab/6.%20Web%20cache%20poisoning%20via%20an%20unkeyed%20query%20parameter.md)

## Note

- `X-Cache: hit` tells us that the response came from the cache, otherwise `X-Cache: miss`
- `Age: n`: cache has lived for `n` seconds
- The cache on labs expire every 30 seconds.
