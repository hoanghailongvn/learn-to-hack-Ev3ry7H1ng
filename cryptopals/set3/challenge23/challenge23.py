from MT19937 import MT19937_32
from time import time     

def invert_rightshift_xor(y: int, shift: int):
    original = 0

    for i in range(1, 32 + 1):
        # Lấy i bit đầu tiên của y
        temp_y = y >> (32 - i)
        temp_original = original >> (shift - 1)

        original = temp_y ^ temp_original

    return original

def invert_leftshift_and_xor(y: int, shift: int, and_const: int) -> int:
    original = 0

    for i in range(1, 32 + 1):
        # Lấy i bit cuối cùng của y và and_const
        temp_y = y & ((1 << i) - 1)
        temp_and_const = and_const & ((1 << i) - 1)

        # Lấy i - shift bit cuối cùng của original đã tính được
        if i - shift > 0:
            temp_original = original & ((1 << (i - shift)) - 1)
        else:
            temp_original = 0

        # invert
        original = temp_y ^ (temp_and_const & (temp_original << shift))

    return original

def untemper(y: int):
    y = invert_rightshift_xor(y, 18)
    y = invert_leftshift_and_xor(y, 15, 0xefc60000)
    y = invert_leftshift_and_xor(y, 7, 0x9d2c5680)
    y = invert_rightshift_xor(y, 11)

    return y

def attack():
    # just for this challenge, don't use time() for seed
    seed = int(time())
    rng = MT19937_32(seed)

    # Lấy 624 số ngẫu nhiên đầu tiên của rng, lưu vào mảng recv, đấy là thứ mà attacker có
    recv = []
    for i in range(624):
        recv.append(rng.extract_number())

    ####################################################
    
    # Khôi phục lại mảng MT thông qua đảo ngược 624 số ngẫu nhiên
    inverted_MT = []
    for i in range(624):
        inverted_MT.append(untemper(recv[i]))

    # Tạo clone_rng với MT thay bằng inverted_MT ở trên, thay index = 624 để kích hoạt twist
    clone_rng = MT19937_32()
    clone_rng.MT = inverted_MT
    clone_rng.index = 624

    print(all([rng.extract_number() == clone_rng.extract_number() for _ in range(624)]))

if __name__ == "__main__":
    attack()