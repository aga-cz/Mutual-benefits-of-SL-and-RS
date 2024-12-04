import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

p = {
    'N': 100,
    'T': 20000,
    'X': 100,
    'L': 1000,
    'p': 0.05,

}

in_dir = f'N{p["N"]}X{p["X"]}_avg_CiCsCr_k5'

rs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

costs = [1, 5, 10]

avg_pay = {}
avg_lvl = {}
n_items = {}
for Ci in costs:
    avg_pay[Ci] = {}
    avg_lvl[Ci] = {}
    n_items[Ci] = {}
    for Cs in costs:
        avg_pay[Ci][Cs] = {}
        avg_lvl[Ci][Cs] = {}
        n_items[Ci][Cs] = {}
        for Cr in costs:
            avg_pay[Ci][Cs][Cr] = []
            avg_lvl[Ci][Cs][Cr] = []
            n_items[Ci][Cs][Cr] = []
            for r in rs:
                in_file_name = f'{in_dir}/avg_N_{p["N"]}_ER_{p["p"]:.3f}_X_{p["X"]}_L_{p["L"]}_Cs_{Cs}_Ci_{Ci}_Cr_{Cr}_r_{r}__200.csv'
                df = pd.read_csv(in_file_name, sep='\t', index_col=0)
                avg_pay[Ci][Cs][Cr].append(np.mean(df['avg_payoff'].iloc[-200:]))
                avg_lvl[Ci][Cs][Cr].append(np.mean(df['avg_level'].iloc[-200:]))
                n_items[Ci][Cs][Cr].append(np.mean(df['n_items'].iloc[-200:]))


styles = {1: ':',
         5: '-.',
         10: '--'}

markers = {1: 'o',
           5: 's',
           10: 'd'}


#cmap = plt.get_cmap('rocket')
#colors = cmap(np.linspace(0,1,9))
colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'gray', 'olive', 'cyan']

plt.figure(figsize=(60,90))
plt.rcParams.update({'font.size': 36})
#plt.subplots_adjust(wspace=0.5, hspace=0.5)
Ci=1

plt.subplot(3, 3, 1)
plt.xlabel('r')
plt.ylabel(r'$\bar{L}_{max}$')
plt.title("Mean group level, $C_i=1$")
i=0

for Cs in costs:
    for Cr in costs:
        plt.plot(rs, avg_lvl[Ci][Cs][Cr], label=f'$C_i$={Ci}, $C_s$={Cs}, $C_r$={Cr}', color=colors[i], marker = markers[Cs], markersize=12, linestyle = styles[Cr], linewidth=4)
        i+=1

#plt.legend(fontsize="18", bbox_to_anchor=(0.97, 1.02), loc="upper left")

plt.subplot(3, 3, 2)
plt.xlabel('r')
plt.ylabel(r'$\bar{T}_{max}$')
plt.ylim((100,150000))
plt.yscale('log')
plt.title("Mean number of traits, $C_i=1$")
i=0
for Cs in costs:
    for Cr in costs:
        plt.plot(rs, n_items[Ci][Cs][Cr], label=f'$C_s$={Cs}, $C_r$={Cr}', color=colors[i], marker = markers[Cs], markersize=12, linestyle = styles[Cr], linewidth=4)
        i+=1

plt.legend(fontsize="32")

plt.subplot(3, 3, 3)
plt.xlabel('r')
plt.ylabel(r'$\bar{Z}_{max}$')
plt.title("Mean group payoff, $C_i=1$")
i=0
for Cs in costs:
    for Cr in costs:
        plt.plot(rs, avg_pay[Ci][Cs][Cr], label=f'$C_i$={Ci}, $C_s$={Cs}, $C_r$={Cr}', color=colors[i], marker = markers[Cs], markersize=12, linestyle = styles[Cr], linewidth=4)
        i+=1

#plt.legend(fontsize="18", bbox_to_anchor=(0.97, 1.02), loc="upper left")

