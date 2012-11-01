CC = gcc
all:
	$(CC) `pkg-config --cflags --libs glib-2.0` -g -O2 -fprofile-generate pgo.c
