# **[set 5 - challenge 39](https://cryptopals.com/sets/5/challenges/39): Implement RSA**

There are two annoying things about implementing RSA. Both of them involve key generation; the actual encryption/decryption in RSA is trivial.

First, you need to generate random primes. You can't just agree on a prime ahead of time, like you do in DH. You can write this algorithm yourself, but I just cheat and use OpenSSL's BN library to do the work.

The second is that you need an "invmod" operation (the multiplicative inverse), which is not an operation that is wired into your language. The algorithm is just a couple lines, but I always lose an hour getting it to work.

I recommend you not bother with primegen, but do take the time to get your own EGCD and invmod algorithm working.

Now:

- Generate 2 random primes. We'll use small numbers to start, so you can just pick them out of a prime table. Call them "p" and "q".
- Let n be p * q. Your RSA math is modulo n.
- Let et be (p-1)*(q-1) (the "totient"). You need this value only for keygen.
- Let e be 3.
- Compute d = invmod(e, et). invmod(17, 3120) is 2753.
- Your public key is [e, n]. Your private key is [d, n].
- To encrypt: c = m**e%n. To decrypt: m = c**d%n
- Test this out with a number, like "42".
- Repeat with bignum primes (keep e=3).
Finally, to encrypt a string, do something cheesy, like convert the string to hex and put "0x" on the front of it to turn it into a number. The math cares not how stupidly you feed it strings.

## RSA

[RSA (Rivest–Shamir–Adleman)](https://en.wikipedia.org/wiki/RSA_(cryptosystem)): is a public-key cryptosystem.

The security of RSA relies on the practical difficulty of factoring the product of two large prime numbers, the "factoring problem".

## Math

a perfect rsa explanation video by Khan Academy: [link](https://www.youtube.com/watch?v=wXB-V_Keiu8)

Euler's totient function:

- In number theory, Euler's totient function counts the positive integers up to a given integer n that are relatively prime to n.
- If n is a prime number => Phi(n) = n - 1
- $Phi(A \times B) = Phi(A) \times Phi(B)$
- $m^{phi(n)} = 1 \mod n$ => $m^{k\times phi(n)+1} = m \mod n$

generate public and private key:

- Choose two large prime numbers p and q
- $n = p \times q$
- $Phi(n) = Phi(p) \times Phi(q) = (p-1)(q-1)$
- Let $e = 3$
- $d = \frac{k\times Phi(n) + 1}{e}$, with k such that the numerator is divisible by the denominator. This operation is invmod [Modular multiplicative inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse)

- Public key: [e, n], Private key: [d, n]
- Encrypt: $c = m ^ e \mod n$
- Decrypt: $m = c ^ d \mod n$

Prove: $m = c ^ d \mod n$:

$m = c ^ d \mod n$\
=> $m = (m ^ e \mod n) ^ d \mod n$\
=> $m = (m)^{ed} \mod n$\
=> $m = (m)^{k\times Phi(n) + 1} \mod n$\
=> $m = m \mod n$ (OK)

## Implement

in python version 3.8+:

- we can use pow function to calculate invmod
- getPrime function in Crypto.Util.number module

```python
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

## References

- RSA:
  - Wikipedia: <https://en.wikipedia.org/wiki/RSA_(cryptosystem)>
  - Computerphile: <https://www.youtube.com/watch?v=JD72Ry60eP4>
  - Khanacademy: <https://www.youtube.com/watch?v=wXB-V_Keiu8>
