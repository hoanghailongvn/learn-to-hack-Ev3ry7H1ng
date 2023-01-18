from random import randint
from MT19937 import MT19937_32
from time import sleep, time

min_sleep_time = 40
max_sleep_time = 1000

def routine():
    sleep(randint(min_sleep_time, max_sleep_time))
    seed = int(time())
    sleep(randint(min_sleep_time, max_sleep_time))
    rng = MT19937_32(seed)

    print(f"used seed: {seed}")
    return rng.extract_number()

def attack():
    recv = routine()
    now = time()

    for i in range(max_sleep_time * 2):
        bruteforce_seed = int(now - i)
        rng = MT19937_32(bruteforce_seed)
        if (rng.extract_number() == recv):
            print(f"found seed: {bruteforce_seed}")
            break

if __name__ == "__main__":
    attack()