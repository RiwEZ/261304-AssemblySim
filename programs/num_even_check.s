lw 0 1 res       # if num is even reg[ 1 ] = 1
lw 0 2 num
lw 0 3 one
lw 0 4 two
lw 0 5 temp
lw 0 6 temp
chk nand 2 3 6
nand 6 6 5
beq 5 3 done
do add 0 3 1
done halt
num .fill 736
one .fill 1
two .fill 2
temp .fill 0
res .fill 0