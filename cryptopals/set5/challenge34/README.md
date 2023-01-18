# **[set 5 - challenge 34](https://cryptopals.com/sets/5/challenges/34): Implement a MITM key-fixing attack on Diffie-Hellman with parameter injection**

MITM là một cách tấn công, trong đỏ, kẻ tấn công đứng ở giữa kết nối giữa 2 bên, có thể đọc và chỉnh sửa message giữa 2 bên.

Trong challenge này, kẻ tấn công là M đứng ở giữa 2 người A và B, chỉnh sửa message của A và B trong quá trình key exchange:
- [A] ----(p, g, A)----> [Eve] ----(p, g, p)----> [B]: Thay A thành p:
    - [B]: $`s = g^A \mod p = g^p \mod p = 0`$
- [B] ----(B)----> [Eve] ----(p)----> [A]: Thay B thành p:
    - [A]: $`s = g^B \mod p = g^p \mod p = 0`$

Khi này MITM attacker đã làm cho s cả hai bên đều bằng 0. Biết được giá trị s của cả 2 bên, MITM attacker có thể decrypt mọi message 2 bên gửi cho nhau khi mà dùng key sinh ra từ s.

## Simulation
[here](./challenge34.py)

Kết quả:
```
A send: p g A: (37, 5, 2)
B received p g a: (37, 5, 37)
B s: 0
B key: b'\xb3v\x88Z\xc8E+l\xbf\x9c\xed\x81\xb1\x08\x0b\xfd'
B send "B": 36
A recv "B": 37
A s: 0
A key: b'\xb3v\x88Z\xc8E+l\xbf\x9c\xed\x81\xb1\x08\x0b\xfd'
A send: b'private message'
mitm: b'private message'
```
# References
