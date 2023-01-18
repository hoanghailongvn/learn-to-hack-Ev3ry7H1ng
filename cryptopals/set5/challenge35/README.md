# **[set 5 - challenge 35](https://cryptopals.com/sets/5/challenges/35): Implement DH with negotiated groups, and break with malicious "g" parameters**

Điều gì xảy ra nếu MITM attacker thay đổi g, với các giá trị 1, p, p - 1:

TH1: Thay g = 1:
- [A] ----(p, g)----> [Eve] ----(p, 1)----> [B]:
    - [B]: $`B = g^b \mod p = 1^b \mod p = 1`$
- [B] ----(B)----> [Eve] ----(B)----> [A]: Lúc này, B đã là 1:
    - [A]: $`s = B^a \mod p = 1^a \mod p = 1`$

- => MITM attacker biết được bên [A] có s = 1.

TH2: Thay g = p:
- [A] ----(p, g)----> [Eve] ----(p, p)----> [B]:
    - [B]: $`B = g^b \mod p = p^b \mod p = 0`$
- [B] ----(B)----> [Eve] ----(B)----> [A]: Lúc này, B đã là 0:
    - [A]: $`s = B^a \mod p = 0^a \mod p = 0`$

- => MITM attacker biết được bên [A] có s = 0.

TH3: Thay g = p - 1:
- [A] ----(p, g)----> [Eve] ----(p, p - 1)----> [B]:
    - [B]: $`B = g^b \mod p = (p - 1)^b \mod p`$
- [B] ----(B)----> [Eve] ----(B)----> [A]: Lúc này, B đã là $`(p - 1)^b \mod p`$:
    - [A]: $`s = B^a \mod p = (p - 1)^{ab} \mod p`$
    - ab chẵn: s = 1
    - ab lẻ: s = p - 1

=> attacker cũng xác định được `s` ở phía A

## Code với g = 1
[here](./challenge35.py)

Kết quả:
```
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

Chú ý rằng, key, g, s hai bên A và B giờ đã khác nhau.
# References
