from audioop import add
from unittest import result

# def convertNum(num):

#         #   /* convert a 16-bit number into a 32-bit integer */
#         if (num & (1<<15) ):
#             # print(bin(num+2**32))
#             # print((1<<16))
#             num = num+2**32
#         # else:
#             # num = num+(0<<16)
#             # print(bin(num))
#         return(bin(num)[2:].zfill(32))

def add(a , b):
    result = str(int(a) + int(b))
    if(len(result) > 32):
        result = result[len(result)-32:len(result)]
    return result





#     max_len = 32
#     a = a.zfill(max_len)
#     b = b.zfill(max_len)
 
#     # Initialize the result
#     result = ''
 
#     # Initialize the carry
#     carry = 0
 
#     # Traverse the string
#     for i in range(max_len - 1, -1, -1):
#         r = carry
#         r += 1 if a[i] == '1' else 0
#         r += 1 if b[i] == '1' else 0
#         result = ('1' if r % 2 == 1 else '0') + result
 
#         # Compute the carry.
#         carry = 0 if r < 2 else 1
 
#     if carry != 0:
#         result = '1' + result
#     if len(result) > 32:
#         result = result[len(result)-32:len(result)]
#     return result.zfill(max_len)

class mul16x16:
    # bitsize = 16
    prod = '0'

    def __init__(self , mcand , mler) -> None:
        self.mcand = mcand
        self.mler = mler
        # print((bin(self.mcand))[2:].zfill(32))
        # print((bin(self.mler))[2:].zfill(32))
        print(self.mcand)
        print(self.mler)


    # def nand(a, b):
    # # """compute the 2's complement of int value val"""
    #     if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
    #         val = val - (1 << bits)        # compute negative value
    #     return val                         # return positive value as is


    def cal(self):
         
        for x in range(16, 0, -1):
             
            self.prod = add(self.prod,self.prod)
            #  (bin(add(bin(self.prod),bin(self.prod),32)))
            # self.prod =  str((self.prod) + (self.prod))

            # print(bin(mul16x16.twos_comp(~( 7 & 4 ) , 4)))
            # print( bool(-1) )
            # print(~( 0b111 & 0b100 ))
            # if(nand(Mcand , 0x8000) == 0 หมด ):
            # print((((self.mcand & self.mler)) ))
            # print(bin(convertNum(32768)))


            # if(  (    ~ (int(self.mcand) & 0x8000 )  )):
                # pass
            #     print("work")
            #     self.prod = bin(add(int(self.prod ,2),int(self.mler,2)))
            # print(bool(self.mcand & 0x8000)  )
            # ถ้า & แล้วค่าไม่ใช่ 0 = true
            # print(bool( ~ (     (~ ((self.mcand) & (self.mcand))   ) & (  ~ ((self.mcand) & (self.mcand) )  )   == 0x8000)  ))
            # if (self.mcand & 0x8000):
            print(-32768 == 32768)
            # print(bool(int(self.mcand) & 0x8000))
            if (int(self.mcand) & 0x8000):
            # else:
                self.prod = add(self.prod,self.mler)
                #  (bin(add(bin(self.prod),bin(self.mler),32)))
                # ((self.prod) + (self.mler))
                 
            # print((self.mcand))
            self.mcand =  add(self.mcand,self.mcand)
            # (bin(add(bin(self.mcand),bin(self.mcand),32)))
            # ((self.mcand) + (self.mcand))
          
        print(self.prod)
    # @staticmethod
    # def nand(a , b):
    #     c = a.copy()
    #     for x in range[a]:
    #         if a[x] != b[x]:

    #     return c

def main():
    mul1 = mul16x16( 20000,3)
    mul1.cal()



main()