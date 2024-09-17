# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 22:40:20 2024

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
from matplotlib.ticker import LogLocator, NullFormatter, LogFormatter

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

YMesh = np.array([40]) # 80, 40, 20, 10

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
    
    Mid40row = MiddelNode[0]
    
    # Mid80row = MiddelNode[0]
    # Mid40row = MiddelNode[1]
    # Mid20row = MiddelNode[2]
    # Mid10row = MiddelNode[3]
    return Mid40row

# ---------- Consider Mesh = 40 row ----------------------------------
W2_Mid40row = Find_Middle(int(2.0), YMesh)
W5_Mid40row = Find_Middle(int(5.0), YMesh)
W10_Mid40row = Find_Middle(int(10.0), YMesh)
W20_Mid40row = Find_Middle(int(20.0), YMesh)

# ============== Read Middle Node Analysis Data ==========================================
# HZ = 40
Wave_Vel = 200 # Vertical; Rocking => cp = 400 m/s ; Horizon => cs = 200 m/s
Force_Condition = f'2D_Absorb/Newmark_Linear_Test/Horizon' # Vertical; Horizon; Rocking

Dy = 0.25 # m
# --------------------- Choose which WaveLength ---------------------------------
Dy_lambP = np.array([Dy/40, Dy/20, Dy/10, Dy/5]) # Pwave = 10, 20, 40, 80HZ ==> 400/f
Dy_lambS = np.array([Dy/20, Dy/10, Dy/5, Dy/2.5]) # Swave = 10, 20, 40, 80HZ ==> 200/f

Dy_lamb = Dy_lambS # --> Use to Draw Dy/WaveLength

# ----------------- f = 10HZ --------------------------------
HZ10 = f'HZ_10'
# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
Condition1 = f'{Force_Condition}/W_2m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file3 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Tie_W2_HZ10_Mid = rdnumpy(file1)
LK_W2_HZ10_Mid = rdnumpy(file2)
BeamType_W2_HZ10_Mid = rdnumpy(file3)
# ============================ SoilWidth = 5.0 m (HZ = 10)=======================================
Condition2 = f'{Force_Condition}/W_5m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file4 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file5 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file6 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Tie_W5_HZ10_Mid = rdnumpy(file4)
LK_W5_HZ10_Mid = rdnumpy(file5)
BeamType_W5_HZ10_Mid = rdnumpy(file6)
# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
Condition3 = f'{Force_Condition}/W_10m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file7 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file8 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file9 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Tie_W10_HZ10_Mid = rdnumpy(file7)
LK_W10_HZ10_Mid = rdnumpy(file8)
BeamType_W10_HZ10_Mid = rdnumpy(file9)
# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
Condition4 = f'{Force_Condition}/W_20m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file10 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file11 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file12 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Tie_W20_HZ10_Mid = rdnumpy(file10)
LK_W20_HZ10_Mid = rdnumpy(file11)
BeamType_W20_HZ10_Mid = rdnumpy(file12)

# ----------------- f = 20HZ --------------------------------
HZ20 = f'HZ_20'
# ============================ SoilWidth = 2.0 m (HZ = 20)=======================================
Condition5 = f'{Force_Condition}/W_2m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file13 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Tie_W2_HZ20_Mid = rdnumpy(file13)
LK_W2_HZ20_Mid = rdnumpy(file14)
BeamType_W2_HZ20_Mid = rdnumpy(file15)
# ============================ SoilWidth = 5.0 m (HZ = 20)=======================================
Condition6 = f'{Force_Condition}/W_5m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file16 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file17 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file18 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Tie_W5_HZ20_Mid = rdnumpy(file16)
LK_W5_HZ20_Mid = rdnumpy(file17)
BeamType_W5_HZ20_Mid = rdnumpy(file18)
# ============================ SoilWidth = 10.0 m (HZ = 20)=======================================
Condition7 = f'{Force_Condition}/W_10m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file19 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file20 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file21 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Tie_W10_HZ20_Mid = rdnumpy(file19)
LK_W10_HZ20_Mid = rdnumpy(file20)
BeamType_W10_HZ20_Mid = rdnumpy(file21)

# ============================ SoilWidth = 20.0 m (HZ = 20)=======================================
Condition8 = f'{Force_Condition}/W_20m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file22 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file23 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file24 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Tie_W20_HZ20_Mid = rdnumpy(file22)
LK_W20_HZ20_Mid = rdnumpy(file23)
BeamType_W20_HZ20_Mid = rdnumpy(file24)

# ----------------- f = 40HZ --------------------------------
HZ40 = f'HZ_40'
# ============================ SoilWidth = 2.0 m (HZ = 40)=======================================
Condition9 = f'{Force_Condition}/W_2m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file25 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file26 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file27 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Tie_W2_HZ40_Mid = rdnumpy(file25)
LK_W2_HZ40_Mid = rdnumpy(file26)
BeamType_W2_HZ40_Mid = rdnumpy(file27)
# ============================ SoilWidth = 5.0 m (HZ = 40)=======================================
Condition10 = f'{Force_Condition}/W_5m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file28 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file29 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file30 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Tie_W5_HZ40_Mid = rdnumpy(file28)
LK_W5_HZ40_Mid = rdnumpy(file29)
BeamType_W5_HZ40_Mid = rdnumpy(file30)
# ============================ SoilWidth = 10.0 m (HZ = 40)=======================================
Condition11 = f'{Force_Condition}/W_10m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file31 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file32 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file33 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Tie_W10_HZ40_Mid = rdnumpy(file31)
LK_W10_HZ40_Mid = rdnumpy(file32)
BeamType_W10_HZ40_Mid = rdnumpy(file33)
# ============================ SoilWidth = 20.0 m (HZ = 40)=======================================
Condition12 = f'{Force_Condition}/W_20m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file34 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file35 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file36 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Tie_W20_HZ40_Mid = rdnumpy(file34)
LK_W20_HZ40_Mid = rdnumpy(file35)
BeamType_W20_HZ40_Mid = rdnumpy(file36)

# ----------------- f = 80HZ --------------------------------
HZ80 = f'HZ_80'
# ============================ SoilWidth = 2.0 m (HZ = 80)=======================================
Condition13 = f'{Force_Condition}/W_2m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file37 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file38 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file39 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Tie_W2_HZ80_Mid = rdnumpy(file37)
LK_W2_HZ80_Mid = rdnumpy(file38)
BeamType_W2_HZ80_Mid = rdnumpy(file39)
# ============================ SoilWidth = 5.0 m (HZ = 80)=======================================
Condition14 = f'{Force_Condition}/W_5m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file40 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file41 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file42 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Tie_W5_HZ80_Mid = rdnumpy(file40)
LK_W5_HZ80_Mid = rdnumpy(file41)
BeamType_W5_HZ80_Mid = rdnumpy(file42)
# ============================ SoilWidth = 10.0 m (HZ = 80)=======================================
Condition15 = f'{Force_Condition}/W_10m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file43 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file44 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file45 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Tie_W10_HZ80_Mid = rdnumpy(file43)
LK_W10_HZ80_Mid = rdnumpy(file44)
BeamType_W10_HZ80_Mid = rdnumpy(file45)
# ============================ SoilWidth = 20.0 m (HZ = 80)=======================================
Condition16 = f'{Force_Condition}/W_20m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file46 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file47 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file48 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Tie_W20_HZ80_Mid = rdnumpy(file46)
LK_W20_HZ80_Mid = rdnumpy(file47)
BeamType_W20_HZ80_Mid = rdnumpy(file48)

def Find_Quarter(soilwidth, YMesh):
    Quarter_RNode = []
    Quarter_LNode = []
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
        Quarter_RNode.append(Top_CenterRight)
        Quarter_LNode.append(Top_CenterLeft)
    # ---------- 80, 40, 20, 10 row -------------------    
    # Away80row = QuarterNode[0]
    # Away40row = QuarterNode[1]
    # Away20row = QuarterNode[2]
    # Away10row = QuarterNode[3]
    # ---------- Only 40 row -------------------
    L_Qua40row = Quarter_LNode[0]
    R_Qua40row = Quarter_RNode[0]
# --------- Vertical/Horizon = R_Qua40row ; Rocking = L_Qua40row  ------------
    return L_Qua40row

W2_Away40row = Find_Quarter(int(2.0), YMesh)
W5_Away40row = Find_Quarter(int(5.0), YMesh)
W10_Away40row = Find_Quarter(int(10.0), YMesh)
W20_Away40row = Find_Quarter(int(20.0), YMesh)
# ============== Read 1m away from Middle Node Analysis Data ==========================================
# ----------------- f = 10HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
# Condition1 = f'{Force_Condition}/W_2m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file49 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file50 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file51 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Tie_W2_HZ10_Away = rdnumpy(file49)
LK_W2_HZ10_Away = rdnumpy(file50)
BeamType_W2_HZ10_Away = rdnumpy(file51)
# ============================ SoilWidth = 5.0 m (HZ = 10)=======================================
# Condition2 = f'{Force_Condition}/W_5m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file52 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file53 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file54 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Tie_W5_HZ10_Away = rdnumpy(file52)
LK_W5_HZ10_Away = rdnumpy(file53)
BeamType_W5_HZ10_Away = rdnumpy(file54)
# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
# Condition3 = f'{Force_Condition}/W_10m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file55 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file56 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file57 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Tie_W10_HZ10_Away = rdnumpy(file55)
LK_W10_HZ10_Away = rdnumpy(file56)
BeamType_W10_HZ10_Away = rdnumpy(file57)
# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
# Condition4 = f'{Force_Condition}/W_20m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file58 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file59 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file60 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Tie_W20_HZ10_Away = rdnumpy(file58)
LK_W20_HZ10_Away = rdnumpy(file59)
BeamType_W20_HZ10_Away = rdnumpy(file60)

# ----------------- f = 20HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 20)=======================================
# Condition5 = f'{Force_Condition}/W_2m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file61 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file62 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file63 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Tie_W2_HZ20_Away = rdnumpy(file61)
LK_W2_HZ20_Away = rdnumpy(file62)
BeamType_W2_HZ20_Away = rdnumpy(file63)
# ============================ SoilWidth = 5.0 m (HZ = 20)=======================================
# Condition6 = f'{Force_Condition}/W_5m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file64 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file65 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file66 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Tie_W5_HZ20_Away = rdnumpy(file64)
LK_W5_HZ20_Away = rdnumpy(file65)
BeamType_W5_HZ20_Away = rdnumpy(file66)
# ============================ SoilWidth = 10.0 m (HZ = 20)=======================================
# Condition7 = f'{Force_Condition}/W_10m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file67 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file68 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file69 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Tie_W10_HZ20_Away = rdnumpy(file67)
LK_W10_HZ20_Away = rdnumpy(file68)
BeamType_W10_HZ20_Away = rdnumpy(file69)
# ============================ SoilWidth = 20.0 m (HZ = 20)=======================================
# Condition8 = f'{Force_Condition}/W_20m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file70 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file71 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file72 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Tie_W20_HZ20_Away = rdnumpy(file70)
LK_W20_HZ20_Away = rdnumpy(file71)
BeamType_W20_HZ20_Away = rdnumpy(file72)

# ----------------- f = 40HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 40)=======================================
# Condition9 = f'{Force_Condition}/W_2m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file73 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file74 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file75 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Tie_W2_HZ40_Away = rdnumpy(file73)
LK_W2_HZ40_Away = rdnumpy(file74)
BeamType_W2_HZ40_Away = rdnumpy(file75)
# ============================ SoilWidth = 5.0 m (HZ = 40)=======================================
# Condition10 = f'{Force_Condition}/W_5m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file76 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file77 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file78 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Tie_W5_HZ40_Away = rdnumpy(file76)
LK_W5_HZ40_Away = rdnumpy(file77)
BeamType_W5_HZ40_Away = rdnumpy(file78)
# ============================ SoilWidth = 10.0 m (HZ = 40)=======================================
# Condition11 = f'{Force_Condition}/W_10m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file79 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file80 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file81 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Tie_W10_HZ40_Away = rdnumpy(file79)
LK_W10_HZ40_Away = rdnumpy(file80)
BeamType_W10_HZ40_Away = rdnumpy(file81)
# ============================ SoilWidth = 20.0 m (HZ = 40)=======================================
# Condition12 = f'{Force_Condition}/W_20m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file82 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file83 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file84 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Tie_W20_HZ40_Away = rdnumpy(file82)
LK_W20_HZ40_Away = rdnumpy(file83)
BeamType_W20_HZ40_Away = rdnumpy(file84)

# ----------------- f = 80HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 80)=======================================
# Condition13 = f'{Force_Condition}/W_2m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file85 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file86 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file87 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Tie_W2_HZ80_Away = rdnumpy(file85)
LK_W2_HZ80_Away = rdnumpy(file86)
BeamType_W2_HZ80_Away = rdnumpy(file87)
# ============================ SoilWidth = 5.0 m (HZ = 80)=======================================
# Condition14 = f'{Force_Condition}/W_5m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file88 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file89 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file90 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Tie_W5_HZ80_Away = rdnumpy(file88)
LK_W5_HZ80_Away = rdnumpy(file89)
BeamType_W5_HZ80_Away = rdnumpy(file90)
# ============================ SoilWidth = 10.0 m (HZ = 80)=======================================
# Condition15 = f'{Force_Condition}/W_10m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file91 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file92 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file93 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Tie_W10_HZ80_Away = rdnumpy(file91)
LK_W10_HZ80_Away = rdnumpy(file92)
BeamType_W10_HZ80_Away = rdnumpy(file93)
# ============================ SoilWidth = 20.0 m (HZ = 80)=======================================
# Condition16 = f'{Force_Condition}/W_20m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file94 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file95 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file96 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Tie_W20_HZ80_Away = rdnumpy(file94)
LK_W20_HZ80_Away = rdnumpy(file95)
BeamType_W20_HZ80_Away = rdnumpy(file96)

