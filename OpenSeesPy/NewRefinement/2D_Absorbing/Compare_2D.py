# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:50:48 2024

@author: User
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
plt.rc('font', family= 'Times New Roman')
pi = np.pi
#------------- Read file ---------------------
def rdnumpy(textname):
    f = open(textname)
    line = f.readlines()
    lines = len(line)
    for l in line:
        le = l.strip('\n').split(' ')
        columns = len(le)
    
    A = np.zeros((lines, columns), dtype = float)
    A_row = 0
    
    for lin in line:
        list = lin.strip('\n').split(' ')
        A[A_row:] = list[0:columns]
        A_row += 1
    return A

# ====================== Read File From Numerical ==================================
soilLength = 10 #m
# soilwidth = int(2.0)
# ny = int(40) # 80, 40, 20. 10

YMesh = np.array([80, 40, 20, 10])

def Find_Middle(soilwidth, YMesh):

    MiddelNode = []
    # ------ Recorde Node/Element ID -----------------------------------------------
    for i in range(len(YMesh)):
        ny = int(YMesh[i])
        Dw = soilLength/ny # soilLength/80 , soilLength/ny

        nx = int(soilwidth/Dw)
        # print('================ Left Column Element and Node ====================')
        LowerN_Left =  1
        CenterN_Left = int(LowerN_Left + (nx+1)*(ny/2))
        UpperN_Left = int(LowerN_Left + (nx+1)* ny)
        # print(f"LowerN_Left = {LowerN_Left},CenterN_Left = {CenterN_Left}, UpperN_Left = {UpperN_Left}")
        
        # print('================ Center Column Element and Node ====================')
        LowerN_Center =  int(1 + (nx/2))
        CenterN_Center = int(LowerN_Center + (nx+1)*(ny/2))
        UpperN_Center = int(LowerN_Center + (nx+1)* ny)
        # print(f"LowerN_Center = {LowerN_Center},CenterN_Center = {CenterN_Center}, UpperN_Center = {UpperN_Center}")
        
        # print('================ Right Column Element and Node ====================')
        LowerN_Right =  int(nx+1)
        CenterN_Right = int(LowerN_Right + (nx+1)*(ny/2))
        UpperN_Right = int(LowerN_Right + (nx+1)* ny)
        # print(f"LowerN_Right = {LowerN_Right},CenterN_Right = {CenterN_Right}, UpperN_Right = {UpperN_Right}")
        
        # # -------- Quarter(3/4) Node ------------------------
        # LowerN_RQuarter = int((3*nx/4)+1)
        # UpperrN_RQuarter = int(LowerN_RQuarter + (nx+1)* ny)
        # print(f"LowerN_RQuarter = {LowerN_RQuarter} ,UpperrN_RQuarter = {UpperrN_RQuarter}")
        
        # print('================ Middle Left And Right 1m Node ====================')
        Top_CenterLeft = UpperN_Center - int(1.0/Dw)
        Top_CenterRight = UpperN_Center + int(1.0/Dw)
        # print(f'Top_CenterLeft Node = {Top_CenterLeft}; Top_CenterRight Node = {Top_CenterRight}')
        
        MiddelNode.append(UpperN_Center)
        
    Mid80row = MiddelNode[0]
    Mid40row = MiddelNode[1]
    Mid20row = MiddelNode[2]
    Mid10row = MiddelNode[3]
    
    return Mid80row, Mid40row, Mid20row, Mid10row

W2_Mid80row, W2_Mid40row, W2_Mid20row, W2_Mid10row = Find_Middle(int(2.0), YMesh)
W5_Mid80row, W5_Mid40row, W5_Mid20row, W5_Mid10row = Find_Middle(int(5.0), YMesh)
W10_Mid80row, W10_Mid40row, W10_Mid20row, W10_Mid10row = Find_Middle(int(10.0), YMesh)
W20_Mid80row, W20_Mid40row, W20_Mid20row, W20_Mid10row = Find_Middle(int(20.0), YMesh)

HZ = 40
Force_Condition = f'Change_Dw/Point_Rocking' # Vertical; Horizon; Distributed_Rocking; Point_Rocking
# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
Condition1 = f'2D_Absorb/{Force_Condition}/W_2m/HZ_{HZ}'
file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/Tie_Surface_80row/Velocity/node{W2_Mid80row}.out"
file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
file3 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/Tie_Surface_20row/Velocity/node{W2_Mid20row}.out"

