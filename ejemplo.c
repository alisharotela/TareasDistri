#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // tamaño del vector argv
    char * programa = argv[1];
    int nro_procesos = atoi(argv[2]);
    printf("%d\nla cantidad es \n", argc);
    // Verificar si el numero de argumentos concide con el esperado
    
    if (argc != nro_procesos + 2)
    {
        printf("Error: Numero de argumentos incorrecto\n");
        return 1;
    }

}