# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:50:48 2024

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
from matplotlib.ticker import ScalarFormatter
from matplotlib import pyplot as plt, ticker as mticker
import scipy.signal
from scipy.signal import find_peaks

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
Wave_Vel = 400 # Vertical; Rocking => cp = 400 m/s ; Horizon => cs = 200 m/s
Force_Condition = f'Central_Differential/Vertical' # Vertical; Horizon; Distributed_Rocking; Point_Rocking
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

Type1_W2_Mid80row = rdnumpy(file7)
Type1_W2_Mid40row = rdnumpy(file8)
Type1_W2_Mid20row = rdnumpy(file9)

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

Type1_W5_Mid80row = rdnumpy(file16)
Type1_W5_Mid40row = rdnumpy(file17)
Type1_W5_Mid20row = rdnumpy(file18)

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

Type1_W10_Mid80row = rdnumpy(file25)
Type1_W10_Mid40row = rdnumpy(file26)
Type1_W10_Mid20row = rdnumpy(file27)

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

Type1_W20_Mid80row = rdnumpy(file34)
Type1_W20_Mid40row = rdnumpy(file35)
Type1_W20_Mid20row = rdnumpy(file36)

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

Type1_W2_Qua80row = rdnumpy(file43)
Type1_W2_Qua40row = rdnumpy(file44)
Type1_W2_Qua20row = rdnumpy(file45)

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

Type1_W5_Qua80row = rdnumpy(file52)
Type1_W5_Qua40row = rdnumpy(file53)
Type1_W5_Qua20row = rdnumpy(file54)

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

Type1_W10_Qua80row = rdnumpy(file61)
Type1_W10_Qua40row = rdnumpy(file62)
Type1_W10_Qua20row = rdnumpy(file63)

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

Type1_W20_Qua80row = rdnumpy(file70)
Type1_W20_Qua40row = rdnumpy(file71)
Type1_W20_Qua20row = rdnumpy(file72)

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
fig1.text(0.55,0.85, r"$\mathrm {Vertical}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig1.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig1.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax1 = plt.subplot(411)
Differ_BCVel(Tie_W20_Mid80row, LK_W20_Mid80row, Type1_W20_Mid80row)
ax1.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.40, y=0.78)

ax2 = plt.subplot(412)
Differ_BCVel(Tie_W10_Mid80row, LK_W10_Mid80row, Type1_W10_Mid80row)
ax2.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.40, y=0.78)

ax3 = plt.subplot(413)
Differ_BCVel(Tie_W5_Mid80row, LK_W5_Mid80row, Type1_W5_Mid80row)
ax3.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.40, y=0.78)

ax4 = plt.subplot(414)
Differ_BCVel(Tie_W2_Mid80row, LK_W2_Mid80row, Type1_W2_Mid80row)
ax4.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.40, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig1.axes[-1].get_legend_handles_labels()
fig1.legend(lines, labels, loc = (0.7, 0.4),prop=font_props)

row_heights = [3,3,3]
fig2, (ax5,ax6,ax7,ax8) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig2.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.25' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig2.text(0.40,0.89, "(Middle Node)", color = "red", fontsize=20)
fig2.text(0.55,0.85, r"$\mathrm {Vertical}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig2.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig2.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax5 = plt.subplot(411)
Differ_BCVel(Tie_W20_Mid40row, LK_W20_Mid40row, Type1_W20_Mid40row)
ax5.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.40, y=0.78)

ax6 = plt.subplot(412)
Differ_BCVel(Tie_W10_Mid40row, LK_W10_Mid40row, Type1_W10_Mid40row)
ax6.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.40, y=0.78)

ax7 = plt.subplot(413)
Differ_BCVel(Tie_W5_Mid40row, LK_W5_Mid40row, Type1_W5_Mid40row)
ax7.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.40, y=0.78)

ax8 = plt.subplot(414)
Differ_BCVel(Tie_W2_Mid40row, LK_W2_Mid40row, Type1_W2_Mid40row)
ax8.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.40, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig2.axes[-1].get_legend_handles_labels()
fig2.legend(lines, labels, loc = (0.7, 0.4),prop=font_props)

row_heights = [3,3,3]
fig3, (ax9,ax10,ax11,ax12) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig3.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.50' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig3.text(0.40,0.89, "(Middle Node)", color = "red", fontsize=20)
fig3.text(0.55,0.85, r"$\mathrm {Vertical}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig3.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig3.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax9 = plt.subplot(411)
Differ_BCVel(Tie_W20_Mid20row, LK_W20_Mid20row, Type1_W20_Mid20row)
ax9.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.40, y=0.78)

ax10 = plt.subplot(412)
Differ_BCVel(Tie_W10_Mid20row, LK_W10_Mid20row, Type1_W10_Mid20row)
ax10.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.40, y=0.78)

ax11 = plt.subplot(413)
Differ_BCVel(Tie_W5_Mid20row, LK_W5_Mid20row, Type1_W5_Mid20row)
ax11.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.40, y=0.78)

ax12 = plt.subplot(414)
Differ_BCVel(Tie_W2_Mid20row, LK_W2_Mid20row, Type1_W2_Mid20row)
ax12.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.40, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig3.axes[-1].get_legend_handles_labels()
fig3.legend(lines, labels, loc = (0.7, 0.4),prop=font_props)

# =============== Middle 1m Away Node Velocity ======================
row_heights = [3,3,3]
fig4, (ax13,ax14,ax15,ax16) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig4.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.125' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig4.text(0.25,0.89, "(Node 1 m away from the midpoint)", color = "purple", fontsize=20)
fig4.text(0.55,0.85, r"$\mathrm {Vertical}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig4.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig4.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax13 = plt.subplot(411)
Differ_BCVel(Tie_W20_Qua80row, LK_W20_Qua80row, Type1_W20_Qua80row)
ax13.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.40, y=0.78)

ax14 = plt.subplot(412)
Differ_BCVel(Tie_W10_Qua80row, LK_W10_Qua80row, Type1_W10_Qua80row)
ax14.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.40, y=0.78)

ax15 = plt.subplot(413)
Differ_BCVel(Tie_W5_Qua80row, LK_W5_Qua80row, Type1_W5_Qua80row)
ax15.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.40, y=0.78)

ax16 = plt.subplot(414)
Differ_BCVel(Tie_W2_Qua80row, LK_W2_Qua80row, Type1_W2_Qua80row)
ax16.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.40, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig4.axes[-1].get_legend_handles_labels()
fig4.legend(lines, labels, loc = (0.7, 0.45),prop=font_props)

row_heights = [3,3,3]
fig5, (ax17,ax18,ax19,ax20) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig5.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.25' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig5.text(0.25,0.89, "(Node 1 m away from the midpoint)", color = "purple", fontsize=20)
fig5.text(0.55,0.85, r"$\mathrm {Vertical}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig5.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig5.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax17 = plt.subplot(411)
Differ_BCVel(Tie_W20_Qua40row, LK_W20_Qua40row, Type1_W20_Qua40row)
ax17.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.40, y=0.78)

ax18 = plt.subplot(412)
Differ_BCVel(Tie_W10_Qua40row, LK_W10_Qua40row, Type1_W10_Qua40row)
ax18.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.40, y=0.78)

ax19 = plt.subplot(413)
Differ_BCVel(Tie_W5_Qua40row, LK_W5_Qua40row, Type1_W5_Qua40row)
ax19.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.40, y=0.78)

ax20 = plt.subplot(414)
Differ_BCVel(Tie_W2_Qua40row, LK_W2_Qua40row, Type1_W2_Qua40row)
ax20.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.40, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig5.axes[-1].get_legend_handles_labels()
fig5.legend(lines, labels, loc = (0.7, 0.45),prop=font_props)

row_heights = [3,3,3]
fig6, (ax21,ax22,ax23,ax24) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig6.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.50' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig6.text(0.25,0.89, "(Node 1 m away from the midpoint)", color = "purple", fontsize=20)
fig6.text(0.55,0.85, r"$\mathrm {Vertical}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig6.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig6.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax21 = plt.subplot(411)
Differ_BCVel(Tie_W20_Qua20row, LK_W20_Qua20row, Type1_W20_Qua20row)
ax21.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.40, y=0.78)

ax22 = plt.subplot(412)
Differ_BCVel(Tie_W10_Qua20row, LK_W10_Qua20row, Type1_W10_Qua20row)
ax22.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.40, y=0.78)

ax23 = plt.subplot(413)
Differ_BCVel(Tie_W5_Qua20row, LK_W5_Qua20row, Type1_W5_Qua20row)
ax23.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.40, y=0.78)

ax24 = plt.subplot(414)
Differ_BCVel(Tie_W2_Qua20row, LK_W2_Qua20row, Type1_W2_Qua20row)
ax24.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.40, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig6.axes[-1].get_legend_handles_labels()
fig6.legend(lines, labels, loc = (0.7, 0.45),prop=font_props)

# ================================== Prepare Relative Error and Absolute Error ============================
Column_Index = 2 # Vertical or Rocking = 2(yaxis) ; Horizon = 1(xaxis)
# ============ Find Positive and Negative Peaks ================================== 
def Find_Peaks(Tie_W20_Mid80row):
    listID = []
    for i in range(1,len(Tie_W20_Mid80row)-1):
        if abs(Tie_W20_Mid80row[i,Column_Index]) > abs(Tie_W20_Mid80row[i-1,Column_Index]) and abs(Tie_W20_Mid80row[i,Column_Index]) > abs(Tie_W20_Mid80row[i+1,Column_Index]):
            listID.append(i)
    return listID

def Add_Peaks(Tie20_Mid80List,Tie_W20_Mid80row, PeakTie20_Mid80):
    for k in range(len(PeakTie20_Mid80)): 
        Id = Tie20_Mid80List[k]    
        # print(Id)
        PeakTie20_Mid80[k,0] = Tie_W20_Mid80row[Id,0]
        PeakTie20_Mid80[k,1] = Tie_W20_Mid80row[Id,Column_Index]
        
# ========================  Middle Node ==============================
# -------------- Tie BC -------------------
Tie20_Mid80List = Find_Peaks(Tie_W20_Mid80row)
PeakTie20_Mid80 = np.zeros((len(Tie20_Mid80List),2))
Add_Peaks(Tie20_Mid80List,Tie_W20_Mid80row, PeakTie20_Mid80)

Tie20_Mid40List = Find_Peaks(Tie_W20_Mid40row)
PeakTie20_Mid40 = np.zeros((len(Tie20_Mid40List),2))
Add_Peaks(Tie20_Mid40List,Tie_W20_Mid40row, PeakTie20_Mid40)

Tie20_Mid20List = Find_Peaks(Tie_W20_Mid20row)
PeakTie20_Mid20 = np.zeros((len(Tie20_Mid20List),2))
Add_Peaks(Tie20_Mid20List,Tie_W20_Mid20row, PeakTie20_Mid20)

Tie10_Mid80List = Find_Peaks(Tie_W10_Mid80row)
PeakTie10_Mid80 = np.zeros((len(Tie10_Mid80List),2))
Add_Peaks(Tie10_Mid80List, Tie_W10_Mid80row, PeakTie10_Mid80)

Tie10_Mid40List = Find_Peaks(Tie_W10_Mid40row)
PeakTie10_Mid40 = np.zeros((len(Tie10_Mid40List),2))
Add_Peaks(Tie10_Mid40List, Tie_W10_Mid40row, PeakTie10_Mid40)

Tie10_Mid20List = Find_Peaks(Tie_W10_Mid20row)
PeakTie10_Mid20 = np.zeros((len(Tie10_Mid20List),2))
Add_Peaks(Tie10_Mid20List, Tie_W10_Mid20row, PeakTie10_Mid20)

Tie5_Mid80List = Find_Peaks(Tie_W5_Mid80row)
PeakTie5_Mid80 = np.zeros((len(Tie5_Mid80List),2))
Add_Peaks(Tie5_Mid80List, Tie_W5_Mid80row, PeakTie5_Mid80)

Tie5_Mid40List = Find_Peaks(Tie_W5_Mid40row)
PeakTie5_Mid40 = np.zeros((len(Tie5_Mid40List),2))
Add_Peaks(Tie5_Mid40List, Tie_W5_Mid40row, PeakTie5_Mid40)

Tie5_Mid20List = Find_Peaks(Tie_W5_Mid20row)
PeakTie5_Mid20 = np.zeros((len(Tie5_Mid20List),2))
Add_Peaks(Tie5_Mid20List, Tie_W5_Mid20row, PeakTie5_Mid20)

Tie2_Mid80List = Find_Peaks(Tie_W2_Mid80row)
PeakTie2_Mid80 = np.zeros((len(Tie2_Mid80List),2))
Add_Peaks(Tie2_Mid80List, Tie_W2_Mid80row, PeakTie2_Mid80)

Tie2_Mid40List = Find_Peaks(Tie_W2_Mid40row)
PeakTie2_Mid40 = np.zeros((len(Tie2_Mid40List),2))
Add_Peaks(Tie2_Mid40List, Tie_W2_Mid40row, PeakTie2_Mid40)

Tie2_Mid20List = Find_Peaks(Tie_W2_Mid20row)
PeakTie2_Mid20 = np.zeros((len(Tie2_Mid20List),2))
Add_Peaks(Tie2_Mid20List, Tie_W2_Mid20row, PeakTie2_Mid20)

# -------------- LK Dashpot BC -------------------
LK20_Mid80List = Find_Peaks(LK_W20_Mid80row)
PeakLK20_Mid80 = np.zeros((len(LK20_Mid80List),2))
Add_Peaks(LK20_Mid80List,LK_W20_Mid80row, PeakLK20_Mid80)

LK20_Mid40List = Find_Peaks(LK_W20_Mid40row)
PeakLK20_Mid40 = np.zeros((len(LK20_Mid40List),2))
Add_Peaks(LK20_Mid40List,LK_W20_Mid40row, PeakLK20_Mid40)

LK20_Mid20List = Find_Peaks(LK_W20_Mid20row)
PeakLK20_Mid20 = np.zeros((len(LK20_Mid20List),2))
Add_Peaks(LK20_Mid20List, LK_W20_Mid20row, PeakLK20_Mid20)

LK10_Mid80List = Find_Peaks(LK_W10_Mid80row)
PeakLK10_Mid80 = np.zeros((len(LK10_Mid80List),2))
Add_Peaks(LK10_Mid80List, LK_W10_Mid80row, PeakLK10_Mid80)

LK10_Mid40List = Find_Peaks(LK_W10_Mid40row)
PeakLK10_Mid40 = np.zeros((len(LK10_Mid40List),2))
Add_Peaks(LK10_Mid40List, LK_W10_Mid40row, PeakLK10_Mid40)

