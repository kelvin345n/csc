.globl read_matrix

.text
# ==============================================================================
# FUNCTION: Allocates memory and reads in a binary file as a matrix of integers
#
# FILE FORMAT:
#   The first 8 bytes are two 4 byte ints representing the # of rows and columns
#   in the matrix. Every 4 bytes afterwards is an element of the matrix in
#   row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is a pointer to an integer, we will set it to the number of rows
#   a2 (int*)  is a pointer to an integer, we will set it to the number of columns
# Returns:
#   a0 (int*)  is the pointer to the matrix in memory
# Exceptions:
# - If malloc returns an error,
#   this function terminates the program with error code 88.
# - If you receive an fopen error or eof, 
#   this function terminates the program with error code 90.
# - If you receive an fread error or eof,
#   this function terminates the program with error code 91.
# - If you receive an fclose error or eof,
#   this function terminates the program with error code 92.
# ==============================================================================
read_matrix:

    # Prologue
	addi sp, sp, -32
    sw ra, 0(sp)
    sw s0, 4(sp)
    sw s1, 8(sp)
    sw s2, 12(sp)
    sw s3, 16(sp)
    sw s4, 20(sp)
    sw s5, 24(sp)
    sw s6, 28(sp)
    # Prologue
    
    mv s0, a0                       # s0 stores the pointer to file name
    mv s1, a1                       # s1 stores the pointer to the number of rows
    mv s2, a2                       # s2 stores the pointer to the number of cols
    
    # Opening file using fopen...
    mv a1, s0                       # moving file name to a1
    li a2, 0                        # gives fopen permission to read file
    jal fopen                       # a0 holds file descriptor of file
    mv s3, a0                       # s3 holds file descriptor
    
    # Testing file descriptor
    mv a1, s3                       # load file descriptor into a1
    jal ferror
    bne a0, x0, fopen_error
    
    # We have a valid file descriptor. Now we use fread to read in the file.
    # Lets read in the first two integers. These represent the rows and cols.
    
    # Loading into fread... Reading in the number of rows
    mv a1, s3                       # file descriptor into a1
    mv a2, s1                       # pointer to the number of rows
    li a3, 4                        # load in 4 bytes
    jal fread                       # returns number of bytes actually read in a0
    
    # Checking for fread error...
    li t0, 4
    bne a0, t0, fread_error
    
    # Loading into fread... Reading in the number of rows
    mv a1, s3                       # file descriptor into a1
    mv a2, s2                       # pointer to the number of cols
    li a3, 4                        # load in 4 bytes
    jal fread                       # returns number of bytes actually read in a0
    
    # Checking for fread error...
    li t0, 4
    bne a0, t0, fread_error
    
    # We have loaded in the number of rows and columns in the matrix. 
    # Now we can determine how many bytes to malloc. rows * cols * sizeof(data type)
    
    lw t0, 0(s1)                    # t0 holds the number of rows
    lw t1, 0(s2)                    # t1 holds the number of cols
    mul t2, t0, t1                  # t2 holds rows * cols (num of elems in matrix)
    mv s6, t2
    li t3, 4                        # 4 bytes in integer
    mul t2, t2, t3                  # t2 holds the number of bytes we want to malloc. 
    
    # Calling malloc...
    mv a0, t2                       
    jal malloc
    
    # Testing if malloc failed
    beq a0, x0, malloc_error
    
    # We now have the memory we need. 
    mv s4, a0                       # s4 holds the pointer in memory to alloced space for matrix
    
    # Now we create loop until the end of the file using fread.
    li s5, 0                       # s5 will hold the current counter. 
    
    loop:
    
    beq s5, s6, end_loop            # End loop if counter is equal to number of elems in matrix
    li t0, 4                        # 4 bytes in a word    
    mul t1, s5, t0                  # number of bytes to offset array. currCounter * 4 bytes. 
    
    add t2, s4, t1                  # t2 holds the next memory location to write to
    
    # Loading into fread...
    mv a1, s3                       # file descriptor into a1
    mv a2, t2                       # pointer to next place in memory
    mv a3, t0                       # load in 4 bytes to read
    jal fread                       # returns number of bytes actually read in a0
    
    # Checking for fread error...
    li t0, 4
    bne a0, t0, fread_error
    addi s5, s5, 1                  # increment counter
    j loop                          # continue loop
    end_loop:
    
    # Calling fclose on file descriptor
    mv a1, s3                      # load in file descriptor
    jal fclose
    # Checking fclose error
    bne a0, x0, fclose_error
   
    # Loading pointer to matrix for return
    mv a0, s4
    # Epilogue
    lw ra, 0(sp)
    lw s0, 4(sp)
    lw s1, 8(sp)
    lw s2, 12(sp)
    lw s3, 16(sp)
    lw s4, 20(sp)
    lw s5, 24(sp)
    lw s6, 28(sp)
    addi sp, sp, 32
    # Epilogue
    ret
    
fopen_error:
    li a1, 90
    j exit2
    
fread_error:
    li a1, 91
    j exit2
    
malloc_error:
    li a1, 88
    j exit2

fclose_error:
    li a1, 92
    j exit2