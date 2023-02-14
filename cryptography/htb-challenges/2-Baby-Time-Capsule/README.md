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

interesting point:

- small e
- one message decrypted multiple times by different key each time

It looks exactly like the problem of the RSA algorithm described in challenge 40 in the cryptopals series. You can read my writeup for that challenge [here](./../../cryptopals/set5/challenge40/)

## Solution

```python
from binascii import unhexlify
from decimal import Decimal
import math

e = 5

# get ciphertext and public key from server 5 times
ciphertext=["592785D1AFD0B38A2D1B4DC0E84E4D41A782E41B3DF2E0FCF4D2D876A802B4F26606FE5AB101AF9A7F8EDC372C8ECDF96532587531AA84F8FCCF315AB21F0C1AF83C40AC6AE4A9ABB38F62A900CA2C64C112F3974F83C5273A9D258C7160BC78A0654BFC1058FE6F4BF4E01246F433B86D3AFFC7210909F94E286BC08BD2E717",
"3D3BB3F64CF4421B0C3720CAE9C3F9D0D3D38ACA41CD787B78C54AD276CACF24C8CE239AF95B03E70CC20D6D58910F0EC9AB0E0558A04C0745079F84929371AB7FE70CDCB8161C3194B22FDE43A17636C333165C6F24BA40DD5BB20F91F5E355C7C683AE99A6CBF329DDB4B370DFEEE489420119A20F1E1775E8E11B39D65874",
"61618623FDA16DD34A1AC58064AD39F4F1E0A8E4B1DDA4FA9FA67E62FAD67B866C643D0B8EC1F2B2867FEE5407BA0D42EBF66F218D877AAD42CD53B055EDCE9233FC5CC01864A1DFB300717B21F68B8D3BB395611527A281E178653F5C2306E802DC23F6C4D8B6BFE753BCF3742E44AAE06B3AE38B1FE2FF8ADF04F21DFE6B87",
"372F3687FFD156DEDBE3DD29D773B7C20FABD65B24396C92166363BD71681A321B139997F5D1485B309459E4FB2C0B0623F0B34332C6A5A227059C3A80089F9A6D53FE6794EB4B7D3BFB5097A8B740F3A0CCE9D0329D4776E4261728DE38289A1472A2DE86B18D2C433DA7669E0642C97789CDEC3D999F285A06319FF7AC2CA2",
"953FAA126A81C6DCC4736FE5CF17A50E96619ACF7822412ABEF44D7E94CE1A82ED14E6B987CF767CE2962CD4A1186A00ACA15764AEFF9ED875EEDFDA88B23DE0CCF1FBF4A0EC229D8DEE0EB9562AD3AECD70CA0702369FC7E31B3EA132B529B88F7A6B86AFE624CD68F107232F26BDA1BFAF95B0E6A7502559F9799A86B568C8"]

n = ["81C2059C22940C8C741FA724271139B78205F2747F75C4C16EAB1FCBE25BC327AF5848051BC0F79EF7AFA05274E1A9DC4F717035F6C2C615C158BDD2EA564E1E1D169FD2CF795FAB2BC54B2BD5BC7F4D52DA0A89D316CD4447303061DB13F526E5B25BD56F4BA868DF7225218DF7899DA6DFCA525880AF190858DC4279FB7651",
"7E414AD95C4A295DF0775DBA001C1A1E2ADD4809CA7B51FB14F8CE23A8DC64330A8C376832381C5ACCD4A2D8740A712452AB732C335E0AC0A505468389798C1AE27C961B6AFA8578911281B17184E9005BEEFEEB3D9E3666D1DFDC6193464643408D44CE62886E2EC86054A735D609B34B6CD871314C1B0B939627D223C8E419",
"804DE32632EB11F0FCA1BE030EC03115A0A6C5AFCF472E2E7CDDB1606DEFE06F7E3E3B7034C564E795CCB199DFC16C83D23E9C7624AF57B4EA83ABB7D2AFD83D7D680D65B40B5999AA9349ED6E1726C635A30831C772BBF79C1772E7B3FD6A933ECA0099E2F6D8D02A44A70BF58642DAAAA451627A8C0E5A5129E723E34A320F",
"9811FE60D29FAE421D420251B3A25B7EE537CF53EF568D455F0BB3CDBD01976D0C90C56DF68BCC25DDD84ED842E4575DBEE5D7D7A432622E8B9EA216E37621C667CF46C099341C6C4DD3ECC0B6F635A2D2CBC121714CFB22935E2E47F5B2ED74980B29DF3502E2ABE412BC75E61F8B7FA210554DC6298617F6BFB21763B7AB65",
"99548718D144A9727E8B2EF480F09A0FAA78776EA1B736662E224AB072EC209A0E6F8246A452AFA654A6FB9DA6E945367BD3FACAD280B8C5B27DB23687BC6128DD0C3EFA79AB257436D9954E11E9025F5CA622CB773A3127ADF7D126EA7816B61741B622E685E94917DBDE02E869078AA86AC673E16B29162D818840C1379D61"]

# convert ciphertext and n to int
for i in range(e):
    ciphertext[i] = int.from_bytes(unhexlify(ciphertext[i]), 'big')
    n[i] = int.from_bytes(unhexlify(n[i]), 'big')

# from challenge 40 cryptopals
result = 0
for i in range(e):
    # --- calculate (n[0] * n[1] * ... * n[e]) but except n[i]
    temp = 1
    for j in range(e):
        if j != i:
            temp *= n[j]
    # --- end ---
    result += ciphertext[i] * temp * pow(temp, -1, n[i])

# --- calculate (n[0] * n[1] * ... * n[e]) ---
temp = 1
for i in range(e):
    temp *= n[i]
# --- end ---

result %= temp
# print(result) # 302104571691219451000547227647557197445855114125921744047262527923520276152187471184832966608014451919142617860953230086917533522168064133137355753548962355447867442282906584458323915936137277507596293058392465365126790592874265661864579154941893845277455975439713980644628329104500897037217924047311695616563557449472670150603945836587107685344612354640130555992181295641626423601935816567492817060685162067844909767041552282405733189486468937545640856429651254664439803449355087566843968669235944005176224217529002030875479755108669584074186941282720628825725257969464166847058895324524666933811896184330396612204823938088064816976936712195178125

# now result = m^e \mod (N_1N_2...N_e)

# but if i calculate nth root of a big integer by Python, it failed:
# plaintext = round(pow(result, 1/e)) # => OverflowError: int too large to convert to float

# i use https://keisan.casio.com/calculator site to calculate it for me
# 5th root of result is 3133512701921564926666059129802238375015291423590355094862405004229914481893581069974415008616334994674940586670768933862016098685

plaintext = 3133512701921564926666059129802238375015291423590355094862405004229914481893581069974415008616334994674940586670768933862016098685

print(plaintext.to_bytes(60, 'big')) #b'\x00\x00\x00\x00\x00\x00HTB{t3h_FuTUr3_15_bR1ghT_1_H0p3_y0uR3_W34r1nG_5h4d35!}'
```

## References

online calculator: <https://keisan.casio.com/calculator>
my writeup for challenge 40: [link](./../../cryptopals/set5/challenge40/)