LK10_Mid20List = Find_Peaks(LK_W10_Mid20row)
PeakLK10_Mid20 = np.zeros((len(LK10_Mid20List),2))
Add_Peaks(LK10_Mid20List, LK_W10_Mid20row, PeakLK10_Mid20)

LK5_Mid80List = Find_Peaks(LK_W5_Mid80row)
PeakLK5_Mid80 = np.zeros((len(LK5_Mid80List),2))
Add_Peaks(LK5_Mid80List, LK_W5_Mid80row, PeakLK5_Mid80)

LK5_Mid40List = Find_Peaks(LK_W5_Mid40row)
PeakLK5_Mid40 = np.zeros((len(LK5_Mid40List),2))
Add_Peaks(LK5_Mid40List, LK_W5_Mid40row, PeakLK5_Mid40)

LK5_Mid20List = Find_Peaks(LK_W5_Mid20row)
PeakLK5_Mid20 = np.zeros((len(LK5_Mid20List),2))
Add_Peaks(LK5_Mid20List, LK_W5_Mid20row, PeakLK5_Mid20)

LK2_Mid80List = Find_Peaks(LK_W2_Mid80row)
PeakLK2_Mid80 = np.zeros((len(LK2_Mid80List),2))
Add_Peaks(LK2_Mid80List, LK_W2_Mid80row, PeakLK2_Mid80)

LK2_Mid40List = Find_Peaks(LK_W2_Mid40row)
PeakLK2_Mid40 = np.zeros((len(LK2_Mid40List),2))
Add_Peaks(LK2_Mid40List, LK_W2_Mid40row, PeakLK2_Mid40)

LK2_Mid20List = Find_Peaks(LK_W2_Mid20row)
PeakLK2_Mid20 = np.zeros((len(LK2_Mid20List),2))
Add_Peaks(LK2_Mid20List, LK_W2_Mid20row, PeakLK2_Mid20)

# --------------Type 1： Distributed Beam Boundary Condition -------------------
Type1_20_Mid80List = Find_Peaks(Type1_W20_Mid80row)
PeakType1_20_Mid80 = np.zeros((len(Type1_20_Mid80List),2))
Add_Peaks(Type1_20_Mid80List, Type1_W20_Mid80row, PeakType1_20_Mid80)

Type1_20_Mid40List = Find_Peaks(Type1_W20_Mid40row)
PeakType1_20_Mid40 = np.zeros((len(Type1_20_Mid40List),2))
Add_Peaks(Type1_20_Mid40List, Type1_W20_Mid40row, PeakType1_20_Mid40)

Type1_20_Mid20List = Find_Peaks(Type1_W20_Mid20row)
PeakType1_20_Mid20 = np.zeros((len(Type1_20_Mid20List),2))
Add_Peaks(Type1_20_Mid20List, Type1_W20_Mid20row, PeakType1_20_Mid20)

Type1_10_Mid80List = Find_Peaks(Type1_W10_Mid80row)
PeakType1_10_Mid80 = np.zeros((len(Type1_10_Mid80List),2))
Add_Peaks(Type1_10_Mid80List, Type1_W10_Mid80row, PeakType1_10_Mid80)

Type1_10_Mid40List = Find_Peaks(Type1_W10_Mid40row)
PeakType1_10_Mid40 = np.zeros((len(Type1_10_Mid40List),2))
Add_Peaks(Type1_10_Mid40List, Type1_W10_Mid40row, PeakType1_10_Mid40)

Type1_10_Mid20List = Find_Peaks(Type1_W10_Mid20row)
PeakType1_10_Mid20 = np.zeros((len(Type1_10_Mid20List),2))
Add_Peaks(Type1_10_Mid20List, Type1_W10_Mid20row, PeakType1_10_Mid20)

Type1_5_Mid80List = Find_Peaks(Type1_W5_Mid80row)
PeakType1_5_Mid80 = np.zeros((len(Type1_5_Mid80List),2))
Add_Peaks(Type1_5_Mid80List, Type1_W5_Mid80row, PeakType1_5_Mid80)

Type1_5_Mid40List = Find_Peaks(Type1_W5_Mid40row)
PeakType1_5_Mid40 = np.zeros((len(Type1_5_Mid40List),2))
Add_Peaks(Type1_5_Mid40List, Type1_W5_Mid40row, PeakType1_5_Mid40)

Type1_5_Mid20List = Find_Peaks(Type1_W5_Mid20row)
PeakType1_5_Mid20 = np.zeros((len(Type1_5_Mid20List),2))
Add_Peaks(Type1_5_Mid20List, Type1_W5_Mid20row, PeakType1_5_Mid20)

Type1_2_Mid80List = Find_Peaks(Type1_W2_Mid80row)
PeakType1_2_Mid80 = np.zeros((len(Type1_2_Mid80List),2))
Add_Peaks(Type1_2_Mid80List, Type1_W2_Mid80row, PeakType1_2_Mid80)

Type1_2_Mid40List = Find_Peaks(Type1_W2_Mid40row)
PeakType1_2_Mid40 = np.zeros((len(Type1_2_Mid40List),2))
Add_Peaks(Type1_2_Mid40List, Type1_W2_Mid40row, PeakType1_2_Mid40)

Type1_2_Mid20List = Find_Peaks(Type1_W2_Mid20row)
PeakType1_2_Mid20 = np.zeros((len(Type1_2_Mid20List),2))
Add_Peaks(Type1_2_Mid20List, Type1_W2_Mid20row, PeakType1_2_Mid20)

# ========================  1m away from Middle Node ==============================
# -------------- Tie BC -------------------
Tie20_Qua80List = Find_Peaks(Tie_W20_Qua80row)
PeakTie20_Qua80 = np.zeros((len(Tie20_Qua80List),2))
Add_Peaks(Tie20_Qua80List, Tie_W20_Qua80row, PeakTie20_Qua80)

Tie20_Qua40List = Find_Peaks(Tie_W20_Qua40row)
PeakTie20_Qua40 = np.zeros((len(Tie20_Qua40List),2))
Add_Peaks(Tie20_Qua40List, Tie_W20_Qua40row, PeakTie20_Qua40)

Tie20_Qua20List = Find_Peaks(Tie_W20_Qua20row)
PeakTie20_Qua20 = np.zeros((len(Tie20_Qua20List),2))
Add_Peaks(Tie20_Qua20List, Tie_W20_Qua20row, PeakTie20_Qua20)

Tie10_Qua80List = Find_Peaks(Tie_W10_Qua80row)
PeakTie10_Qua80 = np.zeros((len(Tie10_Qua80List),2))
Add_Peaks(Tie10_Qua80List, Tie_W10_Qua80row, PeakTie10_Qua80)

Tie10_Qua40List = Find_Peaks(Tie_W10_Qua40row)
PeakTie10_Qua40 = np.zeros((len(Tie10_Qua40List),2))
Add_Peaks(Tie10_Qua40List, Tie_W10_Qua40row, PeakTie10_Qua40)

Tie10_Qua20List = Find_Peaks(Tie_W10_Qua20row)
PeakTie10_Qua20 = np.zeros((len(Tie10_Qua20List),2))
Add_Peaks(Tie10_Qua20List, Tie_W10_Qua20row, PeakTie10_Qua20)

Tie5_Qua80List = Find_Peaks(Tie_W5_Qua80row)
PeakTie5_Qua80 = np.zeros((len(Tie5_Qua80List),2))
Add_Peaks(Tie5_Qua80List, Tie_W5_Qua80row, PeakTie5_Qua80)

Tie5_Qua40List = Find_Peaks(Tie_W5_Qua40row)
PeakTie5_Qua40 = np.zeros((len(Tie5_Qua40List),2))
Add_Peaks(Tie5_Qua40List, Tie_W5_Qua40row, PeakTie5_Qua40)

Tie5_Qua20List = Find_Peaks(Tie_W5_Qua20row)
PeakTie5_Qua20 = np.zeros((len(Tie5_Qua20List),2))
Add_Peaks(Tie5_Qua20List, Tie_W5_Qua20row, PeakTie5_Qua20)

Tie2_Qua80List = Find_Peaks(Tie_W2_Qua80row)
PeakTie2_Qua80 = np.zeros((len(Tie2_Qua80List),2))
Add_Peaks(Tie2_Qua80List, Tie_W2_Qua80row, PeakTie2_Qua80)

Tie2_Qua40List = Find_Peaks(Tie_W2_Qua40row)
PeakTie2_Qua40 = np.zeros((len(Tie2_Qua40List),2))
Add_Peaks(Tie2_Qua40List, Tie_W2_Qua40row, PeakTie2_Qua40)

Tie2_Qua20List = Find_Peaks(Tie_W2_Qua20row)
PeakTie2_Qua20 = np.zeros((len(Tie2_Qua20List),2))
Add_Peaks(Tie2_Qua20List, Tie_W2_Qua20row, PeakTie2_Qua20)

# -------------- LK Dashpot BC -------------------
LK20_Qua80List = Find_Peaks(LK_W20_Qua80row)
PeakLK20_Qua80 = np.zeros((len(LK20_Qua80List),2))
Add_Peaks(LK20_Qua80List,LK_W20_Qua80row, PeakLK20_Qua80)

LK20_Qua40List = Find_Peaks(LK_W20_Qua40row)
PeakLK20_Qua40 = np.zeros((len(LK20_Qua40List),2))
Add_Peaks(LK20_Qua40List,LK_W20_Qua40row, PeakLK20_Qua40)

LK20_Qua20List = Find_Peaks(LK_W20_Qua20row)
PeakLK20_Qua20 = np.zeros((len(LK20_Qua20List),2))
Add_Peaks(LK20_Qua20List, LK_W20_Qua20row, PeakLK20_Qua20)

LK10_Qua80List = Find_Peaks(LK_W10_Qua80row)
PeakLK10_Qua80 = np.zeros((len(LK10_Qua80List),2))
Add_Peaks(LK10_Qua80List, LK_W10_Qua80row, PeakLK10_Qua80)

LK10_Qua40List = Find_Peaks(LK_W10_Qua40row)
PeakLK10_Qua40 = np.zeros((len(LK10_Qua40List),2))
Add_Peaks(LK10_Qua40List, LK_W10_Qua40row, PeakLK10_Qua40)

LK10_Qua20List = Find_Peaks(LK_W10_Qua20row)
PeakLK10_Qua20 = np.zeros((len(LK10_Qua20List),2))
Add_Peaks(LK10_Qua20List, LK_W10_Qua20row, PeakLK10_Qua20)

LK5_Qua80List = Find_Peaks(LK_W5_Qua80row)
PeakLK5_Qua80 = np.zeros((len(LK5_Qua80List),2))
Add_Peaks(LK5_Qua80List, LK_W5_Qua80row, PeakLK5_Qua80)

LK5_Qua40List = Find_Peaks(LK_W5_Qua40row)
PeakLK5_Qua40 = np.zeros((len(LK5_Qua40List),2))
Add_Peaks(LK5_Qua40List, LK_W5_Qua40row, PeakLK5_Qua40)

LK5_Qua20List = Find_Peaks(LK_W5_Qua20row)
PeakLK5_Qua20 = np.zeros((len(LK5_Qua20List),2))
Add_Peaks(LK5_Qua20List, LK_W5_Qua20row, PeakLK5_Qua20)

LK2_Qua80List = Find_Peaks(LK_W2_Qua80row)
PeakLK2_Qua80 = np.zeros((len(LK2_Qua80List),2))
Add_Peaks(LK2_Qua80List, LK_W2_Qua80row, PeakLK2_Qua80)

LK2_Qua40List = Find_Peaks(LK_W2_Qua40row)
PeakLK2_Qua40 = np.zeros((len(LK2_Qua40List),2))
Add_Peaks(LK2_Qua40List, LK_W2_Qua40row, PeakLK2_Qua40)

LK2_Qua20List = Find_Peaks(LK_W2_Qua20row)
PeakLK2_Qua20 = np.zeros((len(LK2_Qua20List),2))
Add_Peaks(LK2_Qua20List, LK_W2_Qua20row, PeakLK2_Qua20)

# --------------Type 1： Distributed Beam Boundary Condition -------------------
Type1_20_Qua80List = Find_Peaks(Type1_W20_Qua80row)
PeakType1_20_Qua80 = np.zeros((len(Type1_20_Qua80List),2))
Add_Peaks(Type1_20_Qua80List,Type1_W20_Qua80row, PeakType1_20_Qua80)

Type1_20_Qua40List = Find_Peaks(Type1_W20_Qua40row)
PeakType1_20_Qua40 = np.zeros((len(Type1_20_Qua40List),2))
Add_Peaks(Type1_20_Qua40List,Type1_W20_Qua40row, PeakType1_20_Qua40)

Type1_20_Qua20List = Find_Peaks(Type1_W20_Qua20row)
PeakType1_20_Qua20 = np.zeros((len(Type1_20_Qua20List),2))
Add_Peaks(Type1_20_Qua20List,Type1_W20_Qua20row, PeakType1_20_Qua20)

Type1_10_Qua80List = Find_Peaks(Type1_W10_Qua80row)
PeakType1_10_Qua80 = np.zeros((len(Type1_10_Qua80List),2))
Add_Peaks(Type1_10_Qua80List,Type1_W10_Qua80row, PeakType1_10_Qua80)

Type1_10_Qua40List = Find_Peaks(Type1_W10_Qua40row)
PeakType1_10_Qua40 = np.zeros((len(Type1_10_Qua40List),2))
Add_Peaks(Type1_10_Qua40List,Type1_W10_Qua40row, PeakType1_10_Qua40)

Type1_10_Qua20List = Find_Peaks(Type1_W10_Qua20row)
PeakType1_10_Qua20 = np.zeros((len(Type1_10_Qua20List),2))
Add_Peaks(Type1_10_Qua20List,Type1_W10_Qua20row, PeakType1_10_Qua20)

Type1_5_Qua80List = Find_Peaks(Type1_W5_Qua80row)
PeakType1_5_Qua80 = np.zeros((len(Type1_5_Qua80List),2))
Add_Peaks(Type1_5_Qua80List,Type1_W5_Qua80row, PeakType1_5_Qua80)

Type1_5_Qua40List = Find_Peaks(Type1_W5_Qua40row)
PeakType1_5_Qua40 = np.zeros((len(Type1_5_Qua40List),2))
Add_Peaks(Type1_5_Qua40List,Type1_W5_Qua40row, PeakType1_5_Qua40)

Type1_5_Qua20List = Find_Peaks(Type1_W5_Qua20row)
PeakType1_5_Qua20 = np.zeros((len(Type1_5_Qua20List),2))
Add_Peaks(Type1_5_Qua20List,Type1_W5_Qua20row, PeakType1_5_Qua20)

