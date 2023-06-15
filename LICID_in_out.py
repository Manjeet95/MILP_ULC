'''
Arguments:
1. Block Size - 64/128 depdends on LICID block size    
2. Number for rounds
3. Minimum Number of active S-boxes
4. fix/no_fix - whether difference of some round is fixed or not
5. No. of trails to find  
6. possilbe/impossible differential characteritics
7. Solver to be used (GUROBI/CPLEX)

python LICID.py 64 11 1 no_fix 1 possible GUROBI 
python LICID.py 64 5 1 no_fix 1 impossible CPLEX
'''

import string
import sys
from math import floor


GUROBI_EXISTS = False
CPLEX_EXISTS = False

try:
  import google.colab
  IN_COLAB = True
except:
  IN_COLAB = False

if (sys.argv[7] == "GUROBI"):
    try: 
    	from gurobipy import *
    	GUROBI_EXISTS = True
    except:
    	GUROBI_EXISTS = False

if (sys.argv[7] == "CPLEX"):
	try: 
		from docplex.mp.model_reader import ModelReader
		CPLEX_EXISTS = True
	except:
		CPLEX_EXISTS = False

#############if manually want to choose the solve then set these parameters###########################
# GUROBI_EXISTS = False
# from gurobipy import *
# CPLEX_EXISTS = True		
# from docplex.mp.model_reader import ModelReader
##############################################################

if (GUROBI_EXISTS == False) and (CPLEX_EXISTS == False):
	sys.exit()
    
conv = (
-1, 2, -1, -2, -2, 0, 2, 1, 4,
-1, 0, 0, 1, -1, 1, 1, -1, 2,
-2, 3, -3, 1, -1, -3, -1, 3, 7,
1, 2, -1, 2, -1, 2, -3, -3, 5,
-1, -1, 1, 1, -2, 2, -2, 1, 4,
0, -1, -2, -1, 2, -2, 1, -1, 5,
-1, 3, 1, 3, 2, -3, 2, 4, 0,
1, 0, 1, -1, -1, 0, 1, -1, 2,
3, 2, 3, 2, -1, -1, 0, -1, 0,
3, 2, 1, -2, 2, 2, -1, 1, 0,
2, 4, -2, -4, 4, 1, -1, 3, 3,
2, -2, 1, 1, 1, 2, 0, 2, 0,
-2, 2, 2, -1, -1, 0, -2, -1, 5,
2, -3, -2, 3, 4, -1, 1, -4, 6,
2, -2, -2, 1, -1, 2, 3, 1, 2,
-1, -1, -2, 1, 3, 4, 3, 2, 0,
-1, 0, 1, -1, 1, 2, 2, 1, 0,
-2, -1, -2, 1, 0, -1, 1, -2, 6,
-1, -1, 0, -2, -1, -1, -2, 2, 6,
-2, -1, 1, 0, 1, -1, -2, -1, 5,
1, -3, 1, -2, -2, -2, -1, 1, 7,
    )
convpbl = (
-3, 0, 2, -4, -2, -1, -1, 2, 9, 7, 8, 0,
-6, 3, -6, 1, -3, -2, 3, -2, 16, 15, 13, 0,
1, -3, -4, 1, -2, 3, 2, 3, -3, 7, 4, 0,
2, -1, 1, -5, -3, 2, 3, -3, -2, 10, 9, 0,
-4, -4, -3, 3, 5, 4, 7, 1, -10, 7, 3, 0,
1, -3, -8, 2, 4, -2, 1, -10, 14, 12, 19, 0,
4, 2, -4, -1, 2, -4, 2, 1, -1, 2, 6, 0,
-1, 0, 2, 3, -3, 1, 1, -1, 1, 2, 4, 0,
-3, 2, 2, -3, 3, -1, 1, -1, 6, 8, 5, 0,
-4, 6, 1, 2, -1, -5, -2, 4, 9, 12, 6, 0,
2, 2, -2, 1, 0, 3, -3, -3, 3, 4, 5, 0,
5, 1, 5, 3, -2, -5, -1, -3, 1, 6, 5, 0,
2, 1, 2, 1, 1, 1, 0, 0, -4, -1, -2, 0,
-1, 4, -3, -4, 4, -2, -5, 7, 12, 4, 10, 0,
-2, 2, 6, 2, -5, 10, -5, 1, -5, 2, 7, 0,
-2, 0, 2, 1, 3, -2, -1, 1, 4, 2, 3, 0,
2, 1, 1, -2, 4, 4, 2, 3, -6, -6, -2, 0,
3, -6, 2, -3, -4, -5, -3, 1, 8, 16, 15, 0,
-7, -3, 2, 1, 2, -3, -7, -3, 16, 15, 18, 0,
0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, 1,
    )
