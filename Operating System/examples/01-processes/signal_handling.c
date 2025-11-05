/*
 * signal_handling.c
 * 
 * Demonstrates signal handling with custom signal handlers.
 * 
 * Compilation: gcc -o signal_handling signal_handling.c
 * Usage: ./signal_handling
 */

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

// Signal handler function
// Called when the process receives SIGINT or SIGTERM
void handle_signal(int sig) {
    if (sig == SIGINT) {
        // SIGINT is sent when user presses Ctrl+C
        printf("Caught SIGINT. Cleaning up...\n");
    } else if (sig == SIGTERM) {
        // SIGTERM is a termination request (default signal for 'kill' command)
        printf("Caught SIGTERM. Exiting gracefully...\n");
    }
    
    // fflush() ensures output is written immediately (important before exit)
    fflush(stdout);
    
    // Exit following Unix convention: 128 + signal number
    // SIGINT (2) -> 130, SIGTERM (15) -> 143
    exit(128 + sig);
}

int main() {
    // signal() sets up a signal handler for a specific signal
    // Returns: SIG_ERR on error, previous handler on success
    
    // Register handler for SIGINT (Interrupt signal - Ctrl+C)
    if (signal(SIGINT, handle_signal) == SIG_ERR) {
        perror("Failed to set SIGINT handler");
        exit(1);
    } else if (signal(SIGTERM, handle_signal) == SIG_ERR) {
        // Register handler for SIGTERM (Termination signal)
        perror("Failed to set SIGTERM handler");
        exit(1);
    }

    printf("Press Ctrl+C or send SIGTERM to trigger signals.\n");
    printf("Process PID: %d\n", getpid());
    printf("To test SIGTERM, run: kill %d\n", getpid());

    // Infinite loop - process will run until it receives a signal
    // The signal handler will interrupt this loop when a signal arrives
    while (1) {
        sleep(1);  // Sleep to avoid consuming CPU
    }
    
    // This line is never reached due to infinite loop (unless signals handled)
    return 0;
}

