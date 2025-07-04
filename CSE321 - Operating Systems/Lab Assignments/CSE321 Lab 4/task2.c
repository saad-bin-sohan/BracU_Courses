#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <unistd.h>

#define MaxCrops 5
#define warehouseSize 5

sem_t empty;
sem_t full;
pthread_mutex_t mutex;

char crops[warehouseSize] = {'R', 'W', 'P', 'S', 'M'};
char warehouse[warehouseSize] = {'N', 'N', 'N', 'N', 'N'};
int in = 0;
int out = 0;

void *Farmer(void *far) {
    int id = *(int *)far;
    for (int i = 0; i < MaxCrops; i++) {
        sem_wait(&empty);
        pthread_mutex_lock(&mutex);
        
        warehouse[in] = crops[in];
        printf("Farmer %d: Insert crops %c at %d\n", id, crops[in], in);
        in = (in + 1) % warehouseSize;

        pthread_mutex_unlock(&mutex);
        sem_post(&full);
        
        sleep(1);
    }
    return NULL;
}

void *ShopOwner(void *sho) {
    int id = *(int *)sho;
    for (int i = 0; i < MaxCrops; i++) {
        sem_wait(&full);
        pthread_mutex_lock(&mutex);
        
        printf("Shop Owner %d: Remove crops %c from %d\n", id, warehouse[out], out);
        warehouse[out] = 'N';
        out = (out + 1) % warehouseSize;

        pthread_mutex_unlock(&mutex);
        sem_post(&empty);

        sleep(1);
    }
    return NULL;
}

int main() {
    pthread_t farmers[5], shopOwners[5];
    pthread_mutex_init(&mutex, NULL);
    sem_init(&empty, 0, warehouseSize);
    sem_init(&full, 0, 0);
    
    int ids[5] = {1, 2, 3, 4, 5};
    
    for (int i = 0; i < 5; i++) {
        pthread_create(&farmers[i], NULL, Farmer, &ids[i]);
    }

    for (int i = 0; i < 5; i++) {
        pthread_create(&shopOwners[i], NULL, ShopOwner, &ids[i]);
    }

    for (int i = 0; i < 5; i++) {
        pthread_join(farmers[i], NULL);
        pthread_join(shopOwners[i], NULL);
    }

    pthread_mutex_destroy(&mutex);
    sem_destroy(&empty);
    sem_destroy(&full);

    return 0;
}
