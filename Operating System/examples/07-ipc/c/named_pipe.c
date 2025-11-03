/*
 * named_pipe.c
 * 
 * Demonstrates named pipes (FIFOs) for communication between unrelated processes.
 * 
 * Compilation: gcc -o named_pipe named_pipe.c
 * Usage: ./named_pipe
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>

int main() {
    // TODO: Implement named pipe (FIFO) example using mkfifo()
    printf("Named pipe example - To be implemented\n");
    
    return 0;
}

