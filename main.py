
import QS
from priorArt import fermat
from priorArt import PollarRho
from priorArt import trial


if __name__ == '__main__':

    tests = [
        7081,  # 4-digit, 97*73
        107531,  # 6-digit, 367*293
        12086519,  # 8-digit, 8803*1373
        7255104209,  # 10-digit, 90833*79873
        229893344719,  # 12-digit, 360509*637691
        # 22325207278849,  # 14-digit, 2522227*8851387
        # 2154835075935523,  # 16-digit, 54630089*39444107
        # 249191903933459161,  # 18-digit, 875835781*284518981
        # 50682718434162113833,  # 20-digit, 5164753303*9813192511
        # 6363931628526038586769,  # 22-digit, 74349983581*85594257349
        # 305587913088118865919593,  # 24-digit, 579960509363*526911588211
        # 46132832683439013113069759,  # 26-digit, 8838723153839*5219400119281
        # 3916559163006939144510093731,  # 28-digit, 40412684430431*96914105514301
        # 370624806691402005928662102881,  # 30-digit, 533251103511899*695028672703219
    ]


    ##--------------Testing Quadratic Sieve Factorization---------
    print("QUADRATIC SIEVE FACTORING:")
    for n in tests:
        print(f"Factoring {n}: ", end='')
        if QS.is_prime(n):
            print("prime")
            continue
        res = QS.QS_factor(n)
        if not res or len(res) != 2:
            print("FAILED")
        else:
            p, q = res
            if p*q == n:
                print(f"OK → {p} * {q}")
            else:
                print(f"WRONG → {p} * {q} != {n}")

    ##--------------Testing Pollar Rho Factorization---------

    print("\nPollar Rho FACTORING:")
    for n in tests:
        print(f"Factoring {n}:", end=' ')
        res = PollarRho.pollard_rho(n)
        if res:
            p, q = res
            print(f"{p} * {q}")
        else:
            print("failed")
    ##--------------Testing Fermat Factorization---------

    print("\nFERMAT FACTORING:")
    for n in tests:
        print(f"Factoring {n}:", end=' ')
        res = fermat.fermat_factor(n)
        if res:
            p, q = res
            print(f"{p} * {q}")
        else:
            print("failed")


    ##--------------Testing Trial division Factorization---------
    print("\n Trial FACTORING:")
    for N in tests:
        print(f"Factoring {N}:", end=' ')
        result = trial.trial_division(N)
        if result is None:
            print(f"{N}: invalid input")
        elif len(result) == 1:
            print(f"{N} is prime.")
        else:
            p, q = result
            print(f" {p} * {q}")
