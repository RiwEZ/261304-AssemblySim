# from tkinter import W


# class assember:
#         #     R-type instructions (add, nand)

#         #        Bits 24-22 opcode

#         #        Bits 21-19 reg A (rs)

#         #        Bits 18-16 res B (rt)

#         #        Bits 15-3 ไม่ใช้ (ควรตั้งไว้ที่ 0)

#         #        Bits 2-0  destReg (rd)

#         # I-type instructions (lw, sw, beq)

#         #        Bits 24-22 opcode

#         #        Bits 21-19 reg A (rs)

#         #        Bits 18-16 reg B (rt)

#         #        Bits 15-0 offsetField (เลข16-bit และเป็น 2’s complement  โดยอยู่ในช่วง –32768 ถึง 32767)

#         # J-Type instructions (jalr)

#         #        Bits 24-22 opcode

#         #        Bits 21-19 reg A (rs)

#         #        Bits 18-16 reg B (rd)

#         #        Bits 15-0 ไม่ใช้ (ควรตั้งไว้ที่ 0)

#         # O-type instructions (halt, noop)

#         #        Bits 24-22 opcode

#         #        Bits 21-0 ไม่ใช้ (ควรตั้งไว้ที่ 0)
#     def __init__(self) -> None:
#         pass        


# list_op = {"add","nand","lw","sw","beq","jalr","halt", "noop","halt"}

# f = open("src\\testcode.txt", "r")
# raw = f.read()
# line = raw.split("\n")
# word = []
# i = 0 
# op_end = False 
# for text in line:
#     tmp = text.split()
#     if len(tmp) == 0:
#         continue
    
    
#     if ".fill" in tmp:
#         word.append(tmp[0:3])
#     elif "halt" in tmp:
#         word.append(tmp[0:2])        
#     else:
#         if tmp[0] in list_op:
#             word.append(tmp[0:4])
#         else:
#             word.append(tmp[0:5])
    
# for code in word:
#     pass    

# # print(word)
# print(word)
# # print(f.read())