Type1_2_Qua80List = Find_Peaks(Type1_W2_Qua80row)
PeakType1_2_Qua80 = np.zeros((len(Type1_2_Qua80List),2))
Add_Peaks(Type1_2_Qua80List,Type1_W2_Qua80row, PeakType1_2_Qua80)

Type1_2_Qua40List = Find_Peaks(Type1_W2_Qua40row)
PeakType1_2_Qua40 = np.zeros((len(Type1_2_Qua40List),2))
Add_Peaks(Type1_2_Qua40List,Type1_W2_Qua40row, PeakType1_2_Qua40)

Type1_2_Qua20List = Find_Peaks(Type1_W2_Qua20row)
PeakType1_2_Qua20 = np.zeros((len(Type1_2_Qua20List),2))
Add_Peaks(Type1_2_Qua20List,Type1_W2_Qua20row, PeakType1_2_Qua20)

# =========== Find Grounf Surface Max/ Min Peak Value in 0.025~0.050 ==========================
Analysis_column = 99

def Find_ColMaxValue(title,start_time, end_time ,ele80_Mid):
    time_column = 0
    mask = (ele80_Mid[:, time_column] >= start_time) & (ele80_Mid[:, time_column] <= end_time)
    
    ColumnIndex = 1
    max_value = np.max(ele80_Mid[mask, ColumnIndex])
    min_value = np.min(ele80_Mid[mask, ColumnIndex])
    max_peak_index = np.argmax(ele80_Mid[mask, ColumnIndex])
    min_peak_index = np.argmin(ele80_Mid[mask, ColumnIndex])

    print(title+ f' max_value= {max_value}; max_Time= {ele80_Mid[max_peak_index,0]}; min_value= {min_value}; min_Time= {ele80_Mid[min_peak_index,0]}')
    # print(title, f'min_value= {min_value}; min_index= {ele80_Mid[min_peak_index,0]}')
    return(max_value,min_value)

pulse_Start = 10/Wave_Vel
pulse_End = 20/Wave_Vel
print(f'Pulse Wave Peak： Start = {pulse_Start} s; End = {pulse_End} s')
# --------------20m Tie BC -------------------            
maxTie20_Mid80, minTie20_Mid80 = Find_ColMaxValue('Tie20_Mid80',pulse_Start, pulse_End, PeakTie20_Mid80)
maxTie20_Mid40, minTie20_Mid40 = Find_ColMaxValue('Tie20_Mid40',pulse_Start, pulse_End, PeakTie20_Mid40)
maxTie20_Mid20, minTie20_Mid20 = Find_ColMaxValue('Tie20_Mid20',pulse_Start, pulse_End, PeakTie20_Mid20)
# --------------20m LK Dashpot BC -------------------
maxLK20_Mid80, minLK20_Mid80 = Find_ColMaxValue('LK20_Mid80',pulse_Start, pulse_End ,PeakLK20_Mid80)
maxLK20_Mid40, minLK20_Mid40 = Find_ColMaxValue('LK20_Mid40',pulse_Start, pulse_End ,PeakLK20_Mid40)
maxLK20_Mid20, minLK20_Mid20 = Find_ColMaxValue('LK20_Mid20',pulse_Start, pulse_End ,PeakLK20_Mid20)

# --------------20m Type1： Distributed Beam Boundary Condition -------------------
maxType1_20_Mid80, minType1_20_Mid80 = Find_ColMaxValue('Tyep1_20_Mid80',pulse_Start, pulse_End ,PeakType1_20_Mid80)
maxType1_20_Mid40, minType1_20_Mid40 = Find_ColMaxValue('Tyep1_20_Mid40',pulse_Start, pulse_End ,PeakType1_20_Mid40)
maxType1_20_Mid20, minType1_20_Mid20 = Find_ColMaxValue('Tyep1_20_Mid20',pulse_Start, pulse_End ,PeakType1_20_Mid20)

# --------------10m Tie BC -------------------            
maxTie10_Mid80, minTie10_Mid80 = Find_ColMaxValue('Tie10_Mid80',pulse_Start, pulse_End ,PeakTie10_Mid80)
maxTie10_Mid40, minTie10_Mid40 = Find_ColMaxValue('Tie10_Mid40',pulse_Start, pulse_End ,PeakTie10_Mid40)
maxTie10_Mid20, minTie10_Mid20 = Find_ColMaxValue('Tie10_Mid20',pulse_Start, pulse_End ,PeakTie10_Mid20)

# --------------10m LK Dashpot BC -------------------
maxLK10_Mid80, minLK10_Mid80 = Find_ColMaxValue('LK10_Mid80',pulse_Start, pulse_End ,PeakLK10_Mid80)
maxLK10_Mid40, minLK10_Mid40 = Find_ColMaxValue('LK10_Mid40',pulse_Start, pulse_End ,PeakLK10_Mid40)
maxLK10_Mid20, minLK10_Mid20 = Find_ColMaxValue('LK10_Mid20',pulse_Start, pulse_End ,PeakLK10_Mid20)

# --------------10m Type1：Distributed Beam Boundary Condition -------------------
maxType1_10_Mid80, minType1_10_Mid80 = Find_ColMaxValue('Tyep1_10_Mid80',pulse_Start, pulse_End ,PeakType1_10_Mid80)
maxType1_10_Mid40, minType1_10_Mid40 = Find_ColMaxValue('Tyep1_10_Mid40',pulse_Start, pulse_End ,PeakType1_10_Mid40)
maxType1_10_Mid20, minType1_10_Mid20 = Find_ColMaxValue('Tyep1_10_Mid20',pulse_Start, pulse_End ,PeakType1_10_Mid20)

# --------------5m Tie BC -------------------            
maxTie5_Mid80, minTie5_Mid80 = Find_ColMaxValue('Tie5_Mid80',pulse_Start, pulse_End ,PeakTie5_Mid80)
maxTie5_Mid40, minTie5_Mid40 = Find_ColMaxValue('Tie5_Mid40',pulse_Start, pulse_End ,PeakTie5_Mid40)
maxTie5_Mid20, minTie5_Mid20 = Find_ColMaxValue('Tie5_Mid20',pulse_Start, pulse_End ,PeakTie5_Mid20)

# --------------5m LK Dashpot BC -------------------
maxLK5_Mid80, minLK5_Mid80 = Find_ColMaxValue('LK5_Mid80',pulse_Start, pulse_End ,PeakLK5_Mid80)
maxLK5_Mid40, minLK5_Mid40 = Find_ColMaxValue('LK5_Mid40',pulse_Start, pulse_End ,PeakLK5_Mid40)
maxLK5_Mid20, minLK5_Mid20 = Find_ColMaxValue('LK5_Mid20',pulse_Start, pulse_End ,PeakLK5_Mid20)

# --------------5m Type1：Distributed Beam Boundary Condition -------------------
maxType1_5_Mid80, minType1_5_Mid80 = Find_ColMaxValue('Type1_5_Mid80',pulse_Start, pulse_End ,PeakType1_5_Mid80)
maxType1_5_Mid40, minType1_5_Mid40 = Find_ColMaxValue('Type1_5_Mid40',pulse_Start, pulse_End ,PeakType1_5_Mid40)
maxType1_5_Mid20, minType1_5_Mid20 = Find_ColMaxValue('Type1_5_Mid20',pulse_Start, pulse_End ,PeakType1_5_Mid20)

# --------------2m Tie BC -------------------            
maxTie2_Mid80, minTie2_Mid80 = Find_ColMaxValue('Tie2_Mid80',pulse_Start, pulse_End ,PeakTie2_Mid80)
maxTie2_Mid40, minTie2_Mid40 = Find_ColMaxValue('Tie2_Mid40',pulse_Start, pulse_End ,PeakTie2_Mid40)
maxTie2_Mid20, minTie2_Mid20 = Find_ColMaxValue('Tie2_Mid20',pulse_Start, pulse_End ,PeakTie2_Mid20)

# --------------2m LK Dashpot BC -------------------
maxLK2_Mid80, minLK2_Mid80 = Find_ColMaxValue('LK2_Mid80',pulse_Start, pulse_End ,PeakLK2_Mid80)
maxLK2_Mid40, minLK2_Mid40 = Find_ColMaxValue('LK2_Mid40',pulse_Start, pulse_End ,PeakLK2_Mid40)
maxLK2_Mid20, minLK2_Mid20 = Find_ColMaxValue('LK2_Mid20',pulse_Start, pulse_End ,PeakLK2_Mid20)

# --------------2m Type1：Distributed Beam Boundary Condition -------------------
maxType1_2_Mid80, minType1_2_Mid80 = Find_ColMaxValue('Type1_2_Mid80',pulse_Start, pulse_End ,PeakType1_2_Mid80)
maxType1_2_Mid40, minType1_2_Mid40 = Find_ColMaxValue('Type1_2_Mid40',pulse_Start, pulse_End ,PeakType1_2_Mid40)
maxType1_2_Mid20, minType1_2_Mid20 = Find_ColMaxValue('Type1_2_Mid20',pulse_Start, pulse_End ,PeakType1_2_Mid20)
# ======================== Make Analysis Solution as Mesh size minium with LK Dashpot BC ========================
MaxAnalysis = maxLK20_Mid80
MinAnalysis = minLK20_Mid80

# ========================  1m away from Middle Node ==============================
# --------------20m Tie BC -------------------            
maxTie20_Qua80, minTie20_Qua80 = Find_ColMaxValue('Tie20_Qua80',pulse_Start, pulse_End ,PeakTie20_Qua80)
maxTie20_Qua40, minTie20_Qua40 = Find_ColMaxValue('Tie20_Qua40',pulse_Start, pulse_End ,PeakTie20_Qua40)
maxTie20_Qua20, minTie20_Qua20 = Find_ColMaxValue('Tie20_Qua20',pulse_Start, pulse_End ,PeakTie20_Qua20)

# --------------20m LK Dashpot BC -------------------
maxLK20_Qua80, minLK20_Qua80 = Find_ColMaxValue('LK20_Qua80',pulse_Start, pulse_End ,PeakLK20_Qua80)
maxLK20_Qua40, minLK20_Qua40 = Find_ColMaxValue('LK20_Qua40',pulse_Start, pulse_End ,PeakLK20_Qua40)
maxLK20_Qua20, minLK20_Qua20 = Find_ColMaxValue('LK20_Qua20',pulse_Start, pulse_End ,PeakLK20_Qua20)

# --------------20m Type1：Distributed Beam Boundary Condition -------------------
maxType1_20_Qua80, minType1_20_Qua80 = Find_ColMaxValue('Type1_20_Qua80',pulse_Start, pulse_End ,PeakType1_20_Qua80)
maxType1_20_Qua40, minType1_20_Qua40 = Find_ColMaxValue('Type1_20_Qua40',pulse_Start, pulse_End ,PeakType1_20_Qua40)
maxType1_20_Qua20, minType1_20_Qua20 = Find_ColMaxValue('Type1_20_Qua20',pulse_Start, pulse_End ,PeakType1_20_Qua20)

# --------------10m Tie BC -------------------            
maxTie10_Qua80, minTie10_Qua80 = Find_ColMaxValue('Tie10_Qua80',pulse_Start, pulse_End ,PeakTie10_Qua80)
maxTie10_Qua40, minTie10_Qua40 = Find_ColMaxValue('Tie10_Qua40',pulse_Start, pulse_End ,PeakTie10_Qua40)
maxTie10_Qua20, minTie10_Qua20 = Find_ColMaxValue('Tie10_Qua20',pulse_Start, pulse_End ,PeakTie10_Qua20)

# --------------10m LK Dashpot BC -------------------
maxLK10_Qua80, minLK10_Qua80 = Find_ColMaxValue('LK10_Qua80',pulse_Start, pulse_End ,PeakLK10_Qua80)
maxLK10_Qua40, minLK10_Qua40 = Find_ColMaxValue('LK10_Qua40',pulse_Start, pulse_End ,PeakLK10_Qua40)
maxLK10_Qua20, minLK10_Qua20 = Find_ColMaxValue('LK10_Qua20',pulse_Start, pulse_End ,PeakLK10_Qua20)

# --------------10m Distributed Beam Boundary Condition -------------------
maxType1_10_Qua80, minType1_10_Qua80 = Find_ColMaxValue('Type1_10_Qua80',pulse_Start, pulse_End ,PeakType1_10_Qua80)
maxType1_10_Qua40, minType1_10_Qua40 = Find_ColMaxValue('Type1_10_Qua40',pulse_Start, pulse_End ,PeakType1_10_Qua40)
maxType1_10_Qua20, minType1_10_Qua20 = Find_ColMaxValue('Type1_10_Qua20',pulse_Start, pulse_End ,PeakType1_10_Qua20)

# --------------5m Tie BC -------------------            
maxTie5_Qua80, minTie5_Qua80 = Find_ColMaxValue('Tie5_Qua80',pulse_Start, pulse_End ,PeakTie5_Qua80)
maxTie5_Qua40, minTie5_Qua40 = Find_ColMaxValue('Tie5_Qua40',pulse_Start, pulse_End ,PeakTie5_Qua40)
maxTie5_Qua20, minTie5_Qua20 = Find_ColMaxValue('Tie5_Qua20',pulse_Start, pulse_End ,PeakTie5_Qua20)

# --------------5m LK Dashpot BC -------------------
maxLK5_Qua80, minLK5_Qua80 = Find_ColMaxValue('LK5_Qua80',pulse_Start, pulse_End ,PeakLK5_Qua80)
maxLK5_Qua40, minLK5_Qua40 = Find_ColMaxValue('LK5_Qua40',pulse_Start, pulse_End ,PeakLK5_Qua40)
maxLK5_Qua20, minLK5_Qua20 = Find_ColMaxValue('LK5_Qua20',pulse_Start, pulse_End ,PeakLK5_Qua20)

# --------------5m Distributed Beam Boundary Condition -------------------
maxType1_5_Qua80, minType1_5_Qua80 = Find_ColMaxValue('Type1_5_Qua80',pulse_Start, pulse_End ,PeakType1_5_Qua80)
maxType1_5_Qua40, minType1_5_Qua40 = Find_ColMaxValue('Type1_5_Qua40',pulse_Start, pulse_End ,PeakType1_5_Qua40)
maxType1_5_Qua20, minType1_5_Qua20 = Find_ColMaxValue('Type1_5_Qua20',pulse_Start, pulse_End ,PeakType1_5_Qua20)

