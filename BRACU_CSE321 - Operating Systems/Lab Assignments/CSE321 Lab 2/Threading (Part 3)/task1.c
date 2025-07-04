#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

void *thread_function(void *arg) {
    int thread_id = *((int *)arg);
    printf("Thread-%d running\n", thread_id);
    sleep(1);
    printf("Thread-%d closed\n", thread_id);
    return NULL;
}

int main() {
    pthread_t threads[5];
    int thread_ids[5];

    for (int i = 0; i < 5; i++) {
        thread_ids[i] = i + 1;
        pthread_create(&threads[i], NULL, thread_function, &thread_ids[i]);
        pthread_join(threads[i], NULL);
    }

    return 0;
}
