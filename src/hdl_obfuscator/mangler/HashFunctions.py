#!/bin/env python3

def hash1(string) -> str:
    hash_value = 5381
    for char in string:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)
    ret_hash = hash_value & 0x7FFFFFFF
    return format(ret_hash, "08x")


def hash2(string) -> str:
    hash_value = 0
    for i, char in enumerate(string):
        if i % 2 == 0:
            hash_value ^= (hash_value << 7) ^ ord(char) ^ (hash_value >> 3)
        else:
            hash_value ^= ~((hash_value << 11) ^ ord(char) ^ (hash_value >> 5))
    ret_hash = hash_value & 0x7FFFFFFF
    return format(ret_hash, "08x")
