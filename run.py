import subprocess
import numpy as np
import pprint


def display(data):
    pp = pprint.PrettyPrinter()
    pp.pprint(data)

class Runner:
    def __init__(self, uftrace_bin, app):
        self.uftrace_bin = uftrace_bin
        self.app = app

    def execute(self, args):
        process = subprocess.run([self.uftrace_bin] + args,
                                 capture_output=True,
                                 check=True,)
        return process

    def parse_data(self, data):
        index_beg = data.find("(")
        if index_beg == -1:
            return int(data)
        index_end = data.find(")")
        value = int(data[:index_beg])
        ratio = float(data[index_beg+1:index_end].strip("%"))
        return str(value), str(ratio)


    def evaluate_coverage(self, rawdata):
        top_fields = ["total", "patched", "failed", "skipped", "no match"]
        fields = ["badsym",
                  "capstone",
                  "no detail",
                  "no detail 2",
                  "relative jump",
                  "relative call",
                  "pic",
                  "jump prologue",
                  "jump function"
                  "cold",
                  "min size",
                  "call size",]
        result = {}
        top_field = None
        for line in rawdata.splitlines():
            line = line.removeprefix("dynamic:").strip()
            index = line.find(":")
            if index == -1:
                continue
            field = line[:index]
            data  = line[index+1:].strip()
            if field in top_fields:
                if field == "total" and top_field != None:
                    continue
                top_field = field
                result[field] = self.parse_data(data), {}
            elif field in fields:
                result[top_field][1][field] = self.parse_data(data)
        return result

    def evaluate_latency(self, rawdata):
        latencies = []
        total_duration = 0
        for line in rawdata.splitlines():
            line = line.removeprefix("dynamic:").strip()
            index = line.find(":")
            if index == -1:
                continue
            field = line[:index]
            data  = line[index+1:].removesuffix("ns")
            if field == "patching latency":
                latencies.append(int(data))
            elif field == "patching duration":
                total_duration = int(data)/1000
        latencies = np.array(latencies)
        latency_stats = {"min" : str(int(np.min(latencies)/1000)),
                         "max" : str(int(np.max(latencies)/1000)),
                         "mean": str(int(np.mean(latencies)/1000)),
                         "std" : str(int(np.std(latencies)/1000)),
                         "med" : str(int(np.median(latencies)/1000))}
        return total_duration, latency_stats

    def evaluate_instrumentation(self):
        process = self.execute(["record",
                                "-P.",
                                "--dry-run",
                                f"applications/{self.app}"])
        rawdata = process.stderr.decode("UTF-8")
        coverage_results = self.evaluate_coverage(rawdata)
        latency_results  = self.evaluate_latency(rawdata)
        display(coverage_results)
        display(latency_results)

    def evaluate_tracing(self):
        result = {}
        modes = ["dynamic", "pg", "fentry"]
        for mode in modes:
            result[mode] = []
            process = self.execute(["record",
                                    "-Pa",
                                    f"perf/t-perf-loop-short-{mode}"])
            rawdata = process.stdout.decode("UTF-8")
            for line in rawdata.splitlines():
                line = line.split()
                field = line[0]
                value = line[1]
                result[mode].append((field, value))
        display(result)