# ========= Calculate V Magnitude ==============================
# ================= Middle Node =================
# -------------- f= 10HZ --------------------
Tie_W2_HZ10_Vm = np.zeros((len(Tie_W2_HZ10_Mid), 2))
LK_W2_HZ10_Vm = np.zeros((len(LK_W2_HZ10_Mid), 2))
BeamType_W2_HZ10_Vm = np.zeros((len(BeamType_W2_HZ10_Mid), 2))

Tie_W5_HZ10_Vm = np.zeros((len(Tie_W5_HZ10_Mid), 2))
LK_W5_HZ10_Vm = np.zeros((len(LK_W5_HZ10_Mid), 2))
BeamType_W5_HZ10_Vm = np.zeros((len(BeamType_W5_HZ10_Mid), 2))

Tie_W10_HZ10_Vm = np.zeros((len(Tie_W10_HZ10_Mid), 2))
LK_W10_HZ10_Vm = np.zeros((len(LK_W10_HZ10_Mid), 2))
BeamType_W10_HZ10_Vm = np.zeros((len(BeamType_W10_HZ10_Mid), 2))

Tie_W20_HZ10_Vm = np.zeros((len(Tie_W20_HZ10_Mid), 2))
LK_W20_HZ10_Vm = np.zeros((len(LK_W20_HZ10_Mid), 2))
BeamType_W20_HZ10_Vm = np.zeros((len(BeamType_W20_HZ10_Mid), 2))
# -------------- f= 20HZ --------------------
Tie_W2_HZ20_Vm = np.zeros((len(Tie_W2_HZ20_Mid), 2))
LK_W2_HZ20_Vm = np.zeros((len(LK_W2_HZ20_Mid), 2))
BeamType_W2_HZ20_Vm = np.zeros((len(BeamType_W2_HZ20_Mid), 2))

Tie_W5_HZ20_Vm = np.zeros((len(Tie_W5_HZ20_Mid), 2))
LK_W5_HZ20_Vm = np.zeros((len(LK_W5_HZ20_Mid), 2))
BeamType_W5_HZ20_Vm = np.zeros((len(BeamType_W5_HZ20_Mid), 2))

Tie_W10_HZ20_Vm = np.zeros((len(Tie_W10_HZ20_Mid), 2))
LK_W10_HZ20_Vm = np.zeros((len(LK_W10_HZ20_Mid), 2))
BeamType_W10_HZ20_Vm = np.zeros((len(BeamType_W10_HZ20_Mid), 2))

Tie_W20_HZ20_Vm = np.zeros((len(Tie_W20_HZ20_Mid), 2))
LK_W20_HZ20_Vm = np.zeros((len(LK_W20_HZ20_Mid), 2))
BeamType_W20_HZ20_Vm = np.zeros((len(BeamType_W20_HZ20_Mid), 2))
# -------------- f= 40HZ --------------------
Tie_W2_HZ40_Vm = np.zeros((len(Tie_W2_HZ40_Mid), 2))
LK_W2_HZ40_Vm = np.zeros((len(LK_W2_HZ40_Mid), 2))
BeamType_W2_HZ40_Vm = np.zeros((len(BeamType_W2_HZ40_Mid), 2))

Tie_W5_HZ40_Vm = np.zeros((len(Tie_W5_HZ40_Mid), 2))
LK_W5_HZ40_Vm = np.zeros((len(LK_W5_HZ40_Mid), 2))
BeamType_W5_HZ40_Vm = np.zeros((len(BeamType_W5_HZ40_Mid), 2))

Tie_W10_HZ40_Vm = np.zeros((len(Tie_W10_HZ40_Mid), 2))
LK_W10_HZ40_Vm = np.zeros((len(LK_W10_HZ40_Mid), 2))
BeamType_W10_HZ40_Vm = np.zeros((len(BeamType_W10_HZ40_Mid), 2))

Tie_W20_HZ40_Vm = np.zeros((len(Tie_W20_HZ40_Mid), 2))
LK_W20_HZ40_Vm = np.zeros((len(LK_W20_HZ40_Mid), 2))
BeamType_W20_HZ40_Vm = np.zeros((len(BeamType_W20_HZ40_Mid), 2))
# -------------- f= 80HZ --------------------
Tie_W2_HZ80_Vm = np.zeros((len(Tie_W2_HZ80_Mid), 2))
LK_W2_HZ80_Vm = np.zeros((len(LK_W2_HZ80_Mid), 2))
BeamType_W2_HZ80_Vm = np.zeros((len(BeamType_W2_HZ80_Mid), 2))

Tie_W5_HZ80_Vm = np.zeros((len(Tie_W5_HZ80_Mid), 2))
LK_W5_HZ80_Vm = np.zeros((len(LK_W5_HZ80_Mid), 2))
BeamType_W5_HZ80_Vm = np.zeros((len(BeamType_W5_HZ80_Mid), 2))

Tie_W10_HZ80_Vm = np.zeros((len(Tie_W10_HZ80_Mid), 2))
LK_W10_HZ80_Vm = np.zeros((len(LK_W10_HZ80_Mid), 2))
BeamType_W10_HZ80_Vm = np.zeros((len(BeamType_W10_HZ80_Mid), 2))

Tie_W20_HZ80_Vm = np.zeros((len(Tie_W20_HZ80_Mid), 2))
LK_W20_HZ80_Vm = np.zeros((len(LK_W20_HZ80_Mid), 2))
BeamType_W20_HZ80_Vm = np.zeros((len(BeamType_W20_HZ80_Mid), 2))

# ================== 1m Away from middle point =============================
# -------------- f= 10HZ --------------------
Tie_W2_HZ10_AwayVm = np.zeros((len(Tie_W2_HZ10_Away), 2))
LK_W2_HZ10_AwayVm = np.zeros((len(LK_W2_HZ10_Away), 2))
BeamType_W2_HZ10_AwayVm = np.zeros((len(BeamType_W2_HZ10_Away), 2))

Tie_W5_HZ10_AwayVm = np.zeros((len(Tie_W5_HZ10_Away), 2))
LK_W5_HZ10_AwayVm = np.zeros((len(LK_W5_HZ10_Away), 2))
BeamType_W5_HZ10_AwayVm = np.zeros((len(BeamType_W5_HZ10_Away), 2))

Tie_W10_HZ10_AwayVm = np.zeros((len(Tie_W10_HZ10_Away), 2))
LK_W10_HZ10_AwayVm = np.zeros((len(LK_W10_HZ10_Away), 2))
BeamType_W10_HZ10_AwayVm = np.zeros((len(BeamType_W10_HZ10_Away), 2))

Tie_W20_HZ10_AwayVm = np.zeros((len(Tie_W20_HZ10_Away), 2))
LK_W20_HZ10_AwayVm = np.zeros((len(LK_W20_HZ10_Away), 2))
BeamType_W20_HZ10_AwayVm = np.zeros((len(BeamType_W20_HZ10_Away), 2))
# -------------- f= 20HZ --------------------
Tie_W2_HZ20_AwayVm = np.zeros((len(Tie_W2_HZ20_Away), 2))
LK_W2_HZ20_AwayVm = np.zeros((len(LK_W2_HZ20_Away), 2))
BeamType_W2_HZ20_AwayVm = np.zeros((len(BeamType_W2_HZ20_Away), 2))

Tie_W5_HZ20_AwayVm = np.zeros((len(Tie_W5_HZ20_Away), 2))
LK_W5_HZ20_AwayVm = np.zeros((len(LK_W5_HZ20_Away), 2))
BeamType_W5_HZ20_AwayVm = np.zeros((len(BeamType_W5_HZ20_Away), 2))

Tie_W10_HZ20_AwayVm = np.zeros((len(Tie_W10_HZ20_Away), 2))
LK_W10_HZ20_AwayVm = np.zeros((len(LK_W10_HZ20_Away), 2))
BeamType_W10_HZ20_AwayVm = np.zeros((len(BeamType_W10_HZ20_Away), 2))

Tie_W20_HZ20_AwayVm = np.zeros((len(Tie_W20_HZ20_Away), 2))
LK_W20_HZ20_AwayVm = np.zeros((len(LK_W20_HZ20_Away), 2))
BeamType_W20_HZ20_AwayVm = np.zeros((len(BeamType_W20_HZ20_Away), 2))
# -------------- f= 40HZ --------------------
Tie_W2_HZ40_AwayVm = np.zeros((len(Tie_W2_HZ40_Away), 2))
LK_W2_HZ40_AwayVm = np.zeros((len(LK_W2_HZ40_Away), 2))
BeamType_W2_HZ40_AwayVm = np.zeros((len(BeamType_W2_HZ40_Away), 2))

Tie_W5_HZ40_AwayVm = np.zeros((len(Tie_W5_HZ40_Away), 2))
LK_W5_HZ40_AwayVm = np.zeros((len(LK_W5_HZ40_Away), 2))
BeamType_W5_HZ40_AwayVm = np.zeros((len(BeamType_W5_HZ40_Away), 2))

Tie_W10_HZ40_AwayVm = np.zeros((len(Tie_W10_HZ40_Away), 2))
LK_W10_HZ40_AwayVm = np.zeros((len(LK_W10_HZ40_Away), 2))
BeamType_W10_HZ40_AwayVm = np.zeros((len(BeamType_W10_HZ40_Away), 2))

Tie_W20_HZ40_AwayVm = np.zeros((len(Tie_W20_HZ40_Away), 2))
LK_W20_HZ40_AwayVm = np.zeros((len(LK_W20_HZ40_Away), 2))
BeamType_W20_HZ40_AwayVm = np.zeros((len(BeamType_W20_HZ40_Away), 2))
# -------------- f= 80HZ --------------------
Tie_W2_HZ80_AwayVm = np.zeros((len(Tie_W2_HZ80_Away), 2))
LK_W2_HZ80_AwayVm = np.zeros((len(LK_W2_HZ80_Away), 2))
BeamType_W2_HZ80_AwayVm = np.zeros((len(BeamType_W2_HZ80_Away), 2))

Tie_W5_HZ80_AwayVm = np.zeros((len(Tie_W5_HZ80_Away), 2))
LK_W5_HZ80_AwayVm = np.zeros((len(LK_W5_HZ80_Away), 2))
BeamType_W5_HZ80_AwayVm = np.zeros((len(BeamType_W5_HZ80_Away), 2))

Tie_W10_HZ80_AwayVm = np.zeros((len(Tie_W10_HZ80_Away), 2))
LK_W10_HZ80_AwayVm = np.zeros((len(LK_W10_HZ80_Away), 2))
BeamType_W10_HZ80_AwayVm = np.zeros((len(BeamType_W10_HZ80_Away), 2))

Tie_W20_HZ80_AwayVm = np.zeros((len(Tie_W20_HZ80_Away), 2))
LK_W20_HZ80_AwayVm = np.zeros((len(LK_W20_HZ80_Away), 2))
BeamType_W20_HZ80_AwayVm = np.zeros((len(BeamType_W20_HZ80_Away), 2))

def V_M(v_magnitude, Tie_W10_HZ20_Mid):
    v_magnitude[:,0] = Tie_W10_HZ20_Mid[:,0]
    for i in range(len(Tie_W10_HZ20_Mid)):
        vx = Tie_W10_HZ20_Mid[i, 1]**2
        vy = Tie_W10_HZ20_Mid[i, 2]**2
        v_magnitude[i, 1] = (vx + vy)**(0.5)
        
    return v_magnitude

# ================= Middle Node =================
# ---------- F = 10HZ ----------------
V_M(Tie_W2_HZ10_Vm, Tie_W2_HZ10_Mid)
V_M(LK_W2_HZ10_Vm, LK_W2_HZ10_Mid)
V_M(BeamType_W2_HZ10_Vm, BeamType_W2_HZ10_Mid)

V_M(Tie_W5_HZ10_Vm, Tie_W5_HZ10_Mid)
V_M(LK_W5_HZ10_Vm, LK_W5_HZ10_Mid)
V_M(BeamType_W5_HZ10_Vm, BeamType_W5_HZ10_Mid)

V_M(Tie_W10_HZ10_Vm, Tie_W10_HZ10_Mid)
V_M(LK_W10_HZ10_Vm, LK_W10_HZ10_Mid)
V_M(BeamType_W10_HZ10_Vm, BeamType_W10_HZ10_Mid)

V_M(Tie_W20_HZ10_Vm, Tie_W20_HZ10_Mid)
V_M(LK_W20_HZ10_Vm, LK_W20_HZ10_Mid)
V_M(BeamType_W20_HZ10_Vm, BeamType_W20_HZ10_Mid)
# ---------- F = 20HZ ----------------
V_M(Tie_W2_HZ20_Vm, Tie_W2_HZ20_Mid)
V_M(LK_W2_HZ20_Vm, LK_W2_HZ20_Mid)
V_M(BeamType_W2_HZ20_Vm, BeamType_W2_HZ20_Mid)

