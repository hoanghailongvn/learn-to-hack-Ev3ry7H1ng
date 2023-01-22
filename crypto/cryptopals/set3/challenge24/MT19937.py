class MT19937_32:
    # coefficients for MT19937 32-bit
    w, n, m, r = 32, 624, 397, 31
    a = 0x9908b0df
    u, d = 11, 0xffffffff
    s, b = 7, 0x9d2c5680
    t, c = 15, 0xefc60000
    l = 18
    f = 1812433253

    lower_mask = (1 << r) - 1
    upper_mask = (1 << w) - 1 - lower_mask

    def __init__(self, seed=5489):
        # seed: 5489 is used in reference C code
        self.MT = [0] * self.n
        self.index = self.n + 1

        self.seed_mt(seed)

    def seed_mt(self, seed: int):
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n):
            self.MT[i] = (self.f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (self.w - 2))) + i) & ((1 << self.w) - 1)

    def twist(self):
        for i in range(self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0: # lowest bit of x is 1
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0
    
    def extract_number(self):
        if self.index >= self.n:
            if self.index > self.n:
                assert "Generator was never seeded"
            self.twist()
        
        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)

        self.index = self.index + 1

        return y & ((1 << self.w) - 1)