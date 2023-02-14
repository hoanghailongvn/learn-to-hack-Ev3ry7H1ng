# [Access control vulnerabilities and privilege escalation](https://portswigger.net/web-security/access-control)

## Lab

- apprentice:
  - [1. Unprotected admin functionality](./lab/1.%20Unprotected%20admin%20functionality.md)
  - [2. Unprotected admin functionality with unpredictable URL](./lab/2.%20Unprotected%20admin%20functionality%20with%20unpredictable%20URL.md)
  - [3. User role controlled by request parameter](./lab/3.%20User%20role%20controlled%20by%20request%20parameter.md)
  - [4. User role can be modified in user profile](./lab/4.%20User%20role%20can%20be%20modified%20in%20user%20profile.md)
  - [5. User ID controlled by request parameter](./lab/5.%20User%20ID%20controlled%20by%20request%20parameter.md)
  - [6. User ID controlled by request parameter, with unpredictable user IDs](./lab/6.%20User%20ID%20controlled%20by%20request%20parameter%2C%20with%20unpredictable%20user%20IDs.md)
  - [7. User ID controlled by request parameter with data leakage in redirect](./lab/7.%20User%20ID%20controlled%20by%20request%20parameter%20with%20data%20leakage%20in%20redirect.md)
  - [8. User ID controlled by request parameter with password disclosure](./lab/8.%20User%20ID%20controlled%20by%20request%20parameter%20with%20password%20disclosure.md)
  - [9. Insecure direct object references](./lab/9.%20Insecure%20direct%20object%20references.md)
- practitioner:
  - [10. URL-based access control can be circumvented](./lab/10.%20URL-based%20access%20control%20can%20be%20circumvented.md)
  - [11. Method-based access control can be circumvented](./lab/11.%20Method-based%20access%20control%20can%20be%20circumvented.md)
  - [12. Multi-step process with no access control on one step](./lab/12.%20Multi-step%20process%20with%20no%20access%20control%20on%20one%20step.md)
  - [13. Referer-based access control](./lab/13.%20Referer-based%20access%20control.md)

## Summary

logic:

- 1. directly access admin panel by normal user account
- 2. directly access admin panel with unpredictable URL by normal user account
- 3. role controlled by request parameters (cookies, ...)
- 4. edit update account information request (add role field in a change email request, ...)
- 5. change userid in request
- 6. find unpredictable userid
- 7. check redirect response
- 8. ...
- 9. check idor
- 10. X-Original-URL
- 11. change method of unauthorized request (POST -> GET)
- 12. check multi-step process
- 13. fake refered header
