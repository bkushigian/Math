#include <stdio.h>
#include "../hash.h"

const int TEST_SIZE = 1<<22;
int main(){

  printf("--- Testing Collisions ---\n");
  uint8_t collisions[TABLE_SIZE];
  for (int i = 0; i < TABLE_SIZE; ++i){
    collisions[i] = 0;
  }

  int total_collisions = 0;
  int max_collisions   = 0;
  uint64_t h;
  // Test some subset of values
  for (Key k = 0; k < TEST_SIZE; ++k){
    h = _hash_key(k);
    if (collisions[h]) {
      printf("Key %lu hashes to %lu: Collision #%d\n", k, h, collisions[h]);
      ++total_collisions;
      if (max_collisions < collisions[h]) {
        max_collisions = collisions[h];
      }
    }
    ++collisions[h];
  }
  printf("Total collisions: %d, Max Collisions: %d\n", total_collisions, max_collisions);
  printf("Collisions Percentage: %f%% \n", ((float)total_collisions / (float)TEST_SIZE) * 100);

  //HashTable *t = new_ht();
  //ht_init(t);

  //printf("Hash Table size = %lu\n", t->size);


}
