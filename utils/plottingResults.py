import pandas as pd
import math
from matplotlib import pyplot as plt

data = """pollard_rho , 1e-05 , 4187
pollard_rho , 4e-06 , 739591
pollard_rho , 6e-06 , 11115289
pollard_rho , 7.2e-05 , 2327711059
pollard_rho , 6.9e-05 , 163602852613
pollard_rho , 0.000606 , 29701710176917
pollard_rho , 0.00786 , 6635466723344743
pollard_rho , 0.016611 , 205099888707518089
pollard_rho , 0.054596 , 62069657128430958631
pollard_rho , 0.169831 , 4073785567840969783807
pollard_rho , 0.266305 , 262057039170877491966281
pollard_rho , 0.212941 , 13139946109093875020707721
pollard_rho , 0.98041 , 3988357603469632857267605887
pollard_rho , 12.85561 , 316223818433693872338471512641
pollard_rho , 4.834053 , 30648897877627229430940290046153
pollard_rho , 152.202171 , 6203233481877206901609616193900549
pollard_rho , 926.147674 , 238632616642889836804093238314530001
QS_factor , 0.009853 , 4187
QS_factor , 0.005238 , 739591
QS_factor , 0.008106 , 11115289
QS_factor , 0.022024 , 2327711059
QS_factor , 0.078055 , 163602852613
QS_factor , 0.394955 , 29701710176917
QS_factor , 2.280267 , 6635466723344743
QS_factor , 7.400351 , 205099888707518089
QS_factor , 48.212217 , 62069657128430958631
QS_factor , 191.242869 , 4073785567840969783807
QS_factor , 1805.743942 , 262057039170877491966281
QS_factor , 3621.788578 , 13139946109093875020707721
"""

rows = [ [c.strip() for c in line.split(",")] for line in data.strip().splitlines() ]
df = pd.DataFrame(rows, columns=["algorithm","time","N"])

df["time"] = df["time"].astype(float)
# index per algorithm sequence order
df["index"] = df.groupby("algorithm").cumcount()

df["time"] = df["time"].astype(float)
df["N"] = df["N"].apply(int)  # keep as python int
df["log10N"] = df["N"].apply(lambda x: math.log10(x))

plt.figure(figsize=(8,6))
for alg, grp in df.groupby("algorithm"):
    grp_sorted = grp.sort_values("log10N")
    plt.plot(grp_sorted["log10N"], grp_sorted["time"], marker="o", label=alg)

plt.yscale("log")
plt.xlabel("Number of Digits")
plt.ylabel("CPU time (s) (log scale)")
plt.title("Runtime vs input size")
plt.legend()
plt.tight_layout()
plt.show()