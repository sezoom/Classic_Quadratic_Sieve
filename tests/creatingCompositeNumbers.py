import random
import math
import QS

# helper: Miller–Rabin from QS
is_prime = QS.is_prime
# simple prime‐generator for k‐digit primes
def gen_prime(digits: int) -> int:
    lower, upper = 10**(digits-1), 10**digits - 1
    while True:
        p = random.randrange(lower, upper) | 1
        if is_prime(p):
            return p

# generate composites p*q of total digit‐length 4,6,8,…,40
digit_tests = {"n":[],
               "p":[],
               "q":[]}
for total_digits in range(4, 41, 2):
    # split roughly half/half
    a = total_digits // 2
    b = total_digits - a
    p = gen_prime(a)
    q = gen_prime(b)
    # ensure p*q has exactly total_digits
    n = p * q
    if len(str(n)) != total_digits:
        # if we got unlucky (very rare), retry that size
        while len(str(n)) != total_digits:
            p = gen_prime(a)
            q = gen_prime(b)
            n = p * q
    digit_tests["n"].append(n)
    digit_tests["p"].append(p)
    digit_tests["q"].append(q)


print("tests=[")
for i in range(len(digit_tests['n'])):
    print(f"{digit_tests['n'][i]},  #{len(str(digit_tests['n'][i]))}-digit, {digit_tests['p'][i]}*{digit_tests['q'][i]}")
print("]")
