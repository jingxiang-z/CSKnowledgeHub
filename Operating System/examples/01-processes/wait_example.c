/*
 * wait_example.c
 * 
 * Demonstrates wait() and waitpid() for parent processes.
 * 
 * Compilation: gcc -o wait_example wait_example.c
 * Usage: ./wait_example
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

void wait_example() {
    // fork() creates a new process by duplicating the calling process
    // Returns: 0 in child, child's PID in parent, -1 on error
    pid_t pid = fork();
    
    if (pid == 0) {
        // Child process executes this block
        printf("Child process (PID: %d) is running\n", getpid());
        sleep(2);  // Simulate some work
        exit(42);  // Exit with status code 42
    } else {
        // Parent process executes this block
        int status;
        
        // wait() blocks until one of its children terminates
        // Returns: PID of terminated child, or -1 on error
        // status: contains exit status and termination info
        pid_t child_pid = wait(&status);
        
        if (child_pid > 0) {
            // WIFEXITED checks if child terminated normally (via exit() or return)
            if (WIFEXITED(status)) {
                // WEXITSTATUS extracts the exit status code passed to exit()
                printf("Child process (PID: %d) exited with status %d\n", child_pid, WEXITSTATUS(status));
            } else {
                // Child terminated abnormally (e.g., killed by signal)
                printf("Child process (PID: %d) terminated abnormally\n", child_pid);
            }
        } else {
            perror("wait failed");
        }
    }
    printf("Parent process (PID: %d) is exiting\n", getpid());
}

void waitpid_example() {
    // fork() creates a new child process
    pid_t pid = fork();
    
    if (pid == 0) {
        // Child process executes this block
        printf("Child process (PID: %d) is running\n", getpid());
        sleep(2);  // Simulate some work
        exit(42);  // Exit with status code 42
    } 
    
    // Parent process continues here
    int status;
    
    // waitpid() allows more control than wait()
    // Can specify which child to wait for and use options like WNOHANG
    while (1) {
        // waitpid() with WNOHANG returns immediately instead of blocking
        // Returns: child PID if terminated, 0 if still running, -1 on error
        pid_t child_pid = waitpid(pid, &status, WNOHANG);
        
        if (child_pid == 0) {
            // Child is still running (WNOHANG returned without waiting)
            printf("Child process (PID: %d) is still running\n", pid);
            sleep(1);  // Check again after 1 second
        } else if (child_pid > 0) {
            // Child has terminated
            if (WIFEXITED(status)) {
                // Normal termination via exit() or return
                printf("Child process (PID: %d) exited with status %d\n", child_pid, WEXITSTATUS(status));
            } else {
                // Abnormal termination (e.g., killed by signal)
                printf("Child process (PID: %d) terminated abnormally\n", child_pid);
            }
            break;
        } else {
            // Error occurred
            perror("waitpid failed");
            break;
        }
    }
    printf("Parent process (PID: %d) is exiting\n", getpid());
}

int main() {
    // Demonstrate blocking wait() - parent waits until child terminates
    wait_example();
    
    sleep(1);  // Small delay between examples for cleaner output
    
    // Demonstrate non-blocking waitpid() - parent can do other work while checking
    waitpid_example();
    
    return 0;
}

