# **[set 5 - challenge 37](https://cryptopals.com/sets/5/challenges/37): Break SRP with a zero key**


## Script
Ta có công thức tính S bên server:
- $`S = g^{ab} \times g^{xub} = A^{b} \times g^{xub} \mod N`$

=> Nếu A = 0 hoặc A là bội của N thì $S = 0$.

Attacker:
- [A] ----(A = 0)----> [Server]:
    - [Server] calculate: $`S = 0`$

- Biết phía [Server] có S = 0, có salt => Attacker tính được hmac:
    - K = SHA256(S)
    - hmac_value = HMAC-SHA256(K, salt)
- [A] ----(hmac_value)----> [Server]:
    - [Server] calculate: accept

## Simulation
Viết python simulation như kịch bản ở trên: [python code](./challenge37.py)

Kết quả:
```
S: accept
```
# References
