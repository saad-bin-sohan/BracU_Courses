#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

void removeExtraSpaces(const char *inputFile, const char *outputFile) {
    FILE *input = fopen(inputFile, "r");
    FILE *output = fopen(outputFile, "w");

    if (!input || !output) {
        printf("Error opening files.\n");
        exit(1);
    }

    char line[1024];
    while (fgets(line, sizeof(line), input)) {
        char *word = strtok(line, " \t\n");
        while (word) {
            fprintf(output, "%s ", word);
            word = strtok(NULL, " \t\n");
        }
        fprintf(output, "\n");
    }

    fclose(input);
    fclose(output);
}

int main() {
    char inputFile[50], outputFile[50];
    printf("Enter input file name: ");
    scanf("%s", inputFile);
    printf("Enter output file name: ");
    scanf("%s", outputFile);

    removeExtraSpaces(inputFile, outputFile);
    printf("Extra spaces removed and written to %s\n", outputFile);

    return 0;
}
