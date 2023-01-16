# [OAuth 2.0 authentication vulnerabilities](https://portswigger.net/web-security/oauth)

## What is OAuth?
OAuth is a commonly used authorization framework that enables websites and web applications to request limited access to a user's account on another application.

Without exposing their login credentials to the requesting application.

Example:
- an application might use OAuth to request access to your email contacts list so that it can suggest people to connect with.
- third-party authentication services

OAuth 2.0 vs 1.0:
- 2.0 was written from scratch => very different.
- OAuth 2.0 is the current standard, some websites still use the legacy version 1a.
## How does OAuth 2.0 work
[oauth_grant_types](../../../../learn/portswigger/Web%20Security%20Academy/OAuth%202.0%20authentication%20vulnerabilities/oauth_grant_types.md)

## How do OAuth authentication vulnerabilities arise?
OAuth is relatively vague and flexible by design, lack of built-in security features


## [Exploiting OAuth authentication vulnerabilities](https://portswigger.net/web-security/oauth#exploiting-oauth-authentication-vulnerabilities)
Vulnerabilities can arise in:
- client application:
	- [lab-oauth-authentication-bypass-via-oauth-implicit-flow](../../../../learn/portswigger/Web%20Security%20Academy/OAuth%202.0%20authentication%20vulnerabilities/lab/apprentice/lab-oauth-authentication-bypass-via-oauth-implicit.md)
	- [lab-oauth-forced-oauth-profile-linking](../../../../learn/portswigger/Web%20Security%20Academy/OAuth%202.0%20authentication%20vulnerabilities/lab/practitioner/lab-oauth-forced-oauth-profile-linking.md)
- OAuth service:
	-
	
### [Vulnerabilities in the OAuth client application](https://portswigger.net/web-security/oauth#vulnerabilities-in-the-oauth-client-application)
#### [Improper implementation of the implicit grant type](https://portswigger.net/web-security/oauth#improper-implementation-of-the-implicit-grant-type)
[lab-oauth-authentication-bypass-via-oauth-implicit-flow](../../../../learn/portswigger/Web%20Security%20Academy/OAuth%202.0%20authentication%20vulnerabilities/lab/apprentice/lab-oauth-authentication-bypass-via-oauth-implicit.md)
#### [Flawed CSRF protection](https://portswigger.net/web-security/oauth#flawed-csrf-protection)
[lab-oauth-forced-oauth-profile-linking](../../../../learn/portswigger/Web%20Security%20Academy/OAuth%202.0%20authentication%20vulnerabilities/lab/practitioner/lab-oauth-forced-oauth-profile-linking.md)

Còn tiếp:...