V_M(Tie_W5_HZ20_Vm, Tie_W5_HZ20_Mid)
V_M(LK_W5_HZ20_Vm, LK_W5_HZ20_Mid)
V_M(BeamType_W5_HZ20_Vm, BeamType_W5_HZ20_Mid)

V_M(Tie_W10_HZ20_Vm, Tie_W10_HZ20_Mid)
V_M(LK_W10_HZ20_Vm, LK_W10_HZ20_Mid)
V_M(BeamType_W10_HZ20_Vm, BeamType_W10_HZ20_Mid)

V_M(Tie_W20_HZ20_Vm, Tie_W20_HZ20_Mid)
V_M(LK_W20_HZ20_Vm, LK_W20_HZ20_Mid)
V_M(BeamType_W20_HZ20_Vm, BeamType_W20_HZ20_Mid)
# ---------- F = 40HZ ----------------
V_M(Tie_W2_HZ40_Vm, Tie_W2_HZ40_Mid)
V_M(LK_W2_HZ40_Vm, LK_W2_HZ40_Mid)
V_M(BeamType_W2_HZ40_Vm, BeamType_W2_HZ40_Mid)

V_M(Tie_W5_HZ40_Vm, Tie_W5_HZ40_Mid)
V_M(LK_W5_HZ40_Vm, LK_W5_HZ40_Mid)
V_M(BeamType_W5_HZ40_Vm, BeamType_W5_HZ40_Mid)

V_M(Tie_W10_HZ40_Vm, Tie_W10_HZ40_Mid)
V_M(LK_W10_HZ40_Vm, LK_W10_HZ40_Mid)
V_M(BeamType_W10_HZ40_Vm, BeamType_W10_HZ40_Mid)

V_M(Tie_W20_HZ40_Vm, Tie_W20_HZ40_Mid)
V_M(LK_W20_HZ40_Vm, LK_W20_HZ40_Mid)
V_M(BeamType_W20_HZ40_Vm, BeamType_W20_HZ40_Mid)
# ---------- F = 80HZ ----------------
V_M(Tie_W2_HZ80_Vm, Tie_W2_HZ80_Mid)
V_M(LK_W2_HZ80_Vm, LK_W2_HZ80_Mid)
V_M(BeamType_W2_HZ80_Vm, BeamType_W2_HZ80_Mid)

V_M(Tie_W5_HZ80_Vm, Tie_W5_HZ80_Mid)
V_M(LK_W5_HZ80_Vm, LK_W5_HZ80_Mid)
V_M(BeamType_W5_HZ80_Vm, BeamType_W5_HZ80_Mid)

V_M(Tie_W10_HZ80_Vm, Tie_W10_HZ80_Mid)
V_M(LK_W10_HZ80_Vm, LK_W10_HZ80_Mid)
V_M(BeamType_W10_HZ80_Vm, BeamType_W10_HZ80_Mid)

V_M(Tie_W20_HZ80_Vm, Tie_W20_HZ80_Mid)
V_M(LK_W20_HZ80_Vm, LK_W20_HZ80_Mid)
V_M(BeamType_W20_HZ80_Vm, BeamType_W20_HZ80_Mid)

# ================== 1m Away from middle point =============================
# ---------- F = 10HZ ----------------
V_M(Tie_W2_HZ10_AwayVm, Tie_W2_HZ10_Away)
V_M(LK_W2_HZ10_AwayVm, LK_W2_HZ10_Away)
V_M(BeamType_W2_HZ10_AwayVm, BeamType_W2_HZ10_Away)

V_M(Tie_W5_HZ10_AwayVm, Tie_W5_HZ10_Away)
V_M(LK_W5_HZ10_AwayVm, LK_W5_HZ10_Away)
V_M(BeamType_W5_HZ10_AwayVm, BeamType_W5_HZ10_Away)

V_M(Tie_W10_HZ10_AwayVm, Tie_W10_HZ10_Away)
V_M(LK_W10_HZ10_AwayVm, LK_W10_HZ10_Away)
V_M(BeamType_W10_HZ10_AwayVm, BeamType_W10_HZ10_Away)

V_M(Tie_W20_HZ10_AwayVm, Tie_W20_HZ10_Away)
V_M(LK_W20_HZ10_AwayVm, LK_W20_HZ10_Away)
V_M(BeamType_W20_HZ10_AwayVm, BeamType_W20_HZ10_Away)
# ---------- F = 20HZ ----------------
V_M(Tie_W2_HZ20_AwayVm, Tie_W2_HZ20_Away)
V_M(LK_W2_HZ20_AwayVm, LK_W2_HZ20_Away)
V_M(BeamType_W2_HZ20_AwayVm, BeamType_W2_HZ20_Away)

V_M(Tie_W5_HZ20_AwayVm, Tie_W5_HZ20_Away)
V_M(LK_W5_HZ20_AwayVm, LK_W5_HZ20_Away)
V_M(BeamType_W5_HZ20_AwayVm, BeamType_W5_HZ20_Away)

V_M(Tie_W10_HZ20_AwayVm, Tie_W10_HZ20_Away)
V_M(LK_W10_HZ20_AwayVm, LK_W10_HZ20_Away)
V_M(BeamType_W10_HZ20_AwayVm, BeamType_W10_HZ20_Away)

V_M(Tie_W20_HZ20_AwayVm, Tie_W20_HZ20_Away)
V_M(LK_W20_HZ20_AwayVm, LK_W20_HZ20_Away)
V_M(BeamType_W20_HZ20_AwayVm, BeamType_W20_HZ20_Away)
# ---------- F = 40HZ ----------------
V_M(Tie_W2_HZ40_AwayVm, Tie_W2_HZ40_Away)
V_M(LK_W2_HZ40_AwayVm, LK_W2_HZ40_Away)
V_M(BeamType_W2_HZ40_AwayVm, BeamType_W2_HZ40_Away)

V_M(Tie_W5_HZ40_AwayVm, Tie_W5_HZ40_Away)
V_M(LK_W5_HZ40_AwayVm, LK_W5_HZ40_Away)
V_M(BeamType_W5_HZ40_AwayVm, BeamType_W5_HZ40_Away)

V_M(Tie_W10_HZ40_AwayVm, Tie_W10_HZ40_Away)
V_M(LK_W10_HZ40_AwayVm, LK_W10_HZ40_Away)
V_M(BeamType_W10_HZ40_AwayVm, BeamType_W10_HZ40_Away)

V_M(Tie_W20_HZ40_AwayVm, Tie_W20_HZ40_Away)
V_M(LK_W20_HZ40_AwayVm, LK_W20_HZ40_Away)
V_M(BeamType_W20_HZ40_AwayVm, BeamType_W20_HZ40_Away)
# ---------- F = 80HZ ----------------
V_M(Tie_W2_HZ80_AwayVm, Tie_W2_HZ80_Away)
V_M(LK_W2_HZ80_AwayVm, LK_W2_HZ80_Away)
V_M(BeamType_W2_HZ80_AwayVm, BeamType_W2_HZ80_Away)

V_M(Tie_W5_HZ80_AwayVm, Tie_W5_HZ80_Away)
V_M(LK_W5_HZ80_AwayVm, LK_W5_HZ80_Away)
V_M(BeamType_W5_HZ80_AwayVm, BeamType_W5_HZ80_Away)

V_M(Tie_W10_HZ80_AwayVm, Tie_W10_HZ80_Away)
V_M(LK_W10_HZ80_AwayVm, LK_W10_HZ80_Away)
V_M(BeamType_W10_HZ80_AwayVm, BeamType_W10_HZ80_Away)

V_M(Tie_W20_HZ80_AwayVm, Tie_W20_HZ80_Away)
V_M(LK_W20_HZ80_AwayVm, LK_W20_HZ80_Away)
V_M(BeamType_W20_HZ80_AwayVm, BeamType_W20_HZ80_Away)

# # ------- wave put into the timeSeries ---------------
def Differ_BCVel(Tie, LKDash, BeamType1):
    # font_props = {'family': 'Arial', 'size': 12}

    plt.plot(Tie[:,0], Tie[:, 1],label ='Tie', ls = '-',color= 'darkorange',linewidth=6.0)
    plt.plot(LKDash[:,0], LKDash[:, 1],label ='LK Dashpot', ls = '--',color= 'blue',linewidth=5.0)
    plt.plot(BeamType1[:,0], BeamType1[:, 1],label ='Proposed', ls = ':',color= 'red',linewidth=4.0)

    plt.xticks(fontsize = 18) # 18 / 15
    plt.yticks(fontsize = 16)
    plt.xlim(0.0, 0.30)  # 0.0, 0.30 / # Horizon=0.025 / Vertical =0.05
    plt.ylim(-1.1, 1.1)  # Middle = -1.1, 1.1 / 1m away = -0.5, 0.5 ; Rocking = -0.2, 0.2
    plt.grid(True)
    
    ax = plt.gca()
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.019)) # Horizon=0.0025 / Vertical =0.005
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
    # ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    # ax.yaxis.get_offset_text().set(size=16)
    
x_axis = 0.25 # 0.1 0.05 **** 10 Times the x axis ******

# # =============== Middle Node Velocity ======================r"($t_d=0.1$ $\mathrm {s}$)"
# row_heights = [3,3,3]
# fig1, (ax1,ax2,ax3,ax4) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig1.suptitle(f'Different Boundary Compare',x=0.50,y =0.95,fontsize = 20)
# fig1.text(0.44,0.72, "Middle Node", color = "black", fontsize=23)
# fig1.text(0.54,0.85, r"$\mathrm {Horizon}$ ($t_d=0.1$ $\mathrm {s}$)", color = "black", fontsize=22)
# fig1.text(0.01,0.5, r"$\mathrm {Velocity}$  $v_m$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=25)
# fig1.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=25) # $(10^{-1}\,s)$

# ax1 = plt.subplot(411)
# Differ_BCVel(Tie_W20_HZ10_Vm, LK_W20_HZ10_Vm, BeamType_W20_HZ10_Vm)
# ax1.set_title(r"$w=$ $\mathrm{20m}$",fontsize =24, x=0.85, y=0.01)
# # ax1.axvline(x=0.100, color='gray', linestyle='--', linewidth=2) # Vertical = 0.100 / Horizon = 0.0500

# ax2 = plt.subplot(412)
# Differ_BCVel(Tie_W10_HZ10_Vm, LK_W10_HZ10_Vm, BeamType_W10_HZ10_Vm)
# ax2.set_title(r"$w=$ $\mathrm{10m}$",fontsize =24, x=0.85, y=0.01)
# # ax2.axvline(x=0.050, color='gray', linestyle='--', linewidth=2) # Vertical = 0.050 / Horizon = 0.0250

# ax3 = plt.subplot(413)
# Differ_BCVel(Tie_W5_HZ10_Vm, LK_W5_HZ10_Vm, BeamType_W5_HZ10_Vm)
# ax3.set_title(r"$w=$ $\mathrm{5m}$",fontsize =24, x=0.85, y=0.01)
# # ax3.axvline(x=0.025, color='gray', linestyle='--', linewidth=2) # Vertical = 0.025 / Horizon = 0.0125

# ax4 = plt.subplot(414)
# Differ_BCVel(Tie_W2_HZ10_Vm, LK_W2_HZ10_Vm, BeamType_W2_HZ10_Vm)
# ax4.set_title(r"$w=$ $\mathrm{2m}$",fontsize =24, x=0.85, y=0.01)
# # ax4.axvline(x=0.010, color='gray', linestyle='--', linewidth=2) # Vertical = 0.010 / Horizon = 0.0050

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig1.axes[-1].get_legend_handles_labels()
# fig1.legend(lines, labels, ncol=3, loc = (0.2, 0.89),prop=font_props)

# row_heights = [3,3,3]
# fig2, (ax5,ax6,ax7,ax8) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig2.suptitle(f'Different Boundary Compare',x=0.50,y =0.95,fontsize = 20)
# fig2.text(0.44,0.72, "Middle Node", color = "black", fontsize=23)
# fig2.text(0.50,0.85, r"$\mathrm {Horizon}$ ($t_d=0.05$ $\mathrm {s}$)", color = "black", fontsize=22)
# fig2.text(0.01,0.5, r"$\mathrm {Velocity}$  $v_m$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=25)
# fig2.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=25) # $(10^{-1}\,s)$

# ax5 = plt.subplot(411)
# Differ_BCVel(Tie_W20_HZ20_Vm, LK_W20_HZ20_Vm, BeamType_W20_HZ20_Vm)
# ax5.set_title(r"$w=$ $\mathrm{20m}$",fontsize =24, x=0.85, y=0.01)
# # ax5.axvline(x=0.100, color='gray', linestyle='--', linewidth=2)

# ax6 = plt.subplot(412)
# Differ_BCVel(Tie_W10_HZ20_Vm, LK_W10_HZ20_Vm, BeamType_W20_HZ20_Vm)
# ax6.set_title(r"$w=$ $\mathrm{10m}$",fontsize =24, x=0.85, y=0.01)
# # ax6.axvline(x=0.050, color='gray', linestyle='--', linewidth=2)

