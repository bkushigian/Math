#ifndef _BENS_TM_HASH_FUNC
#define _BENS_TM_HASH_FUNC

#include <stdint.h>

typedef uint64_t action;

/* The hashtable key has 8 least significant bits to store alphabet, remaining
 * 56 most significant bits storing the state. 
 * 63                                                     8       0
 * +------------------------------------------------------+-------+
 * |      Bits 63 - 8: State Being Mapped From            |Alpha  |
 * +------------------------------------------------------+-------+
 */
typedef uint64_t Key;    

/* Hashtable ValueNode stores the state being transfered to, and sets itself up
 * to be placed in a hash table bucket.
 * */

typedef struct hashtable_value_node_ {
  ValueNode* next;  // Next value in the bucket (w/ same hash code)
  uint64_t   state; // State to be transfered to - Extra 8 bits of storage here
} ValueNode;

/*
 * HashTable: Hashes input for the delta function of a TM, namely, its Keys are
 * of the form:
 *
 *                                 Q x \Gamma 
 *
 * while it's Values are of the form    
 *
 *                           Q x \Gamma x {L, S, R} 
 *
 */
typedef struct hashtable_ {
  
} HashTable;

#endif
