#!/usr/bin/env python3

import sys
import os

import seaborn as sns
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    sys.exit(f"Usage: {sys.argv[0]} RESULTS_DIR")

sns.set()

results_dir = sys.argv[1]
data_files = os.listdir(results_dir)

data = {}
for file in data_files:
    path = f"{results_dir}/{file}"
    with open(path, "r") as fd:
        experiment = file.split(".")[0]
        for line in fd:
            fields = line.split(" ")
            metric, value = fields[0], fields[1]
            if metric in data:
                data[metric] += experiment, value
            else:
                data[metric] = [experiment, value]

nmetrics = len(data)
ncols = 2
nrows = nmetrics // ncols + 0 if ncols % nmetrics else 1
fig, axs = plt.subplots(nrows, ncols)

metrics = list(data.keys())
for i in range(nmetrics):
    row = i // ncols
    col = i % ncols
    values = data[metrics[i]]
    nvalues = len(values)
    ax = axs[row, col]
    ax.bar(range(nvalues), [value[1] for value in values])
    ax.set_title(metrics[i])
plt.show()