# --------------2m Tie BC -------------------            
maxTie2_Qua80, minTie2_Qua80 = Find_ColMaxValue('Tie2_Qua80',pulse_Start, pulse_End ,PeakTie2_Qua80)
maxTie2_Qua40, minTie2_Qua40 = Find_ColMaxValue('Tie2_Qua40',pulse_Start, pulse_End ,PeakTie2_Qua40)
maxTie2_Qua20, minTie2_Qua20 = Find_ColMaxValue('Tie2_Qua20',pulse_Start, pulse_End ,PeakTie2_Qua20)

# --------------2m LK Dashpot BC -------------------
maxLK2_Qua80, minLK2_Qua80 = Find_ColMaxValue('LK2_Qua80',pulse_Start, pulse_End ,PeakLK2_Qua80)
maxLK2_Qua40, minLK2_Qua40 = Find_ColMaxValue('LK2_Qua40',pulse_Start, pulse_End ,PeakLK2_Qua40)
maxLK2_Qua20, minLK2_Qua20 = Find_ColMaxValue('LK2_Qua20',pulse_Start, pulse_End ,PeakLK2_Qua20)

# --------------2m Distributed Beam Boundary Condition -------------------
maxType1_2_Qua80, minType1_2_Qua80 = Find_ColMaxValue('Type1_2_Qua80',pulse_Start, pulse_End ,PeakType1_2_Qua80)
maxType1_2_Qua40, minType1_2_Qua40 = Find_ColMaxValue('Type1_2_Qua40',pulse_Start, pulse_End ,PeakType1_2_Qua40)
maxType1_2_Qua20, minType1_2_Qua20 = Find_ColMaxValue('Type1_2_Qua20',pulse_Start, pulse_End ,PeakType1_2_Qua20)

MaxAnalysis_Qua = maxLK20_Qua80
MinAnalysis_Qua = minLK20_Qua80

L = 10 #m
Mesh_Size = np.zeros(3)
Mesh20m_Size = np.zeros(2)

ele = 80 
for m in range(len(Mesh_Size)):
    if m == 0 :    
        Mesh_Size[m] = L/ (ele)
    if m > 0:    
        Mesh_Size[m] = Mesh_Size[m-1]*2
        Mesh20m_Size[m-1] =  Mesh_Size[m]
        
def errMatrix(error_dc,maxTie20_Mid80,minTie20_Mid80,maxTie20_Mid40,minTie20_Mid40,maxTie20_Mid20,minTie20_Mid20):
    error_dc[:,0] = Mesh_Size[:]
    error_dc[0,1] = maxTie20_Mid80
    error_dc[0,2] = minTie20_Mid80
    error_dc[1,1] = maxTie20_Mid40
    error_dc[1,2] = minTie20_Mid40
    error_dc[2,1] = maxTie20_Mid20
    error_dc[2,2] = minTie20_Mid20

    return error_dc

def err20Mat(error_dc, maxTie20_Mid40,minTie20_Mid40, maxTie20_Mid20,minTie20_Mid20):
    error_dc[:,0] = Mesh20m_Size[:]
    error_dc[0,1] = maxTie20_Mid40
    error_dc[0,2] = minTie20_Mid40
    error_dc[1,1] = maxTie20_Mid20
    error_dc[1,2] = minTie20_Mid20

    return error_dc

# ============================= Middle Node ========================================
# ------------W20m Tie BC Error Peak Value-----------------------
MidTie20_error = np.zeros((len(Mesh_Size),3))
errMatrix(MidTie20_error, maxTie20_Mid80, minTie20_Mid80, maxTie20_Mid40, minTie20_Mid40, maxTie20_Mid20, minTie20_Mid20)
# ------------W20m LK BC Error Peak Value-----------------------
MidLK20_error = np.zeros((len(Mesh20m_Size),3)) #####
err20Mat(MidLK20_error, maxLK20_Mid40, minLK20_Mid40, maxLK20_Mid20,minLK20_Mid20)
# ------------W20m Distributed Beam BC Error Peak Value-----------------------
MidType1_20_error = np.zeros((len(Mesh_Size),3))
errMatrix(MidType1_20_error, maxType1_20_Mid80, minType1_20_Mid80, maxType1_20_Mid40, minType1_20_Mid40, maxType1_20_Mid20, minType1_20_Mid20)

# ------------W10m Tie BC Error Peak Value-----------------------
MidTie10_error = np.zeros((len(Mesh_Size),3))
errMatrix(MidTie10_error, maxTie10_Mid80,minTie10_Mid80, maxTie10_Mid40,minTie10_Mid40, maxTie10_Mid20,minTie10_Mid20)
# ------------W10m LK BC Error Peak Value-----------------------
MidLK10_error = np.zeros((len(Mesh_Size),3))
errMatrix(MidLK10_error, maxLK10_Mid80,minLK10_Mid80, maxLK10_Mid40,minLK10_Mid40, maxLK10_Mid20,minLK10_Mid20)
# ------------W10m Distributed Beam BC Error Peak Value-----------------------
MidType1_10_error = np.zeros((len(Mesh_Size),3))
errMatrix(MidType1_10_error, maxType1_10_Mid80, minType1_10_Mid80, maxType1_10_Mid40, minType1_10_Mid40, maxType1_10_Mid20, minType1_10_Mid20)

# ------------W5m Tie BC Error Peak Value-----------------------
MidTie5_error = np.zeros((len(Mesh_Size),3))
errMatrix(MidTie5_error, maxTie5_Mid80, minTie5_Mid80, maxTie5_Mid40, minTie5_Mid40, maxTie5_Mid20, minTie5_Mid20)
# ------------W5m LK BC Error Peak Value-----------------------
MidLK5_error = np.zeros((len(Mesh_Size),3))
errMatrix(MidLK5_error, maxLK5_Mid80, minLK5_Mid80, maxLK5_Mid40, minLK5_Mid40, maxLK5_Mid20, minLK5_Mid20)
# ------------W5m Distributed Beam BC Error Peak Value-----------------------
MidType1_5_error = np.zeros((len(Mesh_Size),3))
errMatrix(MidType1_5_error, maxType1_5_Mid80, minType1_5_Mid80, maxType1_5_Mid40, minType1_5_Mid40, maxType1_5_Mid20, minType1_5_Mid20)

# ------------W2m Tie BC Error Peak Value-----------------------
MidTie2_error = np.zeros((len(Mesh_Size),3))
errMatrix(MidTie2_error, maxTie2_Mid80, minTie2_Mid80, maxTie2_Mid40, minTie2_Mid40, maxTie2_Mid20, minTie2_Mid20)
# ------------W2m LK BC Error Peak Value-----------------------
MidLK2_error = np.zeros((len(Mesh_Size),3))
errMatrix(MidLK2_error, maxLK2_Mid80, minLK2_Mid80, maxLK2_Mid40, minLK2_Mid40, maxLK2_Mid20, minLK2_Mid20)
# ------------W2m Distributed Beam BC Error Peak Value-----------------------
MidType1_2_error = np.zeros((len(Mesh_Size),3))
errMatrix(MidType1_2_error, maxType1_2_Mid80, minType1_2_Mid80, maxType1_2_Mid40, minType1_2_Mid40, maxType1_2_Mid20, minType1_2_Mid20)

# ============================= Middle 1m away Node ====================================================
# ------------W20m Tie BC Error Peak Value-----------------------
QuaTie20_error = np.zeros((len(Mesh_Size),3))
errMatrix(QuaTie20_error, maxTie20_Qua80, minTie20_Qua80, maxTie20_Qua40, minTie20_Qua40, maxTie20_Qua20, minTie20_Qua20)
# ------------W20m LK BC Error Peak Value-----------------------
QuaLK20_error = np.zeros((len(Mesh20m_Size),3)) ##### # np.zeros((len(Mesh_Size),3))
err20Mat(QuaLK20_error, maxLK20_Qua40, minLK20_Qua40, maxLK20_Qua20, minLK20_Qua20)
# ------------W20m Distributed Beam BC Error Peak Value-----------------------
QuaType1_20_error = np.zeros((len(Mesh_Size),3))
errMatrix(QuaType1_20_error, maxType1_20_Qua80, minType1_20_Qua80, maxType1_20_Qua40, minType1_20_Qua40, maxType1_20_Qua20, minType1_20_Qua20)

# ------------W10m Tie BC Error Peak Value-----------------------
QuaTie10_error = np.zeros((len(Mesh_Size),3))
errMatrix(QuaTie10_error, maxTie10_Qua80, minTie10_Qua80, maxTie10_Qua40, minTie10_Qua40, maxTie10_Qua20, minTie10_Qua20)
# ------------W10m LK BC Error Peak Value-----------------------
QuaLK10_error = np.zeros((len(Mesh_Size),3))
errMatrix(QuaLK10_error, maxLK10_Qua80, minLK10_Qua80, maxLK10_Qua40, minLK10_Qua40, maxLK10_Qua20, minLK10_Qua20)
# ------------W10m Distributed Beam BC Error Peak Value-----------------------
QuaType1_10_error = np.zeros((len(Mesh_Size),3))
errMatrix(QuaType1_10_error, maxType1_10_Qua80, minType1_10_Qua80, maxType1_10_Qua40, minType1_10_Qua40, maxType1_10_Qua20, minType1_10_Qua20)

# ------------W5m Tie BC Error Peak Value-----------------------
QuaTie5_error = np.zeros((len(Mesh_Size),3))
errMatrix(QuaTie5_error, maxTie5_Qua80, minTie5_Qua80, maxTie5_Qua40, minTie5_Qua40, maxTie5_Qua20, minTie5_Qua20)
# ------------W5m LK BC Error Peak Value-----------------------
QuaLK5_error = np.zeros((len(Mesh_Size),3))
errMatrix(QuaLK5_error, maxLK5_Qua80, minLK5_Qua80, maxLK5_Qua40, minLK5_Qua40, maxLK5_Qua20, minLK5_Qua20)
# ------------W5m Distributed Beam BC Error Peak Value-----------------------
QuaType1_5_error = np.zeros((len(Mesh_Size),3))
errMatrix(QuaType1_5_error, maxType1_5_Qua80, minType1_5_Qua80, maxType1_5_Qua40, minType1_5_Qua40, maxType1_5_Qua20, minType1_5_Qua20)

# ------------W2m Tie BC Error Peak Value-----------------------
QuaTie2_error = np.zeros((len(Mesh_Size),3))
errMatrix(QuaTie2_error, maxTie2_Qua80, minTie2_Qua80, maxTie2_Qua40, minTie2_Qua40, maxTie2_Qua20, minTie2_Qua20)
# ------------W2m LK BC Error Peak Value-----------------------
QuaLK2_error = np.zeros((len(Mesh_Size),3))
errMatrix(QuaLK2_error, maxLK2_Qua80, minLK2_Qua80, maxLK2_Qua40, minLK2_Qua40, maxLK2_Qua20, minLK2_Qua20)
# ------------W2m Distributed Beam BC Error Peak Value-----------------------
QuaType1_2_error = np.zeros((len(Mesh_Size),3))
errMatrix(QuaType1_2_error, maxType1_2_Qua80, minType1_2_Qua80, maxType1_2_Qua40, minType1_2_Qua40, maxType1_2_Qua20, minType1_2_Qua20)

# calculate_Error()
MidTieErr20 = np.zeros((len(Mesh_Size),3))
MidLKErr20 = np.zeros((len(Mesh20m_Size),3)) #####
MidType1Err20 = np.zeros((len(Mesh_Size),3))

MidTieErr10 = np.zeros((len(Mesh_Size),3))
MidLKErr10 = np.zeros((len(Mesh_Size),3))
MidType1Err10 = np.zeros((len(Mesh_Size),3))

MidTieErr5 = np.zeros((len(Mesh_Size),3))
MidLKErr5 = np.zeros((len(Mesh_Size),3))
MidType1Err5 = np.zeros((len(Mesh_Size),3))

MidTieErr2 = np.zeros((len(Mesh_Size),3))
MidLKErr2 = np.zeros((len(Mesh_Size),3))
MidType1Err2 = np.zeros((len(Mesh_Size),3))

def Calculate_Error(Mesh_Size, TieErr, Tie_error, MaxAnalysis, MinAnalysis):
    for i in range(len(Mesh_Size)):
        TieErr[:,0] = Tie_error[:,0]
        # ------------------------- Relative Error ----------------------
        TieErr[i,1] = abs((Tie_error[i,1] - MaxAnalysis)/MaxAnalysis)*100
        TieErr[i,2] = abs((Tie_error[i,2] - MinAnalysis)/MinAnalysis)*100
            
        # # ------------------------- Absolute Error ----------------------       
        # TieErr[i,1] = abs(Tie_error[i,1] - MaxAnalysis)
        # TieErr[i,2] = abs(Tie_error[i,2] - MinAnalysis)

# -------- W20 Relative Error --------------   
Calculate_Error(Mesh_Size, MidTieErr20, MidTie20_error, MaxAnalysis, MinAnalysis)
Calculate_Error(Mesh20m_Size, MidLKErr20, MidLK20_error, MaxAnalysis, MinAnalysis)      
Calculate_Error(Mesh_Size, MidType1Err20, MidType1_20_error, MaxAnalysis, MinAnalysis)

# -------- W10 Relative Error --------------   
Calculate_Error(Mesh_Size, MidTieErr10, MidTie10_error, MaxAnalysis, MinAnalysis)
Calculate_Error(Mesh_Size, MidLKErr10, MidLK10_error, MaxAnalysis, MinAnalysis)      
Calculate_Error(Mesh_Size, MidType1Err10, MidType1_10_error, MaxAnalysis, MinAnalysis)

# -------- W5 Relative Error --------------   
Calculate_Error(Mesh_Size, MidTieErr5, MidTie5_error, MaxAnalysis, MinAnalysis)
Calculate_Error(Mesh_Size, MidLKErr5, MidLK5_error, MaxAnalysis, MinAnalysis)      
Calculate_Error(Mesh_Size, MidType1Err5, MidType1_5_error, MaxAnalysis, MinAnalysis)

# -------- W2 Relative Error --------------   
Calculate_Error(Mesh_Size, MidTieErr2, MidTie2_error, MaxAnalysis, MinAnalysis)
Calculate_Error(Mesh_Size, MidLKErr2, MidLK2_error, MaxAnalysis, MinAnalysis)      
Calculate_Error(Mesh_Size, MidType1Err2, MidType1_2_error, MaxAnalysis, MinAnalysis)

# -------  Middle 1m away Node Err ----------------
QuaTieErr20 = np.zeros((len(Mesh_Size),3))
QuaLKErr20 = np.zeros((len(Mesh20m_Size),3)) ##### # np.zeros((len(Mesh_Size),3))
QuaType1Err20 = np.zeros((len(Mesh_Size),3))

QuaTieErr10 = np.zeros((len(Mesh_Size),3))
QuaLKErr10 = np.zeros((len(Mesh_Size),3))
QuaType1Err10 = np.zeros((len(Mesh_Size),3))

