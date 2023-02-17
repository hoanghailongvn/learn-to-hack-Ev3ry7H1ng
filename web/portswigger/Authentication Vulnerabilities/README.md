# [Authentication vulnerabilities](https://portswigger.net/web-security/authentication)

## Lab

- apprentice:
  - [1. Username enumeration via different responses](./lab/1.%20Username%20enumeration%20via%20different%20responses.md)
  - [2. 2FA simple bypass](./lab/2.%202FA%20simple%20bypass.md)
  - [3. Password reset broken logic](./lab/3.%20Password%20reset%20broken%20logic.md)

- practitioner:
  - [4. Username enumeration via subtly different responses](./lab/4.%20Username%20enumeration%20via%20subtly%20different%20responses.md)
  - [5. Username enumeration via response timing](./lab/5.%20Username%20enumeration%20via%20response%20timing.md)
  - [6. Broken brute-force protection, IP block](./lab/6.%20Broken%20brute-force%20protection%2C%20IP%20block.md)
  - [7. Username enumeration via account lock](./lab/7.%20Username%20enumeration%20via%20account%20lock.md)
  - [8. 2FA broken logic](./lab/8.%202FA%20broken%20logic.md)
  - [9. Brute-forcing a stay-logged-in cookie](./lab/9.%20Brute-forcing%20a%20stay-logged-in%20cookie.md)
  - [10. Offline password cracking](./lab/10.%20Offline%20password%20cracking.md)
  - [11. Password reset poisoning via middleware](./lab/11.%20Password%20reset%20poisoning%20via%20middleware.md)
  - [12. Password brute-force via password change](./lab/12.%20Password%20brute-force%20via%20password%20change.md)

## Lab usernames and passwords

- [Candidate usernames](https://portswigger.net/web-security/authentication/auth-lab-usernames)
- [Candidate passwords](https://portswigger.net/web-security/authentication/auth-lab-passwords)

## Checklist

username enumeration:

- different responses
- subtly different responses
- IP block based on `X-Forwarded-For`
- bypass account lock (login to existed account to reset counter)

change password function:

- change host or `X-Forwarded-Host`
