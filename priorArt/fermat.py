import math
import random

# implementation of Fermat's factorization method
def fermat_factor(n: int) -> tuple:
    # handle trivial cases
    if n <= 0:
        return None
    # even factor
    if n % 2 == 0:
        return (2, n // 2)
    # start at ceil(sqrt(n))
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    # search for b^2 = a^2 - n
    while True:
        b2 = a*a - n
        b = math.isqrt(b2)
        if b*b == b2:
            # found a^2 - b^2 = n
            p = a - b
            q = a + b
            if p in (1, n):
                # trivial factor, failure
                return None
            return (p, q)
        a += 1