# P64 = (
#      0,17,34,51,48, 1,18,35,32,49, 2,19,16,33,50, 3,
#      4,21,38,55,52, 5,22,39,36,53, 6,23,20,37,54, 7,
#      8,25,42,59,56, 9,26,43,40,57,10,27,24,41,58,11,
#     12,29,46,63,60,13,30,47,44,61,14,31,28,45,62,15)
P64_paper = (
         2,63,8,5,62,59,4,1,58,55,0,61,54,51,60,57,
         18,15,24,21,14,11,20,17,10,7,16,13,6,3,12,9,
         34,31,40,37,30,27,36,33,26,23,32,29,22,19,28,25,
         50,47,56,53,46,43,52,49,42,39,48,45,38,35,44,41
       )

P128 = (
      0, 33, 66, 99, 96,  1, 34, 67, 64, 97,  2, 35, 32, 65, 98,  3,
      4, 37, 70,103,100,  5, 38, 71, 68,101,  6, 39, 36, 69,102,  7,
      8, 41, 74,107,104,  9, 42, 75, 72,105, 10, 43, 40, 73,106, 11,
     12, 45, 78,111,108, 13, 46, 79, 76,109, 14, 47, 44, 77,110, 15,
     16, 49, 82,115,112, 17, 50, 83, 80,113, 18, 51, 48, 81,114, 19,
     20, 53, 86,119,116, 21, 54, 87, 84,117, 22, 55, 52, 85,118, 23,
     24, 57, 90,123,120, 25, 58, 91, 88,121, 26, 59, 56, 89,122, 27,
     28, 61, 94,127,124, 29, 62, 95, 92,125, 30, 63, 60, 93,126, 31
    )

LICID = int(sys.argv[1])
s_boxes = int(LICID/4)

P64 =  []
for i in range(0,int(LICID/4)):
    P64 = P64 + [P64_paper[i*4+3],P64_paper[i*4+2],P64_paper[i*4+1],P64_paper[i*4]]

for i in range(0,len(P64)):
    if (P64[i]%4==0):
        P64[i] = P64[i] + 3 
    elif (P64[i]%4==1):
        P64[i] = P64[i] + 1 
    elif (P64[i]%4==2):
       P64[i] = P64[i] - 1 
    elif (P64[i]%4==3):
        P64[i] = P64[i] - 3 
#print(P64)
if (LICID==64):
    Perm = P64
elif (LICID==128):
    Perm = P128
else:
    print("Incorrect Parameters!")
    sys.exit()
ROUND = int(sys.argv[2])
min_sbox = int(sys.argv[3])

if (sys.argv[4] == "fix"):
    fix = True
else:
    fix = False

attack_type = sys.argv[6]
	
#fix_diff = [0x0200000000000000, 0x4000000000000000, 0x0480000000000000,0xc800000000000120,0x0c00000000144812,0x4000014C81568C80,0x04d4cb1de9a1e080,0x5956dd7d8921814c]
#fix_pos = [0,1,2,3,4,5,6,7]
    
fix_diff = [0x1000000000000001,0x1000000000000001]
fix_pos = [0,ROUND]

fix_diff_bin_paper = [bin(diff)[2:].zfill(LICID) for diff in fix_diff];

fix_diff_bin = []
for e in fix_diff_bin_paper:
    fix_diff_bin.append("".join([e[i*4]+e[i*4+1]+e[i*4+2]+e[i*4+3] for i in range(0,int(LICID/4))][::-1]))

fix_bit = [];
for diff_1 in fix_diff_bin:
    fix_bit.append([len(diff_1)-1-i for i in range(0,len(diff_1)) if diff_1[i]=="1" ])
