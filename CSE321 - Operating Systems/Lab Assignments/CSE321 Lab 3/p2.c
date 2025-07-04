#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <unistd.h>
#include <sys/wait.h>
#include <time.h>

struct otp_msg {
    long int type;
    char text[7];
};

void otp_generator(int msg_id, struct otp_msg *message) {
    msgrcv(msg_id, message, sizeof(struct otp_msg) - sizeof(long int), 1, 0);
    printf("OTP generator received workspace name from log in: %s\n", message->text);

    snprintf(message->text, sizeof(message->text), "%05d", rand() % 100000);
    message->type = 2;
    msgsnd(msg_id, message, sizeof(struct otp_msg) - sizeof(long int), 0);
    printf("OTP sent to log in from OTP generator: %s\n", message->text);

    message->type = 3;
    msgsnd(msg_id, message, sizeof(struct otp_msg) - sizeof(long int), 0);
    printf("OTP sent to mail from OTP generator: %s\n", message->text);

    exit(0);
}

void mail_process(int msg_id, struct otp_msg *message) {
    msgrcv(msg_id, message, sizeof(struct otp_msg) - sizeof(long int), 3, 0);
    printf("Mail received OTP from OTP generator: %s\n", message->text);

    message->type = 4;
    msgsnd(msg_id, message, sizeof(struct otp_msg) - sizeof(long int), 0);
    printf("OTP sent to log in from mail: %s\n", message->text);

    exit(0);
}

int main() {
    srand(time(NULL));

    int msg_id;
    struct otp_msg message;

    msg_id = msgget(IPC_PRIVATE, 0666 | IPC_CREAT);
    if (msg_id == -1) {
        perror("msgget failed");
        exit(1);
    }

    printf("Please enter the workspace name:\n");
    char workspace[7];
    if (fgets(workspace, sizeof(workspace), stdin) == NULL) {
        perror("Failed to read input");
        exit(1);
    }

    size_t len = strlen(workspace);
    if (len > 0 && workspace[len - 1] == '\n') {
        workspace[len - 1] = '\0';
    }

    if (strcmp(workspace, "cse321") != 0) {
        printf("Invalid workspace name\n");
        msgctl(msg_id, IPC_RMID, NULL);
        exit(0);
    }

    message.type = 1;
    strncpy(message.text, workspace, sizeof(message.text) - 1);
    message.text[sizeof(message.text) - 1] = '\0';
    msgsnd(msg_id, &message, sizeof(struct otp_msg) - sizeof(long int), 0);
    printf("Workspace name sent to OTP generator from log in: %s\n", workspace);

    pid_t pid_otp = fork();
    if (pid_otp == 0) {
        otp_generator(msg_id, &message);
        exit(0);
    }

    wait(NULL);

    pid_t pid_mail = fork();
    if (pid_mail == 0) {
        mail_process(msg_id, &message);
        exit(0);
    }

    wait(NULL);

    msgrcv(msg_id, &message, sizeof(struct otp_msg) - sizeof(long int), 2, 0);
    printf("Log in received OTP from OTP generator: %s\n", message.text);

    char otp_from_otp[7];
    strncpy(otp_from_otp, message.text, sizeof(otp_from_otp) - 1);
    otp_from_otp[sizeof(otp_from_otp) - 1] = '\0';

    msgrcv(msg_id, &message, sizeof(struct otp_msg) - sizeof(long int), 4, 0);
    printf("Log in received OTP from mail: %s\n", message.text);

    char otp_from_mail[7];
    strncpy(otp_from_mail, message.text, sizeof(otp_from_mail) - 1);
    otp_from_mail[sizeof(otp_from_mail) - 1] = '\0';

    if (strcmp(otp_from_otp, otp_from_mail) == 0) {
        printf("OTP Verified\n");
    } else {
        printf("OTP Incorrect\n");
    }

    msgctl(msg_id, IPC_RMID, NULL);

    return 0;
}