QuaTieErr5 = np.zeros((len(Mesh_Size),3))
QuaLKErr5 = np.zeros((len(Mesh_Size),3))
QuaType1Err5 = np.zeros((len(Mesh_Size),3))

QuaTieErr2 = np.zeros((len(Mesh_Size),3))
QuaLKErr2 = np.zeros((len(Mesh_Size),3))
QuaType1Err2 = np.zeros((len(Mesh_Size),3))

# -------- W20 Relative Error --------------   
Calculate_Error(Mesh_Size, QuaTieErr20, QuaTie20_error, MaxAnalysis_Qua, MinAnalysis_Qua)
# Calculate_Error(Mesh_Size, QuaLKErr20, QuaLK20_error)      
Calculate_Error(Mesh20m_Size, QuaLKErr20, QuaLK20_error, MaxAnalysis_Qua, MinAnalysis_Qua) 

Calculate_Error(Mesh_Size, QuaType1Err20, QuaType1_20_error, MaxAnalysis_Qua, MinAnalysis_Qua)

# -------- W10 Relative Error --------------   
Calculate_Error(Mesh_Size, QuaTieErr10, QuaTie10_error, MaxAnalysis_Qua, MinAnalysis_Qua)
Calculate_Error(Mesh_Size, QuaLKErr10, QuaLK10_error, MaxAnalysis_Qua, MinAnalysis_Qua)      
Calculate_Error(Mesh_Size, QuaType1Err10, QuaType1_10_error, MaxAnalysis_Qua, MinAnalysis_Qua)
  
# -------- W5 Relative Error --------------   
Calculate_Error(Mesh_Size, QuaTieErr5, QuaTie5_error, MaxAnalysis_Qua, MinAnalysis_Qua)
Calculate_Error(Mesh_Size, QuaLKErr5, QuaLK5_error, MaxAnalysis_Qua, MinAnalysis_Qua)      
Calculate_Error(Mesh_Size, QuaType1Err5, QuaType1_5_error, MaxAnalysis_Qua, MinAnalysis_Qua)

# -------- W2 Relative Error --------------   
Calculate_Error(Mesh_Size, QuaTieErr2, QuaTie2_error, MaxAnalysis_Qua, MinAnalysis_Qua)
Calculate_Error(Mesh_Size, QuaLKErr2, QuaLK2_error, MaxAnalysis_Qua, MinAnalysis_Qua)      
Calculate_Error(Mesh_Size, QuaType1Err2, QuaType1_2_error, MaxAnalysis_Qua, MinAnalysis_Qua)

# ------------------------------- Time Increment Relative Error: 20、10、1m (Middle point)-------------------- 
# ==================Draw Relative error : Middele point =============================
def DifferTime_elemetError(Peak,TieErr, LKErr, Type1Err):
    # font_props = {'family': 'Arial', 'size': 14}
    plt.plot(TieErr[:,0],TieErr[:,Peak],marker = '^',markersize= 10,markerfacecolor = 'white',label = 'Tie BC')
    plt.plot(LKErr[:,0],LKErr[:,Peak],marker = 'o',markersize= 8,markerfacecolor = 'white',label = 'LK Dashpot')
    plt.plot(Type1Err[:,0],Type1Err[:,Peak],marker = 's',markersize= 6,markerfacecolor = 'white',label = 'Beam Type1')


    # plt.legend(loc='center left',prop=font_props) #ncol=2,fontsize=16 frameon=False
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)

    # plt.xlim(0.0, 0.20)
    plt.grid(True)

x_axis = 0.125
figsize = (10,10)
# # ----------------- Middle Node Relative Error -------------------------
# fig7, (ax25,ax26,ax27,ax28) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize= figsize)
# fig7.suptitle(f'Ground Surface Different Boundary Compare (Surface Impulse)',x=0.50,y =0.94,fontsize = 20)
# fig7.text(0.43,0.89, "(Middle Node)", color = "red", fontsize=20)
# fig7.text(0.15,0.85, r"$\mathrm {Horizon}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)

# fig7.text(0.045,0.5, 'Peak Velocity Error: '+ r"$\ E_{Max}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=20)
# # fig7.text(0.045,0.5, 'Peak Velocity Error: '+  r'$\log_{10}$' + r"$(E_{Max})$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=20)

# # fig7.text(0.035,0.5, 'Peak Velocity Error: '+ r"$Max\ E_{abs}$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig7.text(0.015,0.5, 'Peak Velocity Error: '+  r'$\log_{10}$' +  r"$(Max\ E_{abs})$", va= 'center', rotation= 'vertical', fontsize=20)

# fig7.text(0.40,0.05,  f'Mesh size ' + r'$\Delta_y$  $\mathrm {(m)}$', va= 'center', fontsize=20)
# # fig7.text(0.35,0.056,  f'Mesh size ' + r'$\Delta_c$ $\,(log_{10})\,$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax25 = plt.subplot(411)
# DifferTime_elemetError(1, MidTieErr20, MidLKErr20, MidType1Err20)
# ax25.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.15, y=0.60)

# ax25.set_xscale('log', base=10)
# # ax25.set_yscale('log', base=10)
# ax25.tick_params(axis = 'y', which = 'both', labelsize = 16)
# # ax25.yaxis.set_minor_formatter(mticker.ScalarFormatter()) # Remove Y axix：10^0

# ax26 = plt.subplot(412)
# DifferTime_elemetError(1, MidTieErr10, MidLKErr10, MidType1Err10)
# ax26.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.15, y=0.40)

# ax26.set_xscale('log', base=10)
# # ax26.set_yscale('log', base=10)
# ax26.tick_params(axis = 'y', which = 'both', labelsize = 16)
# # ax26.yaxis.set_minor_formatter(mticker.ScalarFormatter())# Remove Y axix：10^0

# ax27 = plt.subplot(413)
# DifferTime_elemetError(1,MidTieErr5, MidLKErr5, MidType1Err5)
# ax27.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.15, y=0.70)

# ax27.set_xscale('log', base=10)
# # ax27.set_yscale('log', base=10)
# ax27.tick_params(axis = 'y', which = 'both', labelsize = 16)
# # ax27.yaxis.set_minor_formatter(mticker.ScalarFormatter())# Remove Y axix：10^0

# ax28 = plt.subplot(414)
# DifferTime_elemetError(1,MidTieErr2, MidLKErr2, MidType1Err2)
# ax28.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.15, y=0.40)

# ax28.set_xscale('log', base=10)
# # ax28.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
# ax28.tick_params(axis = 'x', which = 'both', labelsize = 17)

# # ax28.set_yscale('log', base=10)
# # ax28.tick_params(axis = 'y', which = 'both', labelsize = 16)
# # ax28.yaxis.set_minor_formatter(mticker.ScalarFormatter()) # Remove Y axix：10^0

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting

# lines, labels = fig7.axes[-1].get_legend_handles_labels()
# # fig5.legend(lines, labels, loc = 'center right',prop=font_props)
# fig7.legend(lines, labels, loc = (0.75,0.70) ,prop=font_props) #(0.7,0.76)

# # for ax in [ax25,ax26,ax27,ax28]:
# #     # formatter = ticker.ScalarFormatter(useMathText =True)
# #     # formatter.set_scientific(True)
# #     # formatter.set_powerlimits((0,0))
    
# # #     # ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# # #     # ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# # #     ax.yaxis.get_offset_text().set(size=18)

# # #     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# # #     ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# # #     ax.xaxis.get_offset_text().set(size=18)

# fig8, (ax29,ax30,ax31, ax32) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize= figsize)
# fig8.suptitle(f'Ground Surface Different Boundary Compare (Surface Impulse)',x=0.50,y =0.94,fontsize = 20)
# fig8.text(0.43,0.89, "(Middle Node)", color = "red", fontsize=20)
# fig8.text(0.15,0.83, r"$\mathrm {Horizon}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)

# fig8.text(0.045,0.5, 'Peak Velocity Error: '+ r"$\ E_{Min}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=20)
# # fig8.text(0.045,0.5, 'Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(E_{Min})$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=20)

# # fig8.text(0.035,0.5, 'Peak Velocity Error: '+ r"$Min\ E_{abs}$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig8.text(0.035,0.5, 'Peak Velocity Error: '+  r'$\log_{10}$' + r"$(Min\ E_{abs})$", va= 'center', rotation= 'vertical', fontsize=20)

# fig8.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_y$  $\mathrm {(m)}$', va= 'center', fontsize=20)
# # fig8.text(0.35,0.056,  f'Mesh size ' + r'$\Delta_c$ $\,(log_{10})\,$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax29 = plt.subplot(411)
# DifferTime_elemetError(2, MidTieErr20, MidLKErr20, MidType1Err20)
# ax29.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23,  x=0.15, y=0.40)

# ax29.set_xscale('log', base=10)
# # ax29.set_yscale('log', base=10)
# # ax29.tick_params(axis = 'y', which = 'both', labelsize = 17)

# ax30 = plt.subplot(412)
# DifferTime_elemetError(2, MidTieErr10, MidLKErr10, MidType1Err10)
# ax30.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23,  x=0.15, y=0.40)

# ax30.set_xscale('log', base=10)
# # ax30.set_yscale('log', base=10)
# # ax30.tick_params(axis = 'y', which = 'both', labelsize = 17)

# ax31 = plt.subplot(413)
# DifferTime_elemetError(2, MidTieErr5, MidLKErr5, MidType1Err5)
# ax31.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23,  x=0.15, y=0.40)

# ax31.set_xscale('log', base=10)
# # ax31.set_yscale('log', base=10)
# # ax31.tick_params(axis = 'y', which = 'both', labelsize = 17)

# ax32 = plt.subplot(414)
# DifferTime_elemetError(2, MidTieErr2, MidLKErr2, MidType1Err2)
# ax32.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23,  x=0.15, y=0.40)

# ax32.set_xscale('log', base=10)
# # ax32.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
# ax32.tick_params(axis = 'x', which = 'both', labelsize = 17)

# # ax32.set_yscale('log', base=10)
# # ax32.tick_params(axis = 'y', which = 'both', labelsize = 17)

# lines, labels = fig8.axes[-1].get_legend_handles_labels()
# fig8.legend(lines, labels, loc = (0.75,0.70),prop=font_props)

# # for ax in [ax29,ax30,ax31, ax32]:
# #     # formatter = ticker.ScalarFormatter(useMathText =True)
# #     # formatter.set_scientific(True)
# #     # formatter.set_powerlimits((0,0))
    
# #     # ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# #     # ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# #     ax.yaxis.get_offset_text().set(size=18)

# #     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# #     ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# #     ax.xaxis.get_offset_text().set(size=18)

# # ----------------- Middle 1m away Node Relative Error -------------------------
# fig9, (ax33,ax34,ax35,ax36) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize= figsize)
# fig9.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig9.text(0.30,0.89, "(Node 1 m away from the midpoint)", color = "purple", fontsize=20)
# fig9.text(0.15,0.85, r"$\mathrm {Horizon}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)

# fig9.text(0.045,0.5, 'Peak Velocity Error: '+ r"$\ E_{Max}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=20)
# # fig9.text(0.045,0.5, 'Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(E_{Max})$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig9.text(0.045,0.5, 'Peak Velocity Error: '+ r"$Max\ E_{abs}$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig9.text(0.045,0.5, 'Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(Max\ E_{abs}$)", va= 'center', rotation= 'vertical', fontsize=20)

# # fig9.text(0.045,0.5, 'Peak Velocity Error: '+ r"$E_{L2}$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig9.text(0.045,0.5, 'Peak Velocity Error: '+ r'$\log_{10}$' + r"$(E_{L2})$", va= 'center', rotation= 'vertical', fontsize=20)

# # fig9.text(0.045,0.5, 'Peak Velocity Error: '+ r"$E_{RL2}$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig9.text(0.040,0.5, 'Peak Velocity Error: '+ r'$\log_{10}$' + r"$(E_{RL2})$", va= 'center', rotation= 'vertical', fontsize=20)
# # 
# # fig9.text(0.40,0.060,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)
# fig9.text(0.35,0.056,  f'Mesh size ' + r'$\Delta_y$ $\,(log_{10})\,$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax33 = plt.subplot(411)
# DifferTime_elemetError(1, QuaTieErr20, QuaLKErr20, QuaType1Err20)
# ax33.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.15, y=0.60)

# ax33.set_xscale('log', base=10)
# # ax33.set_yscale('log', base=10)
# ax33.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # ax33.get_xaxis().set_visible(False) # make X-asis tick dissappear

# ax34 = plt.subplot(412)
# DifferTime_elemetError(1, QuaTieErr10, QuaLKErr10, QuaType1Err10)
# ax34.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.15, y=0.50)

# ax34.set_xscale('log', base=10)
# # ax34.set_yscale('log', base=10)
# ax34.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # ax34.get_xaxis().set_visible(False) # make X-asis tick dissappear

# ax35 = plt.subplot(413)
# DifferTime_elemetError(1, QuaTieErr5, QuaLKErr5, QuaType1Err5)
# ax35.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.15, y=0.50)

# ax35.set_xscale('log', base=10)
# # ax35.set_yscale('log', base=10)
# ax35.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # ax35.get_xaxis().set_visible(False) # make X-asis tick dissappear

# ax36 = plt.subplot(414)
# DifferTime_elemetError(1, QuaTieErr2, QuaLKErr2, QuaType1Err2)
# ax36.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.15, y=0.50)

# ax36.set_xscale('log', base=10)
# ax36.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
# ax36.tick_params(axis = 'x', which = 'both', labelsize = 17)

# # ax36.set_yscale('log', base=10)
# # ax36.tick_params(axis = 'y', which = 'both', labelsize = 17)

# lines, labels = fig9.axes[-1].get_legend_handles_labels()
# fig9.legend(lines, labels, loc = (0.77,0.88) ,prop=font_props)

# # for ax in [ax33,ax34,ax35,ax36]:
# #     # formatter = ticker.ScalarFormatter(useMathText =True)
# #     # formatter.set_scientific(True)
# #     # formatter.set_powerlimits((0,0))
# #     ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# #     ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# #     ax.yaxis.get_offset_text().set(size=18)
    
# #     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# #     ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# #     ax.xaxis.get_offset_text().set(size=18)

# fig10, (ax37,ax38,ax39, ax40) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize= figsize)
# fig10.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig10.text(0.30,0.89, "(Node 1 m away from the midpoint)", color = "purple", fontsize=20)
# fig10.text(0.15,0.85, r"$\mathrm {Horizon}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)

