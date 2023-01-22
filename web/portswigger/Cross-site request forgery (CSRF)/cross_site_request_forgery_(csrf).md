# [Cross-site request forgery (CSRF)](https://portswigger.net/web-security/csrf)

## What is CSRF?
Cross-site request forgery (also known as CSRF) is a web security vulnerability that allows an attacker to induce users to perform actions that they do not intend to perform. It allows an attacker to partly circumvent the same origin policy, which is designed to prevent different websites from interfering with each other.
## Impact of CSRF
- causes the victim user to carry out an action unintentionally: change the email address on their account, change their password, make a funds transfer, ...
- attacker might be able to gain full control over the user's account
- if the compromised user has a privileged role within the application, the attacker might be able to take full control of all the application's data and functionality.
## How does CSRF work?
Three key conditions must be in place:
- **A relevant action**: 
- **Cookies-based session handling**:
- **No unpredictable request parameters**:

## How to construct a CSRF attack
## How to deliver a CSRF exploit
- place	the malicious HTML onto a web site that they control, then induce victims to visit that web site
- place into a popular web site and wait
- if CSRF exploits employ the GET method => just a URL
```
<img src="https://vulnerable-website.com/email/change?email=pwned@evil-user.net">
```
## Preventing CSRF attack
[tokens](../../../../learn/portswigger/Web%20Security%20Academy/Cross-site%20request%20forgery%20%28CSRF%29/tokens.md)
## Common CSRF vulnerabilities

### Validation of CSRF token depends on request method
Some applications correctly validate the token when the request uses the POST method but skip the validation when the GET method is used.
[lab-token-validation-depends-on-request-method](../../../../learn/portswigger/Web%20Security%20Academy/Cross-site%20request%20forgery%20%28CSRF%29/lab/practitioner/2.%20lab-token-validation-depends-on-request-method.md)

### Validation of CSRF token depends on token being present
Some applications correctly validate the token when it is present but skip the validation if the token is omitted.

[lab-token-validation-depends-on-token-being-present](../../../../learn/portswigger/Web%20Security%20Academy/Cross-site%20request%20forgery%20%28CSRF%29/lab/practitioner/3.%20lab-token-validation-depends-on-token-being-pre.md)

### CSRF token is not tied to the user session
Some applications do not validate that the token belongs to the same session as the user who is making the request. Instead, the application maintains a global pool of tokens that it has issued and accepts any token that appears in this pool.

[lab-token-not-tied-to-user-session](../../../../learn/portswigger/Web%20Security%20Academy/Cross-site%20request%20forgery%20%28CSRF%29/lab/practitioner/4.%20lab-token-not-tied-to-user-session.md)

### CSRF token is tied to a non-session cookie
In a variation on the preceding vulnerability, some applications do tie the CSRF token to a cookie, but not to the same cookie that is used to track sessions. This can easily occur when an application employs two different frameworks, one for session handling and one for CSRF protection, which are not integrated together:

```
POST /email/change HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 68
Cookie: session=pSJYSScWKpmC60LpFOAHKixuFuM4uXWF; csrfKey=rZHCnSzEp8dbI6atzagGoSYyqJqTz5dv

csrf=RhV7yQDO0xcq9gLEah2WVbmuFqyOq7tY&email=wiener@normal-user.com
```

Có 2 cái csrf token, một cái ở cookie, một cái ở body.
[lab-token-tied-to-non-session-cookie](../../../../learn/portswigger/Web%20Security%20Academy/Cross-site%20request%20forgery%20%28CSRF%29/lab/practitioner/5.%20lab-token-tied-to-non-session-cookie.md)

### CSRF token is simply duplicated in a cookie
In a further variation on the preceding vulnerability, some applications do not maintain any server-side record of tokens that have been issued, but instead duplicate each token within a cookie and a request parameter. When the subsequent request is validated, the application simply verifies that the token submitted in the request parameter matches the value submitted in the cookie. This is sometimes called the "double submit" defense against CSRF, and is advocated because it is simple to implement and avoids the need for any server-side state:
```
POST /email/change HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 68
Cookie: session=1DQGdzYbOJQzLP7460tfyiv3do7MjyPw; csrf=R8ov2YBfTYmzFyjit8o2hKBuoIjXXVpa

csrf=R8ov2YBfTYmzFyjit8o2hKBuoIjXXVpa&email=wiener@normal-user.com
```
In this situation, the attacker can again perform a CSRF attack if the web site contains any cookie setting functionality. Here, the attacker doesn't need to obtain a valid token of their own. They simply invent a token (perhaps in the required format, if that is being checked), leverage the cookie-setting behavior to place their cookie into the victim's browser, and feed their token to the victim in their CSRF attack.
[lab-token-duplicated-in-cookie](../../../../learn/portswigger/Web%20Security%20Academy/Cross-site%20request%20forgery%20%28CSRF%29/lab/practitioner/6.%20lab-token-duplicated-in-cookie.md)

## Referer-based defenses against CSRF
Aside from defenses that employ CSRF tokens, some applications make use of the HTTP Referer header to attempt to defend against CSRF attacks, normally by verifying that the request originated from the application's own domain. This approach is generally less effective and is often subject to bypasses.
### Validation of Referer depends on header being present
Some applications validate the Referer header when it is present in requests but skip the validation if the header is omitted.

In this situation, an attacker can craft their CSRF exploit in a way that causes the victim user's browser to drop the Referer header in the resulting request. There are various ways to achieve this, but the easiest is using a META tag within the HTML page that hosts the CSRF attack:

`<meta name="referrer" content="never">`

[lab-referer-validation-depends-on-header-being-present](../../../../learn/portswigger/Web%20Security%20Academy/Cross-site%20request%20forgery%20%28CSRF%29/lab/practitioner/7.%20lab-referer-validation-depends-on-header-being-.md)

### Validation of Referer can be circumvented
Some applications validate the Referer header in a naive way that can be bypassed. For example, if the application validates that the domain in the Referer starts with the expected value, then the attacker can place this as a subdomain of their own domain:

`http://vulnerable-website.com.attacker-website.com/csrf-attack`
Likewise, if the application simply validates that the Referer contains its own domain name, then the attacker can place the required value elsewhere in the URL:

`http://attacker-website.com/csrf-attack?vulnerable-website.com`
Note:
Although you may be able to identify this behavior using Burp, you will often find that this approach no longer works when you go to test your proof-of-concept in a browser. In an attempt to reduce the risk of sensitive data being leaked in this way, many browsers now strip the query string from the Referer header by default.

You can override this behavior by making sure that the response containing your exploit has the Referrer-Policy: unsafe-url header set (note that Referrer is spelled correctly in this case, just to make sure you're paying attention!). This ensures that the full URL will be sent, including the query string.
[lab-referer-validation-broken](../../../../learn/portswigger/Web%20Security%20Academy/Cross-site%20request%20forgery%20%28CSRF%29/lab/practitioner/8.%20lab-referer-validation-broken.md)