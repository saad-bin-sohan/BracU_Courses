#include <stdio.h>
#include <string.h>

void checkEmailDomain(const char *email) {
    const char *oldDomain = "@kaaj.com";
    const char *newDomain = "@sheba.xyz";

    if (strstr(email, oldDomain)) {
        printf("Email address is outdated\n");
    } else if (strstr(email, newDomain)) {
        printf("Email address is okay\n");
    } else {
        printf("Invalid email address\n");
    }
}

int main() {
    char email[100];
    printf("Enter email address: ");
    scanf("%s", email);
    checkEmailDomain(email);
    return 0;
}
