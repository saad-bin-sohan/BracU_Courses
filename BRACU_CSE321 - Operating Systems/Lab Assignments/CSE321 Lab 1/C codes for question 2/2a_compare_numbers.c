#include <stdio.h>

int main() {
    int num1, num2;
    printf("Enter two numbers: ");
    scanf("%d %d", &num1, &num2);

    if (num1 > num2) {
        printf("Result (Subtraction): %d\n", num1 - num2);
    } else if (num1 < num2) {
        printf("Result (Addition): %d\n", num1 + num2);
    } else {
        printf("Result (Multiplication): %d\n", num1 * num2);
    }
    return 0;
}

