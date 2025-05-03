import time

import matplotlib.pyplot as plt

from priorArt import fermat
from priorArt import PollarRho
from priorArt import trial
import QS

def benchmark_algorithm(function, data):
        start=time.time()
        res=function(data)
        end=time.time()
        return round(end-start,6),0

def evaluate(tests):
    functions = {
        # 'Trial Division': trial.trial_division,
        # 'Fermat': fermat.fermat_factor,
        # 'Pollard Rho': PollarRho.pollard_rho,
        'Quadratic Sieve':QS.factor
    }

    input_sizes = [len(str(data)) for data in tests]
    execution_times = {}

    for name, function in functions.items():
        times = []
        for data in tests:
            exec_time, _ = benchmark_algorithm(function, data)
            times.append(exec_time)
            print("Completed:",data)
        execution_times[name] = times

    plt.figure(figsize=(10, 6))
    for name, times in execution_times.items():
        plt.plot(input_sizes, times, marker='o', label=name)

    plt.title('Execution Time vs Input Size')
    plt.xlabel('Number of Digits')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# tests = [
#     7081,  # 4-digit, 97*73
#     107531,  # 6-digit, 367*293
#     12086519,  # 8-digit, 8803*1373
#     7255104209,  # 10-digit, 90833*79873
#     229893344719,  # 12-digit, 360509*637691
#     22325207278849,  # 14-digit, 2522227*8851387
#     2154835075935523,  # 16-digit, 54630089*39444107
#     249191903933459161,  # 18-digit, 875835781*284518981
#     50682718434162113833,  # 20-digit, 5164753303*9813192511
#     6363931628526038586769,  # 22-digit, 74349983581*85594257349
#     305587913088118865919593,  # 24-digit, 579960509363*526911588211
# ]
tests=[
4187,  #4-digit, 79*53
739591,  #6-digit, 857*863
11115289,  #8-digit, 3821*2909
2327711059,  #10-digit, 81953*28403
163602852613,  #12-digit, 804653*203321
29701710176917,  #14-digit, 4772993*6222869
6635466723344743,  #16-digit, 73770791*89947073
205099888707518089,  #18-digit, 241370089*849732001
62069657128430958631,  #20-digit, 6602693281*9400657351
4073785567840969783807,  #22-digit, 94171131169*43259388703
262057039170877491966281,  #24-digit, 827119795493*316830815317
# 13139946109093875020707721,  #26-digit, 2063150648189*6368873800189
# 3988357603469632857267605887,  #28-digit, 52028570660707*76657066546741
# 316223818433693872338471512641,  #30-digit, 324485262464513*974539848225857
# 30648897877627229430940290046153,  #32-digit, 6302640799845809*4862866035198617
# 6203233481877206901609616193900549,  #34-digit, 67223988358249937*92277081937164277
# 238632616642889836804093238314530001,  #36-digit, 891883853489153401*267560193750936601
# 56235376781403969985933572935643663349,  #38-digit, 5649261955897936913*9954464356656919973
# 3260307402334386784081127285678456118757,  #40-digit, 84109641066108696911*38762588462027112587
]
evaluate(tests)