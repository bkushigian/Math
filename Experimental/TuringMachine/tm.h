#include <stdio.h>
#include <stdint.h>

typedef struct TM_ {
    uint32_t tapesize;
    uint8_t  *tape;
    /* TODO: Make hash table for function */
    // delta_t delta;
    uint64_t state; // 2^56 maximum states.
} TM;
