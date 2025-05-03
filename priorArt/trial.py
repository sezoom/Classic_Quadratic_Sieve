import math

# implementation of trial-division factorization
def trial_division(n: int) -> tuple:
    if n < 2:
        return None
    # handle factor 2 separately for speed
    if n % 2 == 0:
        return (2, n // 2)
    # check odd divisors from 3 to √n
    limit = math.isqrt(n)
    p = 3
    while p <= limit:
        if n % p == 0:
            return (p, n // p)
        p += 2
    # no divisor found → n is prime
    return (n,)
