.import ../src/abs.s
.globl relu

.text
# ==============================================================================
# FUNCTION: Performs an inplace element-wise ReLU on an array of ints
# Arguments:
# 	a0 (int*) is the pointer to the array
#	a1 (int)  is the # of elements in the array
# Returns:
#	None
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 78.
# ==============================================================================
relu:
    # Prologue
    addi sp, sp, -28
    sw ra, 0(sp)
    sw s0, 4(sp)        # s0 stores the pointer to the array. 
    sw s1, 8(sp)        # s1 stores the num of elems in array
    sw s2, 12(sp)       # s2 stores the current counter. Intialized to 0
    sw s3, 16(sp)       # s3 stores the address of the current elem.
    sw s4, 20(sp)       # s4 stores the value of the current elem. 
    sw s5, 24(sp)       # s5 stores the psuedo-length of the vector. Just the sum of all
                        # the elems    
    # Prologue
    mv s0, a0
    mv s1, a1
    addi s2, x0, 0
    addi s5, x0, 0
loop_start:
    beq s2, s1, loop_end     # If counter is equal to the number of elems in array; exit
    addi t0, x0, 4           # t0 stores the amount of bytes in an integer
    mul t1, s2, t0           # t1 stores the how much to increment by in the array
    add s3, t1, s0           # s3 holds the address of the current elem
    lw s4, 0(s3)             # s4 holds the value of the integer
    mv a0, s4                # Load arg for the abs function
    jal abs                  # a0 holds the absolute value of the integer
    add s5, s5, a0
loop_continue:
    addi t0, x0, 0
    bge s4, t0, big         # Keep the number the same if the integer is greater than 0.
    sw t0, 0(s3)            # Store 0 in place of the integer that is less than 0
big: 
    addi s2, s2, 1          # Increment counter
    j loop_start

loop_end:
    mv t0, s5       # Move sum to temp register      
    # Epilogue
    lw ra, 0(sp)
    lw s0, 4(sp)     
    lw s1, 8(sp)    
    lw s2, 12(sp)
    lw s3, 16(sp)    
    lw s4, 20(sp)
    lw s5, 24(sp)
    addi sp, sp, 28
    # Epilogue
    li t1, 1
    blt t0, t1, error   # If length of psuedo length is less than 1: error
	ret
error:      # return error code 78 if length of vector is less than one
    li a0, 17
    li a1, 78
    ecall
