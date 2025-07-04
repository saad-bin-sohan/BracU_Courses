#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/wait.h>
#include <unistd.h>
#include <fcntl.h>

struct shared {
    char sel[100];
    int b;
};

void process_opr(int shm_id, int pipe_fd[2]) {
    struct shared *data = (struct shared *)shmat(shm_id, NULL, 0);
    if (data == (void *)-1) {
        perror("shmat failed");
        exit(1);
    }

    printf("Your selection: %s\n", data->sel);

    if (strcmp(data->sel, "a") == 0) {
        int amount;
        printf("Enter amount to be added:\n");
        scanf("%d", &amount);
        if (amount > 0) {
            data->b += amount;
            printf("Balance added successfully\n");
            printf("Updated balance after addition: %d\n", data->b);
        } else {
            printf("Adding failed, Invalid amount\n");
        }
    } else if (strcmp(data->sel, "w") == 0) {
        int amount;
        printf("Enter amount to be withdrawn:\n");
        scanf("%d", &amount);
        if (amount > 0 && amount <= data->b) {
            data->b -= amount;
            printf("Balance withdrawn successfully\n");
            printf("Updated balance after withdrawal: %d\n", data->b);
        } else {
            printf("Withdrawal failed, Invalid amount\n");
        }
    } else if (strcmp(data->sel, "c") == 0) {
        printf("Your current balance is: %d\n", data->b);
    } else {
        printf("Invalid selection\n");
    }

    close(pipe_fd[0]);
    write(pipe_fd[1], "Thank you for using\n", 20);
    close(pipe_fd[1]);

    shmdt(data);
    exit(0);
}

int main() {
    key_t key = IPC_PRIVATE;
    int shm_id = shmget(key, sizeof(struct shared), IPC_CREAT | 0666);
    if (shm_id < 0) {
        perror("shmget failed");
        exit(1);
    }

    int pipe_fd[2];
    if (pipe(pipe_fd) == -1) {
        perror("pipe failed");
        exit(1);
    }

    struct shared *data = (struct shared *)shmat(shm_id, NULL, 0);
    if (data == (void *)-1) {
        perror("shmat failed");
        exit(1);
    }

    data->b = 1000;
    printf("Provide Your Input From Given Options:\n");
    printf("1. Type a to Add Money\n");
    printf("2. Type w to Withdraw Money\n");
    printf("3. Type c to Check Balance\n");

    scanf("%s", data->sel);

    pid_t pid = fork();
    if (pid == 0) {
        process_opr(shm_id, pipe_fd);
    } else if (pid > 0) {
        wait(NULL);

        char buffer[100];
        close(pipe_fd[1]);
        read(pipe_fd[0], buffer, sizeof(buffer));
        close(pipe_fd[0]);
        printf("%s", buffer);

        shmdt(data);
        shmctl(shm_id, IPC_RMID, NULL);
    } else {
        perror("fork failed");
        exit(1);
    }

    return 0;
}
