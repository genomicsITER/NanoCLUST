#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd
import os

fastani_results = pd.read_csv("$fastani_output", sep="\\s+",header=None, names=["read1", "reads2", "similarity", "parameter1", "parameter2"])
fastani_results = fastani_results.groupby("read1").mean().sort_values(by="similarity", ascending=False)

os.system("sed 's/-/_/g' " + fastani_results.index.values.astype(str)[0] + " > draft_read.fasta")

