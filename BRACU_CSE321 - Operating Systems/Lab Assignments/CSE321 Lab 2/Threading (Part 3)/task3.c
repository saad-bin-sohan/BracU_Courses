#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

#define NUM_NAMES 3

int ascii_sums[NUM_NAMES];
pthread_mutex_t lock; 

void *calculate_ascii(void *arg) {
    char *name = (char *)arg;
    int sum = 0;

    for (int i = 0; i < strlen(name); i++) {
        sum += name[i];
    }

    pthread_mutex_lock(&lock);
    static int index = 0;
    ascii_sums[index++] = sum;
    pthread_mutex_unlock(&lock);

    return NULL;
}

void *compare_ascii(void *arg) {
    pthread_mutex_lock(&lock);

    if (ascii_sums[0] == ascii_sums[1] && ascii_sums[1] == ascii_sums[2]) {
        printf("Youreka\n");
    } else if (ascii_sums[0] == ascii_sums[1] || ascii_sums[1] == ascii_sums[2] || ascii_sums[0] == ascii_sums[2]) {
        printf("Miracle\n");
    } else {
        printf("Hasta la vista\n");
    }

    pthread_mutex_unlock(&lock);
    return NULL;
}

int main() {
    pthread_t threads[NUM_NAMES + 1];
    char names[NUM_NAMES][50];
    
    printf("Enter 3 names:\n");
    for (int i = 0; i < NUM_NAMES; i++) {
        printf("Name %d: ", i + 1);
        scanf("%s", names[i]);
    }

    pthread_mutex_init(&lock, NULL);

    for (int i = 0; i < NUM_NAMES; i++) {
        pthread_create(&threads[i], NULL, calculate_ascii, names[i]);
    }

    for (int i = 0; i < NUM_NAMES; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_create(&threads[NUM_NAMES], NULL, compare_ascii, NULL);
    pthread_join(threads[NUM_NAMES], NULL);

    pthread_mutex_destroy(&lock);

    return 0;
}