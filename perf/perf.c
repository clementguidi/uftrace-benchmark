#include <stdio.h>
#include <stdlib.h>
#include <asm/unistd.h>
#include <sys/ioctl.h>
#include <string.h>
#include <linux/perf_event.h>

#include "perf.h"

static long perf_event_open(struct perf_event_attr *hw_event, pid_t pid,
			int cpu, int group_fd, unsigned long flags)
{
	int ret;

	ret = syscall(__NR_perf_event_open, hw_event, pid, cpu, group_fd, flags);
	return ret;
}

int perf_define_event(long long config, int group_fd)
{
	struct perf_event_attr pe;
	int fd;

	memset(&pe, 0, sizeof(pe));
	pe.type = PERF_TYPE_HARDWARE;
	pe.size = sizeof(pe);
	pe.config = config;
	pe.disabled = 1;
	pe.exclude_kernel = 1;
	pe.exclude_hv = 1;
	if (group_fd == -1)
		pe.read_format = PERF_FORMAT_GROUP;

	fd = perf_event_open(&pe, 0, -1, group_fd, 0);
	if (fd == -1) {
		fprintf(stderr, "Error opening perf event %llx\n", pe.config);
		exit(EXIT_FAILURE);
	}

	return fd;
}

void perf_reset_event(int fd)
{
	ioctl(fd, PERF_EVENT_IOC_RESET, 0);
}

void perf_enable_event(int fd)
{
	ioctl(fd, PERF_EVENT_IOC_ENABLE, 0);
}

void perf_disable_event(int fd)
{
	ioctl(fd, PERF_EVENT_IOC_DISABLE, 0);
}
