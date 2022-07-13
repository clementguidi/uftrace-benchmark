#include <stdio.h>
#include <time.h>

#include "perf.h"

#define NR_WARMUP 10
#define NR_LOOP 100000
#define NR_PERF_EVENTS 3

void a();

int main(int argc, char **argv)
{
	struct perf_event_attr pe[NR_PERF_EVENTS];
	long long results[NR_PERF_EVENTS+1];
	int fd[NR_PERF_EVENTS];
	struct timespec start, end;
	long long latency;
	int nr_perf_events = NR_PERF_EVENTS;

	int metrics[] = {
		PERF_COUNT_HW_CACHE_MISSES,
		PERF_COUNT_HW_BRANCH_MISSES,
		PERF_COUNT_HW_INSTRUCTIONS,
	};

	fd[0] = -1;
	for (int i = 0; i < nr_perf_events; i++) {
		fd[i] = perf_define_event(metrics[i], fd[0]);
		perf_reset_event(fd[i]);
	}

	for (int i = 0; i < NR_WARMUP; i++) {
		a();
	}

	for (int i = 0; i < nr_perf_events; i++) {
		perf_enable_event(fd[i]);
	}
	clock_gettime(CLOCK_MONOTONIC, &start);

	for (int i = 0; i < NR_LOOP; i++) {
		a();
	}

	clock_gettime(CLOCK_MONOTONIC, &end);
	for (int i = 0; i < nr_perf_events; i++) {
		perf_disable_event(fd[i]);
	}

	latency = (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);
	latency /= NR_LOOP;

	read(fd[0], &results, sizeof(results));

	printf("LATENCY %lld\nCACHE_MISSES %lld\nBRANCH_MISSES %lld\nINSTRUCTIONS %lld\n",
		latency, results[1]/NR_LOOP, results[2]/NR_LOOP, results[3]/NR_LOOP);

	for (int i = 0; i < 3; i++) {
		close(fd[i]);
	}
}

void a()
{
	int i = 0;
	return;
}
