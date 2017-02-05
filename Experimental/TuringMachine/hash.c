#include "hash.h"

uint64_t _hash_key(Key k) {
  // FIXME: Temporary hash. Need to make it better (better quality, better
  // efficiency, etc) This is just a place holder
  uint64_t result = 0;
  uint32_t masked;
  // take 16 bits at a time
  for (int i = 3; i >= 0; --i){
    masked =  0xffff&(k >> (16*i));
    result += (MAGIC_PRIME * masked);  // This is commutative (and therefore shitty)
  }
  return result;
}
