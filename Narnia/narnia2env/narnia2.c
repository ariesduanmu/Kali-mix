#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char * argv[]){
    char buff[128];

    if (argc == 1) {
	printf("Usage: %s argument\n", argv[0]);
	exit(1);
    }
    strcpy(buff, argv[1]);
    printf("%s", buff);

    return 0;
}