Ci=5

plt.subplot(3, 3, 4)
plt.xlabel('r')
plt.ylabel(r'$\bar{L}_{max}$')
plt.title("Mean group level, $C_i=5$")
i=0

for Cs in costs:
    for Cr in costs:
        plt.plot(rs, avg_lvl[Ci][Cs][Cr], label=f'$C_i$={Ci}, $C_s$={Cs}, $C_r$={Cr}', color=colors[i], marker = markers[Cs], markersize=12, linestyle = styles[Cr], linewidth=4)
        i+=1

#plt.legend(fontsize="18", bbox_to_anchor=(0.97, 1.02), loc="upper left")

plt.subplot(3, 3, 5)
plt.xlabel('r')
plt.ylabel(r'$\bar{T}_{max}$')
plt.ylim((100,150000))
plt.yscale('log')
plt.title("Mean number of traits, $C_i=5$")
i=0
for Cs in costs:
    for Cr in costs:
        plt.plot(rs, n_items[Ci][Cs][Cr], label=f'$C_s$={Cs}, $C_r$={Cr}', color=colors[i], marker = markers[Cs], markersize=12, linestyle = styles[Cr], linewidth=4)
        i+=1

plt.legend(fontsize="32")


plt.subplot(3, 3, 6)
plt.xlabel('r')
plt.ylabel(r'$\bar{Z}_{max}$')
plt.title("Mean group payoff, $C_i=5$")
i=0
for Cs in costs:
    for Cr in costs:
        plt.plot(rs, avg_pay[Ci][Cs][Cr], label=f'$C_s$={Cs}, $C_r$={Cr}', color=colors[i], marker = markers[Cs], markersize=12, linestyle = styles[Cr], linewidth=4)
        i+=1

#plt.legend(fontsize="24")

Ci=10

plt.subplot(3, 3, 7)
plt.xlabel('r')
plt.ylabel(r'$\bar{L}_{max}$')
plt.title("Mean group level, $C_i=10$")
i=0

for Cs in costs:
    for Cr in costs:
        plt.plot(rs, avg_lvl[Ci][Cs][Cr], label=f'$C_i$={Ci}, $C_s$={Cs}, $C_r$={Cr}', color=colors[i], marker = markers[Cs], markersize=12, linestyle = styles[Cr], linewidth=4)
        i+=1

#plt.legend(fontsize="18", bbox_to_anchor=(0.97, 1.02), loc="upper left")

plt.subplot(3, 3, 8)
plt.xlabel('r')
plt.ylabel(r'$\bar{T}_{max}$')
plt.ylim((100,150000))
plt.yscale('log')
plt.title("Mean number of traits, $C_i=10$")
i=0
for Cs in costs:
    for Cr in costs:
        plt.plot(rs, n_items[Ci][Cs][Cr], label=f'$C_s$={Cs}, $C_r$={Cr}', color=colors[i], marker = markers[Cs], markersize=12, linestyle = styles[Cr], linewidth=4)
        i+=1

plt.legend(fontsize="32")

plt.subplot(3, 3, 9)
plt.xlabel('r')
plt.ylabel(r'$\bar{Z}_{max}$')
plt.title("Mean group payoff, $C_i=10$")
i=0
for Cs in costs:
    for Cr in costs:
        plt.plot(rs, avg_pay[Ci][Cs][Cr], label=f'$C_i$={Ci}, $C_s$={Cs}, $C_r$={Cr}', color=colors[i], marker = markers[Cs], markersize=12, linestyle = styles[Cr], linewidth=4)
        i+=1

#plt.legend(fontsize="18", bbox_to_anchor=(0.97, 1.02), loc="upper left")

#plt.show()
#plt.savefig("costs_k5.pdf", format='pdf', bbox_inches='tight')
plt.savefig("costs_k5.jpg", format='jpg', bbox_inches='tight')