#include <stdio.h>

int main ()
{
    int max, min, age;

    while(1) {
        scanf("%d %d %d", &age, &min, &max);
        max = (max-age) * (max-age);
        min = (age-min) * (age-min);
        printf("%d %d\n", min, max);
    }
}
