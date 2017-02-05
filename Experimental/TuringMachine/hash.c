#include "hash.h"

// Value Functions
Value* new_value(action_t a, state_t s){
  Value* result  = (Value*)malloc(sizeof(Value));
  result->action = a;
  result->state  = s;
  return result;
}

// KeyValuePair Functions
KeyValuePair *new_kvp(Key k, Value v){
  KeyValuePair* result = (KeyValuePair*)malloc(sizeof(KeyValuePair));
  result->key   = k;
  result->value = v;
}

// HashTable functions
HashTable* new_ht(){
  HashTable* result = (HashTable*)malloc(sizeof(HashTable));
  result->size = 0;
  result->buckets = NULL;
  return result;
}

int ht_init(HashTable *t){
  t->size = TABLE_SIZE;
  t->buckets = (KeyValuePair**)malloc(sizeof(KeyValuePair*)*TABLE_SIZE);
  if (t->buckets == NULL){ 
    return 1; // FAILURE
  } 
  for (int i = 0; i < TABLE_SIZE; ++i){
    t->buckets[i] = NULL;
  }
  return 0;
}

int ht_add(HashTable* t, Key k, Value v){
  KeyValuePair *kvp = (KeyValuePair*)malloc(sizeof(KeyValuePair));
  KeyValuePair *n = NULL;  // For iterating through bucket
  // Create KVP
  kvp->key   = k;
  kvp->value = v;
  kvp->next  = NULL;
  uint64_t hashed;
  hashed = _hash_key(k);
  if (t->buckets[hashed] == NULL){
    return 0;
  }
}


/* Hashy Functions */
uint64_t _hash_key(Key k) {
  // TODO: make an actual hash table...
  return k % TABLE_SIZE;
}
