#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    int pipe_descriptors[2];
    if (pipe(pipe_descriptors) != 0) {
        perror("Pipe creation failed");
        return 1;
    }

    pid_t fork1, fork2, fork3;
    int process_tracker = 0;
    pid_t parent_pid = getpid();
    
    write(pipe_descriptors[1], &process_tracker, sizeof(process_tracker));

    fork1 = fork();
    fork2 = fork();
    fork3 = fork();

    pid_t active_pid = getpid();
    if (active_pid % 2 != 0 && active_pid != parent_pid) {
        fork();
    }

    read(pipe_descriptors[0], &process_tracker, sizeof(process_tracker));
    process_tracker++;
    write(pipe_descriptors[1], &process_tracker, sizeof(process_tracker));

    close(pipe_descriptors[1]);
    waitpid(fork1, NULL, 0);
    waitpid(fork2, NULL, 0);
    waitpid(fork3, NULL, 0);

    if (getpid() == parent_pid) {
        read(pipe_descriptors[0], &process_tracker, sizeof(process_tracker));
        close(pipe_descriptors[0]);
        printf("Final Process Count (including the original parent): %d\n", process_tracker);
    }

    return 0;
}