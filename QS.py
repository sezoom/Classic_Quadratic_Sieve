
import math
import gc
import random
import sys

# 1- Miller–Rabin Primality Test
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    small = [2,3,5,7,11,13,17,19,23,29]
    for p in small:
        if n == p:
            return True
        if n % p == 0:
            return False
    d, s = n-1, 0
    while not (d & 1):
        d >>= 1; s += 1
    bases = [2,325,9375,28178,450775,9780504,1795265022]
    def trial(a):
        x = pow(a, d, n)
        if x in (1, n-1):
            return True
        for _ in range(s-1):
            x = (x*x) % n
            if x == n-1:
                return True
        return False
    for a in bases:
        if a % n == 0:
            continue
        if not trial(a):
            return False
    return True

# 2- Pollard’s Rho Fallback
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
            return d

# 3- Tonelli–Shanks √mod p
def tonelli_shanks(a: int, p: int) -> list:
    if p == 2:
        return [a & 1]
    if pow(a, (p-1)//2, p) != 1:
        raise ValueError("no square root")
    if p % 4 == 3:
        x = pow(a, (p+1)//4, p)
        return [x, p-x]
    # factor p-1 = q·2^s
    q, s = p-1, 0
    while not (q & 1):
        q >>= 1; s += 1
    # find non-residue z
    z = 2
    while pow(z, (p-1)//2, p) != p-1:
        z += 1
    c = pow(z, q, p)
    x = pow(a, (q+1)//2, p)
    t = pow(a, q, p)
    m = s
    while t != 1:
        t2 = t
        for i in range(1, m):
            t2 = pow(t2, 2, p)
            if t2 == 1:
                break
        b = pow(c, 1 << (m-i-1), p)
        x = (x * b) % p
        t = (t * b * b) % p
        c = pow(b, 2, p)
        m = i
    return [x, p-x]

# 4- Simple Sieve to list all primes ≤ n
def primes_up_to(n: int) -> list:
    sieve = [True] * (n+1)
    sieve[0:2] = [False, False]
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i,v in enumerate(sieve) if v]

# 5- Factor m entirely over a given prime base[]
def factor_over_base(m: int, base: list) -> dict:
    e = {}
    if m < 0:
        e[-1] = 1
        m = -m
    for p in base:
        if p < 2:
            continue
        cnt = 0
        while m % p == 0:
            m //= p
            cnt += 1
        if cnt:
            e[p] = cnt
    return e if m == 1 else {}

# 6- Find nontrivial GF(2) dependency via bitmask GE
def find_dependency(mat: list) -> list:
    n = len(mat)
    if n == 0:
        return None
    rows = []
    comb = []
    for i,row in enumerate(mat):
        mask = 0
        for j,bit in enumerate(row):
            if bit:
                mask |= 1<<j
        rows.append(mask)
        comb.append(1<<i)
    piv = {}
    for rv, cv in zip(rows, comb):
        v, c = rv, cv
        for j in sorted(piv.keys(), reverse=True):
            if (v>>j)&1:
                v ^= piv[j][0]
                c ^= piv[j][1]
        if v == 0:
            return [(c>>i)&1 for i in range(n)]
        top = v.bit_length() - 1
        piv[top] = (v, c)
    return None

# 7- Quadratic Sieve with retry & fallback
def QS_factor(n: int, B=None, M=None):
    try:
        if n < 2:
            return None
        if is_prime(n):
            return (n,)
        ln = math.log(n)
        B0 = max(5, int(math.exp(math.sqrt(ln*math.log(ln)))))
        M0 = B0*2
        B = B or B0
        M = M or M0

        for _ in range(3):
            # build factor base
            FB = [-1]
            for p in primes_up_to(B):
                if pow(n, (p-1)//2, p) == 1:
                    FB.append(p)

            r0 = math.isqrt(n)
            if r0*r0 < n:
                r0 += 1
            xs = list(range(-M, M+1))
            Q = [(r0+x)**2 - n for x in xs]
            logs = [math.log(abs(q)) if q else 0 for q in Q]

            # sieve
            for p in FB:
                if p < 2:
                    continue
                try:
                    roots = tonelli_shanks(n % p, p)
                except ValueError:
                    continue
                for r in roots:
                    off = (r - r0) % p
                    start = (-M - off + p-1)//p
                    end   = (M-off)//p
                    for k in range(start, end+1):
                        idx = off + k*p + M
                        while 0 <= idx < len(Q) and Q[idx] % p == 0:
                            Q[idx] //= p
                            logs[idx] -= math.log(p)

            # collect relations
            rels = []
            mat  = []
            for i,lg in enumerate(logs):
                if abs(lg) < 1e-6:
                    val = (r0+xs[i])**2 - n
                    fmap = factor_over_base(val, FB)
                    if fmap:
                        mat.append([fmap.get(p,0)%2 for p in FB])
                        rels.append(xs[i])
                if len(mat) > len(FB):
                    break

            if len(mat) > len(FB):
                break
            B *= 2; M *= 2

        # fallback to Pollard’s Rho if not enough relations
        if len(mat) <= len(FB):
            raise ValueError("not enough relations found")
            p = pollard_rho(n)
            return (p, n//p)

        dep = find_dependency(mat)
        if not dep:
            p = pollard_rho(n)
            print('PollardRho_',end='')
            return (p, n//p)

        # form X and Y
        X = 1; Y = 1
        for bit, x in zip(dep, rels):
            if bit:
                X = (X*(r0+x)) % n
                fmap = factor_over_base((r0+x)**2 - n, FB)
                for p,e in fmap.items():
                    if p>0:
                        Y = (Y*pow(p, e//2, n)) % n

        g = math.gcd(X-Y, n)
        if g in (1,n):
            g = math.gcd(X+Y, n)
        if 1 < g < n:
            return (g, n//g)
        # last resort
        p = pollard_rho(n)
        return (p, n//p)
    finally:
        # deleting large lists for saving memory for each execution
        for name in ("FB", "xs", "Q", "logs", "mat", "rels"):
            if name in locals():
                del locals()[name]

        # asking the GC to free cyclic garbage
        gc.collect()

# CLI entry
if __name__ == '__main__':
    if len(sys.argv)<2:
        print("Usage: python QS.py <n1> [n2 …]")
        sys.exit(1)
    for arg in sys.argv[1:]:
        n = int(arg)
        if is_prime(n):
            print(f"{n} is prime.")
        else:
            f = QS_factor(n)
            if f and len(f)==2:
                print(f"{n} = {f[0]} * {f[1]}")
            else:
                print(f"Failed to factor {n}")