.globl dot

.text
# =======================================================
# FUNCTION: Dot product of 2 int vectors
# Arguments:
#   a0 (int*) is the pointer to the start of v0
#   a1 (int*) is the pointer to the start of v1
#   a2 (int)  is the length of the vectors
#   a3 (int)  is the stride of v0
#   a4 (int)  is the stride of v1
# Returns:
#   a0 (int)  is the dot product of v0 and v1
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 75.
# - If the stride of either vector is less than 1,
#   this function terminates the program with error code 76.
# =======================================================
dot:
    li t0, 1
    blt a2, t0, zero_error              # Function terminates with exit code 75 if length is zero
    blt a3, t0, stride_error            # function terminates with error code 76 if
    blt a4, t0, stride_error            # either vectors have a stride of less than 1
    # Prologue
    addi sp, sp -12
    sw ra, 0(sp)
    sw s0, 4(sp)                        # s0 stores the dot product
    sw s1, 8(sp)                        # s1 stores the current counter
    # Prologue
    li s0, 0                            # dot product initialized to zero
    li s1, 0                            # curr counter init to zero
    
loop_start:
    beq s1, a2, loop_end                # If counter == length of vector: return dot product
    li t0, 4                            # t0 stores amount of bytes per word
    #Take into account stride
    mul t1, t0, a3                      # t1 stores amount of bytes times the stride of v0
    mul t2, t0, a4                      # t2 stores bytes times stride of v1
    mul t1, t1, s1                      # t1 stores amount of bytes next element is away from the start index for v0
    mul t2, t2, s1                      # t2 ^ but for v1
    add t1, a0, t1                      # Memory address for next elem for v0
    add t2, a1, t2                      # Memory address for next elem for v1
    lw t1, 0(t1)                        # Integer of next elem for v0
    lw t2, 0(t2)                        # Integer of next elem for v1
    
    mul t3, t1, t2                      # Multiply v0[i] and v1[i]
    add s0, s0, t3                      # Add product to running dot product total
    
    addi s1, s1, 1                      # Increment counter
    j loop_start
    
loop_end:
    mv a0, s0                           # Load dot product for return
    # Epilogue       
    lw ra, 0(sp)
    lw s0, 4(sp)
    lw s1, 8(sp)
    addi sp, sp 12
    # Epilogue
    ret
    
stride_error:
    li a0, 17
    li a1, 76
    ecall

zero_error:
    li a0, 17
    li a1, 75
    ecall