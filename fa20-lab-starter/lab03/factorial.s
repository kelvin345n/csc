.globl factorial

.data
n: .word 8

.text
main:
    la t0, n
    lw a0, 0(t0)
    jal ra, factorial

    addi a1, a0, 0
    addi a0, x0, 1
    ecall # Print Result

    addi a1, x0, '\n'
    addi a0, x0, 11
    ecall # Print newline

    addi a0, x0, 10
    ecall # Exit

factorial:
    addi t0, x0, 2 # If argument is 1 or 0 then return 
    blt a0, t0, return
    
    #BEGIN PROLOGUE
    addi sp, sp, -8 # Increase Stack by a word
    sw s0, 0(sp)    # Store s0 onto the stack to restore later
    sw ra, 4(sp)    # Store the return address
    mv s0, a0       # Copy the argument into s0 because we will use recursion
    #END PROLOGUE
    
    addi a0, a0, -1 
    jal factorial
    mul s0, s0, a0 # a0 is not another call from factorial
    mv a0, s0       # Return the factorial in a0
    
    #BEGIN EPILOGUE
    lw s0, 0(sp)    # Restoring values
    lw ra, 4(sp)
    addi sp, sp, 8 
    #END EPILOGUE
    
    jr ra
    
return:
    addi a0, x0 1 # argument is 1 or 0 so we return 1
    jr ra