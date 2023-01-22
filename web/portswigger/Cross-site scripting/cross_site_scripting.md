# [Cross-site scripting](https://portswigger.net/web-security/cross-site-scripting)

## [What is cross-site scripting (XSS)?](https://portswigger.net/web-security/cross-site-scripting#what-is-cross-site-scripting-xss)
Cross-site scripting (also known as XSS) is a web security vulnerability that allows an attacker to compromise the interactions that users have with a vulnerable application. It allows an attacker to circumvent the same origin policy, which is designed to segregate different websites from each other. Cross-site scripting vulnerabilities normally allow an attacker to masquerade as a victim user, to carry out any actions that the user is able to perform, and to access any of the user's data. If the victim user has privileged access within the application, then the attacker might be able to gain full control over all of the application's functionality and data.
## [How does XSS work?](https://portswigger.net/web-security/cross-site-scripting#how-does-xss-work)
Cross-site scripting works by manipulating a vulnerable web site so that it returns malicious JavaScript to users. When the malicious code executes inside a victim's browser, the attacker can fully compromise their interaction with the application.

## [XSS Proof of Concept](https://portswigger.net/web-security/cross-site-scripting#xss-proof-of-concept)
Trước thì dùng alert là ok mà, if you use Chrome. From version 92 onward (July 20th, 2021), cross-origin iframes are prevented from calling alert().

Giờ chuyển qua dùng print()

## [XSS types](https://portswigger.net/web-security/cross-site-scripting#what-are-the-types-of-xss-attacks)
- Reflected XSS
- Stored XSS
- DOM-based XSS
### Reflected XSS
[reflected](../../../../learn/portswigger/Web%20Security%20Academy/Cross-site%20scripting/Reflected%20XSS/reflected.md)

### Stored XSS
[stored](../../../../learn/portswigger/Web%20Security%20Academy/Cross-site%20scripting/Stored%20XSS/stored.md)

### Dom-based XSS
[dom-based](../../../../learn/portswigger/Web%20Security%20Academy/Cross-site%20scripting/DOM-based%20XSS/dom-based.md)

## What can XSS be used for?
An attacker who exploits a cross-site scripting vulnerability is typically able to:

- Impersonate or masquerade as the victim user.
- Carry out any action that the user is able to perform.
- Read any data that the user is able to access.
- Capture the user's login credentials.
- Perform virtual defacement of the web site.
- Inject trojan functionality into the web site.

## Impact of XSS vulnerabilities
The actual impact of an XSS attack generally depends on the nature of the application, its functionality and data, and the status of the compromised user. For example:

- In a brochureware application, where all users are anonymous and all information is public, the impact will often be minimal.
- In an application holding sensitive data, such as banking transactions, emails, or healthcare records, the impact will usually be serious.
- If the compromised user has elevated privileges within the application, then the impact will generally be critical, allowing the attacker to take full control of the vulnerable application and compromise all users and their data.