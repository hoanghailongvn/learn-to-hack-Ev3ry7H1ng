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

## Summary

check every user-controlled field that looks like a URL, a path,...

use collaborator everywhere extension to check if any field, such as `User-Agent`, `Referer` has ping back problem.

preventation:

- blacklist
- whitelist

circumvention:

- open redirection

blind ssrf:

- oob detection
- shellshock

## Exam only

If you find an SSRF vulnerability, you can use it to read files by accessing an internal-only service, running on localhost on port 6566

## References

SSRF:

- <https://www.youtube.com/watch?v=ih5R_c16bKc&ab_channel=RanaKhalil>
- <https://www.youtube.com/watch?v=D1S-G8rJrEk&ab_channel=HackInTheBoxSecurityConference>
