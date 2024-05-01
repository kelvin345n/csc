.globl argmax

.text
# =================================================================
# FUNCTION: Given a int vector, return the index of the largest
#	element. If there are multiple, return the one
#	with the smallest index.
# Arguments:
# 	a0 (int*) is the pointer to the start of the vector
#	a1 (int)  is the # of elements in the vector
# Returns:
#	a0 (int)  is the first index of the largest element
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 77.
# =================================================================
argmax:
    beq a1, x0, error        
    
    mv t0, a0          # t0 stores the address of array
    mv t1, a1          # t1 stores the num of elems in array
    li t2, 0           # t2 stores the current counter
                       # t3 stores the address of current element
    li t4, 0           # t4 stores the index of the max elem so far. Initialized to 0
    li a5, 0           # a5 stores the sum of squares of all the elems
                       # a6 stores the value of the current elem.
    lw a7, 0(t0)       # a7 stores the value of the max elem. Initialied to elem at index 0
loop_start:
    beq t1, t2, load_return     # end loop if counter == num of elems in array
    addi t5, x0, 4              # t5 stores the amount of bytes in an integer
    mul t6, t5, t2              # t6 stores amount of bytes until next elem
    add t3, t0, t6          
    lw a6, 0(t3)
    
    mul a4, a6, a6          # Square of the current elem
    add a5, a5, a4          # Add to total sum
    
    beq a6, a7, loop_continue
    blt a6, a7, loop_continue
    # means the current element is larger than the reigning champ
    mv t4, t2
    mv a7, a6
loop_continue:  
    addi t2, t2, 1
    j loop_start
    
load_return:
    mv a0, t4           # Stores index of max elem to return
loop_end:
    ret
 
error:
    li a0, 17
    li a1, 77
    ecall