# --------- LK Dashpot Boundary Condition ----------------
file4 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_Surface_80row/Velocity/node{W2_Mid80row}.out"
file5 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
file6 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_Surface_20row/Velocity/node{W2_Mid20row}.out"

# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file7 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_Surface_80row/Velocity/node{W2_Mid80row}.out"
file8 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"
file9 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_Surface_20row/Velocity/node{W2_Mid20row}.out"

Tie_W2_Mid80row = rdnumpy(file1)
Tie_W2_Mid40row = rdnumpy(file2)
Tie_W2_Mid20row = rdnumpy(file3)

LK_W2_Mid80row = rdnumpy(file4)
LK_W2_Mid40row = rdnumpy(file5)
LK_W2_Mid20row = rdnumpy(file6)

Tyep1_W2_Mid80row = rdnumpy(file7)
Tyep1_W2_Mid40row = rdnumpy(file8)
Tyep1_W2_Mid20row = rdnumpy(file9)

# ============================ SoilWidth = 5.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
Condition2 = f'2D_Absorb/{Force_Condition}/W_5m/HZ_{HZ}'
file10 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Tie_Surface_80row/Velocity/node{W5_Mid80row}.out"
file11 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
file12 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Tie_Surface_20row/Velocity/node{W5_Mid20row}.out"

# --------- LK Dashpot Boundary Condition ----------------
file13 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_Surface_80row/Velocity/node{W5_Mid80row}.out"
file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_Surface_20row/Velocity/node{W5_Mid20row}.out"

# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file16 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_Surface_80row/Velocity/node{W5_Mid80row}.out"
file17 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"
file18 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_Surface_20row/Velocity/node{W5_Mid20row}.out"

Tie_W5_Mid80row = rdnumpy(file10)
Tie_W5_Mid40row = rdnumpy(file11)
Tie_W5_Mid20row = rdnumpy(file12)

LK_W5_Mid80row = rdnumpy(file13)
LK_W5_Mid40row = rdnumpy(file14)
LK_W5_Mid20row = rdnumpy(file15)

Tyep1_W5_Mid80row = rdnumpy(file16)
Tyep1_W5_Mid40row = rdnumpy(file17)
Tyep1_W5_Mid20row = rdnumpy(file18)

# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
Condition3 =f'2D_Absorb/{Force_Condition}/W_10m/HZ_{HZ}'
file19 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/Tie_Surface_80row/Velocity/node{W10_Mid80row}.out"
file20 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
file21 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/Tie_Surface_20row/Velocity/node{W10_Mid20row}.out"

# --------- LK Dashpot Boundary Condition ----------------
file22 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_Surface_80row/Velocity/node{W10_Mid80row}.out"
file23 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
file24 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_Surface_20row/Velocity/node{W10_Mid20row}.out"

# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file25 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_Surface_80row/Velocity/node{W10_Mid80row}.out"
file26 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"
file27 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_Surface_20row/Velocity/node{W10_Mid20row}.out"

Tie_W10_Mid80row = rdnumpy(file19)
Tie_W10_Mid40row = rdnumpy(file20)
Tie_W10_Mid20row = rdnumpy(file21)

LK_W10_Mid80row = rdnumpy(file22)
LK_W10_Mid40row = rdnumpy(file23)
LK_W10_Mid20row = rdnumpy(file24)

Tyep1_W10_Mid80row = rdnumpy(file25)
Tyep1_W10_Mid40row = rdnumpy(file26)
Tyep1_W10_Mid20row = rdnumpy(file27)

# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
Condition4 =f'2D_Absorb/{Force_Condition}/W_20m/HZ_{HZ}'
file28 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/Tie_Surface_80row/Velocity/node{W20_Mid80row}.out"
file29 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
file30 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/Tie_Surface_20row/Velocity/node{W20_Mid20row}.out"

# --------- LK Dashpot Boundary Condition ----------------
file31 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/LKDash_Surface_80row/Velocity/node{W20_Mid80row}.out"
file32 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
file33 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/LKDash_Surface_20row/Velocity/node{W20_Mid20row}.out"

# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file34 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/BeamType1_Surface_80row/Velocity/node{W20_Mid80row}.out"
file35 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"
file36 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/BeamType1_Surface_20row/Velocity/node{W20_Mid20row}.out"