#print(fix_bit)
def PrintOuter(FixList,BanList):
    opOuter = open("Outer" +"_LICID_" + str(LICID) + "_" + str(ROUND)  + "_" + str(attack_type) +".lp",'w+')
    opOuter.write("Minimize\n")
    buf = ''
    if (attack_type == "possible"):
        for i in range(0,ROUND):
            for j in range(0,s_boxes):
                buf = buf + "a" + str(i) + "_" + str(j)
                if i != ROUND-1 or j != (s_boxes-1):
                    buf = buf + " + "
    if (attack_type == "impossible"):
        for i in range(0,LICID):
            if (i!=LICID-1):
                buf = buf + 'x0_' + str(i) + ' + '
            else:
                buf = buf + 'x0_' + str(i)
    opOuter.write(buf)
    opOuter.write('\n')
    opOuter.write("Subject to\n")
    ##################
    if(fix==True):
        for b in range(0,len(fix_bit)):
            buf = ''
            fix_s_box_next = [floor((i)/4) for i in fix_bit[b]]
            for j in range(0,s_boxes):
                    #if (fix_pos!=0):
                    #    if(j in fix_s_box_prev):
                    #        buf = buf + "a" + str(fix_pos[b]-1) + "_" + str(j) + " = 1\n"
                    #    else:
                    #        buf = buf + "a" + str(fix_pos[b]-1) + "_" + str(j) + " = 0\n"
                    if (fix_pos!=ROUND):
                        if(j in fix_s_box_next):
                            buf = buf + "a" + str(fix_pos[b]) + "_" + str(j) + " = 1\n"
                        else:
                            buf = buf + "a" + str(fix_pos[b]) + "_" + str(j) + " = 0\n"
            opOuter.write(buf)
    #################
    ##################
    if (fix==True):
        for b in range(0,len(fix_bit)):
            buf = ''
            for j in range(0,LICID):
                if(j in fix_bit[b]):
                    buf = buf + "x" + str(fix_pos[b]) + "_" + str(j) + " = 1\n"
                else:
                    buf = buf + "x" + str(fix_pos[b]) + "_" + str(j) + " = 0\n"
            opOuter.write(buf)
    #################
            
    buf = ''
    for i in range(0,ROUND):
        buf = ''
        for j in range(0,s_boxes):
            buf = ''
            for k in range(0,4):
                buf = buf +  "x" + str(i) + "_" + str(4*j+k)
                if k != 3:
                    buf = buf + " + "
            buf = buf + " - a" + str(i) + "_" + str(j) + " >= 0\n"
            for k in range(0,4):
                buf = buf + "x" + str(i) + "_" + str(4*j+k) + " - a" + str(i) + "_" + str(j) + " <= 0\n"

            for k in range(0,21):
                for l in range(0,9):
                    if conv[9*k+l] > 0:
                        if l <= 3:
                            buf = buf + " + " + str(conv[9*k+l]) + " x" + str(i) + "_" + str(4*j+3-l)
                        if 4 <= l and l <= 7:
                            buf = buf + " + " + str(conv[9*k+l]) + " x" + str(i+1) + "_" + str(Perm[4*j+7-l])
                        if l == 8:
                            buf = buf + " >= -" + str(conv[9*k+l]) + "\n"
                    if conv[9*k+l] < 0:
                        if l <= 3:
                            buf = buf + " - " + str(-conv[9*k+l]) + " x" + str(i) + "_" + str(4*j+3-l)
                        if 4 <= l and l <= 7:
                            buf = buf + " - " + str(-conv[9*k+l]) + " x" + str(i+1) + "_" + str(Perm[4*j+7-l])
                        if l == 8:
                            buf = buf + " >= " + str(-conv[9*k+l]) + "\n"
                    if conv[9*k+l] == 0:
                        if l == 8:
                            buf = buf + " >= " + str(conv[9*k+l]) + "\n"

            opOuter.write(buf)
            
    buf = ''
    if len(FixList) == 0:
        for i in range(0,LICID):
            buf = buf + "x0_" + str(i)
            if i != (LICID-1):
                buf = buf + " + "
            if i == (LICID-1):
                buf = buf + " >= 1\n"
        for i in BanList:
            for j in range(0,len(i)):
                buf = buf + "a" + str(i[j][0]) + "_" + str(i[j][1])
                if j != len(i)-1:
                    buf = buf + " + "
                else:
                    buf = buf + " <= " + str(len(i)-1) + '\n'
    else:    
        fl = []
        for i in range(0,LICID):
            fl.append(i)
            if fl in FixList:
                buf = buf + "x0_" + str(i) + " = 1\n"
            else:
                buf = buf + "x0_" + str(i) + " = 0\n"
            fl.pop()
    opOuter.write(buf)
   
    buf = ''
    for i in range(0,ROUND):
        for j in range(0,s_boxes):
            buf = buf + "a" + str(i) + "_" + str(j)
            if i != ROUND-1 or j != (s_boxes-1):
                buf = buf + " + "
            else:
                buf = buf + " >= "
    
    buf = buf + str(min_sbox) + "\n"
    
    opOuter.write(buf)

    buf = ''
    for i in [0,ROUND]:
        for j in range(0,LICID):
            buf = buf  + "x" + str(i) + "_" + str(j) + " + "
        if (i==0):
            buf = buf[:-2] + " = 4\n"
        if (i==ROUND):
            buf = buf[:-2] + " = 2\n"
    opOuter.write(buf)
    
    opOuter.write("Binary\n")
    buf = ''
    for i in range(0,ROUND):
        buf = ''
        for j in range(0,s_boxes):
            buf = buf + "a" + str(i) + "_" + str(j) + "\n"
        opOuter.write(buf)
    for i in range(0,ROUND+1):
        buf = ''
        for j in range(0,LICID):
            buf = buf + "x" + str(i) + "_" + str(j) + "\n"
        opOuter.write(buf)
    opOuter.close()


