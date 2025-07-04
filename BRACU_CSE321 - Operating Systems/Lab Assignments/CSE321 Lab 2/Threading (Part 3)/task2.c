#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int current_thread = 0;
pthread_mutex_t lock;
pthread_cond_t cond;

void *print_numbers(void *arg) {
    int thread_id = *((int *)arg);
    int start = thread_id * 5 + 1;

    pthread_mutex_lock(&lock);
    while (current_thread != thread_id) {
        pthread_cond_wait(&cond, &lock);
    }

    for (int i = start; i < start + 5; i++) {
        printf("Thread %d prints %d\n", thread_id, i);
    }

    current_thread++;
    pthread_cond_broadcast(&cond);
    pthread_mutex_unlock(&lock);
    return NULL;
}

int main() {
    pthread_t threads[5];
    int thread_ids[5];

    pthread_mutex_init(&lock, NULL);
    pthread_cond_init(&cond, NULL);

    for (int i = 0; i < 5; i++) {
        thread_ids[i] = i;
        pthread_create(&threads[i], NULL, print_numbers, &thread_ids[i]);
    }

    for (int i = 0; i < 5; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&lock);
    pthread_cond_destroy(&cond);

    return 0;
}