Tie_W20_Mid80row = rdnumpy(file28)
Tie_W20_Mid40row = rdnumpy(file29)
Tie_W20_Mid20row = rdnumpy(file30)

LK_W20_Mid80row = rdnumpy(file31)
LK_W20_Mid40row = rdnumpy(file32)
LK_W20_Mid20row = rdnumpy(file33)

Tyep1_W20_Mid80row = rdnumpy(file34)
Tyep1_W20_Mid40row = rdnumpy(file35)
Tyep1_W20_Mid20row = rdnumpy(file36)

def Find_Quarter(soilwidth, YMesh):
    
    QuarterNode = []
    # ------ Recorde Node/Element ID -----------------------------------------------
    for i in range(len(YMesh)):
        ny = int(YMesh[i])
        Dw = soilLength/ny # soilLength/80 , soilLength/ny
        nx = int(soilwidth/Dw)
        
        # print('================ Center Column Element and Node ====================')
        LowerN_Center =  int(1 + (nx/2))
        CenterN_Center = int(LowerN_Center + (nx+1)*(ny/2))
        UpperN_Center = int(LowerN_Center + (nx+1)* ny)
        # print(f"LowerN_Center = {LowerN_Center},CenterN_Center = {CenterN_Center}, UpperN_Center = {UpperN_Center}")
        
        # print('================ Middle Left And Right 1m Node ====================')
        Top_CenterLeft = UpperN_Center - int(1.0/Dw)
        Top_CenterRight = UpperN_Center + int(1.0/Dw)
        # print(f'Top_CenterLeft Node = {Top_CenterLeft}; Top_CenterRight Node = {Top_CenterRight}')s
        QuarterNode.append(Top_CenterRight)
        
    Qua80row = QuarterNode[0]
    Qua40row = QuarterNode[1]
    Qua20row = QuarterNode[2]
    Qua10row = QuarterNode[3]
    
    return Qua80row, Qua40row, Qua20row, Qua10row

W2_Qua80row, W2_Qua40row, W2_Qua20row, W2_Qua10row = Find_Quarter(int(2.0), YMesh)
W5_Qua80row, W5_Qua40row, W5_Qua20row, W5_Qua10row = Find_Quarter(int(5.0), YMesh)
W10_Qua80row, W10_Qua40row, W10_Qua20row, W10_Qua10row = Find_Quarter(int(10.0), YMesh)
W20_Qua80row, W20_Qua40row, W20_Qua20row, W20_Qua10row = Find_Quarter(int(20.0), YMesh)

# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
file37 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/Tie_Surface_80row/Velocity/node{W2_Qua80row}.out"
file38 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/Tie_Surface_40row/Velocity/node{W2_Qua40row}.out"
file39 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/Tie_Surface_20row/Velocity/node{W2_Qua20row}.out"

# --------- LK Dashpot Boundary Condition ----------------
file40 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_Surface_80row/Velocity/node{W2_Qua80row}.out"
file41 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_Surface_40row/Velocity/node{W2_Qua40row}.out"
file42 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_Surface_20row/Velocity/node{W2_Qua20row}.out"

# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file43 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_Surface_80row/Velocity/node{W2_Qua80row}.out"
file44 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_Surface_40row/Velocity/node{W2_Qua40row}.out"
file45 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_Surface_20row/Velocity/node{W2_Qua20row}.out"

Tie_W2_Qua80row = rdnumpy(file37)
Tie_W2_Qua40row = rdnumpy(file38)
Tie_W2_Qua20row = rdnumpy(file39)

LK_W2_Qua80row = rdnumpy(file40)
LK_W2_Qua40row = rdnumpy(file41)
LK_W2_Qua20row = rdnumpy(file42)

Tyep1_W2_Qua80row = rdnumpy(file43)
Tyep1_W2_Qua40row = rdnumpy(file44)
Tyep1_W2_Qua20row = rdnumpy(file45)

# ============================ SoilWidth = 5.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
file46 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Tie_Surface_80row/Velocity/node{W5_Qua80row}.out"
file47 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Tie_Surface_40row/Velocity/node{W5_Qua40row}.out"
file48 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Tie_Surface_20row/Velocity/node{W5_Qua20row}.out"

# --------- LK Dashpot Boundary Condition ----------------
file49 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_Surface_80row/Velocity/node{W5_Qua80row}.out"
file50 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_Surface_40row/Velocity/node{W5_Qua40row}.out"
file51 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_Surface_20row/Velocity/node{W5_Qua20row}.out"

# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file52 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_Surface_80row/Velocity/node{W5_Qua80row}.out"
file53 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_Surface_40row/Velocity/node{W5_Qua40row}.out"
file54 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_Surface_20row/Velocity/node{W5_Qua20row}.out"

Tie_W5_Qua80row = rdnumpy(file46)
Tie_W5_Qua40row = rdnumpy(file47)
Tie_W5_Qua20row = rdnumpy(file48)

LK_W5_Qua80row = rdnumpy(file49)
LK_W5_Qua40row = rdnumpy(file50)
LK_W5_Qua20row = rdnumpy(file51)

Tyep1_W5_Qua80row = rdnumpy(file52)
Tyep1_W5_Qua40row = rdnumpy(file53)
Tyep1_W5_Qua20row = rdnumpy(file54)

# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
file55 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/Tie_Surface_80row/Velocity/node{W10_Qua80row}.out"
file56 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/Tie_Surface_40row/Velocity/node{W10_Qua40row}.out"
file57 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/Tie_Surface_20row/Velocity/node{W10_Qua20row}.out"

# --------- LK Dashpot Boundary Condition ----------------
file58 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_Surface_80row/Velocity/node{W10_Qua80row}.out"
file59 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_Surface_40row/Velocity/node{W10_Qua40row}.out"
file60 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_Surface_20row/Velocity/node{W10_Qua20row}.out"

# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file61 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_Surface_80row/Velocity/node{W10_Qua80row}.out"
file62 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_Surface_40row/Velocity/node{W10_Qua40row}.out"
file63 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_Surface_20row/Velocity/node{W10_Qua20row}.out"

Tie_W10_Qua80row = rdnumpy(file55)
Tie_W10_Qua40row = rdnumpy(file56)
Tie_W10_Qua20row = rdnumpy(file57)

LK_W10_Qua80row = rdnumpy(file58)
LK_W10_Qua40row = rdnumpy(file59)
LK_W10_Qua20row = rdnumpy(file60)

Tyep1_W10_Qua80row = rdnumpy(file61)
Tyep1_W10_Qua40row = rdnumpy(file62)
Tyep1_W10_Qua20row = rdnumpy(file63)

# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
file64 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/Tie_Surface_80row/Velocity/node{W20_Qua80row}.out"
file65 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/Tie_Surface_40row/Velocity/node{W20_Qua40row}.out"
file66 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/Tie_Surface_20row/Velocity/node{W20_Qua20row}.out"

# --------- LK Dashpot Boundary Condition ----------------
file67 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/LKDash_Surface_80row/Velocity/node{W20_Qua80row}.out"
file68 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/LKDash_Surface_40row/Velocity/node{W20_Qua40row}.out"
file69 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/LKDash_Surface_20row/Velocity/node{W20_Qua20row}.out"

# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file70 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/BeamType1_Surface_80row/Velocity/node{W20_Qua80row}.out"
file71 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/BeamType1_Surface_40row/Velocity/node{W20_Qua40row}.out"
file72 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/BeamType1_Surface_20row/Velocity/node{W20_Qua20row}.out"

Tie_W20_Qua80row = rdnumpy(file64)
Tie_W20_Qua40row = rdnumpy(file65)
Tie_W20_Qua20row = rdnumpy(file66)

LK_W20_Qua80row = rdnumpy(file67)
LK_W20_Qua40row = rdnumpy(file68)
LK_W20_Qua20row = rdnumpy(file69)

Tyep1_W20_Qua80row = rdnumpy(file70)
Tyep1_W20_Qua40row = rdnumpy(file71)
Tyep1_W20_Qua20row = rdnumpy(file72)

def timesTime(Tie, LKDash, BeamType1, BeamType2, BeamType3):
    column_to_multiply = 0
    Tie[:, column_to_multiply] *= 10
    LKDash[:, column_to_multiply] *= 10
    BeamType1[:, column_to_multiply] *= 10
    BeamType2[:, column_to_multiply] *= 10
    BeamType3[:, column_to_multiply] *= 10

# total_time[:]*=10    
# timesTime(Tie_W20_Mid80row, LK_W20_Mid80row, Tyep1_W20_Mid80row, Tyep2_W20_Mid80row, Tyep3_W20_Mid80row)
# timesTime(Tie_W10_Mid80row, LK_W10_Mid80row, Tyep1_W10_Mid80row, Tyep2_W10_Mid80row, Tyep3_W10_Mid80row)
# timesTime(Tie_W2_Mid80row, LK_W2_Mid10row, Tyep1_W2_Mid80row, Tyep2_W2_Mid80row, Tyep3_W2_Mid80row)

