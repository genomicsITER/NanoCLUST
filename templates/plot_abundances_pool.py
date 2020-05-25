#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd

def plot_multi(table):

    df_final_grp = pd.read_csv(table)
    bars = [df_final_grp.iloc[i,1:].values.tolist() for i in range(0,df_final_grp.shape[0])]
    barWidth = 0.25
    colors = ['#a6cee3','#3caea3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#d11141','#ffc425','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
    color_index = 0
    r = np.arange(0, (len(df_final_grp.columns) -1))

    graph_bars = []
    graph_bars.append(plt.bar(r, bars[0], color=colors[0], edgecolor='white', width=barWidth, label=df_final_grp.iloc[0,0]))
    bottomm = bars[0]

    for index in range(1,len(bars)):
            color_index = index if(index < len(colors)) else index%len(colors)
            graph_bars.append(plt.bar(r, bars[index], bottom=bottomm, color=colors[color_index], edgecolor='white', width=barWidth, label=df_final_grp.iloc[index,0]))
            bottomm = [i+j for i,j in zip(bottomm, bars[index])]

    plt.xticks(r, (df_final_grp.columns[1:]))
    plt.legend(graph_bars, df_final_grp["taxid"], ncol=3, fontsize='large',title_fontsize="x-large", loc='center',bbox_to_anchor=(0.5, -0.25))
    plt.savefig("" + table + ".plot.png", bbox_inches="tight")

table = "$table"

plot_multi(table)
plot_multi(table)
plot_multi(table)
plot_multi(table)