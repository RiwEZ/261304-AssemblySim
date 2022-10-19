lw 0 2 mcand            //$2 = #[16]
lw 0 3 mplier           //$3 = #[17]
lw 0 4 nbit             //$4 = #[18]
lw 0 5 Ox8              //$5 =  1000 0000 0000 0000
lw 0 7  neg1            //$7 =  1111 1111 1111 1111
loop  add  1 1 1        //forloop: $1 = $1 + $1 // prod += prod
nand 2 5 6              // nand ( mcand , 32768)  -> $6  
nand 6 7 6              // nand ( $6,$7 ) -> $6
beq  5  6 true          // beq if($6 == 32768 ) jump 2if:
beq  0  0 1             // else jump skip
true add 1 3 1          //2if: $1 = $1 + $3  prod += mler
add 2 2 2               //$(2) = $2 + $2      mcand += mcand
add 4 7 4               //$(4) = $4 + (-1)
beq 4 0 done            // beq if 4 == 0  exit loop
beq  0 0 loop           // beq backto loop
done    halt            //end of program
mcand .fill 32766
mplier .fill 10383
nbit .fill 16
Ox8 .fill 32768         //1000 0000 0000 0000
neg1    .fill   -1      //1111 1111 1111 1111
stAddr  .fill   loop    //will contain the address of start