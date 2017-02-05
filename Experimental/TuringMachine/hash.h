#ifndef _BENS_TM_HASH_FUNC
#define _BENS_TM_HASH_FUNC

#include <stdint.h>
#include <stdlib.h>

// 1 MB for hash table default
// NOTE: the MAGIC_PRIME should be updated with table size
#define  TABLE_SIZE    0x100000
#define  MAGIC_PRIME   0xc0001
#define  STATE_MASK    0xffffff00

/* An action consists of:
 *    - Optionally writing an element of our alphabet (0: write, 1: no write, 
 *        8 bits for alphabet, total of 9 bits.
 *    - Move R,L,S - 2 bits (00: no move; 10: left; 01: right; 11: undefined)
 *
 *    Since we have 8 bytes to work with, we can think of the following layout:
 *
 *    +-----------------+
 *    | 1 bit for write |
 *    +--------+--------+
 *             |
 *    +-------+++--+-----+--------+--------+--------+--------+--------+--------+
 *    | ALPHA |b|  |     | SAME AS 1 AND 2 | SAME AS 1 AND 2 | SAME AS 1 AND 2 |
 *    +-------+-+--+-----+--------+--------+--------+--------+--------+--------+
 *     \_____/   \/ \___/
 *        |       |   |___________________________
 *        +-+     +-------+                      |
 *          |             |                      |
 * +--------+-------++----+------------++--------+--------+
 * | 8 bit encoding || Two bits for    || 5 bits for move |
 * | for alpha char || left/right/stay ||    multiplier   |
 * +----------------++----+------------++-----------------+
 */
typedef uint64_t action_t;
typedef uint64_t state_t;

/* The hashtable key has 8 least significant bits to store alphabet, remaining
 * 56 most significant bits storing the state. 
 * 63                                                     8       0
 * +------------------------------------------------------+-------+
 * |      Bits 63 - 8: State Being Mapped From            |Alpha  |
 * +------------------------------------------------------+-------+
 */
typedef uint64_t Key;

/* Hashtable Value stores the state being transfered to, and sets itself up
 * to be placed in a hash table bucket.
 */

typedef struct ht_value_ {
  state_t    state;  // State to be transfered to - Extra 8 bits of storage here
  action_t   action; // What do we do? This is actually a bit more general than
                     // a strict Turing Machine, but we have the extra space...
                     // (in particular, our system will pad with extra space, so
                     // lets use it...) We can write up to 4 chars and move 32
                     // spaces for each write.
} Value;

Value *new_value(action_t a, state_t s);

/* Key_Value_Pair */
typedef struct key_value_pair_ {
  struct key_value_pair_* next;
  Key key;
  Value value;
} KeyValuePair;

KeyValuePair *new_kvp(Key k, Value v);

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
  uint64_t       size;  
  KeyValuePair** buckets;
} HashTable;

HashTable* new_ht();
int        ht_init(HashTable *t);
int        ht_add(HashTable *t, Key k, Value v); 

/* Some hashy functions */
uint64_t _hash_key(Key k);   


#endif
