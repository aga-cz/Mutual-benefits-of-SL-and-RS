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

ps = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

ps_lim = [0.01, 0.05, 0.1, 1.0]
ks = ['k=1', 'k=5', 'k=10', 'CG']
rs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

colors=['lightgrey', 'darkgrey', 'dimgrey', 'black']
markers=['o', 's', '^', 'X']

dfs_er = {er:[] for er in ps}
avg_pay_er = {er:[] for er in ps}
avg_lvl_er = {er:[] for er in ps}
max_pay_er = {er:[] for er in ps}
max_lvl_er = {er:[] for er in ps}
max_ach_pay_er = {er:[] for er in ps}
n_items_er = {er:[] for er in ps}
for pER in ps:
    for r in rs:
        in_file_name = f'{in_dir}/avg_N_{p["N"]}_ER_{pER:.3f}_X_{p["X"]}_L_{p["L"]}_Cs_{p["Cs"]}_Ci_{p["Ci"]}_Cr_{p["Cr"]}_r_{r}__200.csv'
        df = pd.read_csv(in_file_name, sep='\t', index_col=0)
        dfs_er[pER].append(df)
        avg_pay_er[pER].append(np.mean(df['avg_payoff'].iloc[-200:]))
        avg_lvl_er[pER].append(np.mean(df['avg_level'].iloc[-200:]))
        n_items_er[pER].append(np.mean(df['n_items'].iloc[-200:]))


plt.figure(figsize=(15,10))
plt.rcParams.update({'font.size': 36})
plt.xlabel('r')
plt.ylabel(r'$\bar{Z}_{max}$')
plt.title("Mean group payoff")
for i, pER in enumerate(ps_lim):
    plt.plot(rs, avg_pay_er[pER], label=ks[i], color=colors[i],  marker=markers[i], markersize=12, linestyle = '--', linewidth=4)

#plt.legend()
plt.savefig("RS_plots/RS_zmax_inn.pdf", format="pdf", bbox_inches="tight")

plt.figure(figsize=(15,10))
plt.rcParams.update({'font.size': 36})
plt.xlabel('r')
plt.ylabel(r'$\bar{L}_{max}$')
plt.title("Mean group level")
for i,pER in enumerate(ps_lim):
    plt.plot(rs, avg_lvl_er[pER], label=ks[i],  color=colors[i],  marker=markers[i], markersize=12, linestyle = '--', linewidth=4)

plt.legend()
plt.savefig("RS_plots/RS_lvl_inn.pdf", format="pdf", bbox_inches="tight")

plt.figure(figsize=(15,10))
plt.rcParams.update({'font.size': 36})
plt.xlabel('r')
plt.ylabel(r'$\bar{T}_{max}$')
plt.ylim((500,100000))
plt.yscale('log')
plt.title("Mean number of traits")
for i,pER in enumerate(ps_lim):
    plt.plot(rs, n_items_er[pER], label=ks[i],  color=colors[i],  marker=markers[i],  markersize=12, linestyle = '--', linewidth=4)

#plt.legend()
plt.savefig("RS_plots/RS_nitems_inn.pdf", format="pdf", bbox_inches="tight")