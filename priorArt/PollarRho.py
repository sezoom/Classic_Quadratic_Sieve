import random
import math
# implementation of pollar-rho algorithm
# x=f(x) mod n
# y=f(f(y)) mod n
# factor = gcd(x-y,n)
def pollard_rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    while True:
        x = random.randrange(2, n-1)
        c = random.randrange(1, n-1)
        y = x
        d = 1
        while d == 1:
            x = (x*x + c) % n
            y = (y*y + c) % n
            y = (y*y + c) % n
            d = math.gcd(abs(x-y), n)
            if d == n:
                break
        if 1 < d < n:
            return (d,n//d)