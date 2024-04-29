.globl moretest

.data
n:  .word 0
    .word 1
    .word 2
    .word 3
    .word 4
    .word 5
    
.text
main:
    #BEGIN PROLOGUE
    addi sp, sp, -12
    sw ra, 0(sp)
    sw s0, 4(sp)
    sw s1, 8(sp)
    #END PROLOGUE
    addi s1, x0, 6 # Size of array
    la s0, n            # s0 = &n
    
    mv a0, s0
    mv a1, s1
    jal print_array # Prints Original Array
    
    jal print_newline
    
    mv a0, s0
    mv a1, s1
    jal reverse_array
    
    mv a0, s0
    mv a1, s1
    jal print_array # Prints Reversed Array
    jal print_newline

    #BEGIN EPILOGUE
    lw ra, 0(sp)
    lw s0, 4(sp)
    lw s1, 8(sp)
    addi sp, sp, 12
    #END EPILOGUE
    addi a0, x0, 10
    ecall

print_array: # Takes in two args; a0 = pointer to array, a1 = size of array
    #BEGIN PROLOGUE
    addi sp, sp, -4
    sw ra, 0(sp)
    #END PROLOGUE
    
    addi t0, x0, 4 # t0 holds the size of our word
    add t1, x0, x0 # t1 is the counter
    mv t2, a0      # t2 is the pointer to array
    mv t3, a1      # t3 is the size of array
print_loop:
    bge t1, t3, print_return    # Return if counter is >= size of array
    mul t4, t0, t1              # t4 holds how many bytes away the pointer is from the elem we want to access
    add t5, t2, t4
    
    lw a1, 0(t5)
    addi a0, x0, 1
    ecall
    addi    a1, x0, ' '     # a0 gets address of string containing space
    addi    a0, x0, 11      # prepare for print string syscall
    ecall
    
    addi t1, t1, 1
    j print_loop
    
print_return:
    #BEGIN EPILOGUE
    lw ra, 0(sp)
    addi sp, sp, 4
    #END EPILOGUE
    jr ra
    


reverse_array: # Takes two arguments. a0 = pointer to array and a1 = size of array
    #BEGIN PROLOGUE
    addi sp, sp, -20
    sw ra, 0(sp)
    sw s0, 4(sp)
    sw s1, 8(sp)
    sw s2, 12(sp)
    sw s3, 16(sp)
    #END PROLOGUE
    
    addi t0, x0, 2
    blt a1, t0, return # If array length is 1 or 0 do not change array
    mv s0, a0          # Store address of array in s0
    add s1, x0, x0     # Store index of start of array
    addi s2, a1, -1    # Store index of back of array
    addi s3, x0, 4     # Stores size of the word
loop:
    beq s1, s2, return
    blt s2, s1, return # return if the index at the back of array is less than or equal to front
    # address of front of array
    mul t0, s1, s3  # Calculates how many bytes away from start we need to travel to get to next elem forward
    add t1, t0, s0  # Memory address at the start of array
    lw t5, 0(t1)    # t5 should have the first number
    
    mul t2, s2, s3  # Calculates how many bytes away from start we need to travel to get to next elem backwards
    add t3, t2, s0  # Memory address at the start of array
    lw t6, 0(t3)    # t6 should have the last number
    
    sw t5, 0(t3)
    sw t6, 0(t1)
    
    addi s1, s1, 1
    addi s2, s2, -1
    j loop
    
return:
    #BEGIN EPILOGUE
    lw ra, 0(sp)
    lw s0, 4(sp)
    lw s1, 8(sp)
    lw s2, 12(sp)
    lw s3, 16(sp)
    addi sp, sp, 12
    #END EPILOGUE
    jr ra

print_newline:
    addi    a1, x0, '\n' # Load in ascii code for newline
    addi    a0, x0, 11
    ecall
    jr  ra