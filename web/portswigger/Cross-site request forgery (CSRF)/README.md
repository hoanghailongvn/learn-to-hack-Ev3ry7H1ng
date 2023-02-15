# [Cross-site request forgery (CSRF)](https://portswigger.net/web-security/csrf)

## Lab

- apprentice:
  - [1. CSRF vulnerability with no defenses](./lab/1.%20CSRF%20vulnerability%20with%20no%20defenses.md)
- practitioner:
  - [2. CSRF where token validation depends on request method](./lab/2.%20CSRF%20where%20token%20validation%20depends%20on%20request%20method.md)
  - [3. CSRF where token validation depends on token being present](./lab/3.%20CSRF%20where%20token%20validation%20depends%20on%20token%20being%20present.md)
  - [4. CSRF where token is not tied to user sessionCSRF where token is not tied to user session](./lab/4.%20CSRF%20where%20token%20is%20not%20tied%20to%20user%20sessionCSRF%20where%20token%20is%20not%20tied%20to%20user%20session.md)
  - [5. CSRF where token is tied to non-session cookie](./lab/5.%20CSRF%20where%20token%20is%20tied%20to%20non-session%20cookie.md)
  - [6. CSRF where token is duplicated in cookie](./lab/6.%20CSRF%20where%20token%20is%20duplicated%20in%20cookie.md)
  - [10. SameSite Strict bypass via client-side redirect](./lab/10.%20SameSite%20Strict%20bypass%20via%20client-side%20redirect.md)

## Checklist for exam

1. no csrf tokens
2. change http method => server doesn't check csrf tokens
3. no csrf tokens => server doesn't check csrf tokens
4. token is not tied to user session
5. pair token, but still not tied to user session
6. duplicated tokens => server just compares two user controlled tokens
7. delete `referer` header
8. bypass `referer` header
