# Brinkmann's multi_alphadeficit: 64-bit build (default, <= 63 vertices) and 128-bit build (<= 127 vertices).
CC ?= gcc
CFLAGS ?= -O3

all: bin/multi_alphadeficit bin/multi_alphadeficit128

bin/multi_alphadeficit: analysis/multi_alphadeficit.c
	$(CC) $(CFLAGS) -o $@ $<

bin/multi_alphadeficit128: analysis/multi_alphadeficit.c
	$(CC) $(CFLAGS) -DALPHA128 -o $@ $<

clean:
	rm -f bin/multi_alphadeficit bin/multi_alphadeficit128

.PHONY: all clean
