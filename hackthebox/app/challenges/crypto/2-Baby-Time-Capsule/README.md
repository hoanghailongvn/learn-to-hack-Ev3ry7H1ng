# [Baby Time Capsule](https://app.hackthebox.com/challenges/baby-time-capsule)

## CHALLENGE DESCRIPTION

Qubit Enterprises is a new company touting it's propriety method of qubit stabilization. They expect to be able to build a quantum computer that can factor a RSA-1024 number in the next 10 years. As a promotion they are giving out "time capsules" which contain a message for the future encrypted by 1024 bit RSA. They might be great engineers, but they certainly aren't cryptographers, can you find a way to read the message without having to wait for their futuristic machine?

## Find a way to connect to the server

socket modules:

```python
import socket
import time

HOST = "161.35.162.53"
# HOST = "127.0.0.1"
PORT = 31664

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
```

result:

```python
OSError: [WinError 10049] The requested address is not valid in its context
```

`The reason for why your code fails tho is because you're trying to bind to an external IP.` ([source](https://stackoverflow.com/questions/23857942/winerror-10049-the-requested-address-is-not-valid-in-its-context))

netcat tool:

```bash
kali@kali:~$ nc 161.35.162.53 31664
Welcome to Qubit Enterprises. Would you like your own time capsule? (Y/n) y
{"time_capsule": "581587F4AD823841A259BA82D383B3FE78AB5525DDCC67614BD790A6E047035E3F15FC0E1DA2D52F892D4A451D5A6BC8DA595CF75275941CED79562124CF8E765F256ED613C538BD6755D50D8D46EF2A6F01D9596C3248518DE1DEE23D7377A950CADA4737DEC3F7CD3A77FA1BB153EC1C1017791B9CFC71AA3165DB9DA041CB", "pubkey": ["95CE3A75EAF37E69EF9B7944114279CCADF5F09F5EEC2C05B915770A0A05EEF21D5CA486A7DA0881793CAA10CAFF2BBEBAC1626FADB51E166F8D3F089343EA921A5BB08CA428BACCE0A5D8D87A3234782A963D474FB2F9A049A5B780A6E37120A10A6C9AFD4532B6AFAEB68DC0BBC925699F78334B4E41A4DC2A90E035D91965", "5"]}
Welcome to Qubit Enterprises. Would you like your own time capsule? (Y/n) n
Thank you, take care

```

ok

## Analysis

[source code](./baby_time_capsule/server.py):

```python
from Crypto.Util.number import bytes_to_long, getPrime
import socketserver
import json

FLAG = b'HTB{--REDACTED--}'


class TimeCapsule():

    def __init__(self, msg):
        self.msg = msg
        self.bit_size = 1024
        self.e = 5

    def _get_new_pubkey(self):
        while True:
            p = getPrime(self.bit_size // 2)
            q = getPrime(self.bit_size // 2)
            n = p * q
            phi = (p - 1) * (q - 1)
            try:
                pow(self.e, -1, phi)
                break
            except ValueError:
                pass

        return n, self.e

    def get_new_time_capsule(self):
        n, e = self._get_new_pubkey()
        m = bytes_to_long(self.msg)
        m = pow(m, e, n)

        return {"time_capsule": f"{m:X}", "pubkey": [f"{n:X}", f"{e:X}"]}


def challenge(req):
    time_capsule = TimeCapsule(FLAG)
    while True:
        try:
            req.sendall(
                b'Welcome to Qubit Enterprises. Would you like your own time capsule? (Y/n) '
            )
            msg = req.recv(4096).decode().strip().upper()
            if msg == 'Y' or msg == 'YES':
                capsule = time_capsule.get_new_time_capsule()
                req.sendall(json.dumps(capsule).encode() + b'\n')
            elif msg == 'N' or msg == "NO":
                req.sendall(b'Thank you, take care\n')
                break
            else:
                req.sendall(b'I\'m sorry I don\'t understand\n')
        except:
            # Socket closed, bail
            return


class MyTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        req = self.request
        challenge(req)


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def main():
    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadingTCPServer(("0.0.0.0", 1337), MyTCPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()

```

- `socketserver`: The socketserver module simplifies the task of writing network servers. ([document](https://docs.python.org/3/library/socketserver.html))