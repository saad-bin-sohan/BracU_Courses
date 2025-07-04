#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <numbers>\n", argv[0]);
        return 1;
    }

    char buffer[100];
    pid_t pid = fork();

    if (pid == 0) {
        char *args[argc + 1];
        args[0] = "./sort";
        for (int i = 1; i < argc; i++) {
            sprintf(buffer, "%s", argv[i]);
            args[i] = strdup(buffer);
        }
        args[argc] = NULL;

        execvp(args[0], args);
        perror("exec failed");
        exit(1);
    } else {
        wait(NULL);

        char *args[argc + 1];
        args[0] = "./oddeven";
        for (int i = 1; i < argc; i++) {
            sprintf(buffer, "%s", argv[i]);
            args[i] = strdup(buffer);
        }
        args[argc] = NULL;

        execvp(args[0], args);
        perror("exec failed");
        exit(1);
    }

    return 0;
}