# fig10.text(0.045,0.5, 'Peak Velocity Error: '+ r"$\ E_{Min}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=20)
# # fig10.text(0.015,0.5, 'Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(E_{Min})$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig10.text(0.045,0.5,'Peak Velocity Error: '+ r"$Min\ E_{abs}$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig10.text(0.045,0.5,'Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(Min\ E_{abs})$", va= 'center', rotation= 'vertical', fontsize=20)

# # fig10.text(0.40,0.060,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)
# fig10.text(0.35,0.056,  f'Mesh size ' + r'$\Delta_y$ $\,(log_{10})\,$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax37 = plt.subplot(411)
# DifferTime_elemetError(2, QuaTieErr20, QuaLKErr20, QuaType1Err20)
# ax37.set_title(r"$w$ $\mathrm{20m}$",fontsize =23,  x=0.15, y=0.60)

# ax37.set_xscale('log', base=10)
# # ax37.set_yscale('log', base=10)
# ax37.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # ax37.get_xaxis().set_visible(False) # make X-asis tick dissappear

# ax38 = plt.subplot(412)
# DifferTime_elemetError(2, QuaTieErr10, QuaLKErr10, QuaType1Err10)
# ax38.set_title(r"$w$ $\mathrm{10m}$",fontsize =23, x=0.15, y=0.60)

# ax38.set_xscale('log', base=10)
# # ax38.set_yscale('log', base=10)
# ax38.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # ax38.get_xaxis().set_visible(False) # make X-asis tick dissappear

# ax39 = plt.subplot(413)
# DifferTime_elemetError(2, QuaTieErr5, QuaLKErr5, QuaType1Err5)
# ax39.set_title(r"$w$ $\mathrm{5m}$",fontsize =23, x=0.15, y=0.60)

# ax39.set_xscale('log', base=10)
# # ax39.set_yscale('log', base=10)
# ax39.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # ax39.get_xaxis().set_visible(False) # make X-asis tick dissappear

# ax40 = plt.subplot(414)
# DifferTime_elemetError(2, QuaTieErr2, QuaLKErr2, QuaType1Err2)
# ax40.set_title(r"$w$ $\mathrm{2m}$",fontsize =23, x=0.15, y=0.60)

# ax40.set_xscale('log', base=10)
# ax40.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
# ax40.tick_params(axis = 'x', which = 'both', labelsize = 17)

# # ax40.set_yscale('log', base=10)
# # ax40.tick_params(axis = 'y', which = 'both', labelsize = 17)

# lines, labels = fig10.axes[-1].get_legend_handles_labels()
# fig10.legend(lines, labels, loc = 'upper right',prop=font_props)

# # for ax in [ax37,ax38,ax39, ax40]:
# #     # formatter = ticker.ScalarFormatter(useMathText =True)
# #     # formatter.set_scientific(True)
# #     # formatter.set_powerlimits((0,0))
# #     ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# #     ax.yaxis.get_offset_text().set(size=18)
    
# #     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# #     ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# #     ax.xaxis.get_offset_text().set(size=18)

# ================================== Prepare L2-Norm Error ============================
# # ---------- Find Same Time ---------------------
Compare_Time = LK_W20_Mid80row[:,0]
Element80 = LK_W20_Mid80row[:,0]

Element40 = LK_W20_Mid40row[:,0]
Element20 = LK_W20_Mid20row[:,0]

CompareTime_dt = LK_W20_Mid80row[0,0]
Element80_dt = LK_W20_Mid80row[0,0]
Element40_dt = LK_W20_Mid40row[0,0]
Element20_dt = LK_W20_Mid20row[0,0]

# ================= Calculate_2NormError ===============================
def Calculate_2NormError(Compare_Time,LK_W20_Mid80row, Element80,Tie_W20_Mid80row):
# ------------------------- L-2 Norm Error ------------------------
    common80 = set(Compare_Time) & set(Element80)
    differences = []
    for common_value in common80:
        index1 = np.where(Element80 == common_value)[0][0]
        index2 = np.where(Compare_Time == common_value)[0][0] # Theory
        # print(index1,index2)
        diff = (Tie_W20_Mid80row[index1, Column_Index] - LK_W20_Mid80row[index2, Column_Index])
        differences.append(diff)
        
    compare = np.array(differences) 
    squared_values = np.square(compare)
    sum_of_squares = np.sum(squared_values)
    result = np.sqrt(sum_of_squares)
    
    return result

# ================= Calculate_2NormError ===============================
def Calculate_RelativeL2norm(Compare_Time, LK_W20_Mid80row, Element80, Tie_W20_Mid80row): # , CompareTime_dt, Element80_dt
# ------------------------- L-2 Norm Error ------------------------
    common80 = set(Compare_Time) & set(Element80)
    differences = []
    Mom = []
    
    for common_value in common80:
        index1 = np.where(Element80 == common_value)[0][0]
        index2 = np.where(Compare_Time == common_value)[0][0]

        diff = (Tie_W20_Mid80row[index1, Column_Index] - LK_W20_Mid80row[index2,Column_Index])
        Mother = LK_W20_Mid80row[index2, Column_Index]
        
        differences.append(diff)
        Mom.append(Mother)
        
    compare = np.array(differences)
    Momm = np.array(Mom)
    
    squared_values = np.square(compare)
    squared_value2 = np.square(Momm)
    
    sum_of_squares = np.sum(squared_values)
    sum_of_square2 = np.sum(squared_value2)

    result = np.sqrt((sum_of_squares)/sum_of_square2)
    return result

def Add_Err(LK_W20_Mid80row, MidTieErr20,MidTie20_error,Tie_W20_Mid80row,Tie_W20_Mid40row,Tie_W20_Mid20row):
    MidTieErr20[:,0] = MidTie20_error[:,0] 
# ===================================== Calculate_2NormError ============================================================
    MidTieErr20[0,1] = Calculate_2NormError(Compare_Time,LK_W20_Mid80row, Element80,Tie_W20_Mid80row)
    MidTieErr20[1,1] = Calculate_2NormError(Compare_Time,LK_W20_Mid80row, Element40,Tie_W20_Mid40row)
    MidTieErr20[2,1] = Calculate_2NormError(Compare_Time,LK_W20_Mid80row, Element20,Tie_W20_Mid20row)
    
# # ===================================== Calculate_L2-norm Error ============================================================
#     MidTieErr20[0,1] = Calculate_RelativeL2norm(Compare_Time,LK_W20_Mid80row, Element80,Tie_W20_Mid80row)
#     MidTieErr20[1,1] = Calculate_RelativeL2norm(Compare_Time,LK_W20_Mid80row, Element40,Tie_W20_Mid40row)
#     MidTieErr20[2,1] = Calculate_RelativeL2norm(Compare_Time,LK_W20_Mid80row, Element20,Tie_W20_Mid20row)


# calculate_L2 Norm Error()
MidTieErr20_L2 = np.zeros((len(Mesh_Size),3))
MidLKErr20_L2 = np.zeros((len(Mesh20m_Size),3)) #####
MidType1Err20_L2 = np.zeros((len(Mesh_Size),3))

MidTieErr10_L2 = np.zeros((len(Mesh_Size),3))
MidLKErr10_L2 = np.zeros((len(Mesh_Size),3))
MidType1Err10_L2 = np.zeros((len(Mesh_Size),3))

MidTieErr5_L2 = np.zeros((len(Mesh_Size),3))
MidLKErr5_L2 = np.zeros((len(Mesh_Size),3))
MidType1Err5_L2 = np.zeros((len(Mesh_Size),3))

MidTieErr2_L2 = np.zeros((len(Mesh_Size),3))
MidLKErr2_L2 = np.zeros((len(Mesh_Size),3))
MidType1Err2_L2 = np.zeros((len(Mesh_Size),3))

# ---------------------------- Middle Node -----------------------------
# ----------------- Soil Width 20m -------------------------------------    
Add_Err(LK_W20_Mid80row, MidTieErr20_L2, MidTie20_error, Tie_W20_Mid80row, Tie_W20_Mid40row, Tie_W20_Mid20row)

MidLKErr20_L2[:,0] = MidLK20_error[:,0] 
# ===================================== Calculate_2NormError ===============
MidLKErr20_L2[0,1] = Calculate_2NormError(Compare_Time,LK_W20_Mid80row, Element40,LK_W20_Mid40row)
MidLKErr20_L2[1,1] = Calculate_2NormError(Compare_Time,LK_W20_Mid80row, Element20,LK_W20_Mid20row)

# # ===================================== Calculate_Relative 2NormError ==========================
# MidLKErr20_L2[0,1] = Calculate_RelativeL2norm(Compare_Time,LK_W20_Mid80row, Element40,LK_W20_Mid40row)
# MidLKErr20_L2[1,1] = Calculate_RelativeL2norm(Compare_Time,LK_W20_Mid80row, Element20,LK_W20_Mid20row)

Add_Err(LK_W20_Mid80row, MidType1Err20_L2, MidType1_20_error, Type1_W20_Mid80row, Type1_W20_Mid40row, Type1_W20_Mid20row)

# ----------------- Soil Width 10m -------------------------------------    
Add_Err(LK_W20_Mid80row, MidTieErr10_L2, MidTie10_error, Tie_W10_Mid80row,Tie_W10_Mid40row,Tie_W10_Mid20row)
Add_Err(LK_W20_Mid80row, MidLKErr10_L2, MidLK10_error, LK_W10_Mid80row, LK_W10_Mid40row, LK_W10_Mid20row)
Add_Err(LK_W20_Mid80row, MidType1Err10_L2, MidType1_10_error, Type1_W10_Mid80row, Type1_W10_Mid40row, Type1_W10_Mid20row)

# ----------------- Soil Width 5m -------------------------------------    
Add_Err(LK_W20_Mid80row, MidTieErr5_L2, MidTie5_error, Tie_W5_Mid80row, Tie_W5_Mid40row, Tie_W5_Mid20row)
Add_Err(LK_W20_Mid80row, MidLKErr5_L2, MidLK5_error, LK_W5_Mid80row, LK_W5_Mid40row, LK_W5_Mid20row)
Add_Err(LK_W20_Mid80row, MidType1Err5_L2, MidType1_5_error, Type1_W5_Mid80row, Type1_W5_Mid40row, Type1_W5_Mid20row)

# ----------------- Soil Width 2m -------------------------------------    
Add_Err(LK_W20_Mid80row, MidTieErr2_L2, MidTie2_error, Tie_W2_Mid80row, Tie_W2_Mid40row, Tie_W2_Mid20row)
Add_Err(LK_W20_Mid80row, MidLKErr2_L2, MidLK2_error, LK_W2_Mid80row, LK_W2_Mid40row, LK_W2_Mid20row)
Add_Err(LK_W20_Mid80row, MidType1Err2_L2, MidType1_2_error, Type1_W2_Mid80row, Type1_W2_Mid40row, Type1_W2_Mid20row)

QuaTieErr20_L2 = np.zeros((len(Mesh_Size),3))
QuaLKErr20_L2 = np.zeros((len(Mesh20m_Size),3)) #####
QuaType1Err20_L2 = np.zeros((len(Mesh_Size),3))

QuaTieErr10_L2 = np.zeros((len(Mesh_Size),3))
QuaLKErr10_L2 = np.zeros((len(Mesh_Size),3))
QuaType1Err10_L2 = np.zeros((len(Mesh_Size),3))

QuaTieErr5_L2 = np.zeros((len(Mesh_Size),3))
QuaLKErr5_L2 = np.zeros((len(Mesh_Size),3))
QuaType1Err5_L2 = np.zeros((len(Mesh_Size),3))

QuaTieErr2_L2 = np.zeros((len(Mesh_Size),3))
QuaLKErr2_L2 = np.zeros((len(Mesh_Size),3))
QuaType1Err2_L2 = np.zeros((len(Mesh_Size),3))

# ---------------------------- Middle 1m away Node -----------------------------
# ----------------- Soil Width 20m -------------------------------------    
Add_Err(LK_W20_Qua80row, QuaTieErr20_L2, QuaTie20_error, Tie_W20_Qua80row,Tie_W20_Qua40row,Tie_W20_Qua20row)

QuaLKErr20_L2[:,0] = MidLK20_error[:,0] 
# ===================================== Calculate_2NormError ===============
QuaLKErr20_L2[0,1] = Calculate_2NormError(Compare_Time,LK_W20_Qua80row, Element40,LK_W20_Qua40row)
QuaLKErr20_L2[1,1] = Calculate_2NormError(Compare_Time,LK_W20_Qua80row, Element20,LK_W20_Qua20row)

# # ===================================== Calculate_Relative 2NormError ==========================
# QuaLKErr20_L2[0,1] = Calculate_RelativeL2norm(Compare_Time,LK_W20_Qua80row, Element40,LK_W20_Qua40row)
# QuaLKErr20_L2[1,1] = Calculate_RelativeL2norm(Compare_Time,LK_W20_Qua80row, Element20,LK_W20_Qua20row)

Add_Err(LK_W20_Qua80row, QuaType1Err20_L2, QuaType1_20_error, Type1_W20_Qua80row, Type1_W20_Qua40row, Type1_W20_Qua20row)

# ----------------- Soil Width 10m -------------------------------------    
Add_Err(LK_W20_Qua80row, QuaTieErr10_L2, QuaTie10_error, Tie_W10_Qua80row, Tie_W10_Qua40row,Tie_W10_Qua20row)
Add_Err(LK_W20_Qua80row, QuaLKErr10_L2, QuaLK10_error, LK_W10_Qua80row, LK_W10_Qua40row, LK_W10_Qua20row)
Add_Err(LK_W20_Qua80row, QuaType1Err10_L2, QuaType1_10_error, Type1_W10_Qua80row, Type1_W10_Qua40row, Type1_W10_Qua20row)

# ----------------- Soil Width 5m -------------------------------------    
Add_Err(LK_W20_Qua80row, QuaTieErr5_L2, QuaTie5_error, Tie_W5_Qua80row, Tie_W5_Qua40row,Tie_W5_Qua20row)
Add_Err(LK_W20_Qua80row, QuaLKErr5_L2, QuaLK5_error, LK_W5_Qua80row, LK_W5_Qua40row, LK_W5_Qua20row)
Add_Err(LK_W20_Qua80row, QuaType1Err5_L2, QuaType1_5_error, Type1_W5_Qua80row, Type1_W5_Qua40row, Type1_W5_Qua20row)

# ----------------- Soil Width 2m -------------------------------------    
Add_Err(LK_W20_Qua80row, QuaTieErr2_L2, QuaTie2_error, Tie_W2_Qua80row, Tie_W2_Qua40row,Tie_W2_Qua20row)
Add_Err(LK_W20_Qua80row, QuaLKErr2_L2, QuaLK2_error, LK_W2_Qua80row, LK_W2_Qua40row, LK_W2_Qua20row)
Add_Err(LK_W20_Qua80row, QuaType1Err2_L2, QuaType1_2_error, Type1_W2_Qua80row, Type1_W2_Qua40row, Type1_W2_Qua20row)

