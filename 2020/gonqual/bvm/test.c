#include <stdio.h>

int main ()
{
    int p[4] = {0, 1, 2, 3};
    printf("%d\n", *(char *)(p+2));
}
