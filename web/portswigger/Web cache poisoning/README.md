# [Web cache poisoning](https://portswigger.net/web-security/web-cache-poisoning)

## Lab

- practitioner:
  - [1. Web cache poisoning with an unkeyed header](./lab/1.%20Web%20cache%20poisoning%20with%20an%20unkeyed%20header.md)
  - [2. Web cache poisoning with an unkeyed cookie](./lab/2.%20Web%20cache%20poisoning%20with%20an%20unkeyed%20cookie.md)
  - [3. Web cache poisoning with multiple headers](./lab/3.%20Web%20cache%20poisoning%20with%20multiple%20headers.md)
  - [4. Targeted web cache poisoning using an unknown header](./lab/4.%20Targeted%20web%20cache%20poisoning%20using%20an%20unknown%20header.md)
  - [5. Web cache poisoning via an unkeyed query string](./lab/5.%20Web%20cache%20poisoning%20via%20an%20unkeyed%20query%20string.md)
  - [6. Web cache poisoning via an unkeyed query parameter](./lab/6.%20Web%20cache%20poisoning%20via%20an%20unkeyed%20query%20parameter.md)
  - [7. Parameter cloaking](./lab/7.%20Parameter%20cloaking.md)
  - [8. Web cache poisoning via a fat GET request](./lab/8.%20Web%20cache%20poisoning%20via%20a%20fat%20GET%20request.md)
  - [9. URL normalization](./lab/9.%20URL%20normalization.md)

## Note

- `X-Cache: hit` tells us that the response came from the cache, otherwise `X-Cache: miss`
- `Age: n`: cache has lived for `n` seconds
- The cache on labs expire every 30 seconds.

## Detect

burpsuite `param miner` extension.

## Summary

1. Identify and evaluate unkeyed inputs:

    - header (X-Forwarded-Host): [lab 1](./lab/1.%20Web%20cache%20poisoning%20with%20an%20unkeyed%20header.md)
    - multiple header (X-Forwarded-Scheme and X-Forwarded-Host): [lab 3](./lab/3.%20Web%20cache%20poisoning%20with%20multiple%20headers.md)
    - cookie (fehost): [lab 2](./lab/2.%20Web%20cache%20poisoning%20with%20an%20unkeyed%20cookie.md)
    - query string: [lab 5](./lab/5.%20Web%20cache%20poisoning%20via%20an%20unkeyed%20query%20string.md)
    - query parameter (utm_content): [lab 6](./lab/6.%20Web%20cache%20poisoning%20via%20an%20unkeyed%20query%20parameter.md)
    - cloaking (parsing discrepancy between the cache and the application): [lab 7](./lab/7.%20Parameter%20cloaking.md)
    - fat GET body: [lab 8](./lab/8.%20Web%20cache%20poisoning%20via%20a%20fat%20GET%20request.md)

2. Elicit a harmful response from the back-end server
the next step is to evaluate exactly how the website processes it:

- unkeyed => url: [lab 1](./lab/1.%20Web%20cache%20poisoning%20with%20an%20unkeyed%20header.md), [lab 4](./lab/4.%20Targeted%20web%20cache%20poisoning%20using%20an%20unknown%20header.md)
- unkeyed => js script: [lab 2](./lab/2.%20Web%20cache%20poisoning%20with%20an%20unkeyed%20cookie.md), [lab 5](./lab/5.%20Web%20cache%20poisoning%20via%20an%20unkeyed%20query%20string.md), [lab 6](./lab/6.%20Web%20cache%20poisoning%20via%20an%20unkeyed%20query%20parameter.md), [lab 7](./lab/7.%20Parameter%20cloaking.md), [lab 8](./lab/8.%20Web%20cache%20poisoning%20via%20a%20fat%20GET%20request.md), [lab 9](./lab/9.%20URL%20normalization.md)
- unkeyed => 3xx: [lab 3](./lab/3.%20Web%20cache%20poisoning%20with%20multiple%20headers.md)
