#include <stdio.h>

int is_perfect(int num) {
    int sum = 0;

    for (int i = 1; i < num; i++) {
        if (num % i == 0) {
            sum += i;
        }
    }

    return sum == num;
}

void find_perfect_numbers(int start, int end) {
    printf("Perfect numbers between %d and %d are:\n", start, end);

    for (int i = start; i <= end; i++) {
        if (is_perfect(i)) {
            printf("%d\n", i);
        }
    }
}

int main() {
    int start, end;

    printf("Enter the starting number: ");
    scanf("%d", &start);
    printf("Enter the ending number: ");
    scanf("%d", &end);
    find_perfect_numbers(start, end);
    return 0;
}
