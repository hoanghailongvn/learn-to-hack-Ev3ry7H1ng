# [Javascript - Obfuscation 2](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Obfuscation-2)

## Solutions

```js
unescape('unescape%28%22String.fromCharCode%2528104%252C68%252C117%252C102%252C106%252C100%252C107%252C105%252C49%252C53%252C54%2529%22%29')
=> 'unescape("String.fromCharCode%28104%2C68%2C117%2C102%2C106%2C100%2C107%2C105%2C49%2C53%2C54%29")'
unescape("String.fromCharCode%28104%2C68%2C117%2C102%2C106%2C100%2C107%2C105%2C49%2C53%2C54%29")
=> 'String.fromCharCode(104,68,117,102,106,100,107,105,49,53,54)'
String.fromCharCode(104,68,117,102,106,100,107,105,49,53,54)
=> 'hDufjdki156'
```
