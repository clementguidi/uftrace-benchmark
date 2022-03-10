#!/usr/bin/env python3

import sys
import os

import numpy as np


def process_value(v):
    result = v
    if "(" in v:
        split_v = v.split()
        abs_v = int(split_v[0])
        percent_v = float(split_v[1].strip("(\%)"))
        result = abs_v, percent_v
    else:
        result = int(v.rstrip(" ns"))
    return result

def process_instrumentation(files):
    # assume only one file: instrumentation.txt
    file = files[0]

    latencies = []
    top_fields = ["patched", "no match", "total"]
    top_fields_detailed = ["failed", "skipped"]
    coverage = {}
    with open(f"{results_dir}/{file}", "r") as fd:
        top_field = ""
        for line in fd:
            split_line = line.strip().split(": ")
            field, value = split_line[0], split_line[1]
            value = process_value(value)
            if field == "patching latency":
                latencies.append(value)
            if field == "total patching duration":
                total_duration = value
            elif field in top_fields_detailed:
                top_field = field
                coverage[top_field] = value, {}
            elif top_field == "" and field in top_fields:
                coverage[field] = value
            else:
                coverage[top_field][1][field] = value
    print(int(np.average(latencies)), \
          int(np.std(latencies)), \
          np.min(latencies), \
          np.max(latencies))

def process_tracing(files):
    pass

if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} RESULTS_DIR")

    results_dir = sys.argv[1]
    try:
        data_files = os.listdir(results_dir)
    except FileNotFoundError:
        sys.exit(f"Directory '{results_dir}' not found")


    instrumentation_data_files = []
    tracing_data_files = []
    for file in data_files:
        if file == "instrumentation.txt":
            instrumentation_data_files.append(file)
        if file.startswith("tracing"):
            tracing_data_files.append(file)

    if len(instrumentation_data_files) > 0:
        process_instrumentation(instrumentation_data_files)

    if len(tracing_data_files) > 0:
        process_tracing(tracing_data_files)
