# [Reflected XSS](https://portswigger.net/web-security/cross-site-scripting/reflected)

## What is Reflected XSS?
Reflected cross-site scripting (or XSS) arises when an application receives data in an HTTP request and includes that data within the immediate response in an unsafe way.

## Impact of reflected XSS attacks
If an attacker can control a script that is executed in the victim's browser, then they can typically fully compromise that user. Amongst other things, the attacker can:

- Perform any action within the application that the user can perform.
- View any information that the user is able to view.
- Modify any information that the user is able to modify.
- Initiate interactions with other application users, including malicious attacks, that will appear to originate from the initial victim user.

Deliver:
- placing links on a website controlled by the attacker,or on another website that allows content to be generated
- sending a link in an email, tweet or other message
- ...
Target:
- known user
- any users
- 
The need for an external delivery mechanism for the attack means that the impact of reflected XSS is generally less severe than stored XSS, where a self-contained attack can be delivered within the vulnerable application itself.

## [Reflected XSS in different contexts](https://portswigger.net/web-security/cross-site-scripting/reflected#reflected-xss-in-different-contexts)
There are many different varieties of reflected xss.

The location
The validation

https://portswigger.net/web-security/cross-site-scripting/contexts

