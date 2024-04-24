package com.signature.hdlobf;

public class HashFunctions {
    public static String hash1(String str) {
        int hash = 5381;
        for (int i = 0; i < str.length(); i++) {
            hash = ((hash << 5) + hash) + str.charAt(i);
        }
        long ret_hash = (hash & 0x7FFFFFFF);
        return Long.toHexString(ret_hash);
    }

    public static String hash2(String str) {
        int hash = 0;
        for (int i = 0; i < str.length(); i++) {
            if ((i & 1) == 0) {
                hash ^= ((hash << 7) ^ str.charAt(i) ^ (hash >> 3));
            } else {
                hash ^= (~((hash << 11) ^ str.charAt(i) ^ (hash >> 5)));
            }
        }
        long ret_hash = (hash & 0x7FFFFFFF);
        return Long.toHexString(ret_hash);
    }
}
