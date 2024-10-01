import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import seaborn as sns

p = {
    'N': 100,
    'T': 20000,
    'X': 100,
    'L': 1000,
    'Cs': 5,
    'Ci': 10,
    'Cr': 1,
}

in_dir = f'NX{p["X"]}Ci{p["Ci"]}Cs{p["Cs"]}Cr{p["Cr"]}_N'

ns = [10, 20, 50, 100, 200, 500, 1000]
ns_lim = [10, 100, 1000]
r=0.0
pER=1.0

dfs_n = {n:[] for n in ns}
avg_pay_n = {n:[] for n in ns}

for n in ns:
    in_file_name = f'{in_dir}/avg_N_{n}_ER_{pER:.3f}_X_{p["X"]}_L_{p["L"]}_Cs_{p["Cs"]}_Ci_{p["Ci"]}_Cr_{p["Cr"]}_r_{r}__200.csv'
    df = pd.read_csv(in_file_name, sep='\t', index_col=0)
    dfs_n[n].append(df)
    avg_pay_n[n].append(np.mean(df['avg_payoff'].iloc[-n*10:]))

log_ind_list = [i for i in range(10)] + [12, 15] + [i for i in range(10,50,5)] + [i for i in range(50,100,10)] \
               + [i for i in range(100,500,50)] + [120] + [i for i in range(500,1000,100)] \
                + [i for i in range(1000,5000,500)] + [1200] + [i for i in range(5000,10000,1000)] + [11000, 12000,15000,19999]

plt.figure(figsize=(20, 10))

plt.rcParams.update({'font.size': 32})
plt.xlabel('time')
plt.ylabel(r'$\bar{Z}$')

#plt.xlim([1, 20000])
plt.xscale('log')
markers=['o', 's', '^']
plt.title("Mean group payoff in time")
for i,n in enumerate(ns_lim):
    plt.plot(np.array(dfs_n[n][0].index[log_ind_list]), dfs_n[n][0]['avg_payoff'].values[log_ind_list], label=f'N={n}',  marker= markers[i], markersize=10, linestyle = 'None')

plt.legend()
plt.savefig("CG_plots/CG_time_inn.pdf", format="pdf", bbox_inches="tight")
#plt.show()



plt.figure(figsize=(20,10))
plt.rcParams.update({'font.size': 32})
plt.xlabel('N')
plt.ylabel(r'$\bar{Z}_{max}$')
plt.title("Mean group payoff")

plt.xscale('log')

fitxy = np.polyfit(np.log(ns), list(avg_pay_n.values()), 1)

plt.plot(avg_pay_n.keys(), avg_pay_n.values(), label='CG', color='red', marker='D', markersize=12, linestyle = 'None')
plt.plot(avg_pay_n.keys(), [fitxy[0]*np.log(n)+fitxy[1] for n in ns], label=r'$a\log(x)+b$', color='black', linewidth=2)

plt.legend()
plt.savefig("CG_plots/CG_N_inn.pdf", format="pdf", bbox_inches="tight")
#plt.show()

print(f'a = {fitxy[0]}')
print(f'b = {fitxy[1]}')