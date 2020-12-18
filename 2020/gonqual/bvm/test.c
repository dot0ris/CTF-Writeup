#include <stdio.h>

int main ()
{
    void *p = malloc(0x20);
    free(p);
    free(p);
    return 0;
}
