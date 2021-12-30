#!/usr/bin/env csh

rm -f nc_test_result_1.v nc_test_result_2.v
java -classpath ../../lib/antlr.jar:../../build/classes NameChange sv nc_test.map.dat nc_test_1.v nc_test_result_1.v
java -classpath ../../lib/antlr.jar:../../build/classes NameChange ver nc_test.map.dat nc_test_2.v nc_test_result_2.v
