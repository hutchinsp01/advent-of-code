#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *name;
    int flowRate;
    char *tunnels[10];
} Valve;

typedef struct {
    int length;
    int alloc;
    Valve **array;
} Valves;

static Valves* readValves(char *filename) {
    FILE *fp;
    char name[2];
    int flowRate;

    Valves *valves = malloc(sizeof(Valves));
    valves->alloc = 2;
    valves->length = 0;
    valves->array = malloc(sizeof(Valve) * 2);

    // Valve OM has flow rate=0; tunnels lead to valves AA, EZ
    fp = fopen(filename, "r");
    while (fscanf(fp, "Valve %s has flow rate=%d;", name, flowRate) != EOF)
    {
        printf("name %s, flowRate %d", name, flowRate);

        // if (valves->length == valves->alloc) {
        //     valves->alloc *= 2;
        //     valves->array = realloc(valves->array, sizeof(Valve) * valves->alloc);
        // }

        // Valve *valve = malloc(sizeof(Valve));
        // valves->array[valves->length] = valve;
        // valves->length++;

        // char *name = strtok(buff, " ");
        // printf("name: %s", name);
        // valve->name = name;

        // char *flowRate = strtok(NULL, " ");
        // valve->flowRate = atoi(flowRate);

        // printf("name: %s, flowRate: %d", valve->name, valve->flowRate);

        // char *tunnels = strtok(NULL, " ");
        // int i = 0;
        // while (tunnels != NULL) {
        //     valve->tunnels[i] = tunnels;
        //     i++;
        //     tunnels = strtok(NULL, " ");
        // }
    }
}

int
main()
{
    Valves *valves;

    valves = readValves("day16-test.txt");
}
