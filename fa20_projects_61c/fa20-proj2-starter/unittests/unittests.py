from unittest import TestCase
from framework import AssemblyTest, print_coverage


class TestAbs(TestCase):
    def test_zero(self):
        t = AssemblyTest(self, "abs.s")
        # load 0 into register a0
        t.input_scalar("a0", 0)
        # call the abs function
        t.call("abs")
        # check that after calling abs, a0 is equal to 0 (abs(0) = 0)
        t.check_scalar("a0", 0)
        # generate the `assembly/TestAbs_test_zero.s` file and run it through venus
        t.execute()

    def test_one(self):
        # same as test_zero, but with input 1
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", 1)
        t.call("abs")
        t.check_scalar("a0", 1)
        t.execute()
    
    def test_minus_one(self):
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", -1)
        t.call("abs")
        t.check_scalar("a0", 1)
        t.execute()
    
    def test_minus_69(self):
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", 69)
        t.call("abs")
        t.check_scalar("a0", 69)
        t.execute()
    
    def test_minus_69(self):
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", -69)
        t.call("abs")
        t.check_scalar("a0", 69)
        t.execute()

    @classmethod
    def tearDownClass(cls):
        print_coverage("abs.s", verbose=False)

class TestRelu(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([1, -2, 3, -4, 5, -6, 7, -8, 9])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [1, 0, 3, 0, 5, 0, 7, 0, 9])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()
    
    def test_two_harder(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([10, -10, 30, -44, 15, -160, 7, 99, 100, -1, -1, -1, -4])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [10, 0, 30, 0, 15, 0, 7, 99, 100, 0, 0, 0, 0])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()
    
    def test_one_elem_vector(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([10])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [10])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()
    
    def test_zero_vector(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute(code=78)
        
    def test_zero_more_vector(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([0, 0, 0, 0, -1, 0, 0])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [0, 0, 0, 0, 0, 0, 0])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()

    @classmethod
    def tearDownClass(cls):
        print_coverage("relu.s", verbose=False)

class TestArgmax(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([1, -2, 3, -4, 5, -6, 7, -8, 9])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 8)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()

    def test_duplicates(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([1, 1, 3, 3, 3, 3, 2, 2, 2])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 2)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()

    def test_one_elem(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([1])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 0)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()

    def test_negatives(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([-10, -11, -3, -3, -1, -3, -2, -2, -2])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 4)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()
        
    def test_zero_vector(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([0, 0, 0, 0, 0, 0])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 0)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()
    
    def test_zero_vector2(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute(code=77)
        

    @classmethod
    def tearDownClass(cls):
        print_coverage("argmax.s", verbose=False)

class TestDot(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        # load array attributes into argument registers
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 285)
        # Generate test file
        t.execute()
    
    def test_SUPER(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([-5, 99, 99, -6, 99, 99, -7, 99, 99, -8, 99, 99, -9])
        array1 = t.array([6, 99, 99, 99, 99, 7, 99, 99, 99, 99, 8, 99, 99, 99, 99, 9, 99, 99, 99, 99, 10])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        # load array attributes into argument registers
        t.input_scalar("a2", 5)  # Length of vectors
        t.input_scalar("a3", 3)  # Stride of vector0   
        t.input_scalar("a4", 5)  # Stride of vector1
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", -290)
        # Generate test file
        t.execute()
    
    def test_harder(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([-4, 7, 10])
        array1 = t.array([4, -7, -10])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        # load array attributes into argument registers
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", -165)
        # Generate test file
        t.execute()

    def test_harder(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([0, 4, -8, 0, 12, -1, 0])
        array1 = t.array([5, 8, 2, -4, 1, 9, 0])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        # load array attributes into argument registers
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
         # check the return value
        t.check_scalar("a0", 19)
        # Generate test file
        t.execute()
        
    def test_one_elem(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([4])
        array1 = t.array([5])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        # load array attributes into argument registers
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
         # check the return value
        t.check_scalar("a0", 20)
        # Generate test file
        t.execute()
    
    def test_stride_two(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([4, 5, 6, 7])
        array1 = t.array([4, 99, 5, 99, 6, 99, 7])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        # load array attributes into argument registers
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 2)
        # call the `dot` function
        t.call("dot")
         # check the return value
        t.check_scalar("a0", 126)
        # Generate test file
        t.execute()
    
    def test_stride_two_three(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([1, 99, 99, 2, 99, 99, 3])
        array1 = t.array([1, 99, 3, 99, 5])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        # load array attributes into argument registers
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 3)
        t.input_scalar("a4", 2)
        # call the `dot` function
        t.call("dot")
         # check the return value
        t.check_scalar("a0", 22)
        # Generate test file
        t.execute()
    
    def test_zero_vector(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([1, 0, 0, 0])
        array1 = t.array([0, 0, 0, 0])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        # load array attributes into argument registers
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 0)
        # Generate test file
        t.execute()
        
    def test_zero_vector2(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([])
        array1 = t.array([])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        # load array attributes into argument registers
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # Generate test file
        t.execute(code=75)
    
    def test_zero_stride(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([0, 0, 0, 1])
        array1 = t.array([0, 0, 1, 0])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        # load array attributes into argument registers
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 0)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # Generate test file
        t.execute(code=76)
    
    def test_zero_stride2(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([0, -1, 0, 1])
        array1 = t.array([-1, 0, 1, 0])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        # load array attributes into argument registers
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 0)
        # call the `dot` function
        t.call("dot")
        # Generate test file
        t.execute(code=76)

    @classmethod
    def tearDownClass(cls):
        print_coverage("dot.s", verbose=False)

class TestMatmul(TestCase):

    def do_matmul(self, m0, m0_rows, m0_cols, m1, m1_rows, m1_cols, result, code=0):
        t = AssemblyTest(self, "matmul.s")
        # we need to include (aka import) the dot.s file since it is used by matmul.s
        t.include("dot.s")
        # create arrays for the arguments and to store the result
        array0 = t.array(m0)
        array1 = t.array(m1)
        array_out = t.array([0] * len(result))

        # load address of input matrices and set their dimensions
        t.input_array("a0", array0)
        t.input_scalar("a1", m0_rows)
        t.input_scalar("a2", m0_cols)
        t.input_array("a3", array1)
        t.input_scalar("a4", m1_rows)
        t.input_scalar("a5", m1_cols)
        # load address of output array
        t.input_array("a6", array_out)

        # call the matmul function
        t.call("matmul")
        # check the content of the output array
        t.check_array(array_out, result)
        # generate the assembly file and run it through venus, we expect the simulation to exit with code `code`
        t.execute(code=code)

    def test_simple(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150]
        )

    def test_reverse(self):
        self.do_matmul(
            [3, -2, -1, 2, 6, -5, 7, 1, -8], 3, 3,
            [1, 9, 4, 0, 11, 5, -3, 2, -7], 3, 3,
            [6, 3, 9, 17, 74, 73, 31, 58, 89]
        )
        self.do_matmul(
            [1, 9, 4, 0, 11, 5, -3, 2, -7], 3, 3,
            [3, -2, -1, 2, 6, -5, 7, 1, -8], 3, 3,
            [49, 56, -78, 57, 71, -95, -54, 11, 49]
        )
    
    def test_one_elem(self):
        self.do_matmul(
            [5], 1, 1,
            [6], 1, 1,
            [30]
        )
        self.do_matmul(
            [0], 1, 1,
            [6], 1, 1,
            [0]
        )
    
    def test_uneven_matrices(self):
        self.do_matmul(
            [1], 1, 1,
            [1, 2], 1, 2,
            [1, 2],
        )
        self.do_matmul(
            [1, 2, 4, 5], 2, 2,
            [1, 9], 2, 1,
            [19, 49],
        )
        self.do_matmul(
            [1, -1, 3, 6, 0, -3, -4, 7, -1, 0, 4, 5], 6, 2,
            [-3, 1, 6, 7, 0, -7], 2, 3,
            [-10, 1, 13, 33, 3, -24, -21, 0, 21, 61, -4, -73, 3, -1, -6, 23, 4, -11],
        )
        self.do_matmul(
            [1, 3, 5, 7, 8, 9], 6, 1,
            [3, 1], 1, 2,
            [3, 1, 9, 3, 15, 5, 21, 7, 24, 8, 27, 9],
        )
        self.do_matmul(
            [1, 2, 3, 4, 5], 1, 5,
            [1, -1, 2, -2, 3, -3, 4, -4, 5, -5], 5, 2,
            [55, -55],
        )
     
    def test_cols(self):
        self.do_matmul(
            [5, 6, 7, 8, 9, 10, 11], 1, 7,
            [1, 2, 3, 4, 5, 6, 7], 7, 1,
            [252]
        )
    
    def test_rows(self):
        self.do_matmul(
            [5, 6, 7, -8, 9], 5, 1,
            [1, 2, -3, 4, 5], 1, 5,
            [5, 10, -15, 20, 25, 
             6, 12, -18, 24, 30,
             7, 14, -21, 28, 35,
             -8, -16, 24, -32, -40,
             9, 18, -27, 36, 45]
        )
    
    def test_error_code_72(self):
        self.do_matmul(
            [], 0, 1,
            [3, -2, -1, 2, 6, -5, 7, 1, -8], 3, 3,
            [0],
            72 
        )
        self.do_matmul(
            [], -1, 1,
            [3, -2, -1, 2, 6, -5, 7, 1, -8], 3, 3,
            [0],
            72 
        )
        self.do_matmul(
            [], 3, 0,
            [3, -2, -1, 2, 6, -5, 7, 1, -8], 3, 3,
            [0],
            72 
        )
        self.do_matmul(
            [], 10, -3,
            [3, -2, -1, 2, 6, -5, 7, 1, -8], 3, 3,
            [0],
            72 
        )
        self.do_matmul(
            [], 0, 0,
            [3, -2, -1, 2, 6, -5, 7, 1, -8], 3, 3,
            [0],
            72 
        )
    
    def test_error_code_73(self):
        self.do_matmul(
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2], 2, 4,
            [], 0, 3,
            [0],
            73 
        )
        self.do_matmul(
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2], 2, 4,
            [], -1, 3,
            [0],
            73 
        )
        self.do_matmul(
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2], 2, 4,
            [], 0, 0,
            [0],
            73 
        )
        self.do_matmul(
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2], 2, 4,
            [], 1, -1,
            [0],
            73 
        )

    def test_error_code_74(self):
        self.do_matmul(
            [1, 2, 1, 2, 1, 2, 1, 2], 2, 4,
            [1, 2, 3], 1, 3,
            [0],
            74
        )
        self.do_matmul(
            [1, 2, 1, 2, 1, 2, 1, 2, 1], 3, 3,
            [1, 2, 3], 4, 3,
            [0],
            74
        )
        self.do_matmul(
            [1, 2, 1, 2, 1, 2, 1, 2, 1], 4, 2,
            [1, 2, 1, 2, 1, 2, 1, 2, 1], 4, 2,
            [0],
            74
        )
        self.do_matmul(
            [1], 1, 4,
            [1, 2], 1, 2,
            [0],
            74
        )

    @classmethod
    def tearDownClass(cls):
        print_coverage("matmul.s", verbose=False)

class TestReadMatrix(TestCase):

    def do_read_matrix(self, fail='', code=0):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", "inputs/test_read_matrix/test_input.bin")

        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])

        # load the addresses to the output parameters into the argument registers
        t.input_array("a1", rows)
        t.input_array("a2", cols)

        # call the read_matrix function
        t.call("read_matrix")

        # check the output from the function
        t.check_array_pointer("a0", [1, 2, 3, 4, 5, 6, 7, 8, 9])
        t.check_array(rows, [3])
        t.check_array(cols, [3])

        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)

    def test_simple(self):
        self.do_read_matrix()
    
    
    def do_simple0_m1(self, fail='', code=0):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", "inputs/simple0/bin/m1.bin")

        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])

        # load the addresses to the output parameters into the argument registers
        t.input_array("a1", rows)
        t.input_array("a2", cols)

        # call the read_matrix function
        t.call("read_matrix")

        # check the output from the function
        t.check_array_pointer("a0", [1, 3, 5, 7, 9, 11, 13, 15, 17])
        t.check_array(rows, [3])
        t.check_array(cols, [3])

        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)

    def test_simple0(self):
        self.do_simple0_m1()
        
    def do_simple1_m1(self, fail='', code=0):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", "inputs/simple1/bin/m1.bin")
        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])
        # load the addresses to the output parameters into the argument registers
        t.input_array("a1", rows)
        t.input_array("a2", cols)
        # call the read_matrix function
        t.call("read_matrix")
        # check the output from the function
        t.check_array_pointer("a0", [1, -3, 4, 46, -2, -5, 2, -62, 
                                     0, 1, 3, 13, 26, -7, 34])
        t.check_array(rows, [5])
        t.check_array(cols, [3])
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
    
    def do_simple1_m0(self, fail='', code=0):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", "inputs/simple1/bin/m0.bin")
        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])
        # load the addresses to the output parameters into the argument registers
        t.input_array("a1", rows)
        t.input_array("a2", cols)
        # call the read_matrix function
        t.call("read_matrix")
        # check the output from the function
        t.check_array_pointer("a0", [-1, -2, 3, 4, -5, 6, -7, 8, 
                                     9, -10, 11, -12])
        t.check_array(rows, [3])
        t.check_array(cols, [4])
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
    
    
    def test_simple1(self):
        self.do_simple1_m1()
        self.do_simple1_m0()
    
    def do_simple2_m0(self, fail='', code=0):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", "inputs/simple2/bin/m0.bin")
        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])
        # load the addresses to the output parameters into the argument registers
        t.input_array("a1", rows)
        t.input_array("a2", cols)
        # call the read_matrix function
        t.call("read_matrix")
        # check the output from the function
        t.check_array_pointer("a0", [11, -10, 13, 10, -23, -6, -22, 10])
        t.check_array(rows, [4])
        t.check_array(cols, [2])
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        
    def do_simple2_m1(self, fail='', code=0):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", "inputs/simple2/bin/m1.bin")
        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])
        # load the addresses to the output parameters into the argument registers
        t.input_array("a1", rows)
        t.input_array("a2", cols)
        # call the read_matrix function
        t.call("read_matrix")
        # check the output from the function
        t.check_array_pointer("a0", [34, -14, 63, 15, 12, -5, -25, -63, 
                                     14, 36, -8, 25])
        t.check_array(rows, [3])
        t.check_array(cols, [4])
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)

    def test_simple2(self):
        self.do_simple2_m0()
        self.do_simple2_m1()

    def do_mnist_m1(self, fail='', code=0):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", "inputs/mnist/bin/m1.bin")
        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])
        # load the addresses to the output parameters into the argument registers
        t.input_array("a1", rows)
        t.input_array("a2", cols)
        # call the read_matrix function
        t.call("read_matrix")
        # check the output from the function
        # t.check_array_pointer("a0", [-3, 3, 13, 4, 3, 0, -4, -1, -17, -15, 0, 2, -4, -2, -4, -17, 18, 0, -9, -10, 11, 11, 23, 16, -1, 18, -1, -17, -2, -2, -18, 0, 4, 14, 17, 0, 0, -17, -1, 18, -16, 1, 13, 1, -9, -5, -18, -15, -16, 2, 23, -10, 0, 14, 0, 0, -13, 3, -9, 2, -13, -10, -11, 0, 25, 8, 0, 20, 9, -4, -2, -11, 0, 4, -16, 12, 11, 7, -3, 18, -10, -1, -3, 27, -19, 0, -12, 9, -17, 4, 26, 14, -10, 11, 20, 0, 1, -11, 7, 2, -10, 19, -8, 12, -20, -13, 2, -11, 18, 0, 0, 3, 9, 0, 8, -1, -11, -14, -3, 11, 0, 7, -2, -16, 3, -16, -1, 20,
        #                              -11, 0, 5, -11, 10, 0, 2, 0, -7, 20, 0, -13, -14, -10, -9, -4, 11, -14, 21, -10, -5, -1, 1, -9, 40, -6, 0, 6, 13, -18, 3, 0, -10, 15, 2, 0, 0, 13, 0, -13, -8, 6, 2, -5, -3, 25, 8, -5, -8, -2, -19, 20, 0, 11, 15, 0, 0, 14, -3, 2, -19, -10, 2, 0, 5, 15, 0, -3, -2, 15, 11, 4, 0, 15, 5, -3, 15, -6, 2, -15, 17, 10, 0, 0, 1, 0, -10, -8, -10, -12, 0, 10, -2, 9, 0, 33, 0, -5, 18, -4, -7, 8, -13, 16, 2, 9, 0, 0, -2, 0, 1, 0, 4, 20, 18, 0, 5, -1, -15, -7, 0, -14, -11, -2, -5, 10, 0, 11,
        #                              19, -6, 20, 16, 2, -2, 14, -1, 12, -3, -1, -12, 16, -16, 6, -3, 5, 1, -12, -12, -7, 9, -2, -17, -1, -6, 30, 13, 6, -9, -17, 0, -11, 6, -1, 22, 1, 16, 0, 13, -16, -9, 12, -18, 1, -8, -14, -17, -12, 32, -19, -7, 0, 4, -7, 0, 4, -12, 17, 2, 0, -10, 5, -1, 0, -3, 27, -17, 25, -1, -2, 1, -1, 11, -14, 2, -9, -5, 3, 11, 8, 2, -2, 0, 0, 0, -8, -17, 9, -8, 2, -16, -7, -7, 7, -4, 1, 13, 19, -11, 0, 12, -12, 11, -13, 14, 12, -17, 19, 0, 15, 19, 10, 4, 12, -1, -15, -10, -11, 12, 1, 3, 10, -21, -3, -7, -3, 3,
        #                              8, -5, 10, -5, 2, -1, 19, -2, 10, -17, -1, -7, -11, -5, -18, 5, 0, -11, 6, 16, 7, 12, -5, -8, -5, -9, -2, 14, 16, -21, 5, 32, -3, -15, 7, -4, 5, -17, -4, 0, 7, 0, -4, -10, -15, -9, -6, -8, -4, 0, -5, 9, 0, -15, 11, 0, 3, 15, 12, 13, 8, 7, -9, -2, -3, -9, -1, 5, 4, -6, -19, -3, -3, 3, -4, -19, -18, -9, 3, -1, -4, -7, 2, -1, 0, 0, -1, -11, 3, -1, -1, 17, -3, 2, -15, -1, 2, 15, 9, -3, 5, 15, 8, 16, -6, -14, 0, 21, -6, -1, -8, -14, 19, 11, -11, -2, -9, -5, 17, -5, 1, -8, 6, -15, -15, -6, 31, -4,
        #                              0, -9, 3, 14, 23, 0, 0, -1, 1, -10, 0, -4, 2, 10, 13, 4, -3, -2, 5, -14, 5, -18, 2, -17, -1, 0, 0, -13, -4, 0, -8, 0, 2, 3, -16, 0, 0, -1, -1, 6, -5, -16, 4, -3, 18, 11, -8, -14, -14, 0, -5, -8, 14, -11, 0, 33, 12, -9, -8, 16, 16, -10, -6, 0, -12, -8, -3, -15, 0, 6, -7, -15, 0, 10, 0, 8, -4, 0, 3, -9, -10, -18, 0, 0, -1, 30, -2, -15, 20, -13, 1, 9, 6, 0, -4, 0, 1, 14, 9, -4, -8, -3, 5, -21, 0, -10, -8, -16, -14, 0, -14, 8, 7, -4, 1, -1, 22, -1, 7, 3, 0, -12, 0, -7, -4, 1, -1, 18,
        #                              -1, 16, -10, -14, -18, 0, 1, 32, 0, -14, 0, -6, 23, 13, -18, 18, 9, 17, -8, -3, 0, -11, 3, -8, -1, 19, 0, 20, -4, 7, 18, -5, -2, 6, -22, -1, 0, 3, 35, -9, -15, 4, -2, -6, -18, -4, 11, -5, 1, 0, -6, 13, 0, -16, 13, 0, -15, 9, -2, 7, 11, 7, 13, -1, -6, -2, 0, 19, 13, -8, 18, -15, 0, -11, 17, -13, 21, 0, -3, 6, 13, -6, 27, 0, 12, 0, -20, -11, 7, -5, 3, -8, 11, -3, -11, 0, 0, 8, -13, 3, -8, 18, 1, -12, -7, 23, 0, -16, 20, 0, 6, -18, -8, 2, 6, 32, 1, 7, 1, 1, 0, 20, -14, 3, -5, 14, -1, -10,
        #                              -1, 3, 1, -17, -20, 0, 12, 0, 11, 4, 31, -6, -12, -7, -15, -5, -10, 7, 6, 7, 11, 6, -5, 18, -1, 5, -1, -7, 1, -10, 2, 0, 0, -16, 0, -1, 0, 14, 0, -22, 14, 10, 19, -10, -11, 12, 16, -5, 10, -2, 16, 13, 7, 5, 8, -1, 14, 0, -5, 0, -20, 0, -14, -1, -3, 15, -1, 14, -13, -6, -7, -11, 0, -6, -11, 19, -3, -2, -19, 13, -20, 0, -7, 0, -15, 0, 16, 16, 5, -7, -2, 3, 20, -14, 11, 0, 1, 14, -3, -2, -2, 7, 5, 17, -17, -9, -6, -13, -11, 0, 11, 6, 13, 8, -13, 0, 0, -3, -2, -2, 0, 8, 1, 4, -16, 19, -1, -12,
        #                              0, 0, 1, 13, -1, 26, 13, 0, -6, 13, 0, -8, 13, 21, 7, -6, -12, 18, -8, -2, -16, 7, 1, -15, 0, 8, 0, 10, -10, -17, 14, 0, 5, -1, -20, 0, 1, 13, 0, 7, 1, 19, 8, 19, 5, -3, -19, 3, 8, -6, 0, 0, 0, 18, 2, 0, -10, -6, -10, 9, 3, 18, -5, 0, -8, -13, 0, 15, -11, 13, 20, -8, 30, 10, -18, 1, 0, 1, 8, -11, -11, -8, 0, 0, -11, 0, 10, -7, -12, 0, 2, 18, -7, 15, -7, 0, 0, 0, -11, -2, -1, -11, 9, -18, -2, -4, 16, -19, -15, 0, 11, 2, 2, -8, 4, 0, -14, 24, 2, -13, 31, -3, 12, -4, 3, -19, -1, -12,
        #                              6, -7, -12, -17, 18, -1, -3, -8, 8, -13, -7, 10, -6, -14, -19, -13, 3, -14, 15, 10, 0, -1, 5, -13, -10, -6, -17, 4, 0, -13, -9, -4, -9, 4, -2, -6, 1, 13, -12, -9, 16, -18, 12, -14, 4, 0, -3, 7, 8, 2, 4, 20, 0, 1, 5, -3, 3, 1, 11, -8, 4, -14, 10, 19, 8, 9, -2, 10, 1, -18, 19, 20, -1, 9, 1, 13, 0, -3, 2, -15, -13, 15, -2, -7, -10, 0, 10, 13, -10, -6, -5, -6, 9, -11, -15, -22, 11, -9, -15, 11, -2, 14, -19, 0, -2, 12, -1, 12, 5, -8, 3, -11, 16, 9, 10, -9, -10, 3, -11, -10, 3, -15, 8, -13, 15, 17, -12, -5,
        #                              8, 5, 10, -10, 5, 0, -10, 0, 19, -4, 0, 20, -16, 17, -21, 9, -13, 16, 10, 11, -18, -9, 0, -21, -1, 1, 0, 1, 15, 1, -8, 0, -17, -9, -3, -1, 0, -1, -1, -17, -13, 6, 17, -21, -2, 0, -4, 5, 2, 3, -1, -3, 4, 20, -4, -20, 12, -16, 21, -13, 6, 18, 3, -1, 2, 11, 0, -5, -3, 18, -11, -13, -17, -1, -5, 19, 3, -9, 13, 15, 8, 14, 0, 0, -17, -22, -18, 0, -13, 0, 1, 4, 7, -1, 11, 0, 1, 16, -10, -11, -18, 3, -18, 18, -9, 17, -7, -5, -10, 25, 5, 13, -10, 11, -11, -1, -8, -3, -2, 16, -32, 20, 11, -5, 13, -16, -2, -17])
        t.check_array_pointer("a0", [-3, 3, 13, 4, 3, 0, -4, -1, -17, -15, 0, 2, -4, -2, -4, -17, 18, 0, -9, -10, 11, 11, 23, 16, -1, 18, -1, -17, -2, -2, -18, 0, 4, 14, 17, 0, 0, -17, -1, 18, -16, 1, 13, 1, -9, -5, -18, -15, -16, 2, 23, -10, 0, 14, 0, 0, -13, 3, -9, 2, -13, -10, -11, 0, 25, 8, 0, 20, 9, -4, -2, -11, 0, 4, -16, 12, 11, 7, -3, 18, -10, -1, -3, 27, -19, 0, -12, 9, -17, 4, 26, 14, -10, 11, 20, 0, 1, -11, 7, 2, -10, 19, -8, 12, -20, -13, 2, -11, 18, 0, 0, 3, 9, 0, 8, -1, -11, -14, -3, 11, 0, 7, -2, -16, 3, -16, -1, 20,
                                     -11, 0, 5, -11, 10, 0, 2, 0, -7, 20, 0, -13, -14, -10, -9, -4, 11, -14, 21, -10, -5, -1, 1, -9, 40, -6, 0, 6, 13, -18, 3, 0, -10, 15, 2, 0, 0, 13, 0, -13, -8, 6, 2, -5, -3, 25, 8, -5, -8, -2, -19, 20, 0, 11, 15, 0, 0, 14, -3, 2, -19, -10, 2, 0, 5, 15, 0, -3, -2, 15, 11, 4, 0, 15, 5, -3, 15, -6, 2, -15, 17, 10, 0, 0, 1, 0, -10, -8, -10, -12, 0, 10, -2, 9, 0, 33, 0, -5, 18, -4, -7, 8, -13, 16, 2, 9, 0, 0, -2, 0, 1, 0, 4, 20, 18, 0, 5, -1, -15, -7, 0, -14, -11, -2, -5, 10, 0, 11,
                                     19, -6, 20, 16, 2, -2, 14, -1, 12, -3, -1, -12, 16, -16, 6, -3, 5, 1, -12, -12, -7, 9, -2, -17, -1, -6, 30, 13, 6, -9, -17, 0, -11, 6, -1, 22, 1, 16, 0, 13, -16, -9, 12, -18, 1, -8, -14, -17, -12, 32, -19, -7, 0, 4, -7, 0, 4, -12, 17, 2, 0, -10, 5, -1, 0, -3, 27, -17, 25, -1, -2, 1, -1, 11, -14, 2, -9, -5, 3, 11, 8, 2, -2, 0, 0, 0, -8, -17, 9, -8, 2, -16, -7, -7, 7, -4, 1, 13, 19, -11, 0, 12, -12, 11, -13, 14, 12, -17, 19, 0, 15, 19, 10, 4, 12, -1, -15, -10, -11, 12, 1, 3, 10, -21, -3, -7, -3, 3,
                                     8, -5, 10, -5, 2, -1, 19, -2, 10, -17, -1, -7, -11, -5, -18, 5, 0, -11, 6, 16, 7, 12, -5, -8, -5, -9, -2, 14, 16, -21, 5, 32, -3, -15, 7, -4, 5, -17, -4, 0, 7, 0, -4, -10, -15, -9, -6, -8, -4, 0, -5])
        t.check_array(rows, [10])
        t.check_array(cols, [128])
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
       
    """
    NOTE: mnist does not work on local computer but works on venus terminal 
    """    
    def test_mnist(self):
        self.do_mnist_m1()

    def test_malloc(self):
        self.do_read_matrix('malloc', 88)
        self.do_simple0_m1('malloc', 88)
        self.do_simple2_m0('malloc', 88)
        self.do_mnist_m1('malloc', 88)

    def test_fopen(self):
        self.do_read_matrix('fopen', 90)
        self.do_simple0_m1('fopen', 90)
        self.do_simple2_m0('fopen', 90)
        self.do_mnist_m1('fopen', 90)
    
    def test_fread(self):   
        self.do_read_matrix('fread', 91)
        self.do_simple0_m1('fread', 91)
        self.do_simple2_m0('fread', 91)
        self.do_mnist_m1('fread', 91)
        
    def test_fclose(self):
        self.do_read_matrix('fclose', 92)
        self.do_simple0_m1('fclose', 92)
        self.do_simple2_m0('fclose', 92)
        self.do_mnist_m1('fclose', 92)

    @classmethod
    def tearDownClass(cls):
        print_coverage("read_matrix.s", verbose=False)

class TestWriteMatrix(TestCase):

    def do_write_matrix(self, fail='', code=0):
        t = AssemblyTest(self, "write_matrix.s")
        in_array = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        rows = 3
        cols = 3
        
        outfile = "outputs/test_write_matrix/student.bin"
        # load output file name into a0 register
        t.input_write_filename("a0", outfile)
        # load input array and other arguments
        t.input_array("a1", in_array)
        t.input_scalar("a2", rows)
        t.input_scalar("a3", cols)
        
        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        if not fail:
            t.check_file_output(outfile, "outputs/test_write_matrix/reference.bin")

    def test_simple(self):
        self.do_write_matrix()

    def do_test_basic_main_0(self, fail='', code=0):
        t = AssemblyTest(self, "write_matrix.s")
        in_array = t.array([171, 441, 711])
        rows = 3
        cols = 1
        
        outfile = "outputs/test_basic_main/student0.bin"
        # load output file name into a0 register
        t.input_write_filename("a0", outfile)
        # load input array and other arguments
        t.input_array("a1", in_array)
        t.input_scalar("a2", rows)
        t.input_scalar("a3", cols)
        
        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        
        t.check_file_output(outfile, "outputs/test_basic_main/reference0.bin")

    def do_test_basic_main_1(self, fail='', code=0):
        t = AssemblyTest(self, "write_matrix.s")
        in_array = t.array([-34, 884, -1076, 74, 394])
        rows = 5
        cols = 1
        
        outfile = "outputs/test_basic_main/student1.bin"
        # load output file name into a0 register
        t.input_write_filename("a0", outfile)
        # load input array and other arguments
        t.input_array("a1", in_array)
        t.input_scalar("a2", rows)
        t.input_scalar("a3", cols)
        
        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        if not fail:
            t.check_file_output(outfile, "outputs/test_basic_main/reference1.bin")

    def test_basic_main(self):
        self.do_test_basic_main_0()
        self.do_test_basic_main_1()

    def do_test_harder_0(self, fail='', code=0):
        t = AssemblyTest(self, "write_matrix.s")
        in_array = t.array([1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8,
                            1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8])
        rows = 10
        cols = 8

        outfile = "outputs/test_harder/student0.bin"
        # load output file name into a0 register
        t.input_write_filename("a0", outfile)
        # load input array and other arguments
        t.input_array("a1", in_array)
        t.input_scalar("a2", rows)
        t.input_scalar("a3", cols)
        
        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        if not fail:
            t.check_file_output(outfile, "outputs/test_harder/harder0.bin")

    def do_test_harder_1(self, fail='', code=0):
        t = AssemblyTest(self, "write_matrix.s")
        in_array = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        rows = 1
        cols = 15

        outfile = "outputs/test_harder/student1.bin"
        # load output file name into a0 register
        t.input_write_filename("a0", outfile)
        # load input array and other arguments
        t.input_array("a1", in_array)
        t.input_scalar("a2", rows)
        t.input_scalar("a3", cols)
        
        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        t.check_file_output(outfile, "outputs/test_harder/harder1.bin")

    def do_test_harder_2(self, fail='', code=0):
        t = AssemblyTest(self, "write_matrix.s")
        in_array = t.array([-11])
        rows = 1
        cols = 1

        outfile = "outputs/test_harder/student2.bin"
        # load output file name into a0 register
        t.input_write_filename("a0", outfile)
        # load input array and other arguments
        t.input_array("a1", in_array)
        t.input_scalar("a2", rows)
        t.input_scalar("a3", cols)
        
        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        if not fail:
            t.check_file_output(outfile, "outputs/test_harder/harder2.bin")

    def test_harder(self):
        self.do_test_harder_0()
        self.do_test_harder_1()
        self.do_test_harder_2()

    def test_fopen(self):
        self.do_write_matrix('fopen', 93)
        self.do_test_basic_main_1('fopen', 93)
        self.do_test_harder_0('fopen', 93)
        self.do_test_harder_2('fopen', 93)
    
    def test_fwrite(self):
        self.do_write_matrix('fwrite', 94)
        self.do_test_basic_main_1('fwrite', 94)
        self.do_test_harder_0('fwrite', 94)
        self.do_test_harder_2('fwrite', 94)

    def test_fclose(self):
        self.do_write_matrix('fclose', 95)
        self.do_test_basic_main_1('fclose', 95)
        self.do_test_harder_0('fclose', 95)
        self.do_test_harder_2('fclose', 95)


    @classmethod
    def tearDownClass(cls):
        print_coverage("write_matrix.s", verbose=False)


class TestClassify(TestCase):

    def make_test(self):
        t = AssemblyTest(self, "classify.s")
        t.include("argmax.s")
        t.include("dot.s")
        t.include("matmul.s")
        t.include("read_matrix.s")
        t.include("relu.s")
        t.include("write_matrix.s")
        return t

    def test_simple0_input0(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/student0.bin"
        ref_file = "outputs/test_basic_main/reference0.bin"
        args = ["inputs/simple0/bin/m0.bin", "inputs/simple0/bin/m1.bin",
                "inputs/simple0/bin/inputs/input0.bin", out_file]

        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)

        # compare the output file and
        t.check_file_output(out_file, ref_file)

        # compare the classification output with `check_stdout`
        t.check_stdout("2")

    @classmethod
    def tearDownClass(cls):
        print_coverage("classify.s", verbose=False)


class TestMain(TestCase):

    def run_main(self, inputs, output_id, label):
        args = [f"{inputs}/m0.bin", f"{inputs}/m1.bin", f"{inputs}/inputs/input0.bin",
                f"outputs/test_basic_main/student{output_id}.bin"]
        reference = f"outputs/test_basic_main/reference{output_id}.bin"
        t = AssemblyTest(self, "main.s", no_utils=True)
        t.call("main")
        t.execute(args=args, verbose=False)
        t.check_stdout(label)
        t.check_file_output(args[-1], reference)

    def test0(self):
        self.run_main("inputs/simple0/bin", "0", "2")

    def test1(self):
        self.run_main("inputs/simple1/bin", "1", "1")
