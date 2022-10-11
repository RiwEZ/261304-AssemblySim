lw 0 2 mcand                 //$(2) = #[18]
lw 0 3 mplier             //$(3) = #[19]
lw 0 4 nbit           //$(4) = #[20] 

start   add  1 1 1                             forloop: $1 = $1 + $1 // prod += prod but on start it away 0
lw 0 5 ox8                      //$(5) = 0x8000 
nand 2 5 6                //nand mcand,0x8000  -> $6
lw 0 5  ffff                     //$(5) = 0xFFFF
nand 6 5 6                 // nand $(6),x(5),0xFFFF -> $6
lw 0 5 ox8                      //$(5) = 0x8000 
beq  5  6 1                            //beq if($(6) == $(5)0x8000 ) jump 2if: PC+1+offsetField
beq  0  0 1                              // if not true jump exit
add 1 3 1                             //2if: $(1) = $1 + $(3)  prod = add(prod,mler)
add 3 3 3                           //$(3) = $(3) + $(3)      mcand =  add(mcand,mcand)
lw 0 5 neg1                      //$(5) = -1 
add 4 5 4                                    //$(4) = $(4) + (-1)
beq 4 0 1                            //beq if 4 ==0 1 exit loop
beq  0 0 start                        //beq backto loop
done    halt                        //end of program

mcand .fill 32766
mplier .fill 10383
nbit .fill 32
ffff .fill 65535 //0xFFFF
ox8 .fill 32768 //0x8000
neg1    .fill   -1
stAddr  .fill      start            //will contain the address of start