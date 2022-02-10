#include <stdio.h>
#include <time.h>

#include "perf.h"

#define NR_WARMUP 10
#define NR_LOOP 100000

void a();

int main(int argc, char **argv)
{
	struct perf_event_attr pe[3];
	long long results[3+1];
	int fd[3];
	struct timespec start, end;
	long long latency;

	fd[0] = -1;

	int metrics[] = {
		PERF_COUNT_HW_CACHE_MISSES,
		PERF_COUNT_HW_BRANCH_MISSES,
		PERF_COUNT_HW_INSTRUCTIONS,
	};

	for (int i = 0; i < 3; i++) {
		fd[i] = perf_define_event(metrics[i], fd[0]);
		perf_reset_event(fd[i]);
	}

	for (int i = 0; i < NR_WARMUP; i++) {
		a();
	}

	for (int i = 0; i < 3; i++) {
		perf_enable_event(fd[i]);
	}
	clock_gettime(CLOCK_MONOTONIC, &start);

	for (int i = 0; i < NR_LOOP; i++) {
		a();
	}

	clock_gettime(CLOCK_MONOTONIC, &end);
	for (int i = 0; i < 3; i++) {
		perf_disable_event(fd[i]);
	}

	latency = (end.tv_sec - start.tv_sec) * 10^9 + (end.tv_nsec - start.tv_sec);
	latency /= NR_LOOP;

	read(fd[0], &results, sizeof(results));

	printf("count: %lld\tlatency: %lld ns\tcache misses: %lld\tbranch misses: %lld\tinstructions %lld\n",
		results[0], latency, results[1]/NR_LOOP, results[2]/NR_LOOP, results[3]/NR_LOOP);

	for (int i = 0; i < 3; i++) {
		close(fd[i]);
	}
}

void a()
{
	return;
}
