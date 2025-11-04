/*
 * fork_exec.c
 * 
 * Demonstrates basic process creation using fork() and exec() system calls.
 * 
 * Compilation: gcc -o fork_exec fork_exec.c
 * Usage: ./fork_exec
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    pid_t pid;
    int status;

    printf("Parent process (PID: %d) is starting\n", getpid());

    // fork() creates a new process by duplicating the calling process
    // Returns: -1 on error, 0 in child process, child's PID in parent process
    pid = fork();
    
    if (pid < 0) {
        // Fork failed - no child process was created
        perror("fork failed");
        exit(1);
    } else if (pid == 0) {
        // Child process executes this block
        printf("Child process (PID: %d) is starting\n", getpid());

        // execl() replaces the current process image with a new program
        // Arguments: path to executable, argv[0], argv[1], ..., NULL
        // If successful, execl() never returns (process image is replaced)
        // If it returns, an error occurred
        execl("/bin/ls", "ls", "-l", NULL);
        
        // This line only executes if execl() fails
        perror("exec failed");
        exit(1);
    } else {
        // Parent process executes this block
        // 'pid' contains the child's process ID
        printf("Parent process (PID: %d) is waiting for child process (PID: %d)\n", getpid(), pid);
        
        // wait() blocks until the child terminates
        // The child's exit status is stored in 'status'
        wait(&status);
        
        // Check how the child process terminated
        if (WIFEXITED(status)) {
            // WIFEXITED: true if child terminated normally (via exit() or return)
            // WEXITSTATUS: extracts the exit status code
            printf("Child process (PID: %d) exited with status %d\n", pid, WEXITSTATUS(status));
        } else {
            // Child was terminated by a signal (abnormal termination)
            printf("Child process (PID: %d) terminated abnormally\n", pid);
        }
        printf("Child process (PID: %d) has terminated\n", pid);
    }
    
    return 0;
}