plt_axis2 = 2
# # ------- wave put into the timeSeries ---------------
def Differ_BCVel(Tie, LKDash, BeamType1):
    # font_props = {'family': 'Arial', 'size': 12}

    plt.plot(Tie[:,0], Tie[:,plt_axis2],label ='Tie BC', ls = '-',color= 'limegreen',linewidth=6.0)
    plt.plot(LKDash[:,0], LKDash[:,plt_axis2],label ='LK Dashpot', ls = '-.',color= 'orange',linewidth=5.0)
    plt.plot(BeamType1[:,0], BeamType1[:,plt_axis2],label ='Beam Type1', ls = ':',color= 'purple',linewidth=4.0)

    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xlim(0.0, 0.20) 
    plt.grid(True)
    
    ax = plt.gca()
    # ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
    ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    ax.yaxis.get_offset_text().set(size=18)

x_axis = 0.25 # 0.1 0.05 **** 10 Times the x axis ******

# =============== Middle Node Velocity ======================
row_heights = [3,3,3]
fig1, (ax1,ax2,ax3,ax4) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig1.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.125' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig1.text(0.40,0.89, "(Middle Node)", color = "red", fontsize=20)
fig1.text(0.55,0.85, r"$\mathrm {Rocking}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig1.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig1.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax1 = plt.subplot(411)
Differ_BCVel(Tie_W20_Mid80row, LK_W20_Mid80row, Tyep1_W20_Mid80row)
ax1.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.12, y=0.78)

ax2 = plt.subplot(412)
Differ_BCVel(Tie_W10_Mid80row, LK_W10_Mid80row, Tyep1_W10_Mid80row)
ax2.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.12, y=0.78)

ax3 = plt.subplot(413)
Differ_BCVel(Tie_W5_Mid80row, LK_W5_Mid80row, Tyep1_W5_Mid80row)
ax3.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.12, y=0.78)

ax4 = plt.subplot(414)
Differ_BCVel(Tie_W2_Mid80row, LK_W2_Mid80row, Tyep1_W2_Mid80row)
ax4.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.12, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig1.axes[-1].get_legend_handles_labels()
fig1.legend(lines, labels, loc = (0.7, 0.4),prop=font_props)

row_heights = [3,3,3]
fig2, (ax5,ax6,ax7,ax8) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig2.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.25' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig2.text(0.40,0.89, "(Middle Node)", color = "red", fontsize=20)
fig2.text(0.55,0.85, r"$\mathrm {Rocking}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig2.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig2.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax5 = plt.subplot(411)
Differ_BCVel(Tie_W20_Mid40row, LK_W20_Mid40row, Tyep1_W20_Mid40row)
ax5.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.12, y=0.78)

ax6 = plt.subplot(412)
Differ_BCVel(Tie_W10_Mid40row, LK_W10_Mid40row, Tyep1_W10_Mid40row)
ax6.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.12, y=0.78)

ax7 = plt.subplot(413)
Differ_BCVel(Tie_W5_Mid40row, LK_W5_Mid40row, Tyep1_W5_Mid40row)
ax7.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.12, y=0.78)

ax8 = plt.subplot(414)
Differ_BCVel(Tie_W2_Mid40row, LK_W2_Mid40row, Tyep1_W2_Mid40row)
ax8.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.12, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig2.axes[-1].get_legend_handles_labels()
fig2.legend(lines, labels, loc = (0.7, 0.4),prop=font_props)

row_heights = [3,3,3]
fig3, (ax9,ax10,ax11,ax12) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig3.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.50' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig3.text(0.40,0.89, "(Middle Node)", color = "red", fontsize=20)
fig3.text(0.55,0.85, r"$\mathrm {Rocking}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig3.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig3.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax9 = plt.subplot(411)
Differ_BCVel(Tie_W20_Mid20row, LK_W20_Mid20row, Tyep1_W20_Mid20row)
ax9.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.12, y=0.78)

ax10 = plt.subplot(412)
Differ_BCVel(Tie_W10_Mid20row, LK_W10_Mid20row, Tyep1_W10_Mid20row)
ax10.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.12, y=0.78)