# # ================= Draw L2-Norm and Relative L2-Norm ==========================
# fig11, (ax41,ax42,ax43, ax44) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize= figsize)
# fig11.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig11.text(0.42,0.89, "(Middle Node)", color = "red", fontsize=20)
# fig11.text(0.60,0.82, r"$\mathrm {Horizon}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)

# # fig11.text(0.045,0.5, 'Peak Velocity Error: '+ r"$E_{L2}$", va= 'center', rotation= 'vertical', fontsize=20)
# fig11.text(0.01,0.5, 'Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(E_{L2})$", va= 'center', rotation= 'vertical', fontsize=20)

# # fig11.text(0.020,0.5, 'Peak Velocity Error: '+ r"$E_{RL2}$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig11.text(0.01,0.5, 'Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(E_{RL2})$", va= 'center', rotation= 'vertical', fontsize=20)

# # fig11.text(0.40,0.060,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)
# fig11.text(0.35,0.056,  f'Mesh size ' + r'$\Delta_y$ $\,(log_{10})\,$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax41 = plt.subplot(411)
# DifferTime_elemetError(1, MidTieErr20_L2, MidLKErr20_L2, MidType1Err20_L2)
# ax41.set_title(r"$w$ $\mathrm{20m}$",fontsize =23,  x=0.15, y=0.40)

# ax41.set_xscale('log', base=10)
# # ax41.set_yscale('log', base=10)
# ax41.tick_params(axis = 'y', which = 'both', labelsize = 17)
# ax41.get_xaxis().set_visible(False) # make X-asis tick dissappear

# ax42 = plt.subplot(412)
# DifferTime_elemetError(1, MidTieErr10_L2, MidLKErr10_L2, MidType1Err10_L2)
# ax42.set_title(r"$w$ $\mathrm{10m}$",fontsize =23, x=0.15, y=0.40)

# ax42.set_xscale('log', base=10)
# ax42.set_yscale('log', base=10)
# ax42.tick_params(axis = 'y', which = 'both', labelsize = 17)
# ax42.get_xaxis().set_visible(False) # make X-asis tick dissappear

# ax43 = plt.subplot(413)
# DifferTime_elemetError(1, MidTieErr5_L2, MidLKErr5_L2, MidType1Err5_L2)
# ax43.set_title(r"$w$ $\mathrm{5m}$",fontsize =23, x=0.15, y=0.45)

# ax43.set_xscale('log', base=10)
# ax43.set_yscale('log', base=10)
# ax43.tick_params(axis = 'y', which = 'both', labelsize = 17)
# ax43.get_xaxis().set_visible(False) # make X-asis tick dissappear

# ax44 = plt.subplot(414)
# DifferTime_elemetError(1, MidTieErr2_L2, MidLKErr2_L2, MidType1Err2_L2)
# ax44.set_title(r"$w$ $\mathrm{2m}$",fontsize =23, x=0.15, y=0.60)

# ax44.set_xscale('log', base=10)
# ax44.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
# ax44.tick_params(axis = 'x', which = 'both', labelsize = 17)

# ax44.set_yscale('log', base=10)
# ax44.tick_params(axis = 'y', which = 'both', labelsize = 17)

# lines, labels = fig11.axes[-1].get_legend_handles_labels()
# fig11.legend(lines, labels, loc = 'upper right',prop=font_props)


# for ax in [ax41,ax42,ax43, ax44]:
#     # formatter = ticker.ScalarFormatter(useMathText =True)
#     # formatter.set_scientific(True)
#     # formatter.set_powerlimits((0,0))
#     ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
#     ax.yaxis.get_offset_text().set(size=18)
    
#     # ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
#     # ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
#     # ax.xaxis.get_offset_text().set(size=18)

# fig11, (ax41,ax42,ax43, ax44) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize= figsize)
# fig11.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig11.text(0.30,0.89, "(Node 1 m away from the midpoint)", color = "purple", fontsize=20)
# fig11.text(0.15,0.80, r"$\mathrm {Horizon}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)

# # fig11.text(0.045,0.5, 'Peak Velocity Error: '+ r"$E_{L2}$", va= 'center', rotation= 'vertical', fontsize=20)
# fig11.text(0.01,0.5, 'Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(E_{L2})$", va= 'center', rotation= 'vertical', fontsize=20)

# # fig11.text(0.020,0.5, 'Peak Velocity Error: '+ r"$E_{RL2}$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig11.text(0.01,0.5, 'Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(E_{RL2})$", va= 'center', rotation= 'vertical', fontsize=20)

# # fig11.text(0.40,0.060,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)
# fig11.text(0.35,0.056,  f'Mesh size ' + r'$\Delta_y$ $\,(log_{10})\,$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax41 = plt.subplot(411)
# DifferTime_elemetError(1, QuaTieErr20_L2, QuaLKErr20_L2, QuaType1Err20_L2)
# ax41.set_title(r"$w$ $\mathrm{20m}$",fontsize =23,  x=0.15, y=0.20)

# ax41.set_xscale('log', base=10)
# # ax41.set_yscale('log', base=10)
# ax41.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # ax41.get_xaxis().set_visible(False) # make X-asis tick dissappear

# ax42 = plt.subplot(412)
# DifferTime_elemetError(1, QuaTieErr10_L2, QuaLKErr10_L2, QuaType1Err10_L2)
# ax42.set_title(r"$w$ $\mathrm{10m}$",fontsize =23, x=0.15, y=0.50)

# ax42.set_xscale('log', base=10)
# ax42.set_yscale('log', base=10)
# ax42.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # ax42.get_xaxis().set_visible(False) # make X-asis tick dissappear

# ax43 = plt.subplot(413)
# DifferTime_elemetError(1, QuaTieErr5_L2, QuaLKErr5_L2, QuaType1Err5_L2)
# ax43.set_title(r"$w$ $\mathrm{5m}$",fontsize =23, x=0.15, y=0.50)

# ax43.set_xscale('log', base=10)
# ax43.set_yscale('log', base=10)
# ax43.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # ax43.get_xaxis().set_visible(False) # make X-asis tick dissappear

# ax44 = plt.subplot(414)
# DifferTime_elemetError(1, QuaTieErr2_L2, QuaLKErr2_L2, QuaType1Err2_L2)
# ax44.set_title(r"$w$ $\mathrm{2m}$",fontsize =23, x=0.15, y=0.30)

# ax44.set_xscale('log', base=10)
# ax44.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
# ax44.tick_params(axis = 'x', which = 'both', labelsize = 17)

# ax44.set_yscale('log', base=10)
# ax44.tick_params(axis = 'y', which = 'both', labelsize = 17)

# lines, labels = fig11.axes[-1].get_legend_handles_labels()
# fig11.legend(lines, labels, loc = 'upper right',prop=font_props)

# # for ax in [ax41,ax42,ax43, ax44]:
# #     # formatter = ticker.ScalarFormatter(useMathText =True)
# #     # formatter.set_scientific(True)
# #     # formatter.set_powerlimits((0,0))
# #     ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# #     ax.yaxis.get_offset_text().set(size=18)
    
# #     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# #     ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# #     ax.xaxis.get_offset_text().set(size=18)

# =============== Time At 0.10~0.20 s Relative Error Compare ===========================
# --------------20m Tie BC -------------------            
T10maxTie20_Mid80, T10minTie20_Mid80 = Find_ColMaxValue('Time1.0 Tie20_Mid80',0.10, 0.20 ,PeakTie20_Mid80)
T10maxTie20_Mid40, T10minTie20_Mid40 = Find_ColMaxValue('Time1.0 Tie20_Mid40',0.10, 0.20 ,PeakTie20_Mid40)
T10maxTie20_Mid20, T10minTie20_Mid20 = Find_ColMaxValue('Time1.0 Tie20_Mid20',0.10, 0.20 ,PeakTie20_Mid20)

# --------------20m LK Dashpot BC -------------------
T10maxLK20_Mid80, T10minLK20_Mid80 = Find_ColMaxValue('Time1.0 LK20_Mid80',0.10, 0.20 ,PeakLK20_Mid80)
T10maxLK20_Mid40, T10minLK20_Mid40 = Find_ColMaxValue('Time1.0 LK20_Mid40',0.10, 0.20 ,PeakLK20_Mid40)
T10maxLK20_Mid20, T10minLK20_Mid20 = Find_ColMaxValue('Time1.0 LK20_Mid20',0.10, 0.20 ,PeakLK20_Mid20)

# --------------20m Distributed Beam Boundary Condition -------------------
T10maxType1_20_Mid80, T10minType1_20_Mid80 = Find_ColMaxValue('Time1.0 Beam20_Mid80',0.10, 0.20 ,PeakType1_20_Mid80)
T10maxType1_20_Mid40, T10minType1_20_Mid40 = Find_ColMaxValue('Time1.0 Beam20_Mid40',0.10, 0.20 ,PeakType1_20_Mid40)
T10maxType1_20_Mid20, T10minType1_20_Mid20 = Find_ColMaxValue('Time1.0 Beam20_Mid20',0.10, 0.20 ,PeakType1_20_Mid20)

# --------------10m Tie BC -------------------            
T10maxTie10_Mid80, T10minTie10_Mid80 = Find_ColMaxValue('Time1.0 Tie10_Mid80',0.10, 0.20 ,PeakTie10_Mid80)
T10maxTie10_Mid40, T10minTie10_Mid40 = Find_ColMaxValue('Time1.0 Tie10_Mid40',0.10, 0.20 ,PeakTie10_Mid40)
T10maxTie10_Mid20, T10minTie10_Mid20 = Find_ColMaxValue('Time1.0 Tie10_Mid20',0.10, 0.20 ,PeakTie10_Mid20)

# --------------10m LK Dashpot BC -------------------
T10maxLK10_Mid80, T10minLK10_Mid80 = Find_ColMaxValue('Time1.0 LK10_Mid80',0.10, 0.20 ,PeakLK10_Mid80)
T10maxLK10_Mid40, T10minLK10_Mid40 = Find_ColMaxValue('Time1.0 LK10_Mid40',0.10, 0.20 ,PeakLK10_Mid40)
T10maxLK10_Mid20, T10minLK10_Mid20 = Find_ColMaxValue('Time1.0 LK10_Mid20',0.10, 0.20 ,PeakLK10_Mid20)

# --------------10m Distributed Beam Boundary Condition -------------------
T10maxType1_10_Mid80, T10minType1_10_Mid80 = Find_ColMaxValue('Time1.0 Beam10_Mid80',0.10, 0.20 ,PeakType1_10_Mid80)
T10maxType1_10_Mid40, T10minType1_10_Mid40 = Find_ColMaxValue('Time1.0 Beam10_Mid40',0.10, 0.20 ,PeakType1_10_Mid40)
T10maxType1_10_Mid20, T10minType1_10_Mid20 = Find_ColMaxValue('Time1.0 Beam10_Mid20',0.10, 0.20 ,PeakType1_10_Mid20)

# --------------5m Tie BC -------------------            
T10maxTie5_Mid80, T10minTie5_Mid80 = Find_ColMaxValue('Time1.0 Tie1_Mid80',0.10, 0.20 ,PeakTie5_Mid80)
T10maxTie5_Mid40, T10minTie5_Mid40 = Find_ColMaxValue('Time1.0 Tie1_Mid40',0.10, 0.20 ,PeakTie5_Mid40)
T10maxTie5_Mid20, T10minTie5_Mid20 = Find_ColMaxValue('Time1.0 Tie1_Mid20',0.10, 0.20 ,PeakTie5_Mid20)

# --------------5m LK Dashpot BC -------------------
T10maxLK5_Mid80, T10minLK5_Mid80 = Find_ColMaxValue('Time1.0 LK1_Mid80',0.10, 0.20 ,PeakLK5_Mid80)
T10maxLK5_Mid40, T10minLK5_Mid40 = Find_ColMaxValue('Time1.0 LK1_Mid40',0.10, 0.20 ,PeakLK5_Mid40)
T10maxLK5_Mid20, T10minLK5_Mid20 = Find_ColMaxValue('Time1.0 LK1_Mid20',0.10, 0.20 ,PeakLK5_Mid20)

# --------------5m Distributed Beam Boundary Condition -------------------
T10maxType1_5_Mid80, T10minType1_5_Mid80 = Find_ColMaxValue('Time1.0 Beam1_Mid80',0.10, 0.20 ,PeakType1_5_Mid80)
T10maxType1_5_Mid40, T10minType1_5_Mid40 = Find_ColMaxValue('Time1.0 Beam1_Mid40',0.10, 0.20 ,PeakType1_5_Mid40)
T10maxType1_5_Mid20, T10minType1_5_Mid20 = Find_ColMaxValue('Time1.0 Beam1_Mid20',0.10, 0.20 ,PeakType1_5_Mid20)

# --------------2m Tie BC -------------------            
T10maxTie2_Mid80, T10minTie2_Mid80 = Find_ColMaxValue('Time1.0 Tie1_Mid80',0.10, 0.20 ,PeakTie2_Mid80)
T10maxTie2_Mid40, T10minTie2_Mid40 = Find_ColMaxValue('Time1.0 Tie1_Mid40',0.10, 0.20 ,PeakTie2_Mid40)
T10maxTie2_Mid20, T10minTie2_Mid20 = Find_ColMaxValue('Time1.0 Tie1_Mid20',0.10, 0.20 ,PeakTie2_Mid20)

# --------------2m LK Dashpot BC -------------------
T10maxLK2_Mid80, T10minLK2_Mid80 = Find_ColMaxValue('Time1.0 LK1_Mid80',0.10, 0.20 ,PeakLK2_Mid80)
T10maxLK2_Mid40, T10minLK2_Mid40 = Find_ColMaxValue('Time1.0 LK1_Mid40',0.10, 0.20 ,PeakLK2_Mid40)
T10maxLK2_Mid20, T10minLK2_Mid20 = Find_ColMaxValue('Time1.0 LK1_Mid20',0.10, 0.20 ,PeakLK2_Mid20)

# --------------2m Distributed Beam Boundary Condition -------------------
T10maxType1_2_Mid80, T10minType1_2_Mid80 = Find_ColMaxValue('Time1.0 Beam1_Mid80',0.10, 0.20 ,PeakType1_2_Mid80)
T10maxType1_2_Mid40, T10minType1_2_Mid40 = Find_ColMaxValue('Time1.0 Beam1_Mid40',0.10, 0.20 ,PeakType1_2_Mid40)
T10maxType1_2_Mid20, T10minType1_2_Mid20 = Find_ColMaxValue('Time1.0 Beam1_Mid20',0.10, 0.20 ,PeakType1_2_Mid20)

