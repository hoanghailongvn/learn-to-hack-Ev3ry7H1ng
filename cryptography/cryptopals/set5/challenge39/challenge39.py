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