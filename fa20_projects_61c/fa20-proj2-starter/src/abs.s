.globl abs

.text
# =================================================================
# FUNCTION: Given an int return its absolute value.
# Arguments:
# 	a0 (int) is input integer
# Returns:
#	a0 (int) the absolute value of the input
# =================================================================
abs:
    # return same value if positive
    bge a0, zero, done
    # invert if negative
    sub a0, zero, a0
done:
    ret
