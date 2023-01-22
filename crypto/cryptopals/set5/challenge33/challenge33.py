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