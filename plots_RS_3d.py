import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm
from matplotlib import colors
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

ps = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
ps_lim = [0.01, 0.02, 0.05, 0.1, 0.2, 1.0]
rs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
rs_reverse = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2,0.1, 0.0]
ks = [int(pER*p["N"]) for pER in ps]

dfs_er = {er:[] for er in ps}
avg_pay_er = {er:[] for er in ps}
avg_lvl_er = {er:[] for er in ps}
max_pay_er = {er:[] for er in ps}
max_lvl_er = {er:[] for er in ps}
max_ach_pay_er = {er:[] for er in ps}
n_items_er = {er:[] for er in ps}
df_avg=pd.DataFrame(columns=['k', 'r', 'payoff'])
df_it=pd.DataFrame(columns=['k', 'r', 'items'])
for pER in ps:
    for r in rs:
        in_file_name = f'{in_dir}/avg_N_{p["N"]}_ER_{pER:.3f}_X_{p["X"]}_L_{p["L"]}_Cs_{p["Cs"]}_Ci_{p["Ci"]}_Cr_{p["Cr"]}_r_{r}__200.csv'
        df = pd.read_csv(in_file_name, sep='\t', index_col=0)
        dfs_er[pER].append(df)
        avg_pay_er[pER].append(np.mean(df['avg_payoff'].iloc[-200:]))
        list_row = [pER, r, int(np.mean(df['avg_payoff'].iloc[-200:]))]
        df_avg.loc[len(df_avg)] = list_row
        avg_lvl_er[pER].append(np.mean(df['avg_level'].iloc[-200:]))
        n_items_er[pER].append(np.mean(df['n_items'].iloc[-200:]))
        list_row = [pER, r, int(np.mean(df['n_items'].iloc[-200:]))]
        df_it.loc[len(df_it)] = list_row


df_avg=df_avg.sort_values(by='r', ascending=False)
#df_avg = df_avg[df_avg['k']<=0.1]
# pivot the dataframe from long to wide form
result = df_avg.pivot(index='r', columns='k', values='payoff')
result = result.sort_values(by='r', ascending=False)
extremes = result.values.max(), result.values.min()
extr_lbls = {result.values.max():'MAX', result.values.min():'MIN'}

labels = result.applymap(lambda v: extr_lbls[v] if v in (extremes) else '')
norm = colors.Normalize(vmin=result.values.min(), vmax=result.values.max())
fig, ax = plt.subplots(figsize=(30, 15))

plt.title("Mean group payoff", fontsize=38)
sns.set(font_scale=2.5)
#sns.heatmap(result, cmap='brg', square=True,
    #linewidths=0.8, annot_kws={'size': 'small', 'alpha': 0.95},
    #annot=labels, fmt = '', yticklabels=result.index, xticklabels=ks,
    #cbar_kws={"shrink": 0.8}, vmin=249, vmax=4051 )
sns.heatmap(result, cmap='bone', annot=labels, fmt = '', yticklabels=result.index, xticklabels=ks,
    vmin=249, vmax=4051, square=True, annot_kws={'size': 'small', 'alpha': 0.95},
            cbar_kws={'shrink': 0.75, 'aspect': 20, 'label':r'$\bar{Z}_{max}$' }, norm=norm, linewidth=2, linecolor="black")


ax.figure.axes[-1].yaxis.label.set_rotation('vertical')
ax.figure.axes[-1].yaxis.label.set_size(40)
ax.figure.axes[-1].yaxis.set_label_position('left')



ax.set_xlabel('k', fontsize=38)
ax.set_ylabel('r', fontsize=38)
ax.tick_params(axis='x', labelsize=32, rotation=45)
ax.tick_params(axis='y', labelsize=32, rotation=45)
plt.savefig("RS_3d_plots/3d_zmax_inn.pdf", format="pdf", bbox_inches="tight")



# pivot the dataframe from long to wide form
result = df_it.pivot(index='r', columns='k', values='items')

extremes = result.values.max(), result.values.min()

labels = result.map(lambda v: int(v) if v in (extremes) else '')

fig, ax = plt.subplots(figsize=(30, 20))


sns.heatmap(result, cmap='brg', square=True,
    linewidths=0.5, annot_kws={'size': 'x-small', 'alpha': 0.95},
    annot=labels, fmt = '', yticklabels=rs, xticklabels=ks,
    cbar_kws={"shrink": 0.8}, )
ax.xaxis.tick_top()


ax.set_xlabel('average degree, k', fontsize=32)
ax.set_ylabel('recommendations, r', fontsize=32)
ax.tick_params(axis='x', labelsize=28)
ax.tick_params(axis='y', labelsize=28)

plt.savefig("RS_3d_plots/3d_nitems_inn.pdf", format="pdf", bbox_inches="tight")
#plt.show()