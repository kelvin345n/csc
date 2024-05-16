.globl classify

.text
classify:
    # =====================================
    # COMMAND LINE ARGUMENTS
    # =====================================
    # Args:
    #   a0 (int)    argc
    #   a1 (char**) argv
    #   a2 (int)    print_classification, if this is zero, 
    #               you should print the classification. Otherwise,
    #               this function should not print ANYTHING.
    # Returns:
    #   a0 (int)    Classification
    # Exceptions:
    # - If there are an incorrect number of command line args,
    #   this function terminates the program with exit code 89.
    # - If malloc fails, this function terminates the program with exit code 88.
    #
    # Usage:
    #   main.s <M0_PATH> <M1_PATH> <INPUT_PATH> <OUTPUT_PATH>
    # ===========================================================================
    # Checking for input errors
    li t0, 4                               # 4 is required number of args
    bne a0, t0, argc_error     

    # Prologue
    addi sp, sp, -48
    sw ra 0(sp)
    sw s0, 4(sp)
    sw s1, 8(sp)
    sw s2, 12(sp)
    sw s3, 16(sp)
    sw s4, 20(sp)
    sw s5, 24(sp)
    sw s6, 28(sp)
    sw s7, 32(sp)
    sw s8, 36(sp)
    sw s9, 40(sp)
    sw s10, 44(sp)
    # Prologue
    
    mv s0, a0                               # s0: argc (int)
    mv s1, a1                               # s1: argv (char**)
    mv s2, a2                               # s2: classification (int)
	# =====================================
    # LOAD MATRICES
    # =====================================
    
    # Load pretrained m0
    # we need to malloc memory for the integer pointers. 
    li a0, 8                                # the row and col pointers will be next to eachother in memory
    jal malloc
    # Checking for malloc error *** MUST FREE: s3 & s4 ***
    beq a0, x0, malloc_error
                                            # s3 holds the start of the rows and cols for m0
    mv s3, a0                               # pointer to num of rows for m0
    addi t0, s3, 4                          # pointer to cols for m0
    # calling read_matrix
    lw t1, 0(s1)                            # t1 holds the pointer to the m0 path
    mv a0, t1
    mv a1, s3
    mv a2, t0
    jal read_matrix                         # a0 holds pointer to m0 in memory
    mv s4, a0                               # s4 holds pointer to m0 in memory
   
    # Load pretrained m1
    # we need to malloc memory for the integer pointers. 
    li a0, 8                                # the row and col pointers will be next to eachother in memory
    jal malloc
    # Checking for malloc error             *** MUST FREE: s5 & s6 ***
    beq a0, x0, malloc_error
                                            # s5 holds the start of the rows and cols for m1
    mv s5, a0                               # pointer to num of rows for m1
    addi t0, s5, 4                          # pointer to cols for m1
    # calling read_matrix
    lw t1, 4(s1)                            # t1 holds the pointer to the m1 path
    mv a0, t1
    mv a1, s5
    mv a2, t0
    jal read_matrix                         # a0 holds pointer to m1 in memory
    mv s6, a0                               # s6 holds pointer to m1 in memory

    # Load input matrix m(in)
    # we need to malloc memory for the integer pointers. 
    li a0, 8                                # the row and col pointers will be next to eachother in memory
    jal malloc
    # Checking for malloc error             *** MUST FREE: s7 & s8 ***
    beq a0, x0, malloc_error
                                            # s7 holds the start of the rows and cols for m(in)
    mv s7, a0                               # pointer to num of rows for m(in)
    addi t0, s7, 4                          # pointer to cols for m(in)
    # calling read_matrix
    lw t1, 8(s1)                            # t1 holds the pointer to the m(in) path
    mv a0, t1
    mv a1, s5
    mv a2, t0
    jal read_matrix                         # a0 holds pointer to m(in) in memory
    mv s6, a0                               # s8 holds pointer to m(in) in memory

    # =====================================
    # RUN LAYERS
    # =====================================
    # 1. LINEAR LAYER:    m0 * input   -> matmul.s on m0 and m(in)
    # 2. NONLINEAR LAYER: ReLU(m0 * input)
    # 3. LINEAR LAYER:    m1 * ReLU(m0 * input)

    # -=+ LINEAR LAYER +=-
    # Malloc space for the dot product of m0 and m(in). Should be m0.rows x m(in).cols x 4 bytes
    lw t0, 0(s3)                            # t0 holds (int) m0 rows
    lw t1, 4(s7)                            # t1 holds (int) m(in) cols
    mul t2, t0, t1                          # t2: number of elements of resulting matrix from dot product of m0 and m(in)
    li t3, 4
    mul t2, t2, t3                          # t2: number of bytes we need to malloc for resulting matrix
    # Calling malloc
    mv a0, t2                               
    jal malloc
    # Checking for malloc error             *** MUST FREE: s9***
    beq a0, x0, malloc_error
    mv s9, a0                               # s9 holds the resulting matrix of m0*m(in)
    # Loading into matmul
    mv a0, s4                               # Load in pointer to m0
    lw a1, 0(s3)                            # Load in rows to m0 (int)
    lw a2, 4(s3)                            # Load in cols (int)
    mv a3, s8                               # Load in ptr to m(in)
    lw a4, 0(s7)                            # rows to m(in)   
    lw a5, 4(s7)                            # load in cols
    mv a6, s9                               # load in ptr to new matrix m(0*in)
    jal matmul
    
    # -=+ NONLINEAR LAYER TIME...BOOYAH!!! +=-
    # Calling relu on the m(0*in) matrix
    mv a0, s9                               # Loading ptr to m(0*in)
    # Calculating num of elems in m(0*in). m0.rows * m(in).cols
    lw t0, 0(s3)                            # t0 holds (int) m0 rows
    lw t1, 4(s7)                            # t1 holds (int) m(in) cols
    mul t2, t0, t1                          # t2: number of elements of m(0*in)
    mv a1, t2
    jal relu                                # Note: does relu operation in place.
    
    # -=+ LINEAR LAYER AGAIN!!! AGHHHH +=-
    # calling the dot product of m1*m(0*in)
    # Malloc space for the dot product of m1 and m(0*in). Should be m1.rows x m(0*in).cols x 4 bytes
    lw t0, 0(s5)                            # t0 holds (int) m1 rows
    lw t1, 4(s7)                            # t1 holds (int) m(0*in) cols. (AKA m(in).cols)
    mul t2, t0, t1                          # t2: number of elements of resulting matrix from dot product of m0 and m(in)
    li t3, 4
    mul t2, t2, t3                          # t2: number of bytes we need to malloc for resulting matrix
    # Calling malloc
    mv a0, t2                               
    jal malloc
    # Checking for malloc error             *** MUST FREE: s10***
    beq a0, x0, malloc_error
    mv s10, a0                               # s10 holds the resulting matrix of m1*m(0*in). lets call it m(1*0in)
    
    # Loading into matmul
    mv a0, s6                               # Load in pointer to m1
    lw a1, 0(s5)                            # Load in rows to m1 (int)
    lw a2, 4(s5)                            # Load in cols (int) to ^
    mv a3, s9                               # Load in ptr to m(0*in)
    lw a4, 0(s3)                            # rows to m(0*in) aka (rows to m0)   
    lw a5, 4(s7)                            # load in cols to ^ aka (cols to m(in))
    mv a6, s10                              # load in ptr to new matrix -> m(1*0in)
    jal matmul
    
    # =====================================
    # WRITE OUTPUT
    # =====================================
    # Write output matrix to output path
    # Loading write_matrix

    lw a0, 12(s1)                            # a0 holds the pointer to the output path
    mv a1, s10                               # ptr to m(1*0in)
    lw a2, 0(s5)                             # a2 holds (int) m(1*0in) rows
    lw a3, 4(s7)                             # a3 holds (int) cols
    jal write_matrix

    # =====================================
    # CALCULATE CLASSIFICATION/LABEL
    # =====================================
    # Call argmax on m(1*0in)
    
    # Loading argmax                            
    mv a0, s10                               # ptr to m(1*0in)
    lw t0, 0(s5)                             # t0 holds (int) m(1*0in) rows
    lw t1, 4(s7)                             # t1 holds (int) cols
    mul a1, t0, t1                           # a1 holds number of elems in m(1*0in)  
    jal argmax                               # a0 holds classification (int)

    # Print classification
    # Checking if the print classification was set to 0.
    beq s2, x0, no_print
    # Calling print_int
    mv a1, a0                               # Loading in classification
    jal print_int
 
    # Print newline afterwards for clarity
    li a1 '\n'
    jal print_char

    #only jumps to no_print if print classification was set to 0
    no_print:
    # Epilogue
    lw ra 0(sp)
    lw s0, 4(sp)
    lw s1, 8(sp)
    lw s2, 12(sp)
    lw s3, 16(sp)
    lw s4, 20(sp)
    lw s5, 24(sp)
    lw s6, 28(sp)
    lw s7, 32(sp)
    lw s8, 36(sp)
    lw s9, 40(sp)
    lw s10, 44(sp)
    addi sp, sp, 48
    #Epilogue
    ret
    
argc_error:
    li a1, 89
    j exit2
malloc_error:
    li a1, 88
    j exit2
    
    
