// ----------------------------------------------------------
// Module: nc_test_1
// ----------------------------------------------------------
module nc_test_1
(
	// input ports
	input1,
	input2,
	// output ports
	output1,
	output2
);

	// input ports
	input input1;
	input input2;

	// output ports
	output output1;
	output output2;


	assign output1 = input1 & input2;
	assign output2 = ^{input1,input2};

endmodule // verilogtest_1
