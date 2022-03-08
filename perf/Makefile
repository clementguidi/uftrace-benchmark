TARGETS = t-perf-loop-short-pg t-perf-loop-short-fentry t-perf-loop-short-dynamic

pg_CFLAGS = -pg
fentry_CFLAGS = -finstrument-functions

all: $(TARGETS)

t-perf-loop-short-%: s-perf-loop-short.c perf.c perf.h
	gcc $($*_CFLAGS) -o $@ $^

clean:
	@rm -f $(TARGETS) *.o

.PHONY: clean