def PrintInner(FixList, SolveList):
    opInner = open("Inner" +"_LICID_" + str(LICID) + "_" + str(ROUND) + "_" + str(attack_type) +".lp","w+")
    opInner.write("Minimize\n")
    buf = ''
    
    for i in range(0,len(SolveList)):
        buf = buf + "1.415 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_0 + 2 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_1 + 3 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_2"
        if i != len(SolveList)-1:
            buf = buf + " + "
        else:
            buf = buf + "\n"
    opInner.write(buf)
    opInner.write("Subject to\n")
    ##################
    if (fix==True):
        for b in range(0,len(fix_bit)):
            buf = ''
            for j in range(0,LICID):
                if(j in fix_bit[b]):
                    buf = buf + "x" + str(fix_pos[b]) + "_" + str(j) + " = 1\n"
                else:
                    buf = buf + "x" + str(fix_pos[b]) + "_" + str(j) + " = 0\n"
            opInner.write(buf)
    #################
            
    buf = ''
    for i in range(0,len(SolveList)):
        buf = ''
        
            
        for k in range(0,4):
            buf = buf + "4 x" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+k)
            if k != 3:
                buf = buf + " + "
        for k in range(0,4):
            buf = buf + " - y" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+k)
        buf = buf + " >= 0\n"

        for k in range(0,4):
            buf = buf + "4 y" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+k)
            if k != 3:
                buf = buf + " + "
        for k in range(0,4):
            buf = buf + " - x" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+k)
        buf = buf + " >= 0\n"
        opInner.write(buf)
    
        buf = ''
        for k in range(0,20):
            for l in range(0,12):
                if convpbl[12*k+l] > 0:
                    if l <= 3:
                        buf = buf + " + " + str(convpbl[12*k+l]) + " x" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+3-l)
                    if 4 <= l and l <= 7:
                        buf = buf + " + " + str(convpbl[12*k+l]) + " y" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+7-l)
                    if 8 <=l and l <= 10:
                        buf = buf + " + " + str(convpbl[12*k+l]) + " z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_" + str(l-8)
                    if l == 11:    
                        buf = buf + " >= -" + str(convpbl[12*k+l]) + "\n"
                if convpbl[12*k+l] < 0:
                    if l <= 3:
                        buf = buf + " - " + str(-convpbl[12*k+l]) + " x" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+3-l)
                    if 4 <= l and l <= 7:
                        buf = buf + " - " + str(-convpbl[12*k+l]) + " y" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+7-l)
                    if 8 <= l and l <= 10:
                        buf = buf + " - " + str(-convpbl[12*k+l]) + " z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_" + str(l-8)
                    if l == 11:
                        buf = buf + " >= " + str(-convpbl[12*k+l]) + "\n"
                if convpbl[12*k+l] == 0:
                    if l == 11:
                        buf = buf + " >= " + str(convpbl[12*k+l]) + "\n"

        opInner.write(buf)
    
    buf = ''
    sl = []
    for i in range(0,ROUND):
        buf = ''
        sl = []
        sl.append(i)
        for j in range(0,s_boxes):
            sl.append(j)

            if sl not in SolveList:
                for k in range(0,4):
                    buf = buf + "x" + str(i) + "_" + str(4*j+k) + " = 0\n"
                    buf = buf + "y" + str(i) + "_" + str(4*j+k) + " = 0\n"
            sl.pop()

        if i != ROUND:
            for j in range(0,LICID):
                buf = buf + "x" + str(i+1) + "_" + str(Perm[j]) + " - y" + str(i) + "_" + str(j) + " = 0\n"
        opInner.write(buf)

    
    
    buf = ''

    if len(FixList) == 0:
        for i in SolveList:
            if i[0] == 0:
                buf = buf + "x0_" + str(4*i[1]) + " + x0_" + str(4*i[1]+1) + " + x0_" + str(4*i[1]+2) + " + x0_" + str(4*i[1]+3)
                buf = buf + " >= 1\n"
        opInner.write(buf)
    else:
        fl = []

        for i in range(0,LICID):
            fl.append(i)
            if fl in FixList:
                buf = buf + "x0_" + str(i) + " = 1\n"
            else:
                buf = buf + "x0_" + str(i) + " = 0\n"
            fl.pop()
        opInner.write(buf)
    
    buf = ''
    for i in [0,ROUND]:
        for j in range(0,LICID):
            buf = buf  + "x" + str(i) + "_" + str(j) + " + "
        if (i==0):
            buf = buf[:-2] + " = 4\n"
        if (i==ROUND):
            buf = buf[:-2] + " = 2\n"
    opInner.write(buf)
    
    buf = ''    
    opInner.write("Binary\n")
    buf = ''
    for i in range(0,ROUND):
        buf = ''
        for j in range(0,LICID):
            buf = buf + "x" + str(i) + "_" + str(j) + "\n"
        for j in range(0,LICID):
            buf = buf + "y" + str(i) + "_" + str(j) + "\n"
        opInner.write(buf)
    buf = ''
    for j in range(0,LICID):
        buf = buf + "x" + str(ROUND) + "_" + str(j) + "\n"
    opInner.write(buf)
    buf = ''
    for i in range(0,len(SolveList)):
        buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_0\n"
        buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_1\n"
        buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_2\n"
        opInner.write(buf)
        buf = ''
    opInner.close()

