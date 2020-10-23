#include <stdio.h>

int main ()
{
    char v5 = 0;
    int v8 = 0;
    int v7 = 0;
    int v6;
    char *i;
    char *a1 = "++dlME,hLMM`";
    char a2[64] = {0};
    int a3 = 1000;
    int prev[64] = {96, 104, 47, 106, 107, 108, 40, 110, 89, 61, 97, 94, 99, 100, 101, 102, 73, 74, 42, 76, 77, 43, 79, 80, 81, 82, 83, 84, 85, 60, 87, 88, 65, 66, 67, 45, 69, 70, 71, 72, 119, 120, 121, 122, 48, 49, 46, 51, 111, 126, 113, 114, 115, 116, 41, 118, 53, 44, 55, 62, 57, 56, 78, 105};
    char *mapper;

    for ( int j = 0; j < 64; ++j) 
    {
        mapper[prev[j]] = j;
    }

    for ( i = a1; *i; ++i )
    {
        v6 = mapper[*i];
        if ( v6 != -1 )
        {
        switch ( v7 )
        {
            case 0:
            ++v7;
            break;
            case 1:
            if ( v8 < a3 )
                a2[v8++] = ((v6 & 0x30) >> 4) | 4 * v5;
            ++v7;
            break;
            case 2:
            if ( v8 < a3 )
                a2[v8++] = ((v6 & 0x3C) >> 2) | 16 * (v5 & 0xF);
            ++v7;
            break;
            case 3:
            if ( v8 < a3 )
                a2[v8++] = v6 | ((v5 & 3) << 6);
            v7 = 0;
            break;
            default:
            break;
        }
        v5 = v6;
        }
    }

    printf("%s", a2);
}