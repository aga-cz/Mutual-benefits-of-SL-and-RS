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
rs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
copying_strategies = ['random', 'level', 'payoff']



pERs=[0.05]

pER=0.05
dfs_er_5 = {copying_strategy:[] for copying_strategy in copying_strategies}
avg_pay_er_5 = {copying_strategy:[] for copying_strategy in copying_strategies}
avg_lvl_er_5 = {copying_strategy:[] for copying_strategy in copying_strategies}
n_items_er_5 = {copying_strategy:[] for copying_strategy in copying_strategies}
for copying_strategy in copying_strategies:
    for r in rs:
        in_file_name = f'{copying_strategy}/{in_dir}/avg_N_{p["N"]}_ER_{pER:.3f}_X_{p["X"]}_L_{p["L"]}_Cs_{p["Cs"]}_Ci_{p["Ci"]}_Cr_{p["Cr"]}_r_{r}__200.csv'
        df = pd.read_csv(in_file_name, sep='\t', index_col=0)
        dfs_er_5[copying_strategy].append(df)
        avg_pay_er_5[copying_strategy].append(np.mean(df['avg_payoff'].iloc[-200:]))
        avg_lvl_er_5[copying_strategy].append(np.mean(df['avg_level'].iloc[-200:]))
        n_items_er_5[copying_strategy].append(np.mean(df['n_items'].iloc[-200:]))


colors=['red', 'green', 'blue']
markers=['o', 's', 'd']


dfs_payoff = [avg_pay_er_5]
dfs_level = [avg_lvl_er_5]
dfs_items = [n_items_er_5]

plt.figure(figsize=(40,15))
plt.rcParams.update({'font.size': 36})
# Plot average fitness
plt.subplot(1, 3, 1)
for i,cs in enumerate(copying_strategies):
    plt.plot(rs, avg_lvl_er_5[cs], label=f'{cs}, k=5', color=colors[i], marker=markers[i], markersize=12, linestyle='--', linewidth=4)
plt.xlabel('r')
plt.ylabel(r'$\bar{L}_{max}$')
plt.title("Mean group level, k=5")
#plt.legend()

plt.subplot(1, 3, 2)
for i,cs in enumerate(copying_strategies):
    plt.plot(rs, n_items_er_5[cs], label=f'{cs}, k=5', color=colors[i], marker=markers[i], markersize=12, linestyle='--', linewidth=4)
plt.xlabel('r')
plt.ylabel(r'$\bar{T}_{max}$')
plt.ylim((500,150000))
plt.yscale('log')
plt.title("Mean number of traits, k=5")
plt.legend()

plt.subplot(1, 3, 3)
for i,cs in enumerate(copying_strategies):
    plt.plot(rs, avg_pay_er_5[cs], label=f'{cs}, k=5', color=colors[i], marker=markers[i], markersize=12, linestyle='--', linewidth=4)
plt.xlabel('r')
plt.ylabel(r'$\bar{Z}_{max}$')
plt.title("Mean group payoff, k=5")
#plt.legend()

plt.tight_layout()
plt.savefig("copying_strategies_k5.jpg", format="jpg", bbox_inches="tight")
