# **[set 5 - challenge 33](https://cryptopals.com/sets/5/challenges/33): Implement Diffie-Hellman**


Diffie-Hellman là một phương pháp trao đổi khóa, cách thức hoạt động của DH dựa theo hướng dẫn của đề bài:
```
from random import randint

if __name__ == "__main__":
    # public
    p = 37
    g = 5
    
    # private
    a = randint(0, p - 1)
    # public
    A = pow(g, a, p)

    # private
    b = randint(0, p - 1)
    # public
    B = pow(g, b, p)

    # phía a nhận được B, tính g^(a*b) mod p
    s_a = pow(B, a, p)

    # phía b nhận được A, tính g^(a*b) mod p
    s_b = pow(A, b, p)

    print(s_a == s_b)
```
Kết quả:
```
True
```

Trong đó:
- [A]: $`A = g^a \mod p`$
- [B]: $`B = g^b \mod p`$
- [A]: $`s = B^a \mod p = g^{ab} \mod p`$
- [B]: $`s = A^b \mod p = g^{ab} \mod p`$

- => 2 `s` bằng nhau, từ A và B khó có thể tìm được ra a, b, và s

## Math
```
(ab) mod p = ( (a mod p) (b mod p) ) mod p 
```

# References
- Diffie-Hellman:
    - Secret Key Exchange (Diffie-Hellman) - Computerphile: https://www.youtube.com/watch?v=NmM9HA2MQGI
    - Diffie Hellman -the Mathematics bit- Computerphile: https://www.youtube.com/watch?v=Yjrfm_oRO0w
