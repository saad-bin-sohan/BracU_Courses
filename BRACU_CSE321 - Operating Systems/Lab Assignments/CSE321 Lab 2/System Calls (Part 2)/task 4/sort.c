#include <stdio.h>
#include <stdlib.h>

int compare(const void *a, const void *b) {
    return (*(int *)b - *(int *)a);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <numbers>\n", argv[0]);
        return 1;
    }

    int arr[argc - 1];
    for (int i = 1; i < argc; i++) {
        arr[i - 1] = atoi(argv[i]);
    }

    qsort(arr, argc - 1, sizeof(int), compare);

    printf("Sorted array in descending order:\n");
    for (int i = 0; i < argc - 1; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}