def strtoint(s):
    reg = 0
    s1 = ''
    s2 = ''
    res = 0
    result = []
    for i in range(0,len(s)):
        if s[i] == '_':
            reg = 1
        if s[i] >= '0' and s[i]<= '9':
            if reg == 0:
                s1 = s1 + s[i]
            if reg == 1:
                s2 = s2 + s[i]

    result.append(int(s1))
    result.append(int(s2))    
    return result
def strtoint2(s):
    reg = 0
    s1 = ''
    s2 = ''
    res = 0
    result = []
    for i in range(0,len(s)):
        if s[i] == '_':
            reg = 1
        if s[i] >= '0' and s[i]<= '9':
            if reg == 0:
                s1 = s1 + s[i]
            if reg == 1:
                s2 = s2 + s[i]

    result.append(int(s2))
    return result
def print_binary_data(data,prob):
    for i in range(0,len(data),4):
        print(data[i:i+4],end='  ');
    print(":: Hex => ",end='');
    for i in range(0,len(data),16):
        print(hex(int(data[i:i+16],2))[2:].zfill(4),end='  ')
    print(" :: ",end='0x')
    for i in range(0,len(data),16):
        print(hex(int(data[i:i+16],2))[2:].zfill(4),end='')
    print(" :: Probability => 2^{-"+str(prob)+"}")
    print("");
    
def shift(n,d,N):
    return ((n << d) % (1 << N) | (n >> (N-d) ))