# ax7 = plt.subplot(413)
# Differ_BCVel(Tie_W5_HZ20_Vm, LK_W5_HZ20_Vm, BeamType_W5_HZ20_Vm)
# ax7.set_title(r"$w=$ $\mathrm{5m}$",fontsize =24, x=0.85, y=0.01)
# # ax7.axvline(x=0.025, color='gray', linestyle='--', linewidth=2)

# ax8 = plt.subplot(414)
# Differ_BCVel(Tie_W2_HZ20_Vm, LK_W2_HZ20_Vm, BeamType_W2_HZ20_Vm)
# ax8.set_title(r"$w=$ $\mathrm{2m}$",fontsize =24, x=0.85, y=0.01)
# # ax8.axvline(x=0.010, color='gray', linestyle='--', linewidth=2)

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig2.axes[-1].get_legend_handles_labels()
# fig2.legend(lines, labels, ncol=3, loc = (0.2, 0.89),prop=font_props)

# row_heights = [3,3,3]
# fig3, (ax9,ax10,aX11,ax12) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig3.suptitle(f'Different Boundary Compare',x=0.50,y =0.95,fontsize = 20)
# fig3.text(0.44,0.72, "Middle Node", color = "black", fontsize=23)
# fig3.text(0.48,0.85, r"$\mathrm {Horizon}$ ($t_d=0.025$ $\mathrm {s}$)", color = "black", fontsize=22)
# fig3.text(0.01,0.5, r"$\mathrm {Velocity}$  $v_m$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=25)
# fig3.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=25) # $(10^{-1}\,s)$

# ax9 = plt.subplot(411)
# Differ_BCVel(Tie_W20_HZ40_Vm, LK_W20_HZ40_Vm, BeamType_W20_HZ40_Vm)
# ax9.set_title(r"$w=$ $\mathrm{20m}$",fontsize =24, x=0.85, y=0.01)
# # ax9.axvline(x=0.100, color='gray', linestyle='--', linewidth=2)

# ax10 = plt.subplot(412)
# Differ_BCVel(Tie_W10_HZ40_Vm, LK_W10_HZ40_Vm, BeamType_W20_HZ40_Vm)
# ax10.set_title(r"$w=$ $\mathrm{10m}$",fontsize =24, x=0.85, y=0.01)
# # ax10.axvline(x=0.050, color='gray', linestyle='--', linewidth=2)

# aX11 = plt.subplot(413)
# Differ_BCVel(Tie_W5_HZ40_Vm, LK_W5_HZ40_Vm, BeamType_W5_HZ40_Vm)
# aX11.set_title(r"$w=$ $\mathrm{5m}$",fontsize =24, x=0.85, y=0.01)
# # aX11.axvline(x=0.025, color='gray', linestyle='--', linewidth=2)

# ax12 = plt.subplot(414)
# Differ_BCVel(Tie_W2_HZ40_Vm, LK_W2_HZ40_Vm, BeamType_W2_HZ40_Vm)
# ax12.set_title(r"$w=$ $\mathrm{2m}$",fontsize =24, x=0.85, y=0.01)
# # ax12.axvline(x=0.010, color='gray', linestyle='--', linewidth=2)

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig3.axes[-1].get_legend_handles_labels()
# fig3.legend(lines, labels, ncol=3, loc = (0.2, 0.89),prop=font_props)

# row_heights = [3,3,3]
# fig4, (ax13,ax14,aX15,ax16) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig4.suptitle(f'Different Boundary Compare',x=0.50,y =0.95,fontsize = 20)
# fig4.text(0.44,0.72, "Middle Node", color = "black", fontsize=23)
# fig4.text(0.46,0.85, r"$\mathrm {Horizon}$ ($t_d=0.0125$ $\mathrm {s}$)", color = "black", fontsize=22)
# fig4.text(0.01,0.5, r"$\mathrm {Velocity}$  $v_m$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=25)
# fig4.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=25) # $(10^{-1}\,s)$

# ax13 = plt.subplot(411)
# Differ_BCVel(Tie_W20_HZ80_Vm, LK_W20_HZ80_Vm, BeamType_W20_HZ80_Vm)
# ax13.set_title(r"$w=$ $\mathrm{20m}$",fontsize =24, x=0.85, y=0.01)
# # ax13.axvline(x=0.100, color='gray', linestyle='--', linewidth=2)

# ax14 = plt.subplot(412)
# Differ_BCVel(Tie_W10_HZ80_Vm, LK_W10_HZ80_Vm, BeamType_W20_HZ80_Vm)
# ax14.set_title(r"$w=$ $\mathrm{10m}$",fontsize =24, x=0.85, y=0.01)
# # ax14.axvline(x=0.050, color='gray', linestyle='--', linewidth=2)

# ax15 = plt.subplot(413)
# Differ_BCVel(Tie_W5_HZ80_Vm, LK_W5_HZ80_Vm, BeamType_W5_HZ80_Vm)
# ax15.set_title(r"$w=$ $\mathrm{5m}$",fontsize =24, x=0.85, y=0.01)
# # ax15.axvline(x=0.0125, color='gray', linestyle='--', linewidth=2)

# ax16 = plt.subplot(414)
# Differ_BCVel(Tie_W2_HZ80_Vm, LK_W2_HZ80_Vm, BeamType_W2_HZ80_Vm)
# ax16.set_title(r"$w=$ $\mathrm{2m}$",fontsize =24, x=0.85, y=0.01)
# # ax16.axvline(x=0.010, color='gray', linestyle='--', linewidth=2)

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig4.axes[-1].get_legend_handles_labels()
# fig4.legend(lines, labels, ncol=3, loc = (0.2, 0.89),prop=font_props)

# # =============== Middle 1m Away Node Velocity ======================
# row_heights = [3,3,3]
# fig5, (ax17,ax18,ax19,ax20) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig5.suptitle(f'Different Boundary Compare',x=0.50,y =0.95,fontsize = 20)
# fig5.text(0.13,0.72, "Node 1 m away from the midpoint", color = "black", fontsize=23)
# fig5.text(0.52,0.85, r"$\mathrm {Horizon}$ ($t_d=0.1$ $\mathrm {s}$)", color = "black", fontsize=22)
# fig5.text(0.01,0.5, r"$\mathrm {Velocity}$  $v_m$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=25)
# fig5.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=25) # $(10^{-1}\,s)$

# ax17 = plt.subplot(411)
# Differ_BCVel(Tie_W20_HZ10_AwayVm, LK_W20_HZ10_AwayVm, BeamType_W20_HZ10_AwayVm)
# ax17.set_title(r"$w=$ $\mathrm{20m}$",fontsize =24, x=0.86, y=0.01)
# # ax17.axvline(x=0.095, color='gray', linestyle='--', linewidth=2) # Vertical = 0.095 / Horizon = 0.0475

# ax18 = plt.subplot(412)
# Differ_BCVel(Tie_W10_HZ10_AwayVm, LK_W10_HZ10_AwayVm, BeamType_W10_HZ10_AwayVm)
# ax18.set_title(r"$w=$ $\mathrm{10m}$",fontsize =24, x=0.86, y=0.01)
# # ax18.axvline(x=0.045, color='gray', linestyle='--', linewidth=2) # Vertical = 0.045 / Horizon = 0.0225

# ax19 = plt.subplot(413)
# Differ_BCVel(Tie_W5_HZ10_AwayVm, LK_W5_HZ10_AwayVm, BeamType_W5_HZ10_AwayVm)
# ax19.set_title(r"$w=$ $\mathrm{5m}$",fontsize =24, x=0.86, y=0.01)
# # ax19.axvline(x=0.020, color='gray', linestyle='--', linewidth=2) # Vertical = 0.020 / Horizon = 0.0100

# ax20 = plt.subplot(414)
# Differ_BCVel(Tie_W2_HZ10_AwayVm, LK_W2_HZ10_AwayVm, BeamType_W2_HZ10_AwayVm)
# ax20.set_title(r"$w=$ $\mathrm{2m}$",fontsize =24, x=0.86, y=0.01)
# # ax20.axvline(x=0.005, color='gray', linestyle='--', linewidth=2) # Vertical = 0.005 / Horizon = 0.0025

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig5.axes[-1].get_legend_handles_labels()
# fig5.legend(lines, labels, ncol=3, loc = (0.2, 0.89),prop=font_props)

# row_heights = [3,3,3]
# fig6, (ax21,ax22,ax23,ax24) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig6.suptitle(f'Different Boundary Compare',x=0.50,y =0.95,fontsize = 20)
# fig6.text(0.13,0.72, "Node 1 m away from the midpoint", color = "black", fontsize=23)
# fig6.text(0.50,0.85, r"$\mathrm {Horizon}$ ($t_d=0.05$ $\mathrm {s}$)", color = "black", fontsize=22)
# fig6.text(0.01,0.5, r"$\mathrm {Velocity}$  $v_m$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=25)
# fig6.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=25) # $(10^{-1}\,s)$

# ax21 = plt.subplot(411)
# Differ_BCVel(Tie_W20_HZ20_AwayVm, LK_W20_HZ20_AwayVm, BeamType_W20_HZ20_AwayVm)
# ax21.set_title(r"$w=$ $\mathrm{20m}$",fontsize =24, x=0.86, y=0.01)
# # ax21.axvline(x=0.095, color='gray', linestyle='--', linewidth=2)

# ax22 = plt.subplot(412)
# Differ_BCVel(Tie_W10_HZ20_AwayVm, LK_W10_HZ20_AwayVm, BeamType_W10_HZ20_AwayVm)
# ax22.set_title(r"$w=$ $\mathrm{10m}$",fontsize =24, x=0.86, y=0.01)
# # ax22.axvline(x=0.045, color='gray', linestyle='--', linewidth=2)

# ax23 = plt.subplot(413)
# Differ_BCVel(Tie_W5_HZ20_AwayVm, LK_W5_HZ20_AwayVm, BeamType_W5_HZ20_AwayVm)
# ax23.set_title(r"$w=$ $\mathrm{5m}$",fontsize =24, x=0.86, y=0.01)
# # ax23.axvline(x=0.020, color='gray', linestyle='--', linewidth=2)

# ax24 = plt.subplot(414)
# Differ_BCVel(Tie_W2_HZ20_AwayVm, LK_W2_HZ20_AwayVm, BeamType_W2_HZ20_AwayVm)
# ax24.set_title(r"$w=$ $\mathrm{2m}$",fontsize =24, x=0.86, y=0.01)
# # ax24.axvline(x=0.005, color='gray', linestyle='--', linewidth=2)

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig6.axes[-1].get_legend_handles_labels()
# fig6.legend(lines, labels, ncol=3, loc = (0.2, 0.89),prop=font_props)

# row_heights = [3,3,3]
# fig7, (ax25,ax26,ax27,ax28) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig7.suptitle(f'Different Boundary Compare',x=0.50,y =0.95,fontsize = 20)
# fig7.text(0.13,0.72, "Node 1 m away from the midpoint", color = "black", fontsize=23)
# fig7.text(0.46,0.85, r"$\mathrm {Horizon}$ ($t_d=0.025$ $\mathrm {s}$)", color = "black", fontsize=22)
# fig7.text(0.01,0.5, r"$\mathrm {Velocity}$  $v_m$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=25)
# fig7.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=25) # $(10^{-1}\,s)$

# ax25 = plt.subplot(411)
# Differ_BCVel(Tie_W20_HZ40_AwayVm, LK_W20_HZ40_AwayVm, BeamType_W20_HZ40_AwayVm)
# ax25.set_title(r"$w=$ $\mathrm{20m}$",fontsize =24, x=0.86, y=0.01)
# # ax25.axvline(x=0.095, color='gray', linestyle='--', linewidth=2)

# ax26 = plt.subplot(412)
# Differ_BCVel(Tie_W10_HZ40_AwayVm, LK_W10_HZ40_AwayVm, BeamType_W10_HZ40_AwayVm)
# ax26.set_title(r"$w=$ $\mathrm{10m}$",fontsize =24, x=0.86, y=0.01)
# # ax26.axvline(x=0.045, color='gray', linestyle='--', linewidth=2)

# ax27 = plt.subplot(413)
# Differ_BCVel(Tie_W5_HZ40_AwayVm, LK_W5_HZ40_AwayVm, BeamType_W5_HZ40_AwayVm)
# ax27.set_title(r"$w=$ $\mathrm{5m}$",fontsize =24, x=0.86, y=0.01)
# # ax27.axvline(x=0.020, color='gray', linestyle='--', linewidth=2)

# ax28 = plt.subplot(414)
# Differ_BCVel(Tie_W2_HZ40_AwayVm, LK_W2_HZ40_AwayVm, BeamType_W2_HZ40_AwayVm)
# ax28.set_title(r"$w=$ $\mathrm{2m}$",fontsize =24, x=0.86, y=0.01)
# # ax28.axvline(x=0.005, color='gray', linestyle='--', linewidth=2)

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig7.axes[-1].get_legend_handles_labels()
# fig7.legend(lines, labels, ncol=3, loc = (0.2, 0.89),prop=font_props)

