        lw 0 5 sstack   			// stack = 30
        lw 0 6 one    				//$(6) = 1
		lw 0 1 n     				// &(1) = #5[0]  .30
        lw 0 2 r     				// $(2) = #5[1]  .31	
		lw 0 4 callfn    			// prepare to call 
		jalr   4  7
		done    halt                //end of program 		
addrfn  sw         5   7   2       	//save return address on stack
		beq  1 2 jif      			//if(n==r)  2if:
        beq  2 0 jif      			//if(r==0)  2if: 
		add        5   6   5        //increment stack pointer
		add        5   6   5        //increment stack pointer
		add        5   6   5        //increment stack pointer
		lw 0 4 neq1        			//&(4)  = -1		
		add 1 4 1 // n-1	
		sw         5   1   0      	//save $1 on stack
		sw         5   2   1      	//save $2 on stack
		lw 0 4 callfn           	// prepare to call 
        jalr 4 7
		lw 0 4 neq1       			//&(4)  = -1	
		lw    5   1   0  			// recover original $1
        lw    5   2   1  			// recover original $2	
		add 2 4 2 					// n-1
		sw         5   1   0      	//save $1 on stack
		sw         5   2   1      	//save $2 on stack
		lw 0 4 callfn        		// prepare to call 
		jalr 4 7	
		lw 0 4 neq1        			//&(4)  = -1	
		add   5   4   5         	//decrement stack pointer
		add   5   4   5         	//decrement stack pointer
		add   5   4   5         	//decrement stack pointer
	    lw    5   7   2         	//recover original return address
        jalr 7   4          		//return.  $2 is not restored.	
jif add 3 6 3            			// return 1 (+1) // 3 += 1
	    lw 5 7 2    				//recover  return address	
		jalr 7 0        			// back
callfn   .fill  addrfn  
one    .fill  1
neq1 .fill -1
sstack .fill n
n .fill 7
r .fill 3