filename = "Result" +"_LICID_" + str(LICID) + "_" + str(ROUND) + "_" + str(attack_type) + ".txt"
opResult = open(filename,'w+')
def possible_differential():
    count = 1
    fsl = []
    fslstring = []
    ftlstring = []
    BanList = []
    bl = []
    FixList = []
    while (count<=int(sys.argv[5])):
        PrintOuter(FixList,BanList)
        ###########################GUROBI#################################
        if(GUROBI_EXISTS == True):
            o = read("Outer" +"_LICID_" + str(LICID) + "_" + str(ROUND)  + "_" + str(attack_type) +".lp")
            o.optimize()
            obj = o.getObjective()
        ##########################CPLEX####################################
        if(CPLEX_EXISTS == True):
            mr = ModelReader()
            o = mr.read("Outer" +"_LICID_" + str(LICID) + "_" + str(ROUND) + "_" + str(attack_type)  +".lp")
            o_sol  = o.solve(log_output=True)
        ###########################GUROBI#################################
        if(GUROBI_EXISTS == True):
            o_obj = obj.getValue()
        ##################CPELX###############
        if(CPLEX_EXISTS == True):
            o_obj = o_sol.get_objective_value()
        if o_obj < (min_sbox + 64) :
            b1=[]
            fsl = []
            fslstring = []
            ###########################GUROBI#############################
            if(GUROBI_EXISTS == True):
                for v in o.getVars():
                    if v.x == 1 and v.VarName[0] == 'a':
                        fslstring.append(v.VarName)
            ###########CPLEX###########################
            if(CPLEX_EXISTS == True):
                for v in o_sol.iter_variables():
                    if ('a' in str(v)):
                        fslstring.append(str(v))
            for f in fslstring:
                fsl.append(strtoint(f))
            #if count == 1:
            for f in fslstring:
                bl.append(strtoint(f))
            BanList.append(bl)
            print("*\n*\n*\n*\n")
            print(BanList)
            print("*\n*\n*\n*\n")
            
            print(fsl)
            PrintInner(FixList,fsl)
            
            FixList = []
            ###########################GUROBI#################################
            if(GUROBI_EXISTS == True):
                i = read("Inner" +"_LICID_" + str(LICID) + "_" + str(ROUND) + "_" + str(attack_type)  +".lp")
                i.optimize()
                i_obj = i.getObjective().getValue()
            ###################CPLEX#############################
            if(CPLEX_EXISTS == True):
                i = mr.read("Inner" +"_LICID_" + str(LICID) + "_" + str(ROUND) + "_" + str(attack_type)  +".lp")
                i_sol  = i.solve(log_output=True)
                i_obj = i_sol.get_objective_value()
            print("Number of Active S-boxes: " + str(o_obj))
            print("FOUND Optimal Probability: " + str(i_obj))
            #if i_obj > LICID:
            #    break
            buf = ''
            buf = buf + str(fsl) + " " + str(i_obj) + "\n"
            
            ftlstring = []
            ###########################GUROBI#################################
            if(GUROBI_EXISTS == True):
                for v in i.getVars():
                    if v.x == 1:
                        buf = buf + v.VarName + " "
                    if v.x == 1 and v.VarName[0] == 'x' and v.VarName[1] == str(ROUND-2):
                        ftlstring.append(v.VarName)
            ############CPLEX##################################################
            if(CPLEX_EXISTS == True):
                for v in i_sol.iter_variables():
                    buf = buf + str(v) + " "
                    #if(fix==True):
                    if (('x' in str(v)) and (str(v).split("_")[0][1:] == str(ROUND)) ):
                            ftlstring.append(str(v))
            if(fix==True):
                for f in ftlstring:
                    FixList.append(strtoint2(f))
            
            buf = buf + "\n"
            opResult.write(buf)
            opResult.flush()
            round_bit_arr  = []
            round_bit_arr_y = []
            prob_arr = []
            ###########################GUROBI#################################
            if(GUROBI_EXISTS == True):
                for v in i.getVars():
                    if v.x == 1:
                        var = v.VarName
                        if (var[0] == 'x'):
                            round_bit_arr += [strtoint(var)]
                        elif (var[0] == 'y'):
                            round_bit_arr_y += [strtoint(var)]
                        elif (var[0] == 'z'):
                            new_var = var.split("_");
                            prob_arr += [strtoint("_".join([new_var[0],new_var[2]]))]
    
            ############CPLEX################
            if(CPLEX_EXISTS == True):
                for v in i_sol.iter_variables():
                        var = str(v)
                        if (var[0] == 'x'):
                            round_bit_arr += [strtoint(var)]
                        elif (var[0] == 'y'):
                            round_bit_arr_y += [strtoint(var)]
                        elif (var[0] == 'z'):
                            new_var = var.split("_");
                            prob_arr += [strtoint("_".join([new_var[0],new_var[2]]))]
    
            no_of_rounds = max([_[0] for _ in round_bit_arr])
            print("Differential Probability for " + str(no_of_rounds) + " rounds of LICID_"+str(LICID)+" is 2^{-" + str(i_obj) + "}")
            for r in range(0,no_of_rounds+1):
                print("The input difference of the round "+ str(r+1)+" is: ");
                diff_bits = list("0"*LICID);
                active_bits = [a[1] for a in round_bit_arr if a[0]==r]
                for bit in active_bits:
                    diff_bits[len(diff_bits)-1-bit] = "1";
                diff_bits_new = "".join([diff_bits[i*4]+diff_bits[i*4+1]+diff_bits[i*4+2]+diff_bits[i*4+3] for i in range(int(LICID/4)-1,-1,-1)])
                probability = 0;
                if (r>0):
                    round_prob  = [a[1] for a in prob_arr if a[0]==r-1]
                    for prob in round_prob:
                        if (prob==2):
                            probability += 3;
                        elif (prob==1):
                            probability += 2;
                        elif (prob==0):
                            probability += 1.415;
                print_binary_data("".join(diff_bits_new),probability);
            count = count + 1     
        else:
            continue

    
