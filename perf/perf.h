#ifndef PERF_H_
#define PERF_H_

#include <unistd.h>
#include <linux/perf_event.h>
#include <asm/unistd.h>

int perf_define_event(long long config, int group_fd);
void perf_reset_event(int fd);
void perf_enable_event(int fd);
void perf_disable_event(int fd);

#endif // PERF_H_
