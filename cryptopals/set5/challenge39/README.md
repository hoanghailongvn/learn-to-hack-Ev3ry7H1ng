# **[set 5 - challenge 39](https://cryptopals.com/sets/5/challenges/39): Implement RSA**

## RSA
[RSA (Rivest–Shamir–Adleman)](https://en.wikipedia.org/wiki/RSA_(cryptosystem)): là một public-key cryptosystem, trong đó: encryption key (public) khác biệt với decryption key (private). Hai key được tạo ra dựa trên 2 số nguyên tố.

Sức mạnh của RSA dựa vào độ khó của `phân tích thừa số nguyên tố` hay là `factoring`.

## Math
Một video rất hay về rsa của Khanacademy: [link](https://www.youtube.com/watch?v=wXB-V_Keiu8)

Đầu tiên, tìm hiểu về Phi function:
- Hàm Phi(N) tính số số hạng từ 0 đến N mà không có chung thừa số nguyên tố với N => Nếu N là số nguyên tố => Phi(N) = N - 1
- Phi(A * B) = Phi(A) * Phi(B)
- $`m^{phi(n)} = 1 \mod n`$ => $`m^{k\times phi(n)+1} = m \mod n`$

Tạo public và private key:
- p, q là hai số nguyên tố ngẫu nhiên
- $`n = p \times q`$
- $`Phi(n) = Phi(p) \times Phi(q) = (p-1)(q-1)`$
- Let $`e = 3`$
- $`d = \frac{k\times Phi(n) + 1}{e}`$, với k sao cho tử chia hết cho mẫu. Phép toán này chính là invmod [Modular multiplicative inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse)

- Public key: [e, n], Private key: [d, n]
- Encrypt: $`c = m ^ e \mod n`$
- Decrypt: $`m = c ^ d \mod n`$

Chứng minh: $`m = c ^ d \mod n`$:

$`m = c ^ d \mod n`$\
=> $`m = (m ^ e \mod n) ^ d \mod n`$\
=> $`m = (m)^{ed} \mod n`$\
=> $`m = (m)^{k\times Phi(n) + 1} \mod n`$\
=> $`m = m \mod n`$ (OK)

## Implement
Trong python 3.8+:
- hàm invmod đã có trong hàm pow
- hàm getPrime đã có trong Crypto.Util.number
```
from Crypto.Util.number import getPrime

# Generate 2 random primes. (1024 bit) 
p = getPrime(1024)
q = getPrime(1024)

# Your RSA math is modulo n
n = p * q

# You need this value only for keygen. 
phi = (p - 1) * (q - 1)

# Let e be 3. 
e = 3

# Compute d = invmod(e, phi).
d = pow(e, -1, phi)

# encrypt & decrypt
s = b"secret message"
encrypted = pow(int.from_bytes(s, byteorder='big'), e, n)
decrypted = pow(encrypted, d, n)
print(decrypted.to_bytes(14, byteorder='big'))
```

# References
- RSA:
    - Wikipedia: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
    - Computerphile: https://www.youtube.com/watch?v=JD72Ry60eP4
    - Khanacademy: https://www.youtube.com/watch?v=wXB-V_Keiu8