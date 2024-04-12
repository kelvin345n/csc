#include <stdio.h>
#include <string.h>
struct point {
    char x;
    int i;
    double y;
};

int main(void){
    struct point p1 = {0, 1, 2};
    struct point *p = &p1;

    printf("%d\n", sizeof(p1));
    printf("%d\n", sizeof(p));
}