# row_heights = [3,3,3]
# fig8, (ax29,ax30,ax31,ax32) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig8.suptitle(f'Different Boundary Compare',x=0.50,y =0.95,fontsize = 20)
# fig8.text(0.13,0.72, "Node 1 m away from the midpoint", color = "black", fontsize=23)
# fig8.text(0.44,0.85, r"$\mathrm {Horizon}$ ($t_d=0.0125$ $\mathrm {s}$)", color = "black", fontsize=22)
# fig8.text(0.01,0.5, r"$\mathrm {Velocity}$  $v_m$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=25)
# fig8.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=25) # $(10^{-1}\,s)$

# ax29 = plt.subplot(411)
# Differ_BCVel(Tie_W20_HZ80_AwayVm, LK_W20_HZ80_AwayVm, BeamType_W20_HZ80_AwayVm)
# ax29.set_title(r"$w=$ $\mathrm{20m}$",fontsize =24, x=0.86, y=0.01)
# # ax29.axvline(x=0.095, color='gray', linestyle='--', linewidth=2)

# ax30 = plt.subplot(412)
# Differ_BCVel(Tie_W10_HZ80_AwayVm, LK_W10_HZ80_AwayVm, BeamType_W10_HZ80_AwayVm)
# ax30.set_title(r"$w=$ $\mathrm{10m}$",fontsize =24, x=0.86, y=0.01)
# # ax30.axvline(x=0.045, color='gray', linestyle='--', linewidth=2)

# ax31 = plt.subplot(413)
# Differ_BCVel(Tie_W5_HZ80_AwayVm, LK_W5_HZ80_AwayVm, BeamType_W5_HZ80_AwayVm)
# ax31.set_title(r"$w=$ $\mathrm{5m}$",fontsize =24, x=0.86, y=0.01)
# # ax31.axvline(x=0.020, color='gray', linestyle='--', linewidth=2)

# ax32 = plt.subplot(414)
# Differ_BCVel(Tie_W2_HZ80_AwayVm, LK_W2_HZ80_AwayVm, BeamType_W2_HZ80_AwayVm)
# ax32.set_title(r"$w=$ $\mathrm{2m}$",fontsize =24, x=0.86, y=0.01)
# # ax32.axvline(x=0.005, color='gray', linestyle='--', linewidth=2)

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig8.axes[-1].get_legend_handles_labels()
# fig8.legend(lines, labels, ncol=3, loc = (0.2, 0.89),prop=font_props)

# ================================== Prepare Relative Error ============================
Column_Index = 1 # Vertical or Rocking = 2(yaxis) ; Horizon = 1(xaxis)
def process_column(matrix, Column_Index):
    column = matrix[:, Column_Index]
    abs_column = np.abs(column)
    
    max_index = np.argmax(abs_column)
    max_peak = np.max(abs_column)
    
    print(f'max_value= {max_peak}; max_index= {max_index}')
    return max_peak

# --------------- Middle Node ---------------------
# ----------- f = 10 HZ -------------------------
maxTie2_HZ10 = process_column(Tie_W2_HZ10_Vm, Column_Index)
maxLK2_HZ10 = process_column(LK_W2_HZ10_Vm, Column_Index)
maxBeamType2_HZ10 = process_column(BeamType_W2_HZ10_Vm, Column_Index)

maxTie5_HZ10 = process_column(Tie_W5_HZ10_Vm, Column_Index)
maxLK5_HZ10 = process_column(LK_W5_HZ10_Vm, Column_Index)
maxBeamType5_HZ10 = process_column(BeamType_W5_HZ10_Vm, Column_Index)

maxTie10_HZ10 = process_column(Tie_W10_HZ10_Vm, Column_Index)
maxLK10_HZ10 = process_column(LK_W10_HZ10_Vm, Column_Index)
maxBeamType10_HZ10 = process_column(BeamType_W10_HZ10_Vm, Column_Index)

maxTie20_HZ10 = process_column(Tie_W20_HZ10_Vm, Column_Index)
maxLK20_HZ10 = process_column(LK_W20_HZ10_Vm, Column_Index)
maxBeamType20_HZ10 = process_column(BeamType_W20_HZ10_Vm, Column_Index)
# ----------- f = 20 HZ -------------------------
maxTie2_HZ20 = process_column(Tie_W2_HZ20_Vm, Column_Index)
maxLK2_HZ20 = process_column(LK_W2_HZ20_Vm, Column_Index)
maxBeamType2_HZ20 = process_column(BeamType_W2_HZ20_Vm, Column_Index)

maxTie5_HZ20 = process_column(Tie_W5_HZ20_Vm, Column_Index)
maxLK5_HZ20 = process_column(LK_W5_HZ20_Vm, Column_Index)
maxBeamType5_HZ20 = process_column(BeamType_W5_HZ20_Vm, Column_Index)

maxTie10_HZ20 = process_column(Tie_W10_HZ20_Vm, Column_Index)
maxLK10_HZ20 = process_column(LK_W10_HZ20_Vm, Column_Index)
maxBeamType10_HZ20 = process_column(BeamType_W10_HZ20_Vm, Column_Index)

maxTie20_HZ20 = process_column(Tie_W20_HZ20_Vm, Column_Index)
maxLK20_HZ20 = process_column(LK_W20_HZ20_Vm, Column_Index)
maxBeamType20_HZ20 = process_column(BeamType_W20_HZ20_Vm, Column_Index)
# ----------- f = 40 HZ -------------------------
maxTie2_HZ40 = process_column(Tie_W2_HZ40_Vm, Column_Index)
maxLK2_HZ40 = process_column(LK_W2_HZ40_Vm, Column_Index)
maxBeamType2_HZ40 = process_column(BeamType_W2_HZ40_Vm, Column_Index)

maxTie5_HZ40 = process_column(Tie_W5_HZ40_Vm, Column_Index)
maxLK5_HZ40 = process_column(LK_W5_HZ40_Vm, Column_Index)
maxBeamType5_HZ40 = process_column(BeamType_W5_HZ40_Vm, Column_Index)

maxTie10_HZ40 = process_column(Tie_W10_HZ40_Vm, Column_Index)
maxLK10_HZ40 = process_column(LK_W10_HZ40_Vm, Column_Index)
maxBeamType10_HZ40 = process_column(BeamType_W10_HZ40_Vm, Column_Index)

maxTie20_HZ40 = process_column(Tie_W20_HZ40_Vm, Column_Index)
maxLK20_HZ40 = process_column(LK_W20_HZ40_Vm, Column_Index)
maxBeamType20_HZ40 = process_column(BeamType_W20_HZ40_Vm, Column_Index)
# ----------- f = 80 HZ -------------------------
maxTie2_HZ80 = process_column(Tie_W2_HZ80_Vm, Column_Index)
maxLK2_HZ80 = process_column(LK_W2_HZ80_Vm, Column_Index)
maxBeamType2_HZ80 = process_column(BeamType_W2_HZ80_Vm, Column_Index)

maxTie5_HZ80 = process_column(Tie_W5_HZ80_Vm, Column_Index)
maxLK5_HZ80 = process_column(LK_W5_HZ80_Vm, Column_Index)
maxBeamType5_HZ80 = process_column(BeamType_W5_HZ80_Vm, Column_Index)

maxTie10_HZ80 = process_column(Tie_W10_HZ80_Vm, Column_Index)
maxLK10_HZ80 = process_column(LK_W10_HZ80_Vm, Column_Index)
maxBeamType10_HZ80 = process_column(BeamType_W10_HZ80_Vm, Column_Index)

maxTie20_HZ80 = process_column(Tie_W20_HZ80_Vm, Column_Index)
maxLK20_HZ80 = process_column(LK_W20_HZ80_Vm, Column_Index)
maxBeamType20_HZ80 = process_column(BeamType_W20_HZ80_Vm, Column_Index)

# ========================  1m away from Middle Node ==============================
# ----------- f = 10 HZ -------------------------
maxTie2_HZ10_Away = process_column(Tie_W2_HZ10_AwayVm, Column_Index)
maxLK2_HZ10_Away = process_column(LK_W2_HZ10_AwayVm, Column_Index)
maxBeamType2_HZ10_Away = process_column(BeamType_W2_HZ10_AwayVm, Column_Index)

maxTie5_HZ10_Away = process_column(Tie_W5_HZ10_AwayVm, Column_Index)
maxLK5_HZ10_Away = process_column(LK_W5_HZ10_AwayVm, Column_Index)
maxBeamType5_HZ10_Away = process_column(BeamType_W5_HZ10_AwayVm, Column_Index)

maxTie10_HZ10_Away = process_column(Tie_W10_HZ10_AwayVm, Column_Index)
maxLK10_HZ10_Away = process_column(LK_W10_HZ10_AwayVm, Column_Index)
maxBeamType10_HZ10_Away = process_column(BeamType_W10_HZ10_AwayVm, Column_Index)

maxTie20_HZ10_Away = process_column(Tie_W20_HZ10_AwayVm, Column_Index)
maxLK20_HZ10_Away = process_column(LK_W20_HZ10_AwayVm, Column_Index)
maxBeamType20_HZ10_Away = process_column(BeamType_W20_HZ10_AwayVm, Column_Index)
# ----------- f = 20 HZ -------------------------
maxTie2_HZ20_Away = process_column(Tie_W2_HZ20_AwayVm, Column_Index)
maxLK2_HZ20_Away = process_column(LK_W2_HZ20_AwayVm, Column_Index)
maxBeamType2_HZ20_Away = process_column(BeamType_W2_HZ20_AwayVm, Column_Index)

maxTie5_HZ20_Away = process_column(Tie_W5_HZ20_AwayVm, Column_Index)
maxLK5_HZ20_Away = process_column(LK_W5_HZ20_AwayVm, Column_Index)
maxBeamType5_HZ20_Away = process_column(BeamType_W5_HZ20_AwayVm, Column_Index)

maxTie10_HZ20_Away = process_column(Tie_W10_HZ20_AwayVm, Column_Index)
maxLK10_HZ20_Away = process_column(LK_W10_HZ20_AwayVm, Column_Index)
maxBeamType10_HZ20_Away = process_column(BeamType_W10_HZ20_AwayVm, Column_Index)

maxTie20_HZ20_Away = process_column(Tie_W20_HZ20_AwayVm, Column_Index)
maxLK20_HZ20_Away = process_column(LK_W20_HZ20_AwayVm, Column_Index)
maxBeamType20_HZ20_Away = process_column(BeamType_W20_HZ20_AwayVm, Column_Index)
# ----------- f = 40 HZ -------------------------
maxTie2_HZ40_Away = process_column(Tie_W2_HZ40_AwayVm, Column_Index)
maxLK2_HZ40_Away = process_column(LK_W2_HZ40_AwayVm, Column_Index)
maxBeamType2_HZ40_Away = process_column(BeamType_W2_HZ40_AwayVm, Column_Index)

maxTie5_HZ40_Away = process_column(Tie_W5_HZ40_AwayVm, Column_Index)
maxLK5_HZ40_Away = process_column(LK_W5_HZ40_AwayVm, Column_Index)
maxBeamType5_HZ40_Away = process_column(BeamType_W5_HZ40_AwayVm, Column_Index)

maxTie10_HZ40_Away = process_column(Tie_W10_HZ40_AwayVm, Column_Index)
maxLK10_HZ40_Away = process_column(LK_W10_HZ40_AwayVm, Column_Index)
maxBeamType10_HZ40_Away = process_column(BeamType_W10_HZ40_AwayVm, Column_Index)

maxTie20_HZ40_Away = process_column(Tie_W20_HZ40_AwayVm, Column_Index)
maxLK20_HZ40_Away = process_column(LK_W20_HZ40_AwayVm, Column_Index)
maxBeamType20_HZ40_Away = process_column(BeamType_W20_HZ40_AwayVm, Column_Index)
# ----------- f = 80 HZ -------------------------
maxTie2_HZ80_Away = process_column(Tie_W2_HZ80_AwayVm, Column_Index)
maxLK2_HZ80_Away = process_column(LK_W2_HZ80_AwayVm, Column_Index)
maxBeamType2_HZ80_Away = process_column(BeamType_W2_HZ80_AwayVm, Column_Index)

maxTie5_HZ80_Away = process_column(Tie_W5_HZ80_AwayVm, Column_Index)
maxLK5_HZ80_Away = process_column(LK_W5_HZ80_AwayVm, Column_Index)
maxBeamType5_HZ80_Away = process_column(BeamType_W5_HZ80_AwayVm, Column_Index)

maxTie10_HZ80_Away = process_column(Tie_W10_HZ80_AwayVm, Column_Index)
maxLK10_HZ80_Away = process_column(LK_W10_HZ80_AwayVm, Column_Index)
maxBeamType10_HZ80_Away = process_column(BeamType_W10_HZ80_AwayVm, Column_Index)

maxTie20_HZ80_Away = process_column(Tie_W20_HZ80_AwayVm, Column_Index)
maxLK20_HZ80_Away = process_column(LK_W20_HZ80_AwayVm, Column_Index)
maxBeamType20_HZ80_Away = process_column(BeamType_W20_HZ80_AwayVm, Column_Index)

Frequency_Size = np.array([1/10, 1/20, 1/40, 1/80])

