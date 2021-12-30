#!/usr/bin/env csh

rm obf_test_result_1.v
java -classpath ../../lib/antlr.jar:../../build/classes Obfuscate sv obf_test.map.dat obf_test_1.v obf_test_result_1.v
