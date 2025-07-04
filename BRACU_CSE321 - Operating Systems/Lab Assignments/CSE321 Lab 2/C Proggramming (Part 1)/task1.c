#include <stdio.h>

struct Item {
    int quantity;
    float unit_price;
};

int main() {
    struct Item paratha, vegetable, water;
    int num_people;
    float total_bill, individual_share;

    printf("Quantity of Paratha: ");
    scanf("%d", &paratha.quantity);
    printf("Unit Price: ");
    scanf("%f", &paratha.unit_price);

    printf("Quantity of Vegetables: ");
    scanf("%d", &vegetable.quantity);
    printf("Unit Price: ");
    scanf("%f", &vegetable.unit_price);

    printf("Quantity of Mineral Water: ");
    scanf("%d", &water.quantity);
    printf("Unit Price: ");
    scanf("%f", &water.unit_price);

    total_bill = (paratha.quantity * paratha.unit_price) + (vegetable.quantity * vegetable.unit_price) + (water.quantity * water.unit_price);

    printf("Number of People: ");
    scanf("%d", &num_people);

    if (num_people > 0) {
        individual_share = total_bill / num_people;
        printf("Total Bill: %.2f tk\n", total_bill);
        printf("Individual Share: %.2f tk\n", individual_share);
    } else {
        printf("Number of people must be greater than zero.\n");
    }

    return 0;
}
