#include "perf.h"

static long perf_event_open(struct perf_event_attr *hw_event, pid_t pid,
			int cpu, int group_fd, unsigned long flags)
{
	int ret;

	ret = syscall(__NR_perf_event_open, hw_event, pid, cpu, group_fd, flags);
	return ret;
}

int perf_define_event(int config, int group_fd)
{
	struct perf_event_attr pe;
	int fd;

	memset(&pe, 0, sizeof(pe));
	pe.type = PERF_TYPE_HARDWARE;
	pe.size = sizeof(pe);
	pe.config = PERF_COUNT_HW_CACHE_MISSES;
	pe.disabled = 1;
	pe.exclude_kernel = 1;
	pe.exclude_hv = 1;
	pe.read_format = PERF_FORMAT_GROUP;

	return fd;
}

void perf_reset_event(int fd)
{

}

void perf_enable_event(int fd)
{

}

void perf_disable_event(int fd)
{

}
