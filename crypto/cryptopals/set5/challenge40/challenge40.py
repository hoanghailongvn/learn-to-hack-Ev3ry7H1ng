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