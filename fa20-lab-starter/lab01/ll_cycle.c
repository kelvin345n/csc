#include <stddef.h>
#include "ll_cycle.h"


// No Cycle is 0
// Cycle is 1
int ll_has_cycle(node *head) {
    node* tortoise = head;
    node* hare = head;

    while (hare != NULL){
        hare = (*hare).next;
        tortoise = (*tortoise).next;

        if (hare != NULL){
            hare = (*hare).next;
        }

        if (hare == tortoise){
            if (hare == NULL){
                return 0;
            }
            return 1;
        }
    }
    return 0;
}