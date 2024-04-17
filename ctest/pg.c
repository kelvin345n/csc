#include <stdio.h>
#include <string.h>
struct point {
    char x;
    int i;
    double y;
};

int main(void){
    size_t x = 5;
    int y = 5;
    int z = 2;
    int w = y / z;

    printf("%ld\n", sizeof(y));
    printf("%ld\n", sizeof(x));
    printf("%d\n", w);
}