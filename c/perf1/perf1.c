/**
 * FileName: multiply.c
 * sh# gcc multiply.c -g -o multiply
 */
 
#include <stdio.h>
int fast_multiply(x,  y)
{
    return x * y;
}


int s6(x, y)
{
    int i, j, z;
    for (i = 0, z = 0; i < x; i++)
        z = z + y;
    return z;
}

int s5(x, y)
{
    return s6(x, y);
}

int s4(x, y)
{
    return s5(x, y);
}

int s3(x, y)
{
    return s4(x, y);
}

int s2(x, y)
{
    return s3(x, y);
}

int s1(x, y)
{
    return s2(x, y);
}
 
int main(int argc, char *argv[])
{
    int i,j;
    int x,y;
    for (i = 0; i < 20000; i ++) {
        for (j = 0; j <  30 ; j++) {
            x = fast_multiply(i, j);
            y = s1(i, j);
        }
    }
    printf("x=%d, y=%d\n", x, y);
    return 0;
}
