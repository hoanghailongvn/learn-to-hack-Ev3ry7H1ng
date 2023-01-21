# **[set 5 - challenge 35](https://cryptopals.com/sets/5/challenges/35): Implement DH with negotiated groups, and break with malicious "g" parameters**

```tẽt
A->B
Send "p", "g"
B->A
Send ACK
A->B
Send "A"
B->A
Send "B"
A->B
Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
B->A
Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv
```

Do the MITM attack again, but play with "g". What happens with:

```text
    g = 1
    g = p
    g = p - 1
```

Write attacks for each.

## Analysis

what will happen if MITM attacker change g to 1, p or p - 1:

case 1: g = 1:

- [A] ----(p, g)----> [Eve] ----(p, 1)----> [B]:
  - [B]: $B = g^b \mod p = 1^b \mod p = 1$
- [B] ----(B)----> [Eve] ----(B)----> [A]:
  - [A]: $s = B^a \mod p = 1^a \mod p = 1$

- => MITM attacker know that `s` = 1 on A-side.

case 2: g = p:

- [A] ----(p, g)----> [Eve] ----(p, p)----> [B]:
  - [B]: $B = g^b \mod p = p^b \mod p = 0$
- [B] ----(B)----> [Eve] ----(B)----> [A]:
  - [A]: $s = B^a \mod p = 0^a \mod p = 0$

- => MITM attacker know that `s` = 0 on A-side.

case 3: g = p - 1:

- [A] ----(p, g)----> [Eve] ----(p, p - 1)----> [B]:
  - [B]: $B = g^b \mod p = (p - 1)^b \mod p$
- [B] ----(B)----> [Eve] ----(B)----> [A]:
  - [A]: $s = B^a \mod p = (p - 1)^{ab} \mod p$
  - ab is even: s = 1
  - ab is odd: s = p - 1

## simulation with case g = 1

[here](./challenge35.py)

result:

```text
A send: p g A: (37, 5, 9)
B received p g a: (37, 1, 9)
B s: 10
B key: b'M\x89\x07@R<o*hJC\xc0h\xb5\xa1;'
B send B: 1
A recv: B: 1
A s: 1
A key: b'\xb0\xdf`k\x85\xdfG}\x99\x05\xd3\xd5\xeaU\x85\xfa'
A send: b'private message'
MITM: b'private message'
```

note that `key`, `g`, `s` on both sides of A and B are now different.

## References
