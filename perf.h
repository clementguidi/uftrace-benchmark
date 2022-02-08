#ifndef PERF_H_
#define PERF_H_

#include <unistd.h>
#include <linux/perf_event.h>
#include <asm/unistd.h>
#include <string.h>

static long perf_event_open(struct perf_event_attr *hw_event, pid_t pid,
			int cpu, int group_fd, unsigned long flags);

int perf_define_event(int config, int group_fd);
void perf_reset_event(int fd);
void perf_enable_event(int fd);
void perf_disable_event(int fd);

#endif // PERF_H_