ax11 = plt.subplot(413)
Differ_BCVel(Tie_W5_Mid20row, LK_W5_Mid20row, Tyep1_W5_Mid20row)
ax11.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.12, y=0.78)

ax12 = plt.subplot(414)
Differ_BCVel(Tie_W2_Mid20row, LK_W2_Mid20row, Tyep1_W2_Mid20row)
ax12.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.12, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig3.axes[-1].get_legend_handles_labels()
fig3.legend(lines, labels, loc = (0.7, 0.4),prop=font_props)

# =============== Middle 1m Away Node Velocity ======================
row_heights = [3,3,3]
fig4, (ax13,ax14,ax15,ax16) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig4.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.125' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig4.text(0.25,0.89, "(Node 1 m away from the midpoint)", color = "purple", fontsize=20)
fig4.text(0.55,0.85, r"$\mathrm {Rocking}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig4.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig4.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax13 = plt.subplot(411)
Differ_BCVel(Tie_W20_Qua80row, LK_W20_Qua80row, Tyep1_W20_Qua80row)
ax13.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.12, y=0.78)

ax14 = plt.subplot(412)
Differ_BCVel(Tie_W10_Qua80row, LK_W10_Qua80row, Tyep1_W10_Qua80row)
ax14.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.12, y=0.78)

ax15 = plt.subplot(413)
Differ_BCVel(Tie_W5_Qua80row, LK_W5_Qua80row, Tyep1_W5_Qua80row)
ax15.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.12, y=0.78)

ax16 = plt.subplot(414)
Differ_BCVel(Tie_W2_Qua80row, LK_W2_Qua80row, Tyep1_W2_Qua80row)
ax16.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.12, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig4.axes[-1].get_legend_handles_labels()
fig4.legend(lines, labels, loc = (0.7, 0.45),prop=font_props)

row_heights = [3,3,3]
fig5, (ax17,ax18,ax19,ax20) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig5.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.25' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig5.text(0.25,0.89, "(Node 1 m away from the midpoint)", color = "purple", fontsize=20)
fig5.text(0.55,0.85, r"$\mathrm {Rocking}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig5.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig5.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax17 = plt.subplot(411)
Differ_BCVel(Tie_W20_Qua40row, LK_W20_Qua40row, Tyep1_W20_Qua40row)
ax17.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.12, y=0.78)

ax18 = plt.subplot(412)
Differ_BCVel(Tie_W10_Qua40row, LK_W10_Qua40row, Tyep1_W10_Qua40row)
ax18.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.12, y=0.78)

ax19 = plt.subplot(413)
Differ_BCVel(Tie_W5_Qua40row, LK_W5_Qua40row, Tyep1_W5_Qua40row)
ax19.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.12, y=0.78)

ax20 = plt.subplot(414)
Differ_BCVel(Tie_W2_Qua40row, LK_W2_Qua40row, Tyep1_W2_Qua40row)
ax20.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.12, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig5.axes[-1].get_legend_handles_labels()
fig5.legend(lines, labels, loc = (0.7, 0.45),prop=font_props)

row_heights = [3,3,3]
fig6, (ax21,ax22,ax23,ax24) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig6.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.50' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig6.text(0.25,0.89, "(Node 1 m away from the midpoint)", color = "purple", fontsize=20)
fig6.text(0.55,0.85, r"$\mathrm {Rocking}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig6.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig6.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax21 = plt.subplot(411)
Differ_BCVel(Tie_W20_Qua20row, LK_W20_Qua20row, Tyep1_W20_Qua20row)
ax21.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.12, y=0.78)

ax22 = plt.subplot(412)
Differ_BCVel(Tie_W10_Qua20row, LK_W10_Qua20row, Tyep1_W10_Qua20row)
ax22.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.12, y=0.78)

ax23 = plt.subplot(413)
Differ_BCVel(Tie_W5_Qua20row, LK_W5_Qua20row, Tyep1_W5_Qua20row)
ax23.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.12, y=0.78)

ax24 = plt.subplot(414)
Differ_BCVel(Tie_W2_Qua20row, LK_W2_Qua20row, Tyep1_W2_Qua20row)
ax24.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.12, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig6.axes[-1].get_legend_handles_labels()
fig6.legend(lines, labels, loc = (0.7, 0.45),prop=font_props)