def impossible_differential():
    iter_count_0 = LICID
    iter_count_1 = 1
    global fix_diff;
    global fix_diff_bin;
    while True:
        PrintOuter([],[])
        iter_count_1 = iter_count_1 + 1
        ###########################GUROBI#################################
        if(GUROBI_EXISTS == True):
            o = read("Outer" +"_LICID_" + str(LICID) + "_" + str(ROUND)  + "_" + str(attack_type) +".lp")
            o.optimize()
            solCount = o.getAttr("SolCount")
        ##########################CPLEX####################################
        if(CPLEX_EXISTS == True):
            mr = ModelReader()
            o = mr.read("Outer" +"_LICID_" + str(LICID) + "_" + str(ROUND)  + "_" + str(attack_type) +".lp")
            o_sol  = o.solve(log_output=True)
            if (o_sol==None):
                solCount = 0
            else:
                solCount = 1
        ##########################GUROBI#################################
        if(solCount!=0):
            print([hex(e)[2:].zfill(int(LICID/4)) for e in fix_diff])
            print ("Iteratino No. - " + str(iter_count_0) + "_"+ str(iter_count_1) + "\n")
            print("No. of Solultions: " + str(solCount)+"\n")  
            #fix_diff[1] = fix_diff[1] << 1 
            fix_diff[1] = shift(fix_diff[1],1,LICID) 
            if (iter_count_1==LICID):
                iter_count_0 = iter_count_0 - 1
                fix_diff[0] = shift(fix_diff[0],1,LICID) 
                fix_diff[1] = 0x1000000000000001
                iter_count_1 = 0
            fix_diff_bin_paper = [bin(diff)[2:].zfill(LICID) for diff in fix_diff];
            fix_diff_bin = []
            for e in fix_diff_bin_paper:
                fix_diff_bin.append("".join([e[i*4]+e[i*4+1]+e[i*4+2]+e[i*4+3] for i in range(0,int(LICID/4))][::-1]))
            fix_bit = [];
            for diff_1 in fix_diff_bin:
                fix_bit.append([len(diff_1)-1-i for i in range(0,len(diff_1)) if diff_1[i]=="1" ])
            continue
        else:       
                print([bin(e)[2:].zfill(LICID) for e in fix_diff])
                print([hex(e)[2:].zfill(int(LICID/4)) for e in fix_diff])
                break;
      


    
if (attack_type=="possible"):
    possible_differential()
if (attack_type=="impossible"):
    impossible_differential()
    
opResult.close()