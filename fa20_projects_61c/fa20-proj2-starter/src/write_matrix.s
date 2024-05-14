.globl write_matrix

.text
# ==============================================================================
# FUNCTION: Writes a matrix of integers into a binary file
# FILE FORMAT:
#   The first 8 bytes of the file will be two 4 byte ints representing the
#   numbers of rows and columns respectively. Every 4 bytes thereafter is an
#   element of the matrix in row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is the pointer to the start of the matrix in memory
#   a2 (int)   is the number of rows in the matrix
#   a3 (int)   is the number of columns in the matrix
# Returns:
#   None
# Exceptions:
# - If you receive an fopen error or eof,
#   this function terminates the program with error code 93.
# - If you receive an fwrite error or eof,
#   this function terminates the program with error code 94.
# - If you receive an fclose error or eof,
#   this function terminates the program with error code 95.
# ==============================================================================
write_matrix:
    # Prologue
    addi sp, sp, -36
    sw ra, 0(sp)
    sw s0, 4(sp)
    sw s1, 8(sp)
    sw s2, 12(sp)
    sw s3, 16(sp)
    sw s4, 20(sp)
    sw s5, 24(sp)
    
    # Prologue

    mv s0, a1                       # s0 holds the pointer to the start of matrix
    mv s1, a2                       # s1 holds the number of rows in the matrix
    mv s2, a3                       # s2 holds the number of cols in matrix 
    
    sw s1, 28(sp)
    sw s2, 32(sp)
    
    addi s1, sp, 28
    addi s2, sp, 32
    
    # Calling fopen with write permission
    mv a1, a0          
    li a2, 1
    jal fopen
    mv s3, a0                       # s3 holds the file descriptor
    # Check if fopen is valid
    mv a1, s3                       # Load file descriptor
    jal ferror
    bne a0, x0, fopen_error
    
    # Writing the number of rows and cols into the file
    mv a1, s3                       # Load file descriptor
    mv a2, s1                       # Load in row buffer
    li s4, 1                        # s4 holds how many items to read
    mv a3, s4                       # Load in 1 item to read
    li a4, 4                        # Load in number of bytes per item
    jal fwrite
    # Checking for fwrite error
    blt a0, s4, fwrite_error        
    # Writing cols into the file
    mv a1, s3                      
    mv a2, s2                     
    li s4, 1                        
    mv a3, s4                       
    li a4, 4                       
    jal fwrite
    # Checking for fwrite error
    blt a0, s4, fwrite_error  
    
    # Now time to write each element in the array into the file
    lw t0, 0(s1)
    lw t1, 0(s2)
    mul s5, t0, t1                  # s5 holds the total number of elems in the matrix
    # Writing array into the file
    mv a1, s3                       # load in file descriptor
    mv a2, s0                       # load in array buffer                       
    mv a3, s5                       # load in array length
    li a4, 4                        # load in bytes per element
    jal fwrite
    # Checking for fwrite error
    blt a0, s5, fwrite_error        
   
    # Close the file
    mv a1, s3                       
    jal fclose
    # Check error in fclose
    bne a0, x0, fclose_error
   
    # Epilogue
    lw ra, 0(sp)
    lw s0, 4(sp)
    lw s1, 8(sp)
    lw s2, 12(sp)
    lw s3, 16(sp)
    lw s4, 20(sp)
    lw s5, 24(sp)
    addi sp, sp, 36
    # Epilogue
    ret

fopen_error:
    li a1, 93
    j exit2
fwrite_error:
    li a1, 94
    j exit2
fclose_error:
    li a1, 95
    j exit2
