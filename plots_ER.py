import pandas as pd
import numpy as np
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

in_dir = f'N{p["N"]}X{p["X"]}Ci{p["Ci"]}Cs{p["Cs"]}Cr{p["Cr"]}_avg_inn'

r=0.0
ps = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
ks = [pER*p["N"] for pER in ps]

dfs_k = []
avg_pay_k = []
avg_lvl_k = []
max_pay_k = []
max_lvl_k = []
max_ach_pay_k = []
n_items_k = []

for pER in ps:
    in_file_name = f'{in_dir}/avg_N_{p["N"]}_ER_{pER:.3f}_X_{p["X"]}_L_{p["L"]}_Cs_{p["Cs"]}_Ci_{p["Ci"]}_Cr_{p["Cr"]}_r_{r}__200.csv'
    df = pd.read_csv(in_file_name, sep='\t', index_col=0)
    dfs_k.append(df)
    avg_pay_k.append(np.mean(df['avg_payoff'].iloc[-200:]))
    avg_lvl_k.append(np.mean(df['avg_level'].iloc[-200:]))
    n_items_k.append(np.mean(df['n_items'].iloc[-200:]))



plt.figure(figsize=(15,10))
plt.rcParams.update({'font.size': 36})
plt.xlabel('k')
plt.ylabel(r'$\bar{Z}_{max}$')
plt.title("Mean group payoff")
plt.plot(ks, avg_pay_k, label='N=100', color='black', marker = 'o', markersize=12, linestyle = '--', linewidth=4)

plt.savefig("ER_plots/ER_zmax_inn.pdf", format="pdf", bbox_inches="tight")

plt.figure(figsize=(15,10))
plt.rcParams.update({'font.size': 36})
plt.xlabel('k')
plt.ylabel(r'$\bar{L}_{max}$')
plt.title("Mean group level")
plt.plot(ks, avg_lvl_k, label='ER', color='black', marker = 'o', markersize=12, linestyle = '--', linewidth=4)

plt.savefig("ER_plots/ER_lvl_inn.pdf", format="pdf", bbox_inches="tight")

plt.figure(figsize=(15,10))
plt.rcParams.update({'font.size': 36})
plt.xlabel('k', fontsize=36)
plt.ylabel(r'$\bar{T}_{max}$', fontsize=36)
plt.ylim((1000,100000))
plt.yscale('log')

plt.title("Mean number of traits")
plt.plot(ks, n_items_k, label='ER', color='black', marker = 'o', markersize=12, linestyle = '--', linewidth=4)

plt.savefig("ER_plots/ER_nitems_inn.pdf", format="pdf", bbox_inches="tight")