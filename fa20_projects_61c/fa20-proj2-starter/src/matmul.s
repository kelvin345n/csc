.globl matmul

.text
# =======================================================
# FUNCTION: Matrix Multiplication of 2 integer matrices
# 	d = matmul(m0, m1)
# Arguments:
# 	a0 (int*)  is the pointer to the start of m0 
#	a1 (int)   is the # of rows (height) of m0
#	a2 (int)   is the # of columns (width) of m0
#	a3 (int*)  is the pointer to the start of m1
# 	a4 (int)   is the # of rows (height) of m1
#	a5 (int)   is the # of columns (width) of m1
#	a6 (int*)  is the pointer to the the start of d
# Returns:
#	None (void), sets d = matmul(m0, m1)
# Exceptions:
#   Make sure to check in top to bottom order!
#   - If the dimensions of m0 do not make sense,
#     this function terminates the program with exit code 72.
#   - If the dimensions of m1 do not make sense,
#     this function terminates the program with exit code 73.
#   - If the dimensions of m0 and m1 don't match,
#     this function terminates the program with exit code 74.
# =======================================================
matmul:
    # Error checks
    li t1, 1
    # Checks if row * col of m0 are less than 1. Exit code 72 
    mul t0, a1, a2
    blt t0, t1, error_72
    # Checks if row * col of m1 are less than 1. Exit code 73
    mul t0, a4, a5
    blt t0, t1, error_73
    # columns of m0 should be equal to the number of rows in m1: if not exit code 74
    bne a2, a4, error_74
    
    # Prologue
    addi sp, sp, -52
    sw ra, 0(sp)
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
    sw s11, 48(sp)
    # Prologue

    mv s0, a0                      # s0 stores pointer to m0
    mv s1, a1                      # s1 stores num of rows of m0
    mv s2, a2                      # s2 stores num of cols of m0
    mv s3, a3                      # s3 stores pointer to m1
    mv s4, a4                      # s4 stores num of rows of m1
    mv s5, a5                      # s5 stores num of cols of m1
    mv s6, a6                      # s6 stores pointer to output matrix
    li s7, 0                       # s7 stores the outer counter. Init to zero
    li s8, 0                       # s8 stores the inner counter. Init to zero
    mv s9, s6                      # s9 stores the address of the next element to input into output matrix
    mv s10, s0                     # s10 stores the address of the first elem we want to dot product from m0
    mv s11, s3                     # s11 stores the address of the first elem we want to dot product from m1

outer_loop_start:
    beq s7, s1, outer_loop_end     # outer counter is equal to the number of rows in m0
    li t0, 4                       # t0 stores the amount of bytes in a word
    mul t0, t0, s7                 # bytes per word times the outer counter. 0, 4, 8, 12...
    
    mul t0, t0, s2                 # multiply this by the num of cols in m0, so when we are done
                                   # with the first row, we can go to the next row in m0.
    add s10, s0, t0                # Address of first elem in target row in m0                              
    li s8, 0                       # Set inner counter to 0
    
inner_loop_start:
    beq s8, s5, inner_loop_end     # inner counter is equal to number of cols in m1
    li t0, 4                       # t0 stores the amount of bytes in a word
    mul t0, t0, s8                 # bytes per word times the inner counter. 0, 4, 8, 12...
    
    add s11, s3, t0                # Address of first elem in target col in m1  
    
    # load in arguments for dot
    mv a0, s10                     # load in v0
    mv a1, s11                     # load in v1
    mv a2, s2                      # load in length of vectors (# cols in m0 or # rows in m1)
    li a3, 1                       # the stride of the vector for m0 is always one
    mv a4, s5                      # the stride of the vector for m1 is # cols in m1
    jal dot
    
    # move dot product to output matrix
    sw a0, 0(s9)
    addi s9, s9, 4                 # increment pointer to next index in output matrix
    
    addi s8, s8, 1                 # increment inner loop
    j inner_loop_start
    
inner_loop_end:
    addi s7, s7, 1                 # increment outer counter
    j outer_loop_start

outer_loop_end:
    # Epilogue
    lw ra, 0(sp)
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
    lw s11, 48(sp)
    addi sp, sp, 52
    # Epilogue
    ret

error_72:
    li a0, 17
    li a1, 72
    ecall
error_73:
    li a0, 17
    li a1, 73
    ecall
error_74:
    li a0, 17
    li a1, 74
    ecall
