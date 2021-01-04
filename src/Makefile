CFLAGS = -std=c99 -pedantic -Wall -Werror -Wextra -D_FORTIFY_SOURCE=2 -O3 -fPIC -fstack-protector-all -pie -s

.PHONY: all

all: helloworld

helloworld: helloworld.c
	$(CC) $(CFLAGS) -o $@ $<
