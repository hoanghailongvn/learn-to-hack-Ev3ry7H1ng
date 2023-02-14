# **[set 5 - challenge 38](https://cryptopals.com/sets/5/challenges/38): Offline dictionary attack on simplified SRP**


## simplified SRP
Là một dạng đơn giản hơn của SRP, trong public key B không còn phụ thuộc vào password nữa.

## Math
Một số công thức toán có trong simplified SRP:
- [Client]              : $`x = hash(salt|P)`$
- [Server] -> [Client]  : $`u = random(0, 2^{128})`$
- [Server]              : $`v = g^{x} \mod N`$
- [Client] -> [Server]  : $`A = g^{a} \mod N`$
- [Server] -> [Client]  : $`B = g^{b} \mod N`$
- [Server],   [Client]  : $`S = g^{ab + xub} \mod N`$

## Dictionary attack
Vào vai một MiTM attacker, đóng giả server, gửi B, u, salt tới client để lấy được hmac value tương ứng. Dựa vào đó và bruteforce.

Chỉ có simplified SRP, MiTM attacker mới có thể bruteforce, do dựa vào b, B, u, salt và A của client, có thể tự tính được hmac tương ứng với một password nào đó:
```math
s = A^{b}\times g^{uxb} \mod N
```

Trong khi đó, với SRP, B phụ thuộc vào password nên không bruteforce được (trong công thức tính s cần biết a):
```math
s = (B - k * g ^{x})^{a + u*x} \mod N
```

## Code
Tải file 10k-most-common.txt: https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt

Viết lại protocol RSP, mitm_simulate:

[python code](./challenge38.py)

Kết quả:
```
expected password: stripper
Found password: stripper
```
# References
