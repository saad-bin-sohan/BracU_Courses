#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    int fd = open(argv[1], O_WRONLY | O_CREAT, 0644);
    if (fd == -1) {
        perror("File open failed");
        return 1;
    }

    char buffer[100];
    while (1) {
        printf("Enter a string (or -1 to quit): ");
        fgets(buffer, sizeof(buffer), stdin);
        buffer[strcspn(buffer, "\n")] = 0; 

        if (strcmp(buffer, "-1") == 0)
            break;

        write(fd, buffer, strlen(buffer));
        write(fd, "\n", 1);
    }

    close(fd);
    printf("File operations completed successfully.\n");
    return 0;
}