# ============================= Middle Node ========================================
# ------------W20m Tie BC Error Peak Value-----------------------
T10MidTie20_error = np.zeros((len(Mesh_Size),3))
errMatrix(T10MidTie20_error,  T10maxTie20_Mid80,T10minTie20_Mid80, T10maxTie20_Mid40,T10minTie20_Mid40, T10maxTie20_Mid20,T10minTie20_Mid20)
# ------------W20m LK BC Error Peak Value-----------------------err20Mat
T10MidLK20_error = np.zeros((len(Mesh20m_Size),3))
err20Mat(T10MidLK20_error, T10maxLK20_Mid40,T10minLK20_Mid40, T10maxLK20_Mid20,T10minLK20_Mid20)
# ------------W20m Distributed Beam BC Error Peak Value-----------------------
T10MidType1_20_error = np.zeros((len(Mesh_Size),3))
errMatrix(T10MidType1_20_error, T10maxType1_20_Mid80, T10minType1_20_Mid80, T10maxType1_20_Mid40, T10minType1_20_Mid40, T10maxType1_20_Mid20, T10minType1_20_Mid20)

# ------------W10m Tie BC Error Peak Value-----------------------
T10MidTie10_error = np.zeros((len(Mesh_Size),3))
errMatrix(T10MidTie10_error, T10maxTie10_Mid80,T10minTie10_Mid80, T10maxTie10_Mid40,T10minTie10_Mid40, T10maxTie10_Mid20,T10minTie10_Mid20)
# ------------W10m LK BC Error Peak Value-----------------------
T10MidLK10_error = np.zeros((len(Mesh_Size),3))
errMatrix(T10MidLK10_error, T10maxLK10_Mid80,T10minLK10_Mid80, T10maxLK10_Mid40,T10minLK10_Mid40, T10maxLK10_Mid20,T10minLK10_Mid20,)
# ------------W10m Distributed Beam BC Error Peak Value-----------------------
T10MidType1_10_error = np.zeros((len(Mesh_Size),3))
errMatrix(T10MidType1_10_error, T10maxType1_10_Mid80, T10minType1_10_Mid80, T10maxType1_10_Mid40, T10minType1_10_Mid40, T10maxType1_10_Mid20, T10minType1_10_Mid20)

# ------------W5m Tie BC Error Peak Value-----------------------
T10MidTie5_error = np.zeros((len(Mesh_Size),3))
errMatrix(T10MidTie5_error, T10maxTie5_Mid80,T10minTie5_Mid80, T10maxTie5_Mid40, T10minTie5_Mid40, T10maxTie5_Mid20, T10minTie5_Mid20)
# ------------W5m LK BC Error Peak Value-----------------------
T10MidLK5_error = np.zeros((len(Mesh_Size),3))
errMatrix(T10MidLK5_error, T10maxLK5_Mid80, T10minLK5_Mid80, T10maxLK5_Mid40, T10minLK5_Mid40, T10maxLK5_Mid20, T10minLK5_Mid20,)
# ------------W5m Distributed Beam BC Error Peak Value-----------------------
T10MidType1_5_error = np.zeros((len(Mesh_Size),3))
errMatrix(T10MidType1_5_error, T10maxType1_5_Mid80, T10minType1_5_Mid80, T10maxType1_5_Mid40, T10minType1_5_Mid40, T10maxType1_5_Mid20, T10minType1_5_Mid20)

# ------------W2m Tie BC Error Peak Value-----------------------
T10MidTie2_error = np.zeros((len(Mesh_Size),3))
errMatrix(T10MidTie2_error, T10maxTie2_Mid80,T10minTie2_Mid80, T10maxTie2_Mid40, T10minTie2_Mid40, T10maxTie2_Mid20, T10minTie2_Mid20)
# ------------W2m LK BC Error Peak Value-----------------------
T10MidLK2_error = np.zeros((len(Mesh_Size),3))
errMatrix(T10MidLK2_error, T10maxLK2_Mid80, T10minLK2_Mid80, T10maxLK2_Mid40, T10minLK2_Mid40, T10maxLK2_Mid20, T10minLK2_Mid20,)
# ------------W2m Distributed Beam BC Error Peak Value-----------------------
T10MidType1_2_error = np.zeros((len(Mesh_Size),3))
errMatrix(T10MidType1_2_error, T10maxType1_2_Mid80, T10minType1_2_Mid80, T10maxType1_2_Mid40, T10minType1_2_Mid40, T10maxType1_2_Mid20, T10minType1_2_Mid20)

def Calculate_LaterError(Mesh_Size, TieErr,Tie_error):
    for i in range(len(Mesh_Size)):
        TieErr[:,0] = Tie_error[:,0]
        # ------------------------- Relative Error ----------------------
        TieErr[i,1] = ((Tie_error[i,1] - 0)/MaxAnalysis)*100
        TieErr[i,2] = ((Tie_error[i,2] - 0)/MinAnalysis)*100
                
        # # ------------------------- Absolute Error ----------------------       
        # TieErr[i,1] = abs(Tie_error[i,1] - 0)
        # TieErr[i,2] = abs(Tie_error[i,2] - 0)
        
# calculate_Error()
T10MidTieErr20 = np.zeros((len(Mesh_Size),3))
T10MidLKErr20 = np.zeros((len(Mesh20m_Size),3))
T10MidType1_Err20 = np.zeros((len(Mesh_Size),3))

T10MidTieErr10 = np.zeros((len(Mesh_Size),3))
T10MidLKErr10 = np.zeros((len(Mesh_Size),3))
T10MidType1_Err10 = np.zeros((len(Mesh_Size),3))

T10MidTieErr5 = np.zeros((len(Mesh_Size),3))
T10MidLKErr5 = np.zeros((len(Mesh_Size),3))
T10MidType1_Err5 = np.zeros((len(Mesh_Size),3))

T10MidTieErr2 = np.zeros((len(Mesh_Size),3))
T10MidLKErr2 = np.zeros((len(Mesh_Size),3))
T10MidType1_Err2 = np.zeros((len(Mesh_Size),3))

# -------- W20 Relative Error --------------   
Calculate_LaterError(Mesh_Size, T10MidTieErr20, T10MidTie20_error)
Calculate_LaterError(Mesh20m_Size, T10MidLKErr20, T10MidLK20_error)
Calculate_LaterError(Mesh_Size, T10MidType1_Err20, T10MidType1_20_error)

# -------- W10 Relative Error --------------   
Calculate_LaterError(Mesh_Size, T10MidTieErr10, T10MidTie10_error)
Calculate_LaterError(Mesh_Size, T10MidLKErr10, T10MidLK10_error)      
Calculate_LaterError(Mesh_Size, T10MidType1_Err10, T10MidType1_10_error)
 
# -------- W5 Relative Error --------------   
Calculate_LaterError(Mesh_Size, T10MidTieErr5, T10MidTie5_error)
Calculate_LaterError(Mesh_Size, T10MidLKErr5, T10MidLK5_error)      
Calculate_LaterError(Mesh_Size, T10MidType1_Err5, T10MidType1_5_error)

# -------- W2 Relative Error --------------   
Calculate_LaterError(Mesh_Size, T10MidTieErr2, T10MidTie2_error)
Calculate_LaterError(Mesh_Size, T10MidLKErr2, T10MidLK2_error)      
Calculate_LaterError(Mesh_Size, T10MidType1_Err2, T10MidType1_2_error)

# # -----------------Time:0.10~0.20s Maximum Middle Node Relative Error -------------------------
# fig12, (ax45,ax46,ax47, ax48) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize= figsize)
# fig12.suptitle(f'Ground Surface Different Boundary Compare (Surface Impulse)',x=0.50,y =0.94,fontsize = 20)
# fig12.text(0.43,0.89, "(Middle Node)", color = "red", fontsize=20)
# fig12.text(0.15,0.85, r"$\mathrm {Horizon}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)

# fig12.text(0.045,0.5, '(t = 0.10~0.20s) Peak Velocity Error: '+ r"$PE_{Max}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=20)
# # fig12.text(0.045,0.5, '(t = 0.10~0.20s) Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(PE_{Max})$", va= 'center', rotation= 'vertical', fontsize=20)

# # fig12.text(0.045,0.5, '(t = 0.10~0.20s) Peak Velocity Error: '+ r"$PE_{abs}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=20)
# # fig12.text(0.045,0.5, '(t = 0.10~0.20s) Peak Velocity Error: '+  r'$\log_{10}$'+  r"$(PE_{abs})$", va= 'center', rotation= 'vertical', fontsize=20)

# # fig12.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)
# fig12.text(0.35,0.056,  f'Mesh size ' + r'$\Delta_y$ $\,(log_{10})\,$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax45 = plt.subplot(411)
# DifferTime_elemetError(1,T10MidTieErr20, T10MidLKErr20, T10MidType1_Err20)
# ax45.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.15, y=0.15)

# ax45.set_xscale('log', base=10)
# # ax45.set_yscale('log', base=10)
# ax45.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # ax45.yaxis.set_minor_formatter(mticker.ScalarFormatter())# Remove Y axix：10^0

# ax46 = plt.subplot(412)
# DifferTime_elemetError(1,T10MidTieErr10, T10MidLKErr10, T10MidType1_Err10)
# ax46.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.15, y=0.40)

# ax46.set_xscale('log', base=10)
# # ax46.set_yscale('log', base=10)
# ax46.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # ax46.yaxis.set_minor_formatter(mticker.ScalarFormatter())# Remove Y axix：10^0

# ax47 = plt.subplot(413)
# DifferTime_elemetError(1,T10MidTieErr5, T10MidLKErr5, T10MidType1_Err5)
# ax47.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.15, y=0.35)

# ax47.set_xscale('log', base=10)
# # ax47.set_yscale('log', base=10)
# ax47.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # ax47.yaxis.set_minor_formatter(mticker.ScalarFormatter())# Remove Y axix：10^0

# ax48 = plt.subplot(414)
# DifferTime_elemetError(1,T10MidTieErr2, T10MidLKErr2, T10MidType1_Err2)
# ax48.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.15, y=0.40)

# ax48.set_xscale('log', base=10)
# ax48.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
# ax48.tick_params(axis = 'x', which = 'both', labelsize = 17)

# # ax48.set_yscale('log', base=10)
# # ax48.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # ax48.yaxis.set_minor_formatter(mticker.ScalarFormatter())# Remove Y axix：10^0

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting

# lines, labels = fig12.axes[-1].get_legend_handles_labels()
# fig12.legend(lines, labels, loc = (0.78,0.34),prop=font_props)

# # for ax in [ax45,ax46,ax47, ax48]:
# #     # formatter = ticker.ScalarFormatter(useMathText =True)
# #     # formatter.set_scientific(True)
# #     # formatter.set_powerlimits((0,0))
    
# #     # ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# #     # ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# #     ax.yaxis.get_offset_text().set(size=18)

# #     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# #     ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# #     ax.xaxis.get_offset_text().set(size=18)

# # # -----------------Time:0.10~ 0.20s Minimum Middle Node Relative Error -------------------------
# fig13, (ax49,ax50,ax51,ax52) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize= figsize)
# fig13.suptitle(f'Ground Surface Different Boundary Compare (Surface Impulse)',x=0.50,y =0.94,fontsize = 20)
# fig13.text(0.43,0.89, "(Middle Node)", color = "red", fontsize=20)
# fig13.text(0.15,0.85, r"$\mathrm {Horizon}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)

# fig13.text(0.010,0.5, '(t = 0.10~0.20s) Peak Velocity Error: '+ r"$NE_{Min}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=20)
# # fig13.text(0.045,0.5, '(t = 0.10~0.20s) Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(NE_{Min})$", va= 'center', rotation= 'vertical', fontsize=20)

# # fig13.text(0.045,0.5, '(t = 0.10~0.20s) Peak Velocity Error: '+ r"$NE_{abs}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=20)
# # fig13.text(0.045,0.5, '(t = 0.10~0.20s) Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(NE_{abs})$", va= 'center', rotation= 'vertical', fontsize=20)

# # fig13.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)
# fig13.text(0.35,0.056,  f'Mesh size ' + r'$\Delta_c$ $\,(log_{10})\,$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax49 = plt.subplot(411)
# DifferTime_elemetError(2, T10MidTieErr20, T10MidLKErr20, T10MidType1_Err20)
# ax49.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.15, y=0.30)

# ax49.set_xscale('log', base=10)
# ax49.set_yscale('log', base=10)
# ax49.tick_params(axis = 'y', which = 'both', labelsize = 16)
# # ax49.yaxis.set_minor_formatter(mticker.ScalarFormatter())# Remove Y axix：10^0

# ax50 = plt.subplot(412)
# DifferTime_elemetError(2,T10MidTieErr10, T10MidLKErr10, T10MidType1_Err10)
# ax50.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.15, y=0.30)

# ax50.set_xscale('log', base=10)
# ax50.set_yscale('log', base=10)
# ax50.tick_params(axis = 'y', which = 'both', labelsize = 16)
# # ax50.yaxis.set_minor_formatter(mticker.ScalarFormatter())# Remove Y axix：10^0

# ax51 = plt.subplot(413)
# DifferTime_elemetError(2,T10MidTieErr5, T10MidLKErr5, T10MidType1_Err5)
# ax51.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.15, y=0.35)

# ax51.set_xscale('log', base=10)
# ax51.set_yscale('log', base=10)
# ax51.tick_params(axis = 'y', which = 'both', labelsize = 16)
# # ax51.yaxis.set_minor_formatter(mticker.ScalarFormatter())# Remove Y axix：10^0

# ax52 = plt.subplot(414)
# DifferTime_elemetError(2,T10MidTieErr2, T10MidLKErr2, T10MidType1_Err2)
# ax52.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.15, y=0.35)

# ax52.set_xscale('log', base=10)
# ax52.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
# ax52.tick_params(axis = 'x', which = 'both', labelsize = 17)

# ax52.set_yscale('log', base=10)
# ax52.tick_params(axis = 'y', which = 'both', labelsize = 16)
# # # ax52.yaxis.set_minor_formatter(mticker.ScalarFormatter())# Remove Y axix：10^0

# lines, labels = fig13.axes[-1].get_legend_handles_labels()
# fig13.legend(lines, labels, loc = (0.78,0.75),prop=font_props)

# # for ax in [ax40,ax41,ax42]:
# #     # formatter = ticker.ScalarFormatter(useMathText =True)
# #     # formatter.set_scientific(True)
# #     # formatter.set_powerlimits((0,0))
    
# #     # ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# #     # ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# #     ax.yaxis.get_offset_text().set(size=18)

# #     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# #     ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# #     ax.xaxis.get_offset_text().set(size=18)
