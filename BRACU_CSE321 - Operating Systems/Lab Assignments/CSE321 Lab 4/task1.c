#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define MAX 10
#define BUFLEN 6
#define NUMTHREAD 2

char buffer[BUFLEN];
char source[BUFLEN] = "abcdef";
int pCount = 0;
int cCount = 0;
int buflen;

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t nonEmpty = PTHREAD_COND_INITIALIZER;
pthread_cond_t full = PTHREAD_COND_INITIALIZER;

void *producer(void *id) {
    int *prod_id = (int *)id;
    while (pCount < MAX) {
        pthread_mutex_lock(&lock);

        while (strlen(buffer) == buflen) {
            pthread_cond_wait(&full, &lock);
        }

        char item = source[pCount % buflen];
        buffer[pCount % buflen] = item;
        printf("%d produced %c by Thread %d\n", pCount, item, *prod_id);

        pCount++;

        pthread_cond_signal(&nonEmpty);
        pthread_mutex_unlock(&lock);

        usleep(100000);
    }
    pthread_exit(NULL);
}

void *consumer(void *id) {
    int *cons_id = (int *)id;
    while (cCount < MAX) {
        pthread_mutex_lock(&lock);

        while (pCount == cCount) {
            pthread_cond_wait(&nonEmpty, &lock);
        }

        char item = buffer[cCount % buflen];
        buffer[cCount % buflen] = '\0';
        printf("%d consumed %c by Thread %d\n", cCount, item, *cons_id);

        cCount++;

        pthread_cond_signal(&full);
        pthread_mutex_unlock(&lock);

        usleep(100000);
    }
    pthread_exit(NULL);
}

int main() {
    pthread_t threads[NUMTHREAD];
    int thread_id[NUMTHREAD] = {0, 1};

    buflen = strlen(source);

    pthread_create(&threads[0], NULL, producer, &thread_id[0]);
    pthread_create(&threads[1], NULL, consumer, &thread_id[1]);

    for (int i = 0; i < NUMTHREAD; i++) {
        pthread_join(threads[i], NULL);
    }

    return 0;
}
