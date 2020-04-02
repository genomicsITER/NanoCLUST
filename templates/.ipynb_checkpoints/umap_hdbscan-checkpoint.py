#!/usr/bin/env python

import numpy as np
import umap
import matplotlib.pyplot as plt
from sklearn import decomposition
import random
import pandas as pd
import hdbscan


df = pd.read_csv("$kmer_freqs", delimiter="\t")

#UMAP
motifs = [x for x in df.columns.values if x not in ["read", "length"]]
X = df.loc[:,motifs]
X_embedded = umap.UMAP(n_neighbors=15, min_dist=0.1, verbose=2).fit_transform(X)

df_umap = pd.DataFrame(X_embedded, columns=["D1", "D2"])
umap_out = pd.concat([df["read"], df["length"], df_umap], axis=1)

#HDBSCAN
X = umap_out.loc[:,["D1", "D2"]]
umap_out["bin_id"] = hdbscan.HDBSCAN(min_cluster_size=int($params.min_cluster_size), cluster_selection_epsilon=int($params.cluster_sel_epsilon)).fit_predict(X)
plt.figure(figsize=(30,19))
plt.scatter(X_embedded[:, 0], X_embedded[:, 1], c=umap_out["bin_id"], cmap='Spectral', s=0.7)
plt.gca().set_aspect('equal', 'datalim')
#plt.colorbar(boundaries=np.arange(11)-0.5).set_ticks(np.arange(10))
cluster_cnt = umap_out["bin_id"].max()
plt.colorbar(boundaries=np.arange(-1, cluster_cnt)-0.5).set_ticks(np.arange(-1, cluster_cnt))
plt.title('UMAP projection of the Digits dataset', fontsize=24);
plt.savefig('hdbscan.output.png')
umap_out.to_csv("output.hdbscan.tsv", sep="\t", index=False)