def errMatrix(error_dc, maxTie2_HZ10, maxTie2_HZ20, maxTie2_HZ40, maxTie2_HZ80):
    error_dc[:,0] = Frequency_Size[:]
    error_dc[0,1] = maxTie2_HZ10
    error_dc[1,1] = maxTie2_HZ20
    error_dc[2,1] = maxTie2_HZ40
    error_dc[3,1] = maxTie2_HZ80
    return error_dc

# ============================= Middle Node ========================================
# ------------W20m Error Peak Value-----------------------
Tie20_error = np.zeros((len(Frequency_Size),2))
errMatrix(Tie20_error, maxTie20_HZ10, maxTie20_HZ20, maxTie20_HZ40, maxTie20_HZ80)

LK20_error = np.zeros((len(Frequency_Size),2))
errMatrix(LK20_error, maxLK20_HZ10, maxLK20_HZ20, maxLK20_HZ40, maxLK20_HZ80)

BeamType_20error = np.zeros((len(Frequency_Size),2))
errMatrix(BeamType_20error, maxBeamType20_HZ10, maxBeamType20_HZ20, maxBeamType20_HZ40, maxBeamType20_HZ80)
# ------------W10m Error Peak Value-----------------------
Tie10_error = np.zeros((len(Frequency_Size),2))
errMatrix(Tie10_error, maxTie10_HZ10, maxTie10_HZ20, maxTie10_HZ40, maxTie10_HZ80)

LK10_error = np.zeros((len(Frequency_Size),2))
errMatrix(LK10_error, maxLK10_HZ10, maxLK10_HZ20, maxLK10_HZ40, maxLK10_HZ80)

BeamType_10error = np.zeros((len(Frequency_Size),2))
errMatrix(BeamType_10error, maxBeamType10_HZ10, maxBeamType10_HZ20, maxBeamType10_HZ40, maxBeamType10_HZ80)
# ------------W5m Error Peak Value-----------------------
Tie5_error = np.zeros((len(Frequency_Size),2))
errMatrix(Tie5_error, maxTie5_HZ10, maxTie5_HZ20, maxTie5_HZ40, maxTie5_HZ80)

LK5_error = np.zeros((len(Frequency_Size),2))
errMatrix(LK5_error, maxLK5_HZ10, maxLK5_HZ20, maxLK5_HZ40, maxLK5_HZ80)

BeamType_5error = np.zeros((len(Frequency_Size),2))
errMatrix(BeamType_5error, maxBeamType5_HZ10, maxBeamType5_HZ20, maxBeamType5_HZ40, maxBeamType5_HZ80)
# ------------W2m Error Peak Value-----------------------
Tie2_error = np.zeros((len(Frequency_Size),2))
errMatrix(Tie2_error, maxTie2_HZ10, maxTie2_HZ20, maxTie2_HZ40, maxTie2_HZ80)

LK2_error = np.zeros((len(Frequency_Size),2))
errMatrix(LK2_error, maxLK2_HZ10, maxLK2_HZ20, maxLK2_HZ40, maxLK2_HZ80)

BeamType_2error = np.zeros((len(Frequency_Size),2))
errMatrix(BeamType_2error, maxBeamType2_HZ10, maxBeamType2_HZ20, maxBeamType2_HZ40, maxBeamType2_HZ80)

# ========================  1m away from Middle Node ==============================
# ------------W20m Error Peak Value-----------------------
Tie20_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Tie20_error_Away, maxTie20_HZ10_Away, maxTie20_HZ20_Away, maxTie20_HZ40_Away, maxTie20_HZ80_Away)

LK20_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(LK20_error_Away, maxLK20_HZ10_Away, maxLK20_HZ20_Away, maxLK20_HZ40_Away, maxLK20_HZ80_Away)

BeamType_20error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(BeamType_20error_Away, maxBeamType20_HZ10_Away, maxBeamType20_HZ20_Away, maxBeamType20_HZ40_Away, maxBeamType20_HZ80_Away)
# ------------W10m Error Peak Value-----------------------
Tie10_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Tie10_error_Away, maxTie10_HZ10_Away, maxTie10_HZ20_Away, maxTie10_HZ40_Away, maxTie10_HZ80_Away)

LK10_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(LK10_error_Away, maxLK10_HZ10_Away, maxLK10_HZ20_Away, maxLK10_HZ40_Away, maxLK10_HZ80_Away)

BeamType_10error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(BeamType_10error_Away, maxBeamType10_HZ10_Away, maxBeamType10_HZ20_Away, maxBeamType10_HZ40_Away, maxBeamType10_HZ80_Away)
# ------------W5m Error Peak Value-----------------------
Tie5_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Tie5_error_Away, maxTie5_HZ10_Away, maxTie5_HZ20_Away, maxTie5_HZ40_Away, maxTie5_HZ80_Away)

LK5_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(LK5_error_Away, maxLK5_HZ10_Away, maxLK5_HZ20_Away, maxLK5_HZ40_Away, maxLK5_HZ80_Away)

BeamType_5error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(BeamType_5error_Away, maxBeamType5_HZ10_Away, maxBeamType5_HZ20_Away, maxBeamType5_HZ40_Away, maxBeamType5_HZ80_Away)
# ------------W2m Error Peak Value-----------------------
Tie2_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Tie2_error_Away, maxTie2_HZ10_Away, maxTie2_HZ20_Away, maxTie2_HZ40_Away, maxTie2_HZ80_Away)

LK2_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(LK2_error_Away, maxLK2_HZ10_Away, maxLK2_HZ20_Away, maxLK2_HZ40_Away, maxLK2_HZ80_Away)

BeamType_2error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(BeamType_2error_Away, maxBeamType2_HZ10_Away, maxBeamType2_HZ20_Away, maxBeamType2_HZ40_Away, maxBeamType2_HZ80_Away)

#  ---------- Calculate Relative Error ----------------------------
# ---------- Middle Node -------------
Tie20_err = np.zeros((len(Frequency_Size),2))
LK20_err = np.zeros((len(Frequency_Size),2))
BeamType_20err = np.zeros((len(Frequency_Size),2))

Tie10_err = np.zeros((len(Frequency_Size),2))
LK10_err = np.zeros((len(Frequency_Size),2))
BeamType_10err = np.zeros((len(Frequency_Size),2))

Tie5_err = np.zeros((len(Frequency_Size),2))
LK5_err = np.zeros((len(Frequency_Size),2))
BeamType_5err = np.zeros((len(Frequency_Size),2))

Tie2_err = np.zeros((len(Frequency_Size),2))
LK2_err = np.zeros((len(Frequency_Size),2))
BeamType_2err = np.zeros((len(Frequency_Size),2))

# ---------- 1m away from middle Node -------------
Tie20_err_Away = np.zeros((len(Frequency_Size),2))
LK20_err_Away = np.zeros((len(Frequency_Size),2))
BeamType_20err_Away = np.zeros((len(Frequency_Size),2))

Tie10_err_Away = np.zeros((len(Frequency_Size),2))
LK10_err_Away = np.zeros((len(Frequency_Size),2))
BeamType_10err_Away = np.zeros((len(Frequency_Size),2))

Tie5_err_Away = np.zeros((len(Frequency_Size),2))
LK5_err_Away = np.zeros((len(Frequency_Size),2))
BeamType_5err_Away = np.zeros((len(Frequency_Size),2))

Tie2_err_Away = np.zeros((len(Frequency_Size),2))
LK2_err_Away = np.zeros((len(Frequency_Size),2))
BeamType_2err_Away = np.zeros((len(Frequency_Size),2))

#-------------- Use LK Dashpot as Analysis theory solution ------------------------
maxAnaly_HZ10 = maxLK20_HZ10
maxAnaly_HZ20 = maxLK20_HZ20
maxAnaly_HZ40 = maxLK20_HZ40
maxAnaly_HZ80 = maxLK20_HZ80

maxAnaly_HZ10_Away = maxLK20_HZ10_Away
maxAnaly_HZ20_Away = maxLK20_HZ20_Away
maxAnaly_HZ40_Away = maxLK20_HZ40_Away
maxAnaly_HZ80_Away = maxLK20_HZ80_Away

def Calculate_Error(TieErr, Tie_error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80):
    TieErr[:,0] = Tie_error[:,0]
# ------------------------- Absolute Relative Error ------------------        
    TieErr[0,1] = ((Tie_error[0,1] - maxAnaly_HZ10)/maxAnaly_HZ10)*100
    TieErr[1,1] = ((Tie_error[1,1] - maxAnaly_HZ20)/maxAnaly_HZ20)*100
    TieErr[2,1] = ((Tie_error[2,1] - maxAnaly_HZ40)/maxAnaly_HZ40)*100
    TieErr[3,1] = ((Tie_error[3,1] - maxAnaly_HZ80)/maxAnaly_HZ80)*100
    
# ----------- Middle Node -----------------
Calculate_Error(Tie20_err, Tie20_error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80)
Calculate_Error(LK20_err, LK20_error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80) # *****
Calculate_Error(BeamType_20err, BeamType_20error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80)

Calculate_Error(Tie10_err, Tie10_error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80)
Calculate_Error(LK10_err, LK10_error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80)
Calculate_Error(BeamType_10err, BeamType_10error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80)

Calculate_Error(Tie5_err, Tie5_error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80)
Calculate_Error(LK5_err, LK5_error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80)
Calculate_Error(BeamType_5err, BeamType_5error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80)

Calculate_Error(Tie2_err, Tie2_error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80)
Calculate_Error(LK2_err, LK2_error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80)
Calculate_Error(BeamType_2err, BeamType_2error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80)

# ---------- 1m away from middle Node -------------
Calculate_Error(Tie20_err_Away, Tie20_error_Away, maxAnaly_HZ10_Away, maxAnaly_HZ20_Away, maxAnaly_HZ40_Away, maxAnaly_HZ80_Away)
Calculate_Error(LK20_err_Away, LK20_error_Away, maxAnaly_HZ10_Away, maxAnaly_HZ20_Away, maxAnaly_HZ40_Away, maxAnaly_HZ80_Away) # *****
Calculate_Error(BeamType_20err_Away, BeamType_20error_Away, maxAnaly_HZ10_Away, maxAnaly_HZ20_Away, maxAnaly_HZ40_Away, maxAnaly_HZ80_Away)

Calculate_Error(Tie10_err_Away, Tie10_error_Away, maxAnaly_HZ10_Away, maxAnaly_HZ20_Away, maxAnaly_HZ40_Away, maxAnaly_HZ80_Away)
Calculate_Error(LK10_err_Away, LK10_error_Away, maxAnaly_HZ10_Away, maxAnaly_HZ20_Away, maxAnaly_HZ40_Away, maxAnaly_HZ80_Away) 
Calculate_Error(BeamType_10err_Away, BeamType_10error_Away, maxAnaly_HZ10_Away, maxAnaly_HZ20_Away, maxAnaly_HZ40_Away, maxAnaly_HZ80_Away)

Calculate_Error(Tie5_err_Away, Tie5_error_Away, maxAnaly_HZ10_Away, maxAnaly_HZ20_Away, maxAnaly_HZ40_Away, maxAnaly_HZ80_Away)
Calculate_Error(LK5_err_Away, LK5_error_Away, maxAnaly_HZ10_Away, maxAnaly_HZ20_Away, maxAnaly_HZ40_Away, maxAnaly_HZ80_Away) 
Calculate_Error(BeamType_5err_Away, BeamType_5error_Away, maxAnaly_HZ10_Away, maxAnaly_HZ20_Away, maxAnaly_HZ40_Away, maxAnaly_HZ80_Away)

Calculate_Error(Tie2_err_Away, Tie2_error_Away, maxAnaly_HZ10_Away, maxAnaly_HZ20_Away, maxAnaly_HZ40_Away, maxAnaly_HZ80_Away)
Calculate_Error(LK2_err_Away, LK2_error_Away, maxAnaly_HZ10_Away, maxAnaly_HZ20_Away, maxAnaly_HZ40_Away, maxAnaly_HZ80_Away) 
Calculate_Error(BeamType_2err_Away, BeamType_2error_Away, maxAnaly_HZ10_Away, maxAnaly_HZ20_Away, maxAnaly_HZ40_Away, maxAnaly_HZ80_Away)

