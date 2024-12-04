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

rs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

ms = [3]
dfs_ba = {m:[] for m in ms}
avg_pay_ba = {m:[] for m in ms}
avg_lvl_ba = {m:[] for m in ms}
n_items_ba = {m:[] for m in ms}

for m in ms:
    for r in rs:
        in_file_name = f'BA/avg_N_{p["N"]}_m_{m}_X_{p["X"]}_L_{p["L"]}_Cs_{p["Cs"]}_Ci_{p["Ci"]}_Cr_{p["Cr"]}_r_{r}__200.csv'
        df = pd.read_csv(in_file_name, sep='\t', index_col=0)
        dfs_ba[m].append(df)
        avg_pay_ba[m].append(np.mean(df['avg_payoff'].iloc[-200:]))
        avg_lvl_ba[m].append(np.mean(df['avg_level'].iloc[-200:]))
        n_items_ba[m].append(np.mean(df['n_items'].iloc[-200:]))

print(avg_pay_ba[3])
pWSs=[0.0, 0.01, 0.1, 1.0]
dfs_ws = {ws:[] for ws in pWSs}
avg_pay_ws = {ws:[] for ws in pWSs}
avg_lvl_ws = {ws:[] for ws in pWSs}
n_items_ws = {ws:[] for ws in pWSs}
for pWS in pWSs:
    for r in rs:
        in_file_name = f'WS/avg_N_{p["N"]}_pWS_{pWS:.3f}_k_6_X_{p["X"]}_L_{p["L"]}_Cs_{p["Cs"]}_Ci_{p["Ci"]}_Cr_{p["Cr"]}_r_{r}__200.csv'
        df = pd.read_csv(in_file_name, sep='\t', index_col=0)
        dfs_ws[pWS].append(df)
        avg_pay_ws[pWS].append(np.mean(df['avg_payoff'].iloc[-200:]))
        avg_lvl_ws[pWS].append(np.mean(df['avg_level'].iloc[-200:]))
        n_items_ws[pWS].append(np.mean(df['n_items'].iloc[-200:]))

pERs=[0.06]
dfs_er = {er:[] for er in pERs}
avg_pay_er = {er:[] for er in pERs}
avg_lvl_er = {er:[] for er in pERs}
n_items_er = {er:[] for er in pERs}
for pER in pERs:
    for r in rs:
        in_file_name = f'ER/avg_N_{p["N"]}_ER_{pER:.3f}_X_{p["X"]}_L_{p["L"]}_Cs_{p["Cs"]}_Ci_{p["Ci"]}_Cr_{p["Cr"]}_r_{r}__200.csv'
        df = pd.read_csv(in_file_name, sep='\t', index_col=0)
        dfs_er[pER].append(df)
        avg_pay_er[pER].append(np.mean(df['avg_payoff'].iloc[-200:]))
        avg_lvl_er[pER].append(np.mean(df['avg_level'].iloc[-200:]))
        n_items_er[pER].append(np.mean(df['n_items'].iloc[-200:]))


dfs_payoff = [avg_pay_ba[ms[0]]] + [avg_pay_ws[pWS] for pWS in pWSs] + [avg_pay_er[pERs[0]]]
dfs_level= [avg_lvl_ba[ms[0]]] + [avg_lvl_ws[pWS] for pWS in pWSs] + [avg_lvl_er[pERs[0]]]
dfs_items = [n_items_ba[ms[0]]] + [n_items_ws[pWS] for pWS in pWSs] + [n_items_er[pERs[0]]]

labels = ['BA', 'WS, $p_{WS}=0$', 'WS, $p_{WS}=0.01$', 'WS, $p_{WS}=0.1$', 'WS, $p_{WS}=1.0$', 'ER']
colors=['red', 'green', 'blue', 'yellow', 'orange', 'black']
markers=['o', '+' , '^', 'X', '2', 's']


plt.figure(figsize=(40,15))
plt.rcParams.update({'font.size': 36})
# Plot average fitness
plt.subplot(1, 3, 1)
for i, df in enumerate(dfs_level):
    plt.plot(rs, df, label=labels[i], color=colors[i], marker=markers[i], markersize=12, linestyle='--', linewidth=4)
plt.xlabel('r')
plt.ylabel(r'$\bar{L}_{max}$')
plt.title("Mean group level, k=6")
#plt.legend()

plt.subplot(1, 3, 2)
for i, df in enumerate(dfs_items):
    plt.plot(rs, df, label=labels[i], color=colors[i], marker=markers[i], markersize=12, linestyle='--', linewidth=4)
plt.xlabel('r')
plt.ylabel(r'$\bar{T}_{max}$')
plt.ylim((500,15000))
plt.yscale('log')
plt.title("Mean number of traits, k=6")
plt.legend()

plt.subplot(1, 3, 3)
for i, df in enumerate(dfs_payoff):
    plt.plot(rs, df, label=labels[i], color=colors[i], marker=markers[i], markersize=12, linestyle='--', linewidth=4)

plt.xlabel('r')
plt.ylabel(r'$\bar{Z}_{max}$')
plt.title("Mean group payoff, k=6")
#plt.legend()

plt.tight_layout()

plt.savefig("topologies_k6.jpg", format="jpg", bbox_inches="tight")