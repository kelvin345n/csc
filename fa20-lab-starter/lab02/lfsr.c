#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "lfsr.h"

void lfsr_calculate(uint16_t *reg) {
    uint16_t zeroth, second, third, fifth, fifteenth, temp;

    temp = 1; // Get the 0th bit
    zeroth = *reg & temp;

    temp = 1 << 2; // Get the 2nd bit
    second = (*reg & temp) >> 2;

    temp = 1 << 3; // Get the 3rd bit
    third = (*reg & temp) >> 3;

    temp = 1 << 5; // Get the 5th bit
    fifth = (*reg & temp) >> 5;

    //Calculate new 15th bit.
    fifteenth = (((zeroth ^ second) ^ third) ^ fifth);
    // Add 15th bit to the 15th slot.
    temp = fifteenth << 15;
    *reg = (*reg >> 1) | temp; // Shifts reg to right and adds 15th bit.
}