# ==================Draw Relative error : td (1/HZ)=============================
def DifferTime_RelativeError(Peak,TieErr, LKErr, Type1Err):
    # font_props = {'family': 'Arial', 'size': 14}
    # plt.plot(TieErr[:,0], TieErr[:,Peak],marker = '^',markersize=12,markerfacecolor = 'white',label = 'Tie')
    plt.plot(LKErr[:,0], LKErr[:,Peak],marker = 'o',markersize=12,markerfacecolor = 'white',label = 'LK Dashpot', color='blue',linewidth = 4.0)
    plt.plot(Type1Err[:,0], Type1Err[:,Peak],marker = '<',markersize=12,markerfacecolor = 'white',label = 'Proposed', color='red',linewidth = 2.0)

    # plt.legend(loc='center left',prop=font_props) #ncol=2,fontsize=16 frameon=False
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
# --- Horizon= Mid(-25, 25)/ Away=(-25,100); Vertical = Mid(-5, 5)/ Away=(-30,10); Rocking: -110, 50(with Tie) / -30, 30/110 (no Tie)
    # plt.ylim(-30, 110)  # Middle = -10, 10 / 1m away = -10, 10 ;Horizon = -30, 30
    plt.grid(True)
    
    ax = plt.gca()
    # -------------- Consider X-axis  -----------------------
    ax.set_xscale('log', base=10)
    ax.set_xticks([], minor=False)
    ax.set_xticks([], minor=True)
    x_ticks_Num = np.array([0.01, 0.02, 0.04, 0.06, 0.08, 0.1])  # td = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1] ; Dy/lamb = []
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.2f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='both', labelsize=20)
    # ------- Miner ticks -----------------
    ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='x', which='minor', length=4, color='gray')
    
    # # -------------- Consider Y-axis  -----------------------
    # ax.set_yscale('log', base=10)
    # ax.set_yticks([], minor=False)
    # ax.set_yticks([], minor=True)
    # y_ticks_Num = np.array([0.02, 0.04, 0.06, 0.08, 0.20, 0.40, 0.60])
    # ax.set_yticks(y_ticks_Num)
    # ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks_Num], rotation=0, fontsize=12)
    # ax.tick_params(axis='y', which='both', labelsize=17)
    # # ------- Miner ticks -----------------
    # ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    # ax.yaxis.set_minor_formatter(NullFormatter())
    # ax.tick_params(axis='y', which='minor', length=4, color='gray')

# # ----------------- Middle Node Relative Error -------------------------
figsize = (10, 10)
# # ----------------- Draw Relative error : td (1/HZ) ------------------- 
# fig9, (ax33,ax34,ax35,ax36) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# # fig9.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig9.text(0.13,0.82, "(Middle Node)", color = "black", fontsize=22)
# fig9.text(0.16,0.85, r"$\mathrm {Horizon}$", color = "black", fontsize=22)

# fig9.text(0.02,0.5, 'Peak Velocity Error '+ r"$\ E^{0~0.2s}_{Max}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=25)
# fig9.text(0.41,0.060,  f'Duration ' + r'$t_d$', va= 'center', fontsize=20)

# ax33 = plt.subplot(411)
# DifferTime_RelativeError(1, Tie20_err, LK20_err, BeamType_20err)
# ax33.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.80, y=0.75)

# ax34 = plt.subplot(412)
# DifferTime_RelativeError(1, Tie10_err, LK10_err, BeamType_10err)
# ax34.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.80, y=0.75)

# ax35 = plt.subplot(413)
# DifferTime_RelativeError(1, Tie5_err, LK5_err, BeamType_5err)
# ax35.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.80, y=0.75)

# ax36 = plt.subplot(414)
# DifferTime_RelativeError(1, Tie2_err, LK2_err, BeamType_2err)
# ax36.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.80, y=0.75)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting

# lines, labels = fig9.axes[-1].get_legend_handles_labels()
# fig9.legend(lines, labels, ncol=2, loc = (0.3, 0.89) ,prop=font_props)

# fig10, (ax37,ax38,ax39,ax40) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# # fig10.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig10.text(0.14,0.82, "(Node 1 m away from the midpoint)", color = "black", fontsize=22)
# fig10.text(0.27,0.85, r"$\mathrm {Horizon}$", color = "black", fontsize=23)

# fig10.text(0.02,0.5, 'Peak Velocity Error '+ r"$\ E^{0~0.2s}_{Max}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=25)
# fig10.text(0.41,0.060,  f'Duration ' + r'$t_d$', va= 'center', fontsize= 25)

# ax37 = plt.subplot(411)
# DifferTime_RelativeError(1, Tie20_err_Away, LK20_err_Away, BeamType_20err_Away)
# ax37.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.85, y=0.80)

# ax38 = plt.subplot(412)
# DifferTime_RelativeError(1, Tie10_err_Away, LK10_err_Away, BeamType_10err_Away)
# ax38.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.85, y=0.80)

# ax39 = plt.subplot(413)
# DifferTime_RelativeError(1, Tie5_err_Away, LK5_err_Away, BeamType_5err_Away)
# ax39.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.85, y=0.10)

# ax40 = plt.subplot(414)
# DifferTime_RelativeError(1, Tie2_err_Away, LK2_err_Away, BeamType_2err_Away)
# ax40.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.85, y=0.10)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting

# lines, labels = fig10.axes[-1].get_legend_handles_labels()
# fig10.legend(lines, labels, ncol=2, loc = (0.30,0.89) ,prop=font_props)

def Tie_RelativeError(TieErr2, TieErr5, TieErr10, TieErr20):
    plt.figure(figsize=(10, 8))
    font_props = {'family': 'Arial', 'size': 16}
    plt.text(0.02, 0.90,'Horizon', color='black', fontsize = 28, transform=plt.gca().transAxes)
    plt.text(0.05, 0.82,'Tie', color='black', fontsize = 30, transform=plt.gca().transAxes)
    plt.xlabel(f'Duration ' + r'$t_d$', fontsize = 25)
    plt.ylabel('Peak Velocity Error '+ r"$\ E^{0~0.2s}_{Max}$" + r" (%)", fontsize = 25)

    plt.plot(TieErr2[:,0], TieErr2[:,1],marker = '^',markersize=12,markerfacecolor = 'white',label = r"$w=$ $\mathrm{2m}$", color='darkgrey',linewidth = 6.0)
    plt.plot(TieErr5[:,0], TieErr5[:,1],marker = 'o',markersize=12,markerfacecolor = 'white',label = r"$w=$ $\mathrm{5m}$", color='blue',linewidth = 5.0)
    plt.plot(TieErr10[:,0], TieErr10[:,1],marker = '<',markersize=12,markerfacecolor = 'white',label = r"$w=$ $\mathrm{10m}$", color='darkgreen',linewidth = 4.0)
    plt.plot(TieErr20[:,0], TieErr20[:,1],marker = '*',markersize=12,markerfacecolor = 'white',label = r"$w=$ $\mathrm{20m}$", color='red',linewidth = 3.0)

    plt.legend(ncol= 4, bbox_to_anchor= (0.02, 1.09), loc='upper left', prop=font_props) 
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
# --- Horizon= Mid(-25, 100)/ Away=(-30,220); Vertical = Mid(-30, 15)/ Away=(-30,110); Rocking: -110, 60(with Tie) / -30, 30 (no Tie)
    plt.ylim(-30, 220)  # Middle = -10, 10 / 1m away = -10, 10 ;Horizon = -30, 30
    plt.grid(True)
    
    ax = plt.gca()
    # -------------- Consider X-axis  -----------------------
    ax.set_xscale('log', base=10)
    ax.set_xticks([], minor=False)
    ax.set_xticks([], minor=True)
    x_ticks_Num = np.array([0.01, 0.02, 0.04, 0.06, 0.08, 0.1])  # td = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1] ; Dy/lamb = []
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.2f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='both', labelsize=20)
    # ------- Miner ticks -----------------
    ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='x', which='minor', length=4, color='gray')

# Tie_RelativeError(Tie2_err, Tie5_err, Tie10_err, Tie20_err)
# Tie_RelativeError(Tie2_err_Away, Tie5_err_Away, Tie10_err_Away, Tie20_err_Away)   

# ================================== Prepare L2-Norm Error ============================
# ---------- Find Different Data in 40 row Same Time ---------------------
Analysis_Time = LK_W20_HZ40_Mid[:, 0]
Theory_Time = Tie_W20_HZ40_Mid[:, 0]

# ================= Calculate_2NormError Normalization ===============================
def Calculate_RelativeL2norm(TheoryTime,TheoryData, Analysis_Time,Tie_W20_HZ40_Mid, time_range=(0, 0.20)):
# ------------------------- L-2 Norm Error ------------------------
    common80 = set(TheoryTime) & set(Analysis_Time)
    filtered_common80 = [value for value in common80 if time_range[0] <= value <= time_range[1]]
    
    differences = []
    Mom = []

    for common_value in common80:
        index1 = np.where(Analysis_Time == common_value)[0][0]
        index2 = np.where(TheoryTime == common_value)[0][0]

        diff = (Tie_W20_HZ40_Mid[index1, Column_Index] - TheoryData[index2, Column_Index])
        differences.append(diff)
        
        Mother =  TheoryData[index2, Column_Index]
        Mom.append(Mother)
        
# ------------- numerator and denominator seperate calculate -------------------- 
    compare = np.array(differences)
    Momm = np.array(Mom)
# ------------- numerator and denominator seperate Square --------------------    
    squared_values = np.square(compare)
    squared_value2 = np.square(Momm)
    
    sum_of_squares = np.sum(squared_values)
    sum_of_square2 = np.sum(squared_value2)
    result = np.sqrt((sum_of_squares)/sum_of_square2)
    
    return result, len(compare)

def Add_Err(Index, MidTieErr20,Tie20_error, Tie_W20_HZ10_Mid, Tie_W20_HZ20_Mid, Tie_W20_HZ40_Mid, Tie_W20_HZ80_Mid):
    MidTieErr20[:,0] = Tie20_error[:,0] 
# ===================================== Calculate_L2NormError Normalization : Middle Node============================================================
    MidTieErr20[0,Index], MidTieErr20[0,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ10_Mid, Analysis_Time,Tie_W20_HZ10_Mid, time_range=(0, 0.20))
    MidTieErr20[1,Index], MidTieErr20[1,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ20_Mid, Analysis_Time,Tie_W20_HZ20_Mid, time_range=(0, 0.20))
    MidTieErr20[2,Index], MidTieErr20[2,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ40_Mid, Analysis_Time,Tie_W20_HZ40_Mid, time_range=(0, 0.20))
    MidTieErr20[3,Index], MidTieErr20[3,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ80_Mid, Analysis_Time,Tie_W20_HZ80_Mid, time_range=(0, 0.20))

# -------------- W = 20m-------------------------------
Tie20Err_L2 = np.zeros((4,3))
Add_Err(1, Tie20Err_L2,Tie20_error, Tie_W20_HZ10_Mid, Tie_W20_HZ20_Mid, Tie_W20_HZ40_Mid, Tie_W20_HZ80_Mid)

LK20Err_L2 = np.zeros((4,3))
Add_Err(1, LK20Err_L2,LK20_error, LK_W20_HZ10_Mid, LK_W20_HZ20_Mid, LK_W20_HZ40_Mid, LK_W20_HZ80_Mid)

BeamType_W20Err_L2 = np.zeros((4,3))
Add_Err(1, BeamType_W20Err_L2, BeamType_20error, BeamType_W20_HZ10_Mid, BeamType_W20_HZ20_Mid, BeamType_W20_HZ40_Mid, BeamType_W20_HZ80_Mid)
# -------------- W = 10m-------------------------------
Tie10Err_L2 = np.zeros((4,3))
Add_Err(1, Tie10Err_L2,Tie10_error, Tie_W10_HZ10_Mid, Tie_W10_HZ20_Mid, Tie_W10_HZ40_Mid, Tie_W10_HZ80_Mid)

LK10Err_L2 = np.zeros((4,3))
Add_Err(1, LK10Err_L2,LK10_error, LK_W10_HZ10_Mid, LK_W10_HZ20_Mid, LK_W10_HZ40_Mid, LK_W10_HZ80_Mid)

BeamType_W10Err_L2 = np.zeros((4,3))
Add_Err(1, BeamType_W10Err_L2, BeamType_10error, BeamType_W10_HZ10_Mid, BeamType_W10_HZ20_Mid, BeamType_W10_HZ40_Mid, BeamType_W10_HZ80_Mid)
# -------------- W = 5m-------------------------------
Tie5Err_L2 = np.zeros((4,3))
Add_Err(1, Tie5Err_L2,Tie5_error, Tie_W5_HZ10_Mid, Tie_W5_HZ20_Mid, Tie_W5_HZ40_Mid, Tie_W5_HZ80_Mid)

LK5Err_L2 = np.zeros((4,3))
Add_Err(1, LK5Err_L2,LK5_error, LK_W5_HZ10_Mid, LK_W5_HZ20_Mid, LK_W5_HZ40_Mid, LK_W5_HZ80_Mid)

BeamType_W5Err_L2 = np.zeros((4,3))
Add_Err(1, BeamType_W5Err_L2, BeamType_5error, BeamType_W5_HZ10_Mid, BeamType_W5_HZ20_Mid, BeamType_W5_HZ40_Mid, BeamType_W5_HZ80_Mid)
# -------------- W = 2m-------------------------------
Tie2Err_L2 = np.zeros((4,3))
Add_Err(1, Tie2Err_L2,Tie2_error, Tie_W2_HZ10_Mid, Tie_W2_HZ20_Mid, Tie_W2_HZ40_Mid, Tie_W2_HZ80_Mid)

LK2Err_L2 = np.zeros((4,3))
Add_Err(1, LK2Err_L2,LK2_error, LK_W2_HZ10_Mid, LK_W2_HZ20_Mid, LK_W2_HZ40_Mid, LK_W2_HZ80_Mid)

BeamType_W2Err_L2 = np.zeros((4,3))
Add_Err(1, BeamType_W2Err_L2, BeamType_2error, BeamType_W2_HZ10_Mid, BeamType_W2_HZ20_Mid, BeamType_W2_HZ40_Mid, BeamType_W2_HZ80_Mid)

def Add_Err2(Index, AwayTieErr20, Tie20_error, Tie_W20_HZ10_Away, Tie_W20_HZ20_Away, Tie_W20_HZ40_Away, Tie_W20_HZ80_Away):
    AwayTieErr20[:,0] = Tie20_error[:,0] 
