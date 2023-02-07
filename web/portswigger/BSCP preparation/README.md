# Preparation

## List all the labs

- [File upload vulnerabilities](./../File%20upload%20vulnerabilities/)
- [OAuth 2.0 authentication vulnerabilities](./../OAuth%202.0%20authentication%20vulnerabilities/)
- [SSRF](./../Server-side%20request%20forgery%20(SSRF)/)
- [SQLi](./../SQL%20injection/)
- [XSS](./../Cross-site%20scripting/)
- [CSRF](./../Cross-site%20request%20forgery%20(CSRF)/)
- [XXE](./../XXE%20injection/)
- [Clickjacking](./../Clickjacking/)
- [CORS](./../CORS/)
- [Request smuggling](./../Request%20smuggling/)
- [SSTi](./../Server-side%20template%20injection/)
- [Insecure deserialization](./../Insecure%20deserialization/)
- [Directory traversal](./../Directory%20traversal/)
- [Access control](./../Access%20control/)
- [Authentication vulnerabilities](./../Authentication%20Vulnerabilities/)
- [Business logic vulnerabilities](./../Business%20logic%20vulnerabilities/)
- [WebSockets](./../WebSockets/)
- [Web cache poisoning](./../Web%20cache%20poisoning/)
- [Information disclosure vulnerabilities](./../Information%20disclosure%20vulnerabilities/)
- [OS command injection](./../OS%20command%20injection/)

| Category | Stage 1 | Stage 2 | Stage 3 |
| --- | --- | --- | --- |
| SQL Injection |     | ✔️  | ✔️  |
| Cross-site scripting | ✔️  | ✔️  |     |
| Cross-site request forgery (CSRF) | ✔️  | ✔️  |     |
| Clickjacking | ✔️  | ✔️  |     |
| DOM-based vulnerabilities | ✔️  | ✔️  |     |
| Cross-origin resource sharing (CORS) | ✔️  | ✔️  |     |
| XML external entity (XXE) injection |     |     | ✔️  |
| Server-side request forgery (SSRF) |     |     | ✔️  |
| HTTP request smuggling | ✔️  | ✔️  |     |
| OS command injection |     |     | ✔️  |
| Server-side template injection |     |     | ✔️  |
| Directory traversal |     |     | ✔️  |
| Access control vulnerabilities | ✔️  | ✔️  |     |
| Authentication | ✔️  | ✔️  |     |
| Web cache poisoning | ✔️  | ✔️  |     |
| Insecure deserialization |     |     | ✔️  |
| HTTP Host header attacks | ✔️  | ✔️  |     |
| OAuth authentication | ✔️  | ✔️  |     |
| File upload vulnerabilities |     |     | ✔️  |
| JWT | ✔️  | ✔️  |

## Note

If you find an SSRF vulnerability, you can use it to read files by accessing an internal-only service, running on localhost on port 6566.

learn to troubleshoot JavaScript.

## References

<https://medium.com/@ryan.beebe/burp-suite-certified-practitioner-exam-review-9077b14f8eb1>
