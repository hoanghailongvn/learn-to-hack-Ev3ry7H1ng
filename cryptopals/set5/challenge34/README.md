# **[set 5 - challenge 34](https://cryptopals.com/sets/5/challenges/34): Implement a MITM key-fixing attack on Diffie-Hellman with parameter injection**

Use the code you just worked out to build a protocol and an "echo" bot. You don't actually have to do the network part of this if you don't want; just simulate that. The protocol is:

```text
A->B
Send "p", "g", "A"
B->A
Send "B"
A->B
Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
B->A
Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv
```

(In other words, derive an AES key from DH with SHA1, use it in both directions, and do CBC with random IVs appended or prepended to the message).

Now implement the following MITM attack:

```text
A->M
Send "p", "g", "A"
M->B
Send "p", "g", "p"
B->M
Send "B"
M->A
Send "p"
A->M
Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
M->B
Relay that to B
B->M
Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv
M->A
Relay that to A
```

M should be able to decrypt the messages. "A" and "B" in the protocol --- the public keys, over the wire --- have been swapped out with "p". Do the DH math on this quickly to see what that does to the predictability of the key.

Decrypt the messages from M's vantage point as they go by.

Note that you don't actually have to inject bogus parameters to make this attack work; you could just generate Ma, MA, Mb, and MB as valid DH parameters to do a generic MITM attack. But do the parameter injection attack; it's going to come up again.

## Man in the middle

In cryptography and computer security, a man-in-the-middle, monster-in-the-middle, machine-in-the-middle, monkey-in-the-middle (lmao),meddler-in-the-middle, manipulator-in-the-middle (MITM), person-in-the-middle (PITM) or adversary-in-the-middle (AiTM) attack is a cyberattack where the attacker secretly relays and possibly alters the communications between two parties who believe that they are directly communicating with each other, as the attacker has inserted themselves between the two parties.

## MITM diffie hellman

- [A] ----(p, g, A)----> [Eve] ----(p, g, p)----> [B]: Change A to p:
  - [B]: $s = g^A \mod p = g^p \mod p = 0$
- [B] ----(B)----> [Eve] ----(p)----> [A]: Change B to p:
  - [A]: $s = g^B \mod p = g^p \mod p = 0$

Now, `s` on both sides are 0, and the mitm know that.

## Simulation

[here](./challenge34.py)

result:

```text

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

## References
