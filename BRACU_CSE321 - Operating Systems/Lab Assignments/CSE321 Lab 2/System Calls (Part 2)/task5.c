#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main()
{
    pid_t pid = fork();

    if (pid > 0) 
    {
        printf("1. Parent process ID: 0\n");
        wait(NULL);
    }
    else if (pid == 0) 
    {
        printf("2. Child process ID: %d\n", getpid());

        pid_t grand_child_1 = fork();
        if (grand_child_1 == 0) 
        {
            printf("3. Grand Child process ID: %d\n", getpid());
            exit(0);
        } 
        else 
        {
            wait(NULL);
            
            pid_t grand_child_2 = fork();
            if (grand_child_2 == 0) 
            {
                printf("4. Grand Child process ID: %d\n", getpid());
                exit(0);
            } 
            else 
            {
                wait(NULL);

                pid_t grand_child_3 = fork();
                if (grand_child_3 == 0) 
                {
                    printf("5. Grand Child process ID: %d\n", getpid());
                    exit(0);
                } 
                else 
                {
                    wait(NULL);
                }
            }
        }

        exit(0);
    }

    return 0;
}