# ===================================== Calculate_L2NormError Normalization : 1m away from Middle Node============================================================
    AwayTieErr20[0,Index], AwayTieErr20[0,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ10_Away, Analysis_Time,Tie_W20_HZ10_Away, time_range=(0, 0.20))
    AwayTieErr20[1,Index], AwayTieErr20[1,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ20_Away, Analysis_Time,Tie_W20_HZ20_Away, time_range=(0, 0.20))
    AwayTieErr20[2,Index], AwayTieErr20[2,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ40_Away, Analysis_Time,Tie_W20_HZ40_Away, time_range=(0, 0.20))
    AwayTieErr20[3,Index], AwayTieErr20[3,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ80_Away, Analysis_Time,Tie_W20_HZ80_Away, time_range=(0, 0.20))

# -------------- W = 20m-------------------------------
Tie20Err_L2Away = np.zeros((4,3))
Add_Err2(1, Tie20Err_L2Away, Tie20_error_Away, Tie_W20_HZ10_Away, Tie_W20_HZ20_Away, Tie_W20_HZ40_Away, Tie_W20_HZ80_Away)

LK20Err_L2Away = np.zeros((4,3))
Add_Err2(1, LK20Err_L2Away, LK20_error_Away, LK_W20_HZ10_Away, LK_W20_HZ20_Away, LK_W20_HZ40_Away, LK_W20_HZ80_Away)

BeamType_W20Err_L2Away = np.zeros((4,3))
Add_Err2(1, BeamType_W20Err_L2Away, BeamType_20error_Away, BeamType_W20_HZ10_Away, BeamType_W20_HZ20_Away, BeamType_W20_HZ40_Away, BeamType_W20_HZ80_Away)
# -------------- W = 10m-------------------------------
Tie10Err_L2Away = np.zeros((4,3))
Add_Err2(1, Tie10Err_L2Away, Tie10_error_Away, Tie_W10_HZ10_Away, Tie_W10_HZ20_Away, Tie_W10_HZ40_Away, Tie_W10_HZ80_Away)

LK10Err_L2Away = np.zeros((4,3))
Add_Err2(1, LK10Err_L2Away, LK10_error_Away, LK_W10_HZ10_Away, LK_W10_HZ20_Away, LK_W10_HZ40_Away, LK_W10_HZ80_Away)

BeamType_W10Err_L2Away = np.zeros((4,3))
Add_Err2(1, BeamType_W10Err_L2Away, BeamType_10error_Away, BeamType_W10_HZ10_Away, BeamType_W10_HZ20_Away, BeamType_W10_HZ40_Away, BeamType_W10_HZ80_Away)
# -------------- W = 5m-------------------------------
Tie5Err_L2Away = np.zeros((4,3))
Add_Err2(1, Tie5Err_L2Away, Tie5_error_Away, Tie_W5_HZ10_Away, Tie_W5_HZ20_Away, Tie_W5_HZ40_Away, Tie_W5_HZ80_Away)

LK5Err_L2Away = np.zeros((4,3))
Add_Err2(1, LK5Err_L2Away, LK5_error_Away, LK_W5_HZ10_Away, LK_W5_HZ20_Away, LK_W5_HZ40_Away, LK_W5_HZ80_Away)

BeamType_W5Err_L2Away = np.zeros((4,3))
Add_Err2(1, BeamType_W5Err_L2Away, BeamType_5error_Away, BeamType_W5_HZ10_Away, BeamType_W5_HZ20_Away, BeamType_W5_HZ40_Away, BeamType_W5_HZ80_Away)
# -------------- W = 2m-------------------------------
Tie2Err_L2Away = np.zeros((4,3))
Add_Err2(1, Tie2Err_L2Away, Tie2_error_Away, Tie_W2_HZ10_Away, Tie_W2_HZ20_Away, Tie_W2_HZ40_Away, Tie_W2_HZ80_Away)

LK2Err_L2Away = np.zeros((4,3))
Add_Err2(1, LK2Err_L2Away, LK2_error_Away, LK_W2_HZ10_Away, LK_W2_HZ20_Away, LK_W2_HZ40_Away, LK_W2_HZ80_Away)

BeamType_W2Err_L2Away = np.zeros((4,3))
Add_Err2(1, BeamType_W2Err_L2Away, BeamType_2error_Away, BeamType_W2_HZ10_Away, BeamType_W2_HZ20_Away, BeamType_W2_HZ40_Away, BeamType_W2_HZ80_Away)

# ==================Draw L2 Norm error : Dy =============================
def DifferTime_L2Error(Peak,TieErr, LKErr, Type1Err):
    # plt.plot(TieErr[:,0],TieErr[:,Peak],marker = '^',markersize=12,markerfacecolor = 'white',label = 'Tie')
    plt.plot(LKErr[:,0],LKErr[:,Peak],marker = 'o',markersize=12,markerfacecolor = 'white',label = 'LK Dashpot', color='blue',linewidth = 4.0)
    plt.plot(Type1Err[:,0],Type1Err[:,Peak],marker = '<',markersize=12,markerfacecolor = 'white',label = 'Proposed', color='red',linewidth = 2.0)

    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 18)

    # plt.ylim(0.0, 1.5)
    plt.grid(True)
    
    ax = plt.gca()
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.125))
    # -------------- Consider X-axis  -----------------------
    ax.set_xscale('log', base=10)
    ax.set_xticks([], minor=False)
    ax.set_xticks([], minor=True)
    x_ticks_Num = np.array([0.01, 0.02, 0.04, 0.06, 0.08, 0.1])
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.2f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # ------- Miner ticks -----------------
    ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='x', which='minor', length=4, color='gray')
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='both', labelsize= 18)
    
    # -------------- Consider Y-axis  -----------------------
# Vertical =0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4, 0.6 / Rocking =0.1 ,0.2, 0.4, 0.6, 0.8, 1.0, 2.0 / Horizon = 0.08, 0.1, 0.2, 0.4, 0.6, 0.8
    ax.set_yscale('log', base=10)
    ax.set_yticks([], minor=False)
    ax.set_yticks([], minor=True)
    y_ticks_Num = np.array([0.1 ,0.2, 0.4, 0.6, 0.8]) 
    ax.set_yticks(y_ticks_Num)
    ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks_Num], rotation=0, fontsize=12)
    ax.tick_params(axis='y', which='both', labelsize=14)
    # ------- Miner ticks -----------------
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='y', which='minor', length=4, color='gray')

    # ax.set_ylim(-0.0, 1.5)  # Vertical = -0.0, 1.5 / Rocking = -0.0, 2.0
    
# ----------------- Middle Node L2-Norm Error -------------------------
figsize = (10, 10)
# fig13, (ax49,ax50,ax51) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# # fig13.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig13.text(0.14,0.82, "(Middle Node)", color = "black", fontsize=22)
# fig13.text(0.17,0.85, r"$\mathrm {Horizon}$", color = "black", fontsize=22)

# fig13.text(0.01,0.5, 'Normalized L2 Norm Error '+ r"$\ E^{0~0.2s}_{L2}$", va= 'center', rotation= 'vertical', fontsize=25)

# fig13.text(0.39,0.060,  f'Duration ' + r'$t_d$', va= 'center', fontsize=25)

# # ax49 = plt.subplot(411)
# # DifferTime_L2Error(1, Tie20Err_L2, LK20Err_L2, BeamType_W20Err_L2)
# # ax49.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.15, y=0.30)

# ax49 = plt.subplot(311)
# DifferTime_L2Error(1, Tie10Err_L2, LK10Err_L2, BeamType_W10Err_L2)
# ax49.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.80, y=0.80)

# ax50 = plt.subplot(312)
# DifferTime_L2Error(1, Tie5Err_L2, LK5Err_L2, BeamType_W5Err_L2)
# ax50.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.80, y=0.80)

# ax51 = plt.subplot(313)
# DifferTime_L2Error(1, Tie2Err_L2, LK2Err_L2, BeamType_W2Err_L2)
# ax51.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.80, y=0.10)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting

# lines, labels = fig13.axes[-1].get_legend_handles_labels()
# fig13.legend(lines, labels, ncol=2, loc = (0.30,0.89) ,prop=font_props)

# fig14, (ax53,ax54,ax55) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# # fig14.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig14.text(0.14,0.82, "(Node 1 m away from the midpoint)", color = "black", fontsize=22)
# fig14.text(0.20,0.85, r"$\mathrm {Horizon}$", color = "black", fontsize=22)

# fig14.text(0.01,0.5, 'Normalized L2 Norm Error '+ r"$\ E^{0~0.2s}_{L2}$", va= 'center', rotation= 'vertical', fontsize=25)

# fig14.text(0.39,0.060,  f'Duration ' + r'$t_d$', va= 'center', fontsize=25)

# # ax53 = plt.subplot(311)
# # DifferTime_L2Error(1, Tie20Err_L2Away, LK20Err_L2Away, BeamType_W20Err_L2Away)
# # ax53.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.15, y=0.15)

# ax53 = plt.subplot(311)
# DifferTime_L2Error(1, Tie10Err_L2Away, LK10Err_L2Away, BeamType_W10Err_L2Away)
# ax53.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.85, y=0.80)

# ax54 = plt.subplot(312)
# DifferTime_L2Error(1, Tie5Err_L2Away, LK5Err_L2Away, BeamType_W5Err_L2Away)
# ax54.set_title(r"$w=$ $\mathrm{5m}$",fontsize =23, x=0.85, y=0.80)

# ax55 = plt.subplot(313)
# DifferTime_L2Error(1, Tie2Err_L2Away, LK2Err_L2Away, BeamType_W2Err_L2Away)
# ax55.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.85, y=0.10)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting

# lines, labels = fig14.axes[-1].get_legend_handles_labels()
# fig14.legend(lines, labels, ncol=2, loc = (0.30,0.89) ,prop=font_props)

def Tie_L2Error(TieErr2, TieErr5, TieErr10, TieErr20):
    plt.figure(figsize=(10, 8))
    font_props = {'family': 'Arial', 'size': 16}
    plt.text(0.06, 0.10,'Horizon', color='black', fontsize = 28, transform=plt.gca().transAxes)
    plt.text(0.10, 0.04,'Tie', color='black', fontsize = 28, transform=plt.gca().transAxes)
    plt.xlabel(f'Duration ' + r'$t_d$', fontsize = 25)
    plt.ylabel('Normalized L2 Norm Error '+ r"$\ E^{0~0.2s}_{L2}$", fontsize = 25)

    plt.plot(TieErr2[:,0], TieErr2[:,1],marker = '^',markersize=12,markerfacecolor = 'white',label = r"$w=$ $\mathrm{2m}$", color='darkgrey',linewidth = 6.0)
    plt.plot(TieErr5[:,0], TieErr5[:,1],marker = 'o',markersize=12,markerfacecolor = 'white',label = r"$w=$ $\mathrm{5m}$", color='blue',linewidth = 5.0)
    plt.plot(TieErr10[:,0], TieErr10[:,1],marker = '<',markersize=12,markerfacecolor = 'white',label = r"$w=$ $\mathrm{10m}$", color='darkgreen',linewidth = 4.0)
    plt.plot(TieErr20[:,0], TieErr20[:,1],marker = '*',markersize=12,markerfacecolor = 'white',label = r"$w=$ $\mathrm{20m}$", color='red',linewidth = 3.0)

    plt.legend(ncol= 4, bbox_to_anchor= (0.02, 1.09), loc='upper left', prop=font_props) 

    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 18)

    # plt.ylim(0.0, 1.5)
    plt.grid(True)
    
    ax = plt.gca()
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.125))
    # -------------- Consider X-axis  -----------------------
    ax.set_xscale('log', base=10)
    ax.set_xticks([], minor=False)
    ax.set_xticks([], minor=True)
    x_ticks_Num = np.array([0.01, 0.02, 0.04, 0.06, 0.08, 0.1])
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.2f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # ------- Miner ticks -----------------
    ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='x', which='minor', length=4, color='gray')
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='both', labelsize= 18)
    
    # -------------- Consider Y-axis  -----------------------
# Vertical =1.0, 2.0, 4.0, 6.0, 8.0, 10.0 / Rocking =1.0, 2.0, 4.0, 6.0 / Horizon = 0.2, 0.4, 0.6, 0.8, 1.0, 2.0, 4.0
    ax.set_yscale('log', base=10)
    ax.set_yticks([], minor=False)
    ax.set_yticks([], minor=True)
    y_ticks_Num = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 2.0, 4.0]) # , 8.0, 10.0
    ax.set_yticks(y_ticks_Num)
    ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks_Num], rotation=0, fontsize=12)
    ax.tick_params(axis='y', which='both', labelsize=16)
    # ------- Miner ticks -----------------
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='y', which='minor', length=4, color='gray')

    # ax.set_ylim(-0.0, 1.5)  # Vertical = -0.0, 1.5 / Rocking = -0.0, 2.0

# Tie_L2Error(Tie2Err_L2, Tie5Err_L2, Tie10Err_L2, Tie20Err_L2)
# Tie_L2Error(Tie2Err_L2Away, Tie5Err_L2Away, Tie10Err_L2Away, Tie20Err_L2Away)
