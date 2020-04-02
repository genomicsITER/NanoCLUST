#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("$hdbscan", sep="\t")

fig, ax1 = plt.subplots()
fig.set_size_inches(13, 10)

#labels
ax1.set_xlabel('UMAP1')
ax1.set_ylabel('UMAP2')
ax1.set_title('UMAP+HDBSCAN clustering')

#TO DO
#Set square axis for proper UMAP representation
plt.scatter(df['D1'], df['D2'], cmap='Paired', c=df['bin_id'], s=2)
plt.savefig("umap_plot.png")