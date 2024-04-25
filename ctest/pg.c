#include <stdio.h>
#include <string.h>
#include <stdint.h>

struct point {
    char x;
    int i;
    double y;
};

int main(void){
    int8_t x = 50;
    int8_t y = 5;
    int8_t z = x * y;
    printf("%d\n", z);
}