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
        raise NotImplementedError("TODO")
        # TODO

        # call the read_matrix function
        t.call("read_matrix")

        # check the output from the function
        # TODO

        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)

    def test_simple(self):
        self.do_read_matrix()

    @classmethod
    def tearDownClass(cls):
        print_coverage("read_matrix.s", verbose=False)


class TestWriteMatrix(TestCase):

    def do_write_matrix(self, fail='', code=0):
        t = AssemblyTest(self, "write_matrix.s")
        outfile = "outputs/test_write_matrix/student.bin"
        # load output file name into a0 register
        t.input_write_filename("a0", outfile)
        # load input array and other arguments
        raise NotImplementedError("TODO")
        # TODO
        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        t.check_file_output(outfile, "outputs/test_write_matrix/reference.bin")

    def test_simple(self):
        self.do_write_matrix()

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
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)

        # compare the output file and
        raise NotImplementedError("TODO")
        # TODO
        # compare the classification output with `check_stdout`

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
