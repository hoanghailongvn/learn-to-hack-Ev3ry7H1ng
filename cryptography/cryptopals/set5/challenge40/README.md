# **[set 5 - challenge 40](https://cryptopals.com/sets/5/challenges/40): Implement an E=3 RSA Broadcast attack**

Assume you're a Javascript programmer. That is, you're using a naive handrolled RSA to encrypt without padding.

Assume you can be coerced into encrypting the same plaintext three times, under three different public keys. You can; it's happened.

Then an attacker can trivially decrypt your message, by:

Capturing any 3 of the ciphertexts and their corresponding pubkeys
Using the CRT to solve for the number represented by the three ciphertexts (which are residues mod their respective pubkeys)
Taking the cube root of the resulting number
The CRT says you can take any number and represent it as the combination of a series of residues mod a series of moduli. In the three-residue case, you have:

```text
result =
  (c_0 * m_s_0 * invmod(m_s_0, n_0)) +
  (c_1 * m_s_1 * invmod(m_s_1, n_1)) +
  (c_2 * m_s_2 * invmod(m_s_2, n_2)) mod N_012
```

where:

```text
 c_0, c_1, c_2 are the three respective residues mod
 n_0, n_1, n_2

 m_s_n (for n in 0, 1, 2) are the product of the moduli
 EXCEPT n_n --- ie, m_s_1 is n_0 * n_2

 N_012 is the product of all three moduli
```

To decrypt RSA using a simple cube root, leave off the final modulus operation; just take the raw accumulated result and cube-root it.

## Håstad's broadcast attack

If a message is encrypted `e` times, we can use the [Chinese remainder theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem) to calculate a ciphertext

$
c = m^e \mod (N_1N_2...N_e)
$

that $m < N_i \forall i$:\
=> $m^e < N_1N_2...N_e$\
=> $c = m^e \mod (N_1N_2...N_e)$ <=> $c = m^e$\
=> $m = \sqrt[e]{c}$

## Implement

Python code:

```python
from Crypto.Util.number import getPrime

e = 5
s = 401923

n = [] # n = p * q
c = [] # ciphertext
for i in range(e):
    n.append(getPrime(1024) * getPrime(1024))
    c.append(pow(s, e, n[i]))



## attacker side
# n, c, e

# result = (
#     c0 * n1 * n2 * pow(n1 * n2, -1, n0) +
#     c1 * n0 * n2 * pow(n0 * n2, -1, n1) +
#     c2 * n0 * n1 * pow(n0 * n1, -1, n2)
# ) % (n0 * n1 * n2)

result = 0
for i in range(e):
    # --- calculate (n[0] * n[1] * ... * n[e]) but except n[i]
    temp = 1
    for j in range(e):
        if j != i:
            temp *= n[j]
    # --- end ---
    result += c[i] * temp * pow(temp, -1, n[i])

# --- calculate (n[0] * n[1] * ... * n[e]) ---
temp = 1
for i in range(e):
    temp *= n[i]
# --- end ---

result %= temp

# now result = m^e \mod (N_1N_2...N_e)

plaintext = round(pow(result, 1/e))
print(plaintext)
```

## References

- Håstad's broadcast attack:
  - Wikipedia: <https://en.wikipedia.org/wiki/Coppersmith>'s_attack#H%C3%A5stad's_broadcast_attack
  - Youtube: <https://www.youtube.com/watch?v=aS57JCzJw_o>
- Chinese remainder theorem:
  - Wikipedia: <https://en.wikipedia.org/wiki/Chinese_remainder_theorem>
