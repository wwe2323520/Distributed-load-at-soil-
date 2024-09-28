# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 16:20:27 2024

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
from matplotlib.lines import Line2D

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

        # print('================ Middle Left And Right 1m Node ====================')
        Top_CenterLeft = UpperN_Center - int(1.0/Dw)
        Top_CenterRight = UpperN_Center + int(1.0/Dw)
        # print(f'Top_CenterLeft Node = {Top_CenterLeft}; Top_CenterRight Node = {Top_CenterRight}')
        
        MiddelNode.append(UpperN_Center)
    
    Mid40row = MiddelNode[0]
    return Mid40row

# ---------- Consider Mesh = 40 row ----------------------------------
W2_Mid40row = Find_Middle(int(2.0), YMesh)
W5_Mid40row = Find_Middle(int(5.0), YMesh)
W10_Mid40row = Find_Middle(int(10.0), YMesh)
W20_Mid40row = Find_Middle(int(20.0), YMesh)

Ver_Condition = f'2D_Absorb/NewMark_Linear/Vertical' # Vertical; Horizon; Rocking
Hor_Condition = f'2D_Absorb/NewMark_Linear/Horizon' # Vertical; Horizon; Rocking
Roc_Condition = f'2D_Absorb/NewMark_Linear/Rocking' # Vertical; Horizon; Rocking


# ===================================== Vertical Condition: Middle Node ==========================================================================
# ----------------- f = 10HZ --------------------------------
HZ10 = f'HZ_10'
# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
Ver_2mHZ10 = f'{Ver_Condition}/W_2m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ10}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ10}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file3 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ10}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Ver_Tie_W2_HZ10 = rdnumpy(file1)
Ver_LK_W2_HZ10 = rdnumpy(file2)
Ver_BeamType_W2_HZ10 = rdnumpy(file3)
# ============================ SoilWidth = 5.0 m (HZ = 10)=======================================
Ver_5mHZ10 = f'{Ver_Condition}/W_5m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file4 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ10}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file5 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ10}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file6 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ10}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Ver_Tie_W5_HZ10 = rdnumpy(file4)
Ver_LK_W5_HZ10 = rdnumpy(file5)
Ver_BeamType_W5_HZ10 = rdnumpy(file6)
# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
Ver_10mHZ10 = f'{Ver_Condition}/W_10m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file7 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ10}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file8 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ10}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file9 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ10}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Ver_Tie_W10_HZ10 = rdnumpy(file7)
Ver_LK_W10_HZ10 = rdnumpy(file8)
Ver_BeamType_W10_HZ10 = rdnumpy(file9)
# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
Ver_20mHZ10 = f'{Ver_Condition}/W_20m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file10 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ10}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file11 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ10}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file12 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ10}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Ver_Tie_W20_HZ10 = rdnumpy(file10)
Ver_LK_W20_HZ10 = rdnumpy(file11)
Ver_BeamType_W20_HZ10 = rdnumpy(file12)

# ----------------- f = 20HZ --------------------------------
HZ20 = f'HZ_20'
# ============================ SoilWidth = 2.0 m (HZ = 20)=======================================
Ver_2mHZ20 = f'{Ver_Condition}/W_2m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file13 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ20}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ20}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ20}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Ver_Tie_W2_HZ20 = rdnumpy(file13)
Ver_LK_W2_HZ20 = rdnumpy(file14)
Ver_BeamType_W2_HZ20 = rdnumpy(file15)
# ============================ SoilWidth = 5.0 m (HZ = 20)=======================================
Ver_5mHZ20 = f'{Ver_Condition}/W_5m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file16 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ20}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file17 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ20}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file18 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ20}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Ver_Tie_W5_HZ20 = rdnumpy(file16)
Ver_LK_W5_HZ20 = rdnumpy(file17)
Ver_BeamType_W5_HZ20 = rdnumpy(file18)
# ============================ SoilWidth = 10.0 m (HZ = 20)=======================================
Ver_10mHZ20 = f'{Ver_Condition}/W_10m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file19 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ20}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file20 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ20}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file21 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ20}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Ver_Tie_W10_HZ20 = rdnumpy(file19)
Ver_LK_W10_HZ20 = rdnumpy(file20)
Ver_BeamType_W10_HZ20 = rdnumpy(file21)
# ============================ SoilWidth = 20.0 m (HZ = 20)=======================================
Ver_20mHZ20 = f'{Ver_Condition}/W_20m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file22 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ20}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file23 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ20}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file24 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ20}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Ver_Tie_W20_HZ20 = rdnumpy(file22)
Ver_LK_W20_HZ20 = rdnumpy(file23)
Ver_BeamType_W20_HZ20 = rdnumpy(file24)

# ----------------- f = 40HZ --------------------------------
HZ40 = f'HZ_40'
# ============================ SoilWidth = 2.0 m (HZ = 40)=======================================
Ver_2mHZ40 = f'{Ver_Condition}/W_2m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file25 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ40}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file26 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ40}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file27 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ40}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Ver_Tie_W2_HZ40 = rdnumpy(file25)
Ver_LK_W2_HZ40 = rdnumpy(file26)
Ver_BeamType_W2_HZ40 = rdnumpy(file27)
# ============================ SoilWidth = 5.0 m (HZ = 40)=======================================
Ver_5mHZ40 = f'{Ver_Condition}/W_5m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file28 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ40}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file29 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ40}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file30 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ40}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Ver_Tie_W5_HZ40 = rdnumpy(file28)
Ver_LK_W5_HZ40 = rdnumpy(file29)
Ver_BeamType_W5_HZ40 = rdnumpy(file30)
# ============================ SoilWidth = 10.0 m (HZ = 40)=======================================
Ver_10mHZ40 = f'{Ver_Condition}/W_10m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file31 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ40}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file32 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ40}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file33 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ40}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Ver_Tie_W10_HZ40 = rdnumpy(file31)
Ver_LK_W10_HZ40 = rdnumpy(file32)
Ver_BeamType_W10_HZ40 = rdnumpy(file33)
# ============================ SoilWidth = 20.0 m (HZ = 40)=======================================
Ver_20mHZ40 = f'{Ver_Condition}/W_20m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file34 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ40}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file35 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ40}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file36 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ40}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Ver_Tie_W20_HZ40 = rdnumpy(file34)
Ver_LK_W20_HZ40 = rdnumpy(file35)
Ver_BeamType_W20_HZ40 = rdnumpy(file36)

# ----------------- f = 80HZ --------------------------------
HZ80 = f'HZ_80'
# ============================ SoilWidth = 2.0 m (HZ = 80)=======================================
Ver_2mHZ80 = f'{Ver_Condition}/W_2m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file37 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ80}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file38 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ80}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file39 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ80}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Ver_Tie_W2_HZ80 = rdnumpy(file37)
Ver_LK_W2_HZ80 = rdnumpy(file38)
Ver_BeamType_W2_HZ80 = rdnumpy(file39)
# ============================ SoilWidth = 5.0 m (HZ = 80)=======================================
Ver_5mHZ80 = f'{Ver_Condition}/W_5m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file40 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ80}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file41 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ80}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file42 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ80}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Ver_Tie_W5_HZ80 = rdnumpy(file40)
Ver_LK_W5_HZ80 = rdnumpy(file41)
Ver_BeamType_W5_HZ80 = rdnumpy(file42)
# ============================ SoilWidth = 10.0 m (HZ = 80)=======================================
Ver_10mHZ80 = f'{Ver_Condition}/W_10m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file43 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ80}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file44 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ80}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file45 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ80}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Ver_Tie_W10_HZ80 = rdnumpy(file43)
Ver_LK_W10_HZ80 = rdnumpy(file44)
Ver_BeamType_W10_HZ80 = rdnumpy(file45)
# ============================ SoilWidth = 20.0 m (HZ = 80)=======================================
Ver_20mHZ80 = f'{Ver_Condition}/W_20m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file46 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ80}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file47 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ80}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file48 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ80}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Ver_Tie_W20_HZ80 = rdnumpy(file46)
Ver_LK_W20_HZ80 = rdnumpy(file47)
Ver_BeamType_W20_HZ80 = rdnumpy(file48)

# ============================ Horizon Condition: Middle Node =========================================
# ----------------- f = 10HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
Hor_2mHZ10 = f'{Hor_Condition}/W_2m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file49 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ10}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file50 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ10}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file51 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ10}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Hor_Tie_W2_HZ10 = rdnumpy(file49)
Hor_LK_W2_HZ10 = rdnumpy(file50)
Hor_BeamType_W2_HZ10 = rdnumpy(file51)
# ============================ SoilWidth = 5.0 m (HZ = 10)=======================================
Hor_5mHZ10 = f'{Hor_Condition}/W_5m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file52 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ10}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file53 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ10}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file54 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ10}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Hor_Tie_W5_HZ10 = rdnumpy(file52)
Hor_LK_W5_HZ10 = rdnumpy(file53)
Hor_BeamType_W5_HZ10 = rdnumpy(file54)
# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
Hor_10mHZ10 = f'{Hor_Condition}/W_10m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file55 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ10}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file56 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ10}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file57 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ10}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Hor_Tie_W10_HZ10 = rdnumpy(file55)
Hor_LK_W10_HZ10 = rdnumpy(file56)
Hor_BeamType_W10_HZ10 = rdnumpy(file57)
# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
Hor_20mHZ10 = f'{Hor_Condition}/W_20m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file58 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ10}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file59 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ10}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file60 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ10}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Hor_Tie_W20_HZ10 = rdnumpy(file58)
Hor_LK_W20_HZ10 = rdnumpy(file59)
Hor_BeamType_W20_HZ10 = rdnumpy(file60)

# ----------------- f = 20HZ --------------------------------

# ============================ SoilWidth = 2.0 m (HZ = 20)=======================================
Hor_2mHZ20 = f'{Hor_Condition}/W_2m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file61 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ20}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file62 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ20}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file63 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ20}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Hor_Tie_W2_HZ20 = rdnumpy(file61)
Hor_LK_W2_HZ20 = rdnumpy(file62)
Hor_BeamType_W2_HZ20 = rdnumpy(file63)
# ============================ SoilWidth = 5.0 m (HZ = 20)=======================================
Hor_5mHZ20 = f'{Hor_Condition}/W_5m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file64 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ20}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file65 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ20}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file66 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ20}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Hor_Tie_W5_HZ20 = rdnumpy(file64)
Hor_LK_W5_HZ20 = rdnumpy(file65)
Hor_BeamType_W5_HZ20 = rdnumpy(file66)
# ============================ SoilWidth = 10.0 m (HZ = 20)=======================================
Hor_10mHZ20 = f'{Hor_Condition}/W_10m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file67 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ20}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file68 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ20}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file69 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ20}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Hor_Tie_W10_HZ20 = rdnumpy(file67)
Hor_LK_W10_HZ20 = rdnumpy(file68)
Hor_BeamType_W10_HZ20 = rdnumpy(file69)
# ============================ SoilWidth = 20.0 m (HZ = 20)=======================================
Hor_20mHZ20 = f'{Hor_Condition}/W_20m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file70 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ20}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file71 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ20}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file72 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ20}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Hor_Tie_W20_HZ20 = rdnumpy(file70)
Hor_LK_W20_HZ20 = rdnumpy(file71)
Hor_BeamType_W20_HZ20 = rdnumpy(file72)

# ----------------- f = 40HZ --------------------------------

# ============================ SoilWidth = 2.0 m (HZ = 40)=======================================
Hor_2mHZ40 = f'{Hor_Condition}/W_2m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file73 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ40}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file74 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ40}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file75 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ40}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Hor_Tie_W2_HZ40 = rdnumpy(file73)
Hor_LK_W2_HZ40 = rdnumpy(file74)
Hor_BeamType_W2_HZ40 = rdnumpy(file75)
# ============================ SoilWidth = 5.0 m (HZ = 40)=======================================
Hor_5mHZ40 = f'{Hor_Condition}/W_5m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file76 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ40}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file77 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ40}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file78 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ40}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Hor_Tie_W5_HZ40 = rdnumpy(file76)
Hor_LK_W5_HZ40 = rdnumpy(file77)
Hor_BeamType_W5_HZ40 = rdnumpy(file78)
# ============================ SoilWidth = 10.0 m (HZ = 40)=======================================
Hor_10mHZ40 = f'{Hor_Condition}/W_10m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file79 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ40}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file80 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ40}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file81 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ40}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Hor_Tie_W10_HZ40 = rdnumpy(file79)
Hor_LK_W10_HZ40 = rdnumpy(file80)
Hor_BeamType_W10_HZ40 = rdnumpy(file81)
# ============================ SoilWidth = 20.0 m (HZ = 40)=======================================
Hor_20mHZ40 = f'{Hor_Condition}/W_20m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file82 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ40}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file83 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ40}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file84 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ40}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Hor_Tie_W20_HZ40 = rdnumpy(file82)
Hor_LK_W20_HZ40 = rdnumpy(file83)
Hor_BeamType_W20_HZ40 = rdnumpy(file84)

# ----------------- f = 80HZ --------------------------------

# ============================ SoilWidth = 2.0 m (HZ = 80)=======================================
Hor_2mHZ80 = f'{Hor_Condition}/W_2m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file85 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ80}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file86 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ80}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file87 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ80}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Hor_Tie_W2_HZ80 = rdnumpy(file85)
Hor_LK_W2_HZ80 = rdnumpy(file86)
Hor_BeamType_W2_HZ80 = rdnumpy(file87)
# ============================ SoilWidth = 5.0 m (HZ = 80)=======================================
Hor_5mHZ80 = f'{Hor_Condition}/W_5m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file88 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ80}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file89 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ80}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file90 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ80}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Hor_Tie_W5_HZ80 = rdnumpy(file88)
Hor_LK_W5_HZ80 = rdnumpy(file89)
Hor_BeamType_W5_HZ80 = rdnumpy(file90)
# ============================ SoilWidth = 10.0 m (HZ = 80)=======================================
Hor_10mHZ80 = f'{Hor_Condition}/W_10m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file91 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ80}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file92 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ80}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file93 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ80}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Hor_Tie_W10_HZ80 = rdnumpy(file91)
Hor_LK_W10_HZ80 = rdnumpy(file92)
Hor_BeamType_W10_HZ80 = rdnumpy(file93)
# ============================ SoilWidth = 20.0 m (HZ = 80)=======================================
Hor_20mHZ80 = f'{Hor_Condition}/W_20m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file94 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ80}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file95 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ80}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file96 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ80}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Hor_Tie_W20_HZ80 = rdnumpy(file94)
Hor_LK_W20_HZ80 = rdnumpy(file95)
Hor_BeamType_W20_HZ80 = rdnumpy(file96)

# ============================ Rocking Condition: Middle Node =========================================
# ----------------- f = 10HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
Roc_2mHZ10 = f'{Roc_Condition}/W_2m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file97 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ10}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file98 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ10}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file99 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ10}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Roc_Tie_W2_HZ10 = rdnumpy(file97)
Roc_LK_W2_HZ10 = rdnumpy(file98)
Roc_BeamType_W2_HZ10 = rdnumpy(file99)
# ============================ SoilWidth = 5.0 m (HZ = 10)=======================================
Roc_5mHZ10 = f'{Roc_Condition}/W_5m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file100 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ10}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file101 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ10}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file102 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ10}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Roc_Tie_W5_HZ10 = rdnumpy(file100)
Roc_LK_W5_HZ10 = rdnumpy(file101)
Roc_BeamType_W5_HZ10 = rdnumpy(file102)
# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
Roc_10mHZ10 = f'{Roc_Condition}/W_10m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file103 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ10}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file104 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ10}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file105 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ10}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Roc_Tie_W10_HZ10 = rdnumpy(file103)
Roc_LK_W10_HZ10 = rdnumpy(file104)
Roc_BeamType_W10_HZ10 = rdnumpy(file105)
# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
Roc_20mHZ10 = f'{Roc_Condition}/W_20m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file106 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ10}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file107 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ10}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file108 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ10}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Roc_Tie_W20_HZ10 = rdnumpy(file106)
Roc_LK_W20_HZ10 = rdnumpy(file107)
Roc_BeamType_W20_HZ10 = rdnumpy(file108)

# ----------------- f = 20HZ --------------------------------

# ============================ SoilWidth = 2.0 m (HZ = 20)=======================================
Roc_2mHZ20 = f'{Roc_Condition}/W_2m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file109 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ20}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file110 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ20}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file111 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ20}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Roc_Tie_W2_HZ20 = rdnumpy(file109)
Roc_LK_W2_HZ20 = rdnumpy(file110)
Roc_BeamType_W2_HZ20 = rdnumpy(file111)
# ============================ SoilWidth = 5.0 m (HZ = 20)=======================================
Roc_5mHZ20 = f'{Roc_Condition}/W_5m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file112 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ20}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file113 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ20}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file114 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ20}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Roc_Tie_W5_HZ20 = rdnumpy(file112)
Roc_LK_W5_HZ20 = rdnumpy(file113)
Roc_BeamType_W5_HZ20 = rdnumpy(file114)
# ============================ SoilWidth = 10.0 m (HZ = 20)=======================================
Roc_10mHZ20 = f'{Roc_Condition}/W_10m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file115 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ20}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file116 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ20}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file117 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ20}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Roc_Tie_W10_HZ20 = rdnumpy(file115)
Roc_LK_W10_HZ20 = rdnumpy(file116)
Roc_BeamType_W10_HZ20 = rdnumpy(file117)
# ============================ SoilWidth = 20.0 m (HZ = 20)=======================================
Roc_20mHZ20 = f'{Roc_Condition}/W_20m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file118 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ20}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file119 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ20}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file120 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ20}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Roc_Tie_W20_HZ20 = rdnumpy(file118)
Roc_LK_W20_HZ20 = rdnumpy(file119)
Roc_BeamType_W20_HZ20 = rdnumpy(file120)

# ----------------- f = 40HZ --------------------------------

# ============================ SoilWidth = 2.0 m (HZ = 40)=======================================
Roc_2mHZ40 = f'{Roc_Condition}/W_2m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file121 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ40}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file122 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ40}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file123 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ40}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Roc_Tie_W2_HZ40 = rdnumpy(file121)
Roc_LK_W2_HZ40 = rdnumpy(file122)
Roc_BeamType_W2_HZ40 = rdnumpy(file123)
# ============================ SoilWidth = 5.0 m (HZ = 40)=======================================
Roc_5mHZ40 = f'{Roc_Condition}/W_5m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file124 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ40}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file125 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ40}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file126 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ40}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Roc_Tie_W5_HZ40 = rdnumpy(file124)
Roc_LK_W5_HZ40 = rdnumpy(file125)
Roc_BeamType_W5_HZ40 = rdnumpy(file126)
# ============================ SoilWidth = 10.0 m (HZ = 40)=======================================
Roc_10mHZ40 = f'{Roc_Condition}/W_10m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file127 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ40}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file128 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ40}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file129 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ40}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Roc_Tie_W10_HZ40 = rdnumpy(file127)
Roc_LK_W10_HZ40 = rdnumpy(file128)
Roc_BeamType_W10_HZ40 = rdnumpy(file129)
# ============================ SoilWidth = 20.0 m (HZ = 40)=======================================
Roc_20mHZ40 = f'{Roc_Condition}/W_20m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file130 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ40}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file131 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ40}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file132 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ40}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Roc_Tie_W20_HZ40 = rdnumpy(file130)
Roc_LK_W20_HZ40 = rdnumpy(file131)
Roc_BeamType_W20_HZ40 = rdnumpy(file132)

# ----------------- f = 80HZ --------------------------------

# ============================ SoilWidth = 2.0 m (HZ = 80)=======================================
Roc_2mHZ80 = f'{Roc_Condition}/W_2m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file133 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ80}/Tie_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file134 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ80}/LKDash_Surface_40row/Velocity/node{W2_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file135 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ80}/BeamType1_Surface_40row/Velocity/node{W2_Mid40row}.out"

Roc_Tie_W2_HZ80 = rdnumpy(file133)
Roc_LK_W2_HZ80 = rdnumpy(file134)
Roc_BeamType_W2_HZ80 = rdnumpy(file135)
# ============================ SoilWidth = 5.0 m (HZ = 80)=======================================
Roc_5mHZ80 = f'{Roc_Condition}/W_5m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file136 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ80}/Tie_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file137 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ80}/LKDash_Surface_40row/Velocity/node{W5_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file138 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ80}/BeamType1_Surface_40row/Velocity/node{W5_Mid40row}.out"

Roc_Tie_W5_HZ80 = rdnumpy(file136)
Roc_LK_W5_HZ80 = rdnumpy(file137)
Roc_BeamType_W5_HZ80 = rdnumpy(file138)
# ============================ SoilWidth = 10.0 m (HZ = 80)=======================================
Roc_10mHZ80 = f'{Roc_Condition}/W_10m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file139 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ80}/Tie_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file140 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ80}/LKDash_Surface_40row/Velocity/node{W10_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file141 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ80}/BeamType1_Surface_40row/Velocity/node{W10_Mid40row}.out"

Roc_Tie_W10_HZ80 = rdnumpy(file139)
Roc_LK_W10_HZ80 = rdnumpy(file140)
Roc_BeamType_W10_HZ80 = rdnumpy(file141)
# ============================ SoilWidth = 20.0 m (HZ = 80)=======================================
Roc_20mHZ80 = f'{Roc_Condition}/W_20m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file142 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ80}/Tie_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file143 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ80}/LKDash_Surface_40row/Velocity/node{W20_Mid40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file144 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ80}/BeamType1_Surface_40row/Velocity/node{W20_Mid40row}.out"

Roc_Tie_W20_HZ80 = rdnumpy(file142)
Roc_LK_W20_HZ80 = rdnumpy(file143)
Roc_BeamType_W20_HZ80 = rdnumpy(file144)

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

    # ---------- Only 40 row -------------------
    L_Qua40row = Quarter_LNode[0]
    R_Qua40row = Quarter_RNode[0]
# --------- Vertical/Horizon = R_Qua40row ; Rocking = L_Qua40row  ------------
    return L_Qua40row

W2_Away40row = Find_Quarter(int(2.0), YMesh)
W5_Away40row = Find_Quarter(int(5.0), YMesh)
W10_Away40row = Find_Quarter(int(10.0), YMesh)
W20_Away40row = Find_Quarter(int(20.0), YMesh)

# =============================================== Read 1m away from Middle Node Analysis Data ===========================================================================
# ======================== Vertical Condition: 1m Away =====================================
# ----------------- f = 10HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
# Condition1 = f'{Force_Condition}/W_2m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file145 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ10}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file146 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ10}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file147 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ10}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Ver_Tie_W2_HZ10_Away = rdnumpy(file145)
Ver_LK_W2_HZ10_Away = rdnumpy(file146)
Ver_BeamType_W2_HZ10_Away = rdnumpy(file147)
# ============================ SoilWidth = 5.0 m (HZ = 10)=======================================
# Condition2 = f'{Force_Condition}/W_5m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file148 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ10}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file149 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ10}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file150 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ10}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Ver_Tie_W5_HZ10_Away = rdnumpy(file148)
Ver_LK_W5_HZ10_Away = rdnumpy(file149)
Ver_BeamType_W5_HZ10_Away = rdnumpy(file150)
# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
# Condition3 = f'{Force_Condition}/W_10m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file151 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ10}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file152 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ10}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file153 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ10}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Ver_Tie_W10_HZ10_Away = rdnumpy(file151)
Ver_LK_W10_HZ10_Away = rdnumpy(file152)
Ver_BeamType_W10_HZ10_Away = rdnumpy(file153)
# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
# Condition4 = f'{Force_Condition}/W_20m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file154 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ10}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file155 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ10}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file156 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ10}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Ver_Tie_W20_HZ10_Away = rdnumpy(file154)
Ver_LK_W20_HZ10_Away = rdnumpy(file155)
Ver_BeamType_W20_HZ10_Away = rdnumpy(file156)

# ----------------- f = 20HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 20)=======================================
# Condition5 = f'{Force_Condition}/W_2m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file157 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ20}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file158 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ20}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file159 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ20}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Ver_Tie_W2_HZ20_Away = rdnumpy(file157)
Ver_LK_W2_HZ20_Away = rdnumpy(file158)
Ver_BeamType_W2_HZ20_Away = rdnumpy(file159)
# ============================ SoilWidth = 5.0 m (HZ = 20)=======================================
# Condition6 = f'{Force_Condition}/W_5m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file160 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ20}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file161 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ20}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file162 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ20}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Ver_Tie_W5_HZ20_Away = rdnumpy(file160)
Ver_LK_W5_HZ20_Away = rdnumpy(file161)
Ver_BeamType_W5_HZ20_Away = rdnumpy(file162)
# ============================ SoilWidth = 10.0 m (HZ = 20)=======================================
# Condition7 = f'{Force_Condition}/W_10m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file163 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ20}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file164 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ20}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file165 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ20}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Ver_Tie_W10_HZ20_Away = rdnumpy(file163)
Ver_LK_W10_HZ20_Away = rdnumpy(file164)
Ver_BeamType_W10_HZ20_Away = rdnumpy(file165)
# ============================ SoilWidth = 20.0 m (HZ = 20)=======================================
# Condition8 = f'{Force_Condition}/W_20m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file166 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ20}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file167 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ20}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file168 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ20}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Ver_Tie_W20_HZ20_Away = rdnumpy(file166)
Ver_LK_W20_HZ20_Away = rdnumpy(file167)
Ver_BeamType_W20_HZ20_Away = rdnumpy(file168)

# ----------------- f = 40HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 40)=======================================
# Condition9 = f'{Force_Condition}/W_2m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file169 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ40}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file170 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ40}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file171 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ40}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Ver_Tie_W2_HZ40_Away = rdnumpy(file169)
Ver_LK_W2_HZ40_Away = rdnumpy(file170)
Ver_BeamType_W2_HZ40_Away = rdnumpy(file171)
# ============================ SoilWidth = 5.0 m (HZ = 40)=======================================
# Condition10 = f'{Force_Condition}/W_5m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file172 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ40}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file173 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ40}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file174 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ40}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Ver_Tie_W5_HZ40_Away = rdnumpy(file172)
Ver_LK_W5_HZ40_Away = rdnumpy(file173)
Ver_BeamType_W5_HZ40_Away = rdnumpy(file174)
# ============================ SoilWidth = 10.0 m (HZ = 40)=======================================
# Condition11 = f'{Force_Condition}/W_10m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file175 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ40}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file176 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ40}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file177 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ40}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Ver_Tie_W10_HZ40_Away = rdnumpy(file175)
Ver_LK_W10_HZ40_Away = rdnumpy(file176)
Ver_BeamType_W10_HZ40_Away = rdnumpy(file177)
# ============================ SoilWidth = 20.0 m (HZ = 40)=======================================
# Condition12 = f'{Force_Condition}/W_20m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file178 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ40}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file179 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ40}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file180 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ40}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Ver_Tie_W20_HZ40_Away = rdnumpy(file178)
Ver_LK_W20_HZ40_Away = rdnumpy(file179)
Ver_BeamType_W20_HZ40_Away = rdnumpy(file180)

# ----------------- f = 80HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 80)=======================================
# Condition13 = f'{Force_Condition}/W_2m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file181 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ80}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file182 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ80}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file183 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_2mHZ80}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Ver_Tie_W2_HZ80_Away = rdnumpy(file181)
Ver_LK_W2_HZ80_Away = rdnumpy(file182)
Ver_BeamType_W2_HZ80_Away = rdnumpy(file183)
# ============================ SoilWidth = 5.0 m (HZ = 80)=======================================
# Condition14 = f'{Force_Condition}/W_5m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file184 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ80}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file185 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ80}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file186 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_5mHZ80}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Ver_Tie_W5_HZ80_Away = rdnumpy(file184)
Ver_LK_W5_HZ80_Away = rdnumpy(file185)
Ver_BeamType_W5_HZ80_Away = rdnumpy(file186)
# ============================ SoilWidth = 10.0 m (HZ = 80)=======================================
# Condition15 = f'{Force_Condition}/W_10m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file187 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ80}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file188 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ80}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file189 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_10mHZ80}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Ver_Tie_W10_HZ80_Away = rdnumpy(file187)
Ver_LK_W10_HZ80_Away = rdnumpy(file188)
Ver_BeamType_W10_HZ80_Away = rdnumpy(file189)
# ============================ SoilWidth = 20.0 m (HZ = 80)=======================================
# Condition16 = f'{Force_Condition}/W_20m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file190 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ80}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file191 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ80}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file192 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Ver_20mHZ80}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Ver_Tie_W20_HZ80_Away = rdnumpy(file190)
Ver_LK_W20_HZ80_Away = rdnumpy(file191)
Ver_BeamType_W20_HZ80_Away = rdnumpy(file192)

# ======================== Horizon Condition: 1m Away =====================================
# ----------------- f = 10HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
# Condition1 = f'{Force_Condition}/W_2m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file193 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ10}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file194 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ10}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file195 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ10}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Hor_Tie_W2_HZ10_Away = rdnumpy(file193)
Hor_LK_W2_HZ10_Away = rdnumpy(file194)
Hor_BeamType_W2_HZ10_Away = rdnumpy(file195)
# ============================ SoilWidth = 5.0 m (HZ = 10)=======================================
# Condition2 = f'{Force_Condition}/W_5m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file196 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ10}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file197 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ10}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file198 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ10}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Hor_Tie_W5_HZ10_Away = rdnumpy(file196)
Hor_LK_W5_HZ10_Away = rdnumpy(file197)
Hor_BeamType_W5_HZ10_Away = rdnumpy(file198)
# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
# Condition3 = f'{Force_Condition}/W_10m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file199 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ10}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file200 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ10}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file201 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ10}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Hor_Tie_W10_HZ10_Away = rdnumpy(file199)
Hor_LK_W10_HZ10_Away = rdnumpy(file200)
Hor_BeamType_W10_HZ10_Away = rdnumpy(file201)
# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
# Condition4 = f'{Force_Condition}/W_20m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file202 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ10}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file203 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ10}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file204 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ10}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Hor_Tie_W20_HZ10_Away = rdnumpy(file202)
Hor_LK_W20_HZ10_Away = rdnumpy(file203)
Hor_BeamType_W20_HZ10_Away = rdnumpy(file204)

# ----------------- f = 20HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 20)=======================================
# Condition5 = f'{Force_Condition}/W_2m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file205 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ20}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file206 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ20}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file207 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ20}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Hor_Tie_W2_HZ20_Away = rdnumpy(file205)
Hor_LK_W2_HZ20_Away = rdnumpy(file206)
Hor_BeamType_W2_HZ20_Away = rdnumpy(file207)
# ============================ SoilWidth = 5.0 m (HZ = 20)=======================================
# Condition6 = f'{Force_Condition}/W_5m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file208 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ20}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file209 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ20}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file210 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ20}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Hor_Tie_W5_HZ20_Away = rdnumpy(file208)
Hor_LK_W5_HZ20_Away = rdnumpy(file209)
Hor_BeamType_W5_HZ20_Away = rdnumpy(file210)
# ============================ SoilWidth = 10.0 m (HZ = 20)=======================================
# Condition7 = f'{Force_Condition}/W_10m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file211 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ20}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file212 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ20}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file213 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ20}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Hor_Tie_W10_HZ20_Away = rdnumpy(file211)
Hor_LK_W10_HZ20_Away = rdnumpy(file212)
Hor_BeamType_W10_HZ20_Away = rdnumpy(file213)
# ============================ SoilWidth = 20.0 m (HZ = 20)=======================================
# Condition8 = f'{Force_Condition}/W_20m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file214 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ20}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file215 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ20}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file216 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ20}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Hor_Tie_W20_HZ20_Away = rdnumpy(file214)
Hor_LK_W20_HZ20_Away = rdnumpy(file215)
Hor_BeamType_W20_HZ20_Away = rdnumpy(file216)

# ----------------- f = 40HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 40)=======================================
# Condition9 = f'{Force_Condition}/W_2m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file217 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ40}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file218 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ40}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file219 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ40}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Hor_Tie_W2_HZ40_Away = rdnumpy(file217)
Hor_LK_W2_HZ40_Away = rdnumpy(file218)
Hor_BeamType_W2_HZ40_Away = rdnumpy(file219)
# ============================ SoilWidth = 5.0 m (HZ = 40)=======================================
# Condition10 = f'{Force_Condition}/W_5m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file220 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ40}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file221 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ40}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file222 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ40}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Hor_Tie_W5_HZ40_Away = rdnumpy(file220)
Hor_LK_W5_HZ40_Away = rdnumpy(file221)
Hor_BeamType_W5_HZ40_Away = rdnumpy(file222)
# ============================ SoilWidth = 10.0 m (HZ = 40)=======================================
# Condition11 = f'{Force_Condition}/W_10m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file223 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ40}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file224 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ40}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file225 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ40}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Hor_Tie_W10_HZ40_Away = rdnumpy(file223)
Hor_LK_W10_HZ40_Away = rdnumpy(file224)
Hor_BeamType_W10_HZ40_Away = rdnumpy(file225)
# ============================ SoilWidth = 20.0 m (HZ = 40)=======================================
# Condition12 = f'{Force_Condition}/W_20m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file226 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ40}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file227 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ40}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file228 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ40}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Hor_Tie_W20_HZ40_Away = rdnumpy(file226)
Hor_LK_W20_HZ40_Away = rdnumpy(file227)
Hor_BeamType_W20_HZ40_Away = rdnumpy(file228)

# ----------------- f = 80HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 80)=======================================
# Condition13 = f'{Force_Condition}/W_2m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file229 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ80}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file230 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ80}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file231 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_2mHZ80}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Hor_Tie_W2_HZ80_Away = rdnumpy(file229)
Hor_LK_W2_HZ80_Away = rdnumpy(file230)
Hor_BeamType_W2_HZ80_Away = rdnumpy(file231)
# ============================ SoilWidth = 5.0 m (HZ = 80)=======================================
# Condition14 = f'{Force_Condition}/W_5m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file232 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ80}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file233 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ80}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file234 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_5mHZ80}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Hor_Tie_W5_HZ80_Away = rdnumpy(file232)
Hor_LK_W5_HZ80_Away = rdnumpy(file233)
Hor_BeamType_W5_HZ80_Away = rdnumpy(file234)
# ============================ SoilWidth = 10.0 m (HZ = 80)=======================================
# Condition15 = f'{Force_Condition}/W_10m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file235 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ80}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file236 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ80}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file237 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_10mHZ80}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Hor_Tie_W10_HZ80_Away = rdnumpy(file235)
Hor_LK_W10_HZ80_Away = rdnumpy(file236)
Hor_BeamType_W10_HZ80_Away = rdnumpy(file237)
# ============================ SoilWidth = 20.0 m (HZ = 80)=======================================
# Condition16 = f'{Force_Condition}/W_20m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file238 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ80}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file239 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ80}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file240 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Hor_20mHZ80}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Hor_Tie_W20_HZ80_Away = rdnumpy(file238)
Hor_LK_W20_HZ80_Away = rdnumpy(file239)
Hor_BeamType_W20_HZ80_Away = rdnumpy(file240)

# ======================== Rocking Condition: 1m Away =====================================
# ----------------- f = 10HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
# Condition1 = f'{Force_Condition}/W_2m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file241 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ10}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file242 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ10}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file243 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ10}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Roc_Tie_W2_HZ10_Away = rdnumpy(file241)
Roc_LK_W2_HZ10_Away = rdnumpy(file242)
Roc_BeamType_W2_HZ10_Away = rdnumpy(file243)
# ============================ SoilWidth = 5.0 m (HZ = 10)=======================================
# Condition2 = f'{Force_Condition}/W_5m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file244 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ10}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file245 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ10}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file246 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ10}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Roc_Tie_W5_HZ10_Away = rdnumpy(file244)
Roc_LK_W5_HZ10_Away = rdnumpy(file245)
Roc_BeamType_W5_HZ10_Away = rdnumpy(file246)
# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
# Condition3 = f'{Force_Condition}/W_10m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file247 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ10}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file248 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ10}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file249 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ10}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Roc_Tie_W10_HZ10_Away = rdnumpy(file247)
Roc_LK_W10_HZ10_Away = rdnumpy(file248)
Roc_BeamType_W10_HZ10_Away = rdnumpy(file249)
# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
# Condition4 = f'{Force_Condition}/W_20m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file250 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ10}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file251 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ10}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file252 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ10}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Roc_Tie_W20_HZ10_Away = rdnumpy(file250)
Roc_LK_W20_HZ10_Away = rdnumpy(file251)
Roc_BeamType_W20_HZ10_Away = rdnumpy(file252)

# ----------------- f = 20HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 20)=======================================
# Condition5 = f'{Force_Condition}/W_2m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file253 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ20}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file254 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ20}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file255 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ20}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Roc_Tie_W2_HZ20_Away = rdnumpy(file253)
Roc_LK_W2_HZ20_Away = rdnumpy(file254)
Roc_BeamType_W2_HZ20_Away = rdnumpy(file255)
# ============================ SoilWidth = 5.0 m (HZ = 20)=======================================
# Condition6 = f'{Force_Condition}/W_5m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file256 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ20}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file257 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ20}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file258 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ20}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Roc_Tie_W5_HZ20_Away = rdnumpy(file256)
Roc_LK_W5_HZ20_Away = rdnumpy(file257)
Roc_BeamType_W5_HZ20_Away = rdnumpy(file258)
# ============================ SoilWidth = 10.0 m (HZ = 20)=======================================
# Condition7 = f'{Force_Condition}/W_10m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file259 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ20}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file260 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ20}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file261 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ20}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Roc_Tie_W10_HZ20_Away = rdnumpy(file259)
Roc_LK_W10_HZ20_Away = rdnumpy(file260)
Roc_BeamType_W10_HZ20_Away = rdnumpy(file261)
# ============================ SoilWidth = 20.0 m (HZ = 20)=======================================
# Condition8 = f'{Force_Condition}/W_20m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file262 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ20}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file263 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ20}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file264 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ20}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Roc_Tie_W20_HZ20_Away = rdnumpy(file262)
Roc_LK_W20_HZ20_Away = rdnumpy(file263)
Roc_BeamType_W20_HZ20_Away = rdnumpy(file264)

# ----------------- f = 40HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 40)=======================================
# Condition9 = f'{Force_Condition}/W_2m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file265 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ40}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file266 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ40}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file267 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ40}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Roc_Tie_W2_HZ40_Away = rdnumpy(file265)
Roc_LK_W2_HZ40_Away = rdnumpy(file266)
Roc_BeamType_W2_HZ40_Away = rdnumpy(file267)
# ============================ SoilWidth = 5.0 m (HZ = 40)=======================================
# Condition10 = f'{Force_Condition}/W_5m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file268 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ40}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file269 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ40}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file270 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ40}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Roc_Tie_W5_HZ40_Away = rdnumpy(file268)
Roc_LK_W5_HZ40_Away = rdnumpy(file269)
Roc_BeamType_W5_HZ40_Away = rdnumpy(file270)
# ============================ SoilWidth = 10.0 m (HZ = 40)=======================================
# Condition11 = f'{Force_Condition}/W_10m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file271 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ40}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file272 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ40}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file273 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ40}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Roc_Tie_W10_HZ40_Away = rdnumpy(file271)
Roc_LK_W10_HZ40_Away = rdnumpy(file272)
Roc_BeamType_W10_HZ40_Away = rdnumpy(file273)
# ============================ SoilWidth = 20.0 m (HZ = 40)=======================================
# Condition12 = f'{Force_Condition}/W_20m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file274 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ40}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file275 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ40}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file276 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ40}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Roc_Tie_W20_HZ40_Away = rdnumpy(file274)
Roc_LK_W20_HZ40_Away = rdnumpy(file275)
Roc_BeamType_W20_HZ40_Away = rdnumpy(file276)

# ----------------- f = 80HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 80)=======================================
# Condition13 = f'{Force_Condition}/W_2m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file277 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ80}/Tie_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file278 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ80}/LKDash_Surface_40row/Velocity/node{W2_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file279 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_2mHZ80}/BeamType1_Surface_40row/Velocity/node{W2_Away40row}.out"

Roc_Tie_W2_HZ80_Away = rdnumpy(file277)
Roc_LK_W2_HZ80_Away = rdnumpy(file278)
Roc_BeamType_W2_HZ80_Away = rdnumpy(file279)
# ============================ SoilWidth = 5.0 m (HZ = 80)=======================================
# Condition14 = f'{Force_Condition}/W_5m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file280 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ80}/Tie_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file281 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ80}/LKDash_Surface_40row/Velocity/node{W5_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file282 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_5mHZ80}/BeamType1_Surface_40row/Velocity/node{W5_Away40row}.out"

Roc_Tie_W5_HZ80_Away = rdnumpy(file280)
Roc_LK_W5_HZ80_Away = rdnumpy(file281)
Roc_BeamType_W5_HZ80_Away = rdnumpy(file282)
# ============================ SoilWidth = 10.0 m (HZ = 80)=======================================
# Condition15 = f'{Force_Condition}/W_10m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file283 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ80}/Tie_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file284 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ80}/LKDash_Surface_40row/Velocity/node{W10_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file285 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_10mHZ80}/BeamType1_Surface_40row/Velocity/node{W10_Away40row}.out"

Roc_Tie_W10_HZ80_Away = rdnumpy(file283)
Roc_LK_W10_HZ80_Away = rdnumpy(file284)
Roc_BeamType_W10_HZ80_Away = rdnumpy(file285)
# ============================ SoilWidth = 20.0 m (HZ = 80)=======================================
# Condition16 = f'{Force_Condition}/W_20m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file286 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ80}/Tie_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file287 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ80}/LKDash_Surface_40row/Velocity/node{W20_Away40row}.out"
# --------- Beam Type: Beam Boundary Condition ----------------
file288 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Roc_20mHZ80}/BeamType1_Surface_40row/Velocity/node{W20_Away40row}.out"

Roc_Tie_W20_HZ80_Away = rdnumpy(file286)
Roc_LK_W20_HZ80_Away = rdnumpy(file287)
Roc_BeamType_W20_HZ80_Away = rdnumpy(file288)

# Wave_Vel = 200 # Vertical; Rocking => cp = 400 m/s ; Horizon => cs = 200 m/s

Dy = 0.25 # m
# --------------------- Choose which WaveLength ---------------------------------
Dy_lambP = np.array([Dy/40, Dy/20, Dy/10, Dy/5]) # Horizon: Pwave = 10, 20, 40, 80HZ ==> 400/f
Dy_lambS = np.array([Dy/20, Dy/10, Dy/5, Dy/2.5]) # Vertical/ Rocking: Swave = 10, 20, 40, 80HZ ==> 200/f

# ================================== Prepare Relative Error / Letter Relative Error============================
Ver_Column = 2 # Vertical or Rocking = 2(yaxis)
Hor_Column = 1 # Horizon = 1(xaxis)

# ============ For initial : 0.0 to 0.8 ==================
# ============ FOr Letter reflect wave: 0.2 to 0.8 ===================
start_time = 0.2 # 0.0 / 0.2
end_time = 0.6   # 0.8
def process_column(matrix, start_time, end_time, Column_Index):
    # 选择在指定时间范围内的数据
    time_column = matrix[:, 0]
    column = matrix[:, Column_Index]
    
    # 限定在时间范围内
    within_time_range = (time_column >= start_time) & (time_column <= end_time)
    filtered_column = column[within_time_range]
    
    # 计算绝对值并找出最大值
    abs_filtered_column = np.abs(filtered_column)
    max_peak = np.max(abs_filtered_column)
    max_index = np.argmax(abs_filtered_column)
    
    print(f'max_value= {max_peak}; max_index= {max_index}')
    return max_peak

#======================= Middle Node =======================
# ======================================= Vertical Loading ===================================
# ----------- f = 10 HZ -------------------------
Ver_maxTie2_HZ10 = process_column(Ver_Tie_W2_HZ10, start_time, end_time, Ver_Column)
Ver_maxLK2_HZ10 = process_column(Ver_LK_W2_HZ10, start_time, end_time, Ver_Column)
Ver_maxBeamType2_HZ10 = process_column(Ver_BeamType_W2_HZ10, start_time, end_time, Ver_Column)

Ver_maxTie5_HZ10 = process_column(Ver_Tie_W5_HZ10, start_time, end_time, Ver_Column)
Ver_maxLK5_HZ10 = process_column(Ver_LK_W5_HZ10, start_time, end_time, Ver_Column)
Ver_maxBeamType5_HZ10 = process_column(Ver_BeamType_W5_HZ10, start_time, end_time, Ver_Column)

Ver_maxTie10_HZ10 = process_column(Ver_Tie_W10_HZ10, start_time, end_time, Ver_Column)
Ver_maxLK10_HZ10 = process_column(Ver_LK_W10_HZ10, start_time, end_time, Ver_Column)
Ver_maxBeamType10_HZ10 = process_column(Ver_BeamType_W10_HZ10, start_time, end_time, Ver_Column)

Ver_maxTie20_HZ10 = process_column(Ver_Tie_W20_HZ10, start_time, end_time, Ver_Column)
Ver_maxLK20_HZ10 = process_column(Ver_LK_W20_HZ10, start_time, end_time, Ver_Column)
Ver_maxBeamType20_HZ10 = process_column(Ver_BeamType_W20_HZ10, start_time, end_time, Ver_Column)
# ----------- f = 20 HZ -------------------------
Ver_maxTie2_HZ20 = process_column(Ver_Tie_W2_HZ20, start_time, end_time, Ver_Column)
Ver_maxLK2_HZ20 = process_column(Ver_LK_W2_HZ20, start_time, end_time, Ver_Column)
Ver_maxBeamType2_HZ20 = process_column(Ver_BeamType_W2_HZ20, start_time, end_time, Ver_Column)

Ver_maxTie5_HZ20 = process_column(Ver_Tie_W5_HZ20, start_time, end_time, Ver_Column)
Ver_maxLK5_HZ20 = process_column(Ver_LK_W5_HZ20, start_time, end_time, Ver_Column)
Ver_maxBeamType5_HZ20 = process_column(Ver_BeamType_W5_HZ20, start_time, end_time, Ver_Column)

Ver_maxTie10_HZ20 = process_column(Ver_Tie_W10_HZ20, start_time, end_time, Ver_Column)
Ver_maxLK10_HZ20 = process_column(Ver_LK_W10_HZ20, start_time, end_time, Ver_Column)
Ver_maxBeamType10_HZ20 = process_column(Ver_BeamType_W10_HZ20, start_time, end_time, Ver_Column)

Ver_maxTie20_HZ20 = process_column(Ver_Tie_W20_HZ20, start_time, end_time, Ver_Column)
Ver_maxLK20_HZ20 = process_column(Ver_LK_W20_HZ20, start_time, end_time, Ver_Column)
Ver_maxBeamType20_HZ20 = process_column(Ver_BeamType_W20_HZ20, start_time, end_time, Ver_Column)
# ----------- f = 40 HZ -------------------------
Ver_maxTie2_HZ40 = process_column(Ver_Tie_W2_HZ40, start_time, end_time, Ver_Column)
Ver_maxLK2_HZ40 = process_column(Ver_LK_W2_HZ40, start_time, end_time, Ver_Column)
Ver_maxBeamType2_HZ40 = process_column(Ver_BeamType_W2_HZ40, start_time, end_time, Ver_Column)

Ver_maxTie5_HZ40 = process_column(Ver_Tie_W5_HZ40, start_time, end_time, Ver_Column)
Ver_maxLK5_HZ40 = process_column(Ver_LK_W5_HZ40, start_time, end_time, Ver_Column)
Ver_maxBeamType5_HZ40 = process_column(Ver_BeamType_W5_HZ40, start_time, end_time, Ver_Column)

Ver_maxTie10_HZ40 = process_column(Ver_Tie_W10_HZ40, start_time, end_time, Ver_Column)
Ver_maxLK10_HZ40 = process_column(Ver_LK_W10_HZ40, start_time, end_time, Ver_Column)
Ver_maxBeamType10_HZ40 = process_column(Ver_BeamType_W10_HZ40, start_time, end_time, Ver_Column)

Ver_maxTie20_HZ40 = process_column(Ver_Tie_W20_HZ40, start_time, end_time, Ver_Column)
Ver_maxLK20_HZ40 = process_column(Ver_LK_W20_HZ40, start_time, end_time, Ver_Column)
Ver_maxBeamType20_HZ40 = process_column(Ver_BeamType_W20_HZ40, start_time, end_time, Ver_Column)
# ----------- f = 80 HZ -------------------------
Ver_maxTie2_HZ80 = process_column(Ver_Tie_W2_HZ80, start_time, end_time, Ver_Column)
Ver_maxLK2_HZ80 = process_column(Ver_LK_W2_HZ80, start_time, end_time, Ver_Column)
Ver_maxBeamType2_HZ80 = process_column(Ver_BeamType_W2_HZ80, start_time, end_time, Ver_Column)

Ver_maxTie5_HZ80 = process_column(Ver_Tie_W5_HZ80, start_time, end_time, Ver_Column)
Ver_maxLK5_HZ80 = process_column(Ver_LK_W5_HZ80, start_time, end_time, Ver_Column)
Ver_maxBeamType5_HZ80 = process_column(Ver_BeamType_W5_HZ80, start_time, end_time, Ver_Column)

Ver_maxTie10_HZ80 = process_column(Ver_Tie_W10_HZ80, start_time, end_time, Ver_Column)
Ver_maxLK10_HZ80 = process_column(Ver_LK_W10_HZ80, start_time, end_time, Ver_Column)
Ver_maxBeamType10_HZ80 = process_column(Ver_BeamType_W10_HZ80, start_time, end_time, Ver_Column)

Ver_maxTie20_HZ80 = process_column(Ver_Tie_W20_HZ80, start_time, end_time, Ver_Column)
Ver_maxLK20_HZ80 = process_column(Ver_LK_W20_HZ80, start_time, end_time, Ver_Column)
Ver_maxBeamType20_HZ80 = process_column(Ver_BeamType_W20_HZ80, start_time, end_time, Ver_Column)

# ======================================= Horizon Loading ===================================
# ----------- f = 10 HZ -------------------------
Hor_maxTie2_HZ10 = process_column(Hor_Tie_W2_HZ10, start_time, end_time, Hor_Column)
Hor_maxLK2_HZ10 = process_column(Hor_LK_W2_HZ10, start_time, end_time, Hor_Column)
Hor_maxBeamType2_HZ10 = process_column(Hor_BeamType_W2_HZ10, start_time, end_time, Hor_Column)

Hor_maxTie5_HZ10 = process_column(Hor_Tie_W5_HZ10, start_time, end_time, Hor_Column)
Hor_maxLK5_HZ10 = process_column(Hor_LK_W5_HZ10, start_time, end_time, Hor_Column)
Hor_maxBeamType5_HZ10 = process_column(Hor_BeamType_W5_HZ10, start_time, end_time, Hor_Column)

Hor_maxTie10_HZ10 = process_column(Hor_Tie_W10_HZ10, start_time, end_time, Hor_Column)
Hor_maxLK10_HZ10 = process_column(Hor_LK_W10_HZ10, start_time, end_time, Hor_Column)
Hor_maxBeamType10_HZ10 = process_column(Hor_BeamType_W10_HZ10, start_time, end_time, Hor_Column)

Hor_maxTie20_HZ10 = process_column(Hor_Tie_W20_HZ10, start_time, end_time, Hor_Column)
Hor_maxLK20_HZ10 = process_column(Hor_LK_W20_HZ10, start_time, end_time, Hor_Column)
Hor_maxBeamType20_HZ10 = process_column(Hor_BeamType_W20_HZ10, start_time, end_time, Hor_Column)
# ----------- f = 20 HZ -------------------------
Hor_maxTie2_HZ20 = process_column(Hor_Tie_W2_HZ20, start_time, end_time, Hor_Column)
Hor_maxLK2_HZ20 = process_column(Hor_LK_W2_HZ20, start_time, end_time, Hor_Column)
Hor_maxBeamType2_HZ20 = process_column(Hor_BeamType_W2_HZ20, start_time, end_time, Hor_Column)

Hor_maxTie5_HZ20 = process_column(Hor_Tie_W5_HZ20, start_time, end_time, Hor_Column)
Hor_maxLK5_HZ20 = process_column(Hor_LK_W5_HZ20, start_time, end_time, Hor_Column)
Hor_maxBeamType5_HZ20 = process_column(Hor_BeamType_W5_HZ20, start_time, end_time, Hor_Column)

Hor_maxTie10_HZ20 = process_column(Hor_Tie_W10_HZ20, start_time, end_time, Hor_Column)
Hor_maxLK10_HZ20 = process_column(Hor_LK_W10_HZ20, start_time, end_time, Hor_Column)
Hor_maxBeamType10_HZ20 = process_column(Hor_BeamType_W10_HZ20, start_time, end_time, Hor_Column)

Hor_maxTie20_HZ20 = process_column(Hor_Tie_W20_HZ20, start_time, end_time, Hor_Column)
Hor_maxLK20_HZ20 = process_column(Hor_LK_W20_HZ20, start_time, end_time, Hor_Column)
Hor_maxBeamType20_HZ20 = process_column(Hor_BeamType_W20_HZ20, start_time, end_time, Hor_Column)
# ----------- f = 40 HZ -------------------------
Hor_maxTie2_HZ40 = process_column(Hor_Tie_W2_HZ40, start_time, end_time, Hor_Column)
Hor_maxLK2_HZ40 = process_column(Hor_LK_W2_HZ40, start_time, end_time, Hor_Column)
Hor_maxBeamType2_HZ40 = process_column(Hor_BeamType_W2_HZ40, start_time, end_time, Hor_Column)

Hor_maxTie5_HZ40 = process_column(Hor_Tie_W5_HZ40, start_time, end_time, Hor_Column)
Hor_maxLK5_HZ40 = process_column(Hor_LK_W5_HZ40, start_time, end_time, Hor_Column)
Hor_maxBeamType5_HZ40 = process_column(Hor_BeamType_W5_HZ40, start_time, end_time, Hor_Column)

Hor_maxTie10_HZ40 = process_column(Hor_Tie_W10_HZ40, start_time, end_time, Hor_Column)
Hor_maxLK10_HZ40 = process_column(Hor_LK_W10_HZ40, start_time, end_time, Hor_Column)
Hor_maxBeamType10_HZ40 = process_column(Hor_BeamType_W10_HZ40, start_time, end_time, Hor_Column)

Hor_maxTie20_HZ40 = process_column(Hor_Tie_W20_HZ40, start_time, end_time, Hor_Column)
Hor_maxLK20_HZ40 = process_column(Hor_LK_W20_HZ40, start_time, end_time, Hor_Column)
Hor_maxBeamType20_HZ40 = process_column(Hor_BeamType_W20_HZ40, start_time, end_time, Hor_Column)
# ----------- f = 80 HZ -------------------------
Hor_maxTie2_HZ80 = process_column(Hor_Tie_W2_HZ80, start_time, end_time, Hor_Column)
Hor_maxLK2_HZ80 = process_column(Hor_LK_W2_HZ80, start_time, end_time, Hor_Column)
Hor_maxBeamType2_HZ80 = process_column(Hor_BeamType_W2_HZ80, start_time, end_time, Hor_Column)

Hor_maxTie5_HZ80 = process_column(Hor_Tie_W5_HZ80, start_time, end_time, Hor_Column)
Hor_maxLK5_HZ80 = process_column(Hor_LK_W5_HZ80, start_time, end_time, Hor_Column)
Hor_maxBeamType5_HZ80 = process_column(Hor_BeamType_W5_HZ80, start_time, end_time, Hor_Column)

Hor_maxTie10_HZ80 = process_column(Hor_Tie_W10_HZ80, start_time, end_time, Hor_Column)
Hor_maxLK10_HZ80 = process_column(Hor_LK_W10_HZ80, start_time, end_time, Hor_Column)
Hor_maxBeamType10_HZ80 = process_column(Hor_BeamType_W10_HZ80, start_time, end_time, Hor_Column)

Hor_maxTie20_HZ80 = process_column(Hor_Tie_W20_HZ80, start_time, end_time, Hor_Column)
Hor_maxLK20_HZ80 = process_column(Hor_LK_W20_HZ80, start_time, end_time, Hor_Column)
Hor_maxBeamType20_HZ80 = process_column(Hor_BeamType_W20_HZ80, start_time, end_time, Hor_Column)

# ======================================= Rocking Loading ===================================
# ----------- f = 10 HZ -------------------------
Roc_maxTie2_HZ10 = process_column(Roc_Tie_W2_HZ10, start_time, end_time, Ver_Column)
Roc_maxLK2_HZ10 = process_column(Roc_LK_W2_HZ10, start_time, end_time, Ver_Column)
Roc_maxBeamType2_HZ10 = process_column(Roc_BeamType_W2_HZ10, start_time, end_time, Ver_Column)

Roc_maxTie5_HZ10 = process_column(Roc_Tie_W5_HZ10, start_time, end_time, Ver_Column)
Roc_maxLK5_HZ10 = process_column(Roc_LK_W5_HZ10, start_time, end_time, Ver_Column)
Roc_maxBeamType5_HZ10 = process_column(Roc_BeamType_W5_HZ10, start_time, end_time, Ver_Column)

Roc_maxTie10_HZ10 = process_column(Roc_Tie_W10_HZ10, start_time, end_time, Ver_Column)
Roc_maxLK10_HZ10 = process_column(Roc_LK_W10_HZ10, start_time, end_time, Ver_Column)
Roc_maxBeamType10_HZ10 = process_column(Roc_BeamType_W10_HZ10, start_time, end_time, Ver_Column)

Roc_maxTie20_HZ10 = process_column(Roc_Tie_W20_HZ10, start_time, end_time, Ver_Column)
Roc_maxLK20_HZ10 = process_column(Roc_LK_W20_HZ10, start_time, end_time, Ver_Column)
Roc_maxBeamType20_HZ10 = process_column(Roc_BeamType_W20_HZ10, start_time, end_time, Ver_Column)
# ----------- f = 20 HZ -------------------------
Roc_maxTie2_HZ20 = process_column(Roc_Tie_W2_HZ20, start_time, end_time, Ver_Column)
Roc_maxLK2_HZ20 = process_column(Roc_LK_W2_HZ20, start_time, end_time, Ver_Column)
Roc_maxBeamType2_HZ20 = process_column(Roc_BeamType_W2_HZ20, start_time, end_time, Ver_Column)

Roc_maxTie5_HZ20 = process_column(Roc_Tie_W5_HZ20, start_time, end_time, Ver_Column)
Roc_maxLK5_HZ20 = process_column(Roc_LK_W5_HZ20, start_time, end_time, Ver_Column)
Roc_maxBeamType5_HZ20 = process_column(Roc_BeamType_W5_HZ20, start_time, end_time, Ver_Column)

Roc_maxTie10_HZ20 = process_column(Roc_Tie_W10_HZ20, start_time, end_time, Ver_Column)
Roc_maxLK10_HZ20 = process_column(Roc_LK_W10_HZ20, start_time, end_time, Ver_Column)
Roc_maxBeamType10_HZ20 = process_column(Roc_BeamType_W10_HZ20, start_time, end_time, Ver_Column)

Roc_maxTie20_HZ20 = process_column(Roc_Tie_W20_HZ20, start_time, end_time, Ver_Column)
Roc_maxLK20_HZ20 = process_column(Roc_LK_W20_HZ20, start_time, end_time, Ver_Column)
Roc_maxBeamType20_HZ20 = process_column(Roc_BeamType_W20_HZ20, start_time, end_time, Ver_Column)
# ----------- f = 40 HZ -------------------------
Roc_maxTie2_HZ40 = process_column(Roc_Tie_W2_HZ40, start_time, end_time, Ver_Column)
Roc_maxLK2_HZ40 = process_column(Roc_LK_W2_HZ40, start_time, end_time, Ver_Column)
Roc_maxBeamType2_HZ40 = process_column(Roc_BeamType_W2_HZ40, start_time, end_time, Ver_Column)

Roc_maxTie5_HZ40 = process_column(Roc_Tie_W5_HZ40, start_time, end_time, Ver_Column)
Roc_maxLK5_HZ40 = process_column(Roc_LK_W5_HZ40, start_time, end_time, Ver_Column)
Roc_maxBeamType5_HZ40 = process_column(Roc_BeamType_W5_HZ40, start_time, end_time, Ver_Column)

Roc_maxTie10_HZ40 = process_column(Roc_Tie_W10_HZ40, start_time, end_time, Ver_Column)
Roc_maxLK10_HZ40 = process_column(Roc_LK_W10_HZ40, start_time, end_time, Ver_Column)
Roc_maxBeamType10_HZ40 = process_column(Roc_BeamType_W10_HZ40, start_time, end_time, Ver_Column)

Roc_maxTie20_HZ40 = process_column(Roc_Tie_W20_HZ40, start_time, end_time, Ver_Column)
Roc_maxLK20_HZ40 = process_column(Roc_LK_W20_HZ40, start_time, end_time, Ver_Column)
Roc_maxBeamType20_HZ40 = process_column(Roc_BeamType_W20_HZ40, start_time, end_time, Ver_Column)
# ----------- f = 80 HZ -------------------------
Roc_maxTie2_HZ80 = process_column(Roc_Tie_W2_HZ80, start_time, end_time, Ver_Column)
Roc_maxLK2_HZ80 = process_column(Roc_LK_W2_HZ80, start_time, end_time, Ver_Column)
Roc_maxBeamType2_HZ80 = process_column(Roc_BeamType_W2_HZ80, start_time, end_time, Ver_Column)

Roc_maxTie5_HZ80 = process_column(Roc_Tie_W5_HZ80, start_time, end_time, Ver_Column)
Roc_maxLK5_HZ80 = process_column(Roc_LK_W5_HZ80, start_time, end_time, Ver_Column)
Roc_maxBeamType5_HZ80 = process_column(Roc_BeamType_W5_HZ80, start_time, end_time, Ver_Column)

Roc_maxTie10_HZ80 = process_column(Roc_Tie_W10_HZ80, start_time, end_time, Ver_Column)
Roc_maxLK10_HZ80 = process_column(Roc_LK_W10_HZ80, start_time, end_time, Ver_Column)
Roc_maxBeamType10_HZ80 = process_column(Roc_BeamType_W10_HZ80, start_time, end_time, Ver_Column)

Roc_maxTie20_HZ80 = process_column(Roc_Tie_W20_HZ80, start_time, end_time, Ver_Column)
Roc_maxLK20_HZ80 = process_column(Roc_LK_W20_HZ80, start_time, end_time, Ver_Column)
Roc_maxBeamType20_HZ80 = process_column(Roc_BeamType_W20_HZ80, start_time, end_time, Ver_Column)

# ========================  1m away from Middle Node ==============================
# ======================================= Vertical Loading ===================================
# ----------- f = 10 HZ -------------------------
Ver_maxTie2_HZ10_Away = process_column(Ver_Tie_W2_HZ10_Away, start_time, end_time, Ver_Column)
Ver_maxLK2_HZ10_Away = process_column(Ver_LK_W2_HZ10_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType2_HZ10_Away = process_column(Ver_BeamType_W2_HZ10_Away, start_time, end_time, Ver_Column)

Ver_maxTie5_HZ10_Away = process_column(Ver_Tie_W5_HZ10_Away, start_time, end_time, Ver_Column)
Ver_maxLK5_HZ10_Away = process_column(Ver_LK_W5_HZ10_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType5_HZ10_Away = process_column(Ver_BeamType_W5_HZ10_Away, start_time, end_time, Ver_Column)

Ver_maxTie10_HZ10_Away = process_column(Ver_Tie_W10_HZ10_Away, start_time, end_time, Ver_Column)
Ver_maxLK10_HZ10_Away = process_column(Ver_LK_W10_HZ10_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType10_HZ10_Away = process_column(Ver_BeamType_W10_HZ10_Away, start_time, end_time, Ver_Column)

Ver_maxTie20_HZ10_Away = process_column(Ver_Tie_W20_HZ10_Away, start_time, end_time, Ver_Column)
Ver_maxLK20_HZ10_Away = process_column(Ver_LK_W20_HZ10_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType20_HZ10_Away = process_column(Ver_BeamType_W20_HZ10_Away, start_time, end_time, Ver_Column)
# ----------- f = 20 HZ -------------------------
Ver_maxTie2_HZ20_Away = process_column(Ver_Tie_W2_HZ20_Away, start_time, end_time, Ver_Column)
Ver_maxLK2_HZ20_Away = process_column(Ver_LK_W2_HZ20_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType2_HZ20_Away = process_column(Ver_BeamType_W2_HZ20_Away, start_time, end_time, Ver_Column)

Ver_maxTie5_HZ20_Away = process_column(Ver_Tie_W5_HZ20_Away, start_time, end_time, Ver_Column)
Ver_maxLK5_HZ20_Away = process_column(Ver_LK_W5_HZ20_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType5_HZ20_Away = process_column(Ver_BeamType_W5_HZ20_Away, start_time, end_time, Ver_Column)

Ver_maxTie10_HZ20_Away = process_column(Ver_Tie_W10_HZ20_Away, start_time, end_time, Ver_Column)
Ver_maxLK10_HZ20_Away = process_column(Ver_LK_W10_HZ20_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType10_HZ20_Away = process_column(Ver_BeamType_W10_HZ20_Away, start_time, end_time, Ver_Column)

Ver_maxTie20_HZ20_Away = process_column(Ver_Tie_W20_HZ20_Away, start_time, end_time, Ver_Column)
Ver_maxLK20_HZ20_Away = process_column(Ver_LK_W20_HZ20_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType20_HZ20_Away = process_column(Ver_BeamType_W20_HZ20_Away, start_time, end_time, Ver_Column)
# ----------- f = 40 HZ -------------------------
Ver_maxTie2_HZ40_Away = process_column(Ver_Tie_W2_HZ40_Away, start_time, end_time, Ver_Column)
Ver_maxLK2_HZ40_Away = process_column(Ver_LK_W2_HZ40_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType2_HZ40_Away = process_column(Ver_BeamType_W2_HZ40_Away, start_time, end_time, Ver_Column)

Ver_maxTie5_HZ40_Away = process_column(Ver_Tie_W5_HZ40_Away, start_time, end_time, Ver_Column)
Ver_maxLK5_HZ40_Away = process_column(Ver_LK_W5_HZ40_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType5_HZ40_Away = process_column(Ver_BeamType_W5_HZ40_Away, start_time, end_time, Ver_Column)

Ver_maxTie10_HZ40_Away = process_column(Ver_Tie_W10_HZ40_Away, start_time, end_time, Ver_Column)
Ver_maxLK10_HZ40_Away = process_column(Ver_LK_W10_HZ40_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType10_HZ40_Away = process_column(Ver_BeamType_W10_HZ40_Away, start_time, end_time, Ver_Column)

Ver_maxTie20_HZ40_Away = process_column(Ver_Tie_W20_HZ40_Away, start_time, end_time, Ver_Column)
Ver_maxLK20_HZ40_Away = process_column(Ver_LK_W20_HZ40_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType20_HZ40_Away = process_column(Ver_BeamType_W20_HZ40_Away, start_time, end_time, Ver_Column)
# ----------- f = 80 HZ -------------------------
Ver_maxTie2_HZ80_Away = process_column(Ver_Tie_W2_HZ80_Away, start_time, end_time, Ver_Column)
Ver_maxLK2_HZ80_Away = process_column(Ver_LK_W2_HZ80_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType2_HZ80_Away = process_column(Ver_BeamType_W2_HZ80_Away, start_time, end_time, Ver_Column)

Ver_maxTie5_HZ80_Away = process_column(Ver_Tie_W5_HZ80_Away, start_time, end_time, Ver_Column)
Ver_maxLK5_HZ80_Away = process_column(Ver_LK_W5_HZ80_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType5_HZ80_Away = process_column(Ver_BeamType_W5_HZ80_Away, start_time, end_time, Ver_Column)

Ver_maxTie10_HZ80_Away = process_column(Ver_Tie_W10_HZ80_Away, start_time, end_time, Ver_Column)
Ver_maxLK10_HZ80_Away = process_column(Ver_LK_W10_HZ80_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType10_HZ80_Away = process_column(Ver_BeamType_W10_HZ80_Away, start_time, end_time, Ver_Column)

Ver_maxTie20_HZ80_Away = process_column(Ver_Tie_W20_HZ80_Away, start_time, end_time, Ver_Column)
Ver_maxLK20_HZ80_Away = process_column(Ver_LK_W20_HZ80_Away, start_time, end_time, Ver_Column)
Ver_maxBeamType20_HZ80_Away = process_column(Ver_BeamType_W20_HZ80_Away, start_time, end_time, Ver_Column)

# ======================================= Horizon Loading ===================================
# ----------- f = 10 HZ -------------------------
Hor_maxTie2_HZ10_Away = process_column(Hor_Tie_W2_HZ10_Away, start_time, end_time, Hor_Column)
Hor_maxLK2_HZ10_Away = process_column(Hor_LK_W2_HZ10_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType2_HZ10_Away = process_column(Hor_BeamType_W2_HZ10_Away, start_time, end_time, Hor_Column)

Hor_maxTie5_HZ10_Away = process_column(Hor_Tie_W5_HZ10_Away, start_time, end_time, Hor_Column)
Hor_maxLK5_HZ10_Away = process_column(Hor_LK_W5_HZ10_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType5_HZ10_Away = process_column(Hor_BeamType_W5_HZ10_Away, start_time, end_time, Hor_Column)

Hor_maxTie10_HZ10_Away = process_column(Hor_Tie_W10_HZ10_Away, start_time, end_time, Hor_Column)
Hor_maxLK10_HZ10_Away = process_column(Hor_LK_W10_HZ10_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType10_HZ10_Away = process_column(Hor_BeamType_W10_HZ10_Away, start_time, end_time, Hor_Column)

Hor_maxTie20_HZ10_Away = process_column(Hor_Tie_W20_HZ10_Away, start_time, end_time, Hor_Column)
Hor_maxLK20_HZ10_Away = process_column(Hor_LK_W20_HZ10_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType20_HZ10_Away = process_column(Hor_BeamType_W20_HZ10_Away, start_time, end_time, Hor_Column)
# ----------- f = 20 HZ -------------------------
Hor_maxTie2_HZ20_Away = process_column(Hor_Tie_W2_HZ20_Away, start_time, end_time, Hor_Column)
Hor_maxLK2_HZ20_Away = process_column(Hor_LK_W2_HZ20_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType2_HZ20_Away = process_column(Hor_BeamType_W2_HZ20_Away, start_time, end_time, Hor_Column)

Hor_maxTie5_HZ20_Away = process_column(Hor_Tie_W5_HZ20_Away, start_time, end_time, Hor_Column)
Hor_maxLK5_HZ20_Away = process_column(Hor_LK_W5_HZ20_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType5_HZ20_Away = process_column(Hor_BeamType_W5_HZ20_Away, start_time, end_time, Hor_Column)

Hor_maxTie10_HZ20_Away = process_column(Hor_Tie_W10_HZ20_Away, start_time, end_time, Hor_Column)
Hor_maxLK10_HZ20_Away = process_column(Hor_LK_W10_HZ20_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType10_HZ20_Away = process_column(Hor_BeamType_W10_HZ20_Away, start_time, end_time, Hor_Column)

Hor_maxTie20_HZ20_Away = process_column(Hor_Tie_W20_HZ20_Away, start_time, end_time, Hor_Column)
Hor_maxLK20_HZ20_Away = process_column(Hor_LK_W20_HZ20_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType20_HZ20_Away = process_column(Hor_BeamType_W20_HZ20_Away, start_time, end_time, Hor_Column)
# ----------- f = 40 HZ -------------------------
Hor_maxTie2_HZ40_Away = process_column(Hor_Tie_W2_HZ40_Away, start_time, end_time, Hor_Column)
Hor_maxLK2_HZ40_Away = process_column(Hor_LK_W2_HZ40_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType2_HZ40_Away = process_column(Hor_BeamType_W2_HZ40_Away, start_time, end_time, Hor_Column)

Hor_maxTie5_HZ40_Away = process_column(Hor_Tie_W5_HZ40_Away, start_time, end_time, Hor_Column)
Hor_maxLK5_HZ40_Away = process_column(Hor_LK_W5_HZ40_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType5_HZ40_Away = process_column(Hor_BeamType_W5_HZ40_Away, start_time, end_time, Hor_Column)

Hor_maxTie10_HZ40_Away = process_column(Hor_Tie_W10_HZ40_Away, start_time, end_time, Hor_Column)
Hor_maxLK10_HZ40_Away = process_column(Hor_LK_W10_HZ40_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType10_HZ40_Away = process_column(Hor_BeamType_W10_HZ40_Away, start_time, end_time, Hor_Column)

Hor_maxTie20_HZ40_Away = process_column(Hor_Tie_W20_HZ40_Away, start_time, end_time, Hor_Column)
Hor_maxLK20_HZ40_Away = process_column(Hor_LK_W20_HZ40_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType20_HZ40_Away = process_column(Hor_BeamType_W20_HZ40_Away, start_time, end_time, Hor_Column)
# ----------- f = 80 HZ -------------------------
Hor_maxTie2_HZ80_Away = process_column(Hor_Tie_W2_HZ80_Away, start_time, end_time, Hor_Column)
Hor_maxLK2_HZ80_Away = process_column(Hor_LK_W2_HZ80_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType2_HZ80_Away = process_column(Hor_BeamType_W2_HZ80_Away, start_time, end_time, Hor_Column)

Hor_maxTie5_HZ80_Away = process_column(Hor_Tie_W5_HZ80_Away, start_time, end_time, Hor_Column)
Hor_maxLK5_HZ80_Away = process_column(Hor_LK_W5_HZ80_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType5_HZ80_Away = process_column(Hor_BeamType_W5_HZ80_Away, start_time, end_time, Hor_Column)

Hor_maxTie10_HZ80_Away = process_column(Hor_Tie_W10_HZ80_Away, start_time, end_time, Hor_Column)
Hor_maxLK10_HZ80_Away = process_column(Hor_LK_W10_HZ80_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType10_HZ80_Away = process_column(Hor_BeamType_W10_HZ80_Away, start_time, end_time, Hor_Column)

Hor_maxTie20_HZ80_Away = process_column(Hor_Tie_W20_HZ80_Away, start_time, end_time, Hor_Column)
Hor_maxLK20_HZ80_Away = process_column(Hor_LK_W20_HZ80_Away, start_time, end_time, Hor_Column)
Hor_maxBeamType20_HZ80_Away = process_column(Hor_BeamType_W20_HZ80_Away, start_time, end_time, Hor_Column)

# ======================================= Rocking Loading ===================================
# ----------- f = 10 HZ -------------------------
Roc_maxTie2_HZ10_Away = process_column(Roc_Tie_W2_HZ10_Away, start_time, end_time, Ver_Column)
Roc_maxLK2_HZ10_Away = process_column(Roc_LK_W2_HZ10_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType2_HZ10_Away = process_column(Roc_BeamType_W2_HZ10_Away, start_time, end_time, Ver_Column)

Roc_maxTie5_HZ10_Away = process_column(Roc_Tie_W5_HZ10_Away, start_time, end_time, Ver_Column)
Roc_maxLK5_HZ10_Away = process_column(Roc_LK_W5_HZ10_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType5_HZ10_Away = process_column(Roc_BeamType_W5_HZ10_Away, start_time, end_time, Ver_Column)

Roc_maxTie10_HZ10_Away = process_column(Roc_Tie_W10_HZ10_Away, start_time, end_time, Ver_Column)
Roc_maxLK10_HZ10_Away = process_column(Roc_LK_W10_HZ10_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType10_HZ10_Away = process_column(Roc_BeamType_W10_HZ10_Away, start_time, end_time, Ver_Column)

Roc_maxTie20_HZ10_Away = process_column(Roc_Tie_W20_HZ10_Away, start_time, end_time, Ver_Column)
Roc_maxLK20_HZ10_Away = process_column(Roc_LK_W20_HZ10_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType20_HZ10_Away = process_column(Roc_BeamType_W20_HZ10_Away, start_time, end_time, Ver_Column)
# ----------- f = 20 HZ -------------------------
Roc_maxTie2_HZ20_Away = process_column(Roc_Tie_W2_HZ20_Away, start_time, end_time, Ver_Column)
Roc_maxLK2_HZ20_Away = process_column(Roc_LK_W2_HZ20_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType2_HZ20_Away = process_column(Roc_BeamType_W2_HZ20_Away, start_time, end_time, Ver_Column)

Roc_maxTie5_HZ20_Away = process_column(Roc_Tie_W5_HZ20_Away, start_time, end_time, Ver_Column)
Roc_maxLK5_HZ20_Away = process_column(Roc_LK_W5_HZ20_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType5_HZ20_Away = process_column(Roc_BeamType_W5_HZ20_Away, start_time, end_time, Ver_Column)

Roc_maxTie10_HZ20_Away = process_column(Roc_Tie_W10_HZ20_Away, start_time, end_time, Ver_Column)
Roc_maxLK10_HZ20_Away = process_column(Roc_LK_W10_HZ20_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType10_HZ20_Away = process_column(Roc_BeamType_W10_HZ20_Away, start_time, end_time, Ver_Column)

Roc_maxTie20_HZ20_Away = process_column(Roc_Tie_W20_HZ20_Away, start_time, end_time, Ver_Column)
Roc_maxLK20_HZ20_Away = process_column(Roc_LK_W20_HZ20_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType20_HZ20_Away = process_column(Roc_BeamType_W20_HZ20_Away, start_time, end_time, Ver_Column)
# ----------- f = 40 HZ -------------------------
Roc_maxTie2_HZ40_Away = process_column(Roc_Tie_W2_HZ40_Away, start_time, end_time, Ver_Column)
Roc_maxLK2_HZ40_Away = process_column(Roc_LK_W2_HZ40_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType2_HZ40_Away = process_column(Roc_BeamType_W2_HZ40_Away, start_time, end_time, Ver_Column)

Roc_maxTie5_HZ40_Away = process_column(Roc_Tie_W5_HZ40_Away, start_time, end_time, Ver_Column)
Roc_maxLK5_HZ40_Away = process_column(Roc_LK_W5_HZ40_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType5_HZ40_Away = process_column(Roc_BeamType_W5_HZ40_Away, start_time, end_time, Ver_Column)

Roc_maxTie10_HZ40_Away = process_column(Roc_Tie_W10_HZ40_Away, start_time, end_time, Ver_Column)
Roc_maxLK10_HZ40_Away = process_column(Roc_LK_W10_HZ40_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType10_HZ40_Away = process_column(Roc_BeamType_W10_HZ40_Away, start_time, end_time, Ver_Column)

Roc_maxTie20_HZ40_Away = process_column(Roc_Tie_W20_HZ40_Away, start_time, end_time, Ver_Column)
Roc_maxLK20_HZ40_Away = process_column(Roc_LK_W20_HZ40_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType20_HZ40_Away = process_column(Roc_BeamType_W20_HZ40_Away, start_time, end_time, Ver_Column)
# ----------- f = 80 HZ -------------------------
Roc_maxTie2_HZ80_Away = process_column(Roc_Tie_W2_HZ80_Away, start_time, end_time, Ver_Column)
Roc_maxLK2_HZ80_Away = process_column(Roc_LK_W2_HZ80_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType2_HZ80_Away = process_column(Roc_BeamType_W2_HZ80_Away, start_time, end_time, Ver_Column)

Roc_maxTie5_HZ80_Away = process_column(Roc_Tie_W5_HZ80_Away, start_time, end_time, Ver_Column)
Roc_maxLK5_HZ80_Away = process_column(Roc_LK_W5_HZ80_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType5_HZ80_Away = process_column(Roc_BeamType_W5_HZ80_Away, start_time, end_time, Ver_Column)

Roc_maxTie10_HZ80_Away = process_column(Roc_Tie_W10_HZ80_Away, start_time, end_time, Ver_Column)
Roc_maxLK10_HZ80_Away = process_column(Roc_LK_W10_HZ80_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType10_HZ80_Away = process_column(Roc_BeamType_W10_HZ80_Away, start_time, end_time, Ver_Column)

Roc_maxTie20_HZ80_Away = process_column(Roc_Tie_W20_HZ80_Away, start_time, end_time, Ver_Column)
Roc_maxLK20_HZ80_Away = process_column(Roc_LK_W20_HZ80_Away, start_time, end_time, Ver_Column)
Roc_maxBeamType20_HZ80_Away = process_column(Roc_BeamType_W20_HZ80_Away, start_time, end_time, Ver_Column)

Frequency_Size = np.array([1/10, 1/20, 1/40, 1/80])
def errMatrix(error_dc, maxTie2_HZ10, maxTie2_HZ20, maxTie2_HZ40, maxTie2_HZ80):
    error_dc[:,0] = Frequency_Size[:]
    error_dc[0,1] = maxTie2_HZ10
    error_dc[1,1] = maxTie2_HZ20
    error_dc[2,1] = maxTie2_HZ40
    error_dc[3,1] = maxTie2_HZ80
    return error_dc

# ============================= Middle Node ========================================
# ======================================= Vertical Loading ===================================
# ------------W20m Error Peak Value-----------------------
Ver_Tie20_error = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_Tie20_error, Ver_maxTie20_HZ10, Ver_maxTie20_HZ20, Ver_maxTie20_HZ40, Ver_maxTie20_HZ80)

Ver_LK20_error = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_LK20_error, Ver_maxLK20_HZ10, Ver_maxLK20_HZ20, Ver_maxLK20_HZ40, Ver_maxLK20_HZ80)

Ver_BeamType_20error = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_BeamType_20error, Ver_maxBeamType20_HZ10, Ver_maxBeamType20_HZ20, Ver_maxBeamType20_HZ40, Ver_maxBeamType20_HZ80)
# ------------W10m Error Peak Value-----------------------
Ver_Tie10_error = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_Tie10_error, Ver_maxTie10_HZ10, Ver_maxTie10_HZ20, Ver_maxTie10_HZ40, Ver_maxTie10_HZ80)

Ver_LK10_error = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_LK10_error, Ver_maxLK10_HZ10, Ver_maxLK10_HZ20, Ver_maxLK10_HZ40, Ver_maxLK10_HZ80)

Ver_BeamType_10error = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_BeamType_10error, Ver_maxBeamType10_HZ10, Ver_maxBeamType10_HZ20, Ver_maxBeamType10_HZ40, Ver_maxBeamType10_HZ80)
# ------------W5m Error Peak Value-----------------------
Ver_Tie5_error = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_Tie5_error, Ver_maxTie5_HZ10, Ver_maxTie5_HZ20, Ver_maxTie5_HZ40, Ver_maxTie5_HZ80)

Ver_LK5_error = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_LK5_error, Ver_maxLK5_HZ10, Ver_maxLK5_HZ20, Ver_maxLK5_HZ40, Ver_maxLK5_HZ80)

Ver_BeamType_5error = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_BeamType_5error, Ver_maxBeamType5_HZ10, Ver_maxBeamType5_HZ20, Ver_maxBeamType5_HZ40, Ver_maxBeamType5_HZ80)
# ------------W2m Error Peak Value-----------------------
Ver_Tie2_error = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_Tie2_error, Ver_maxTie2_HZ10, Ver_maxTie2_HZ20, Ver_maxTie2_HZ40, Ver_maxTie2_HZ80)

Ver_LK2_error = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_LK2_error, Ver_maxLK2_HZ10, Ver_maxLK2_HZ20, Ver_maxLK2_HZ40, Ver_maxLK2_HZ80)

Ver_BeamType_2error = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_BeamType_2error, Ver_maxBeamType2_HZ10, Ver_maxBeamType2_HZ20, Ver_maxBeamType2_HZ40, Ver_maxBeamType2_HZ80)

# ======================================= Horizon Loading ===================================
# ------------W20m Error Peak Value-----------------------
Hor_Tie20_error = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_Tie20_error, Hor_maxTie20_HZ10, Hor_maxTie20_HZ20, Hor_maxTie20_HZ40, Hor_maxTie20_HZ80)

Hor_LK20_error = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_LK20_error, Hor_maxLK20_HZ10, Hor_maxLK20_HZ20, Hor_maxLK20_HZ40, Hor_maxLK20_HZ80)

Hor_BeamType_20error = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_BeamType_20error, Hor_maxBeamType20_HZ10, Hor_maxBeamType20_HZ20, Hor_maxBeamType20_HZ40, Hor_maxBeamType20_HZ80)
# ------------W10m Error Peak Value-----------------------
Hor_Tie10_error = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_Tie10_error, Hor_maxTie10_HZ10, Hor_maxTie10_HZ20, Hor_maxTie10_HZ40, Hor_maxTie10_HZ80)

Hor_LK10_error = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_LK10_error, Hor_maxLK10_HZ10, Hor_maxLK10_HZ20, Hor_maxLK10_HZ40, Hor_maxLK10_HZ80)

Hor_BeamType_10error = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_BeamType_10error, Hor_maxBeamType10_HZ10, Hor_maxBeamType10_HZ20, Hor_maxBeamType10_HZ40, Hor_maxBeamType10_HZ80)
# ------------W5m Error Peak Value-----------------------
Hor_Tie5_error = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_Tie5_error, Hor_maxTie5_HZ10, Hor_maxTie5_HZ20, Hor_maxTie5_HZ40, Hor_maxTie5_HZ80)

Hor_LK5_error = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_LK5_error, Hor_maxLK5_HZ10, Hor_maxLK5_HZ20, Hor_maxLK5_HZ40, Hor_maxLK5_HZ80)

Hor_BeamType_5error = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_BeamType_5error, Hor_maxBeamType5_HZ10, Hor_maxBeamType5_HZ20, Hor_maxBeamType5_HZ40, Hor_maxBeamType5_HZ80)
# ------------W2m Error Peak Value-----------------------
Hor_Tie2_error = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_Tie2_error, Hor_maxTie2_HZ10, Hor_maxTie2_HZ20, Hor_maxTie2_HZ40, Hor_maxTie2_HZ80)

Hor_LK2_error = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_LK2_error, Hor_maxLK2_HZ10, Hor_maxLK2_HZ20, Hor_maxLK2_HZ40, Hor_maxLK2_HZ80)

Hor_BeamType_2error = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_BeamType_2error, Hor_maxBeamType2_HZ10, Hor_maxBeamType2_HZ20, Hor_maxBeamType2_HZ40, Hor_maxBeamType2_HZ80)

# ======================================= Rocking Loading ===================================
# ------------W20m Error Peak Value-----------------------
Roc_Tie20_error = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_Tie20_error, Roc_maxTie20_HZ10, Roc_maxTie20_HZ20, Roc_maxTie20_HZ40, Roc_maxTie20_HZ80)

Roc_LK20_error = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_LK20_error, Roc_maxLK20_HZ10, Roc_maxLK20_HZ20, Roc_maxLK20_HZ40, Roc_maxLK20_HZ80)

Roc_BeamType_20error = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_BeamType_20error, Roc_maxBeamType20_HZ10, Roc_maxBeamType20_HZ20, Roc_maxBeamType20_HZ40, Roc_maxBeamType20_HZ80)
# ------------W10m Error Peak Value-----------------------
Roc_Tie10_error = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_Tie10_error, Roc_maxTie10_HZ10, Roc_maxTie10_HZ20, Roc_maxTie10_HZ40, Roc_maxTie10_HZ80)

Roc_LK10_error = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_LK10_error, Roc_maxLK10_HZ10, Roc_maxLK10_HZ20, Roc_maxLK10_HZ40, Roc_maxLK10_HZ80)

Roc_BeamType_10error = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_BeamType_10error, Roc_maxBeamType10_HZ10, Roc_maxBeamType10_HZ20, Roc_maxBeamType10_HZ40, Roc_maxBeamType10_HZ80)
# ------------W5m Error Peak Value-----------------------
Roc_Tie5_error = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_Tie5_error, Roc_maxTie5_HZ10, Roc_maxTie5_HZ20, Roc_maxTie5_HZ40, Roc_maxTie5_HZ80)

Roc_LK5_error = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_LK5_error, Roc_maxLK5_HZ10, Roc_maxLK5_HZ20, Roc_maxLK5_HZ40, Roc_maxLK5_HZ80)

Roc_BeamType_5error = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_BeamType_5error, Roc_maxBeamType5_HZ10, Roc_maxBeamType5_HZ20, Roc_maxBeamType5_HZ40, Roc_maxBeamType5_HZ80)
# ------------W2m Error Peak Value-----------------------
Roc_Tie2_error = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_Tie2_error, Roc_maxTie2_HZ10, Roc_maxTie2_HZ20, Roc_maxTie2_HZ40, Roc_maxTie2_HZ80)

Roc_LK2_error = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_LK2_error, Roc_maxLK2_HZ10, Roc_maxLK2_HZ20, Roc_maxLK2_HZ40, Roc_maxLK2_HZ80)

Roc_BeamType_2error = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_BeamType_2error, Roc_maxBeamType2_HZ10, Roc_maxBeamType2_HZ20, Roc_maxBeamType2_HZ40, Roc_maxBeamType2_HZ80)

# ========================  1m away from Middle Node ==============================
# ======================================= Vertical Loading ===================================
# ------------W20m Error Peak Value-----------------------
Ver_Tie20_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_Tie20_error_Away, Ver_maxTie20_HZ10_Away, Ver_maxTie20_HZ20_Away, Ver_maxTie20_HZ40_Away, Ver_maxTie20_HZ80_Away)

Ver_LK20_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_LK20_error_Away, Ver_maxLK20_HZ10_Away, Ver_maxLK20_HZ20_Away, Ver_maxLK20_HZ40_Away, Ver_maxLK20_HZ80_Away)

Ver_BeamType_20error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_BeamType_20error_Away, Ver_maxBeamType20_HZ10_Away, Ver_maxBeamType20_HZ20_Away, Ver_maxBeamType20_HZ40_Away, Ver_maxBeamType20_HZ80_Away)
# ------------W10m Error Peak Value-----------------------
Ver_Tie10_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_Tie10_error_Away, Ver_maxTie10_HZ10_Away, Ver_maxTie10_HZ20_Away, Ver_maxTie10_HZ40_Away, Ver_maxTie10_HZ80_Away)

Ver_LK10_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_LK10_error_Away, Ver_maxLK10_HZ10_Away, Ver_maxLK10_HZ20_Away, Ver_maxLK10_HZ40_Away, Ver_maxLK10_HZ80_Away)

Ver_BeamType_10error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_BeamType_10error_Away, Ver_maxBeamType10_HZ10_Away, Ver_maxBeamType10_HZ20_Away, Ver_maxBeamType10_HZ40_Away, Ver_maxBeamType10_HZ80_Away)
# ------------W5m Error Peak Value-----------------------
Ver_Tie5_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_Tie5_error_Away, Ver_maxTie5_HZ10_Away, Ver_maxTie5_HZ20_Away, Ver_maxTie5_HZ40_Away, Ver_maxTie5_HZ80_Away)

Ver_LK5_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_LK5_error_Away, Ver_maxLK5_HZ10_Away, Ver_maxLK5_HZ20_Away, Ver_maxLK5_HZ40_Away, Ver_maxLK5_HZ80_Away)

Ver_BeamType_5error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_BeamType_5error_Away, Ver_maxBeamType5_HZ10_Away, Ver_maxBeamType5_HZ20_Away, Ver_maxBeamType5_HZ40_Away, Ver_maxBeamType5_HZ80_Away)
# ------------W2m Error Peak Value-----------------------
Ver_Tie2_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_Tie2_error_Away, Ver_maxTie2_HZ10_Away, Ver_maxTie2_HZ20_Away, Ver_maxTie2_HZ40_Away, Ver_maxTie2_HZ80_Away)

Ver_LK2_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_LK2_error_Away, Ver_maxLK2_HZ10_Away, Ver_maxLK2_HZ20_Away, Ver_maxLK2_HZ40_Away, Ver_maxLK2_HZ80_Away)

Ver_BeamType_2error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Ver_BeamType_2error_Away, Ver_maxBeamType2_HZ10_Away, Ver_maxBeamType2_HZ20_Away, Ver_maxBeamType2_HZ40_Away, Ver_maxBeamType2_HZ80_Away)

# ======================================= Horizon Loading ===================================
# ------------W20m Error Peak Value-----------------------
Hor_Tie20_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_Tie20_error_Away, Hor_maxTie20_HZ10_Away, Hor_maxTie20_HZ20_Away, Hor_maxTie20_HZ40_Away, Hor_maxTie20_HZ80_Away)

Hor_LK20_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_LK20_error_Away, Hor_maxLK20_HZ10_Away, Hor_maxLK20_HZ20_Away, Hor_maxLK20_HZ40_Away, Hor_maxLK20_HZ80_Away)

Hor_BeamType_20error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_BeamType_20error_Away, Hor_maxBeamType20_HZ10_Away, Hor_maxBeamType20_HZ20_Away, Hor_maxBeamType20_HZ40_Away, Hor_maxBeamType20_HZ80_Away)
# ------------W10m Error Peak Value-----------------------
Hor_Tie10_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_Tie10_error_Away, Hor_maxTie10_HZ10_Away, Hor_maxTie10_HZ20_Away, Hor_maxTie10_HZ40_Away, Hor_maxTie10_HZ80_Away)

Hor_LK10_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_LK10_error_Away, Hor_maxLK10_HZ10_Away, Hor_maxLK10_HZ20_Away, Hor_maxLK10_HZ40_Away, Hor_maxLK10_HZ80_Away)

Hor_BeamType_10error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_BeamType_10error_Away, Hor_maxBeamType10_HZ10_Away, Hor_maxBeamType10_HZ20_Away, Hor_maxBeamType10_HZ40_Away, Hor_maxBeamType10_HZ80_Away)
# ------------W5m Error Peak Value-----------------------
Hor_Tie5_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_Tie5_error_Away, Hor_maxTie5_HZ10_Away, Hor_maxTie5_HZ20_Away, Hor_maxTie5_HZ40_Away, Hor_maxTie5_HZ80_Away)

Hor_LK5_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_LK5_error_Away, Hor_maxLK5_HZ10_Away, Hor_maxLK5_HZ20_Away, Hor_maxLK5_HZ40_Away, Hor_maxLK5_HZ80_Away)

Hor_BeamType_5error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_BeamType_5error_Away, Hor_maxBeamType5_HZ10_Away, Hor_maxBeamType5_HZ20_Away, Hor_maxBeamType5_HZ40_Away, Hor_maxBeamType5_HZ80_Away)
# ------------W2m Error Peak Value-----------------------
Hor_Tie2_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_Tie2_error_Away, Hor_maxTie2_HZ10_Away, Hor_maxTie2_HZ20_Away, Hor_maxTie2_HZ40_Away, Hor_maxTie2_HZ80_Away)

Hor_LK2_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_LK2_error_Away, Hor_maxLK2_HZ10_Away, Hor_maxLK2_HZ20_Away, Hor_maxLK2_HZ40_Away, Hor_maxLK2_HZ80_Away)

Hor_BeamType_2error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Hor_BeamType_2error_Away, Hor_maxBeamType2_HZ10_Away, Hor_maxBeamType2_HZ20_Away, Hor_maxBeamType2_HZ40_Away, Hor_maxBeamType2_HZ80_Away)

# ======================================= Rocking Loading ===================================
# ------------W20m Error Peak Value-----------------------
Roc_Tie20_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_Tie20_error_Away, Roc_maxTie20_HZ10_Away, Roc_maxTie20_HZ20_Away, Roc_maxTie20_HZ40_Away, Roc_maxTie20_HZ80_Away)

Roc_LK20_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_LK20_error_Away, Roc_maxLK20_HZ10_Away, Roc_maxLK20_HZ20_Away, Roc_maxLK20_HZ40_Away, Roc_maxLK20_HZ80_Away)

Roc_BeamType_20error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_BeamType_20error_Away, Roc_maxBeamType20_HZ10_Away, Roc_maxBeamType20_HZ20_Away, Roc_maxBeamType20_HZ40_Away, Roc_maxBeamType20_HZ80_Away)
# ------------W10m Error Peak Value-----------------------
Roc_Tie10_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_Tie10_error_Away, Roc_maxTie10_HZ10_Away, Roc_maxTie10_HZ20_Away, Roc_maxTie10_HZ40_Away, Roc_maxTie10_HZ80_Away)

Roc_LK10_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_LK10_error_Away, Roc_maxLK10_HZ10_Away, Roc_maxLK10_HZ20_Away, Roc_maxLK10_HZ40_Away, Roc_maxLK10_HZ80_Away)

Roc_BeamType_10error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_BeamType_10error_Away, Roc_maxBeamType10_HZ10_Away, Roc_maxBeamType10_HZ20_Away, Roc_maxBeamType10_HZ40_Away, Roc_maxBeamType10_HZ80_Away)
# ------------W5m Error Peak Value-----------------------
Roc_Tie5_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_Tie5_error_Away, Roc_maxTie5_HZ10_Away, Roc_maxTie5_HZ20_Away, Roc_maxTie5_HZ40_Away, Roc_maxTie5_HZ80_Away)

Roc_LK5_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_LK5_error_Away, Roc_maxLK5_HZ10_Away, Roc_maxLK5_HZ20_Away, Roc_maxLK5_HZ40_Away, Roc_maxLK5_HZ80_Away)

Roc_BeamType_5error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_BeamType_5error_Away, Roc_maxBeamType5_HZ10_Away, Roc_maxBeamType5_HZ20_Away, Roc_maxBeamType5_HZ40_Away, Roc_maxBeamType5_HZ80_Away)
# ------------W2m Error Peak Value-----------------------
Roc_Tie2_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_Tie2_error_Away, Roc_maxTie2_HZ10_Away, Roc_maxTie2_HZ20_Away, Roc_maxTie2_HZ40_Away, Roc_maxTie2_HZ80_Away)

Roc_LK2_error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_LK2_error_Away, Roc_maxLK2_HZ10_Away, Roc_maxLK2_HZ20_Away, Roc_maxLK2_HZ40_Away, Roc_maxLK2_HZ80_Away)

Roc_BeamType_2error_Away = np.zeros((len(Frequency_Size),2))
errMatrix(Roc_BeamType_2error_Away, Roc_maxBeamType2_HZ10_Away, Roc_maxBeamType2_HZ20_Away, Roc_maxBeamType2_HZ40_Away, Roc_maxBeamType2_HZ80_Away)


#  -------------------------------------------------- Calculate Relative Error --------------------------------------------------------
def Peak_Theory_max(matrix, Column_Index):
    # 选择在指定时间范围内的数据
    time_column = matrix[:, 0]
    column = matrix[:, Column_Index]
    
    # 限定在时间范围内
    within_time_range = (time_column >= 0.0) & (time_column <= 0.2)
    filtered_column = column[within_time_range]
    
    # 计算绝对值并找出最大值
    abs_filtered_column = np.abs(filtered_column)
    max_peak = np.max(abs_filtered_column)
    max_index = np.argmax(abs_filtered_column)
    
    print(f'max_value= {max_peak}; max_index= {max_index}')
    return max_peak

#-------------- Use LK Dashpot as Analysis theory solution ------------------------
Ver_maxAnaly_HZ10 = Peak_Theory_max(Ver_LK_W20_HZ10, Ver_Column) # Ver_maxLK20_HZ10
Ver_maxAnaly_HZ20 = Peak_Theory_max(Ver_LK_W20_HZ20, Ver_Column)# Ver_maxLK20_HZ20
Ver_maxAnaly_HZ40 = Peak_Theory_max(Ver_LK_W20_HZ40, Ver_Column)
Ver_maxAnaly_HZ80 = Peak_Theory_max(Ver_LK_W20_HZ80, Ver_Column)

Hor_maxAnaly_HZ10 = Peak_Theory_max(Hor_LK_W20_HZ10, Hor_Column)# Hor_maxLK20_HZ10
Hor_maxAnaly_HZ20 = Peak_Theory_max(Hor_LK_W20_HZ20, Hor_Column)# Hor_maxLK20_HZ20
Hor_maxAnaly_HZ40 = Peak_Theory_max(Hor_LK_W20_HZ40, Hor_Column)
Hor_maxAnaly_HZ80 = Peak_Theory_max(Hor_LK_W20_HZ80, Hor_Column)

Roc_maxAnaly_HZ10 = Peak_Theory_max(Roc_LK_W20_HZ10, Ver_Column)# Roc_maxLK20_HZ10
Roc_maxAnaly_HZ20 = Peak_Theory_max(Roc_LK_W20_HZ20, Ver_Column)# Roc_maxLK20_HZ20
Roc_maxAnaly_HZ40 = Peak_Theory_max(Roc_LK_W20_HZ40, Ver_Column)
Roc_maxAnaly_HZ80 = Peak_Theory_max(Roc_LK_W20_HZ80, Ver_Column)

Ver_maxAnaly_HZ10_Away = Peak_Theory_max(Ver_LK_W20_HZ10_Away, Ver_Column)# Ver_maxLK20_HZ10_Away
Ver_maxAnaly_HZ20_Away = Peak_Theory_max(Ver_LK_W20_HZ20_Away, Ver_Column)# Ver_maxLK20_HZ20_Away
Ver_maxAnaly_HZ40_Away = Peak_Theory_max(Ver_LK_W20_HZ40_Away, Ver_Column)
Ver_maxAnaly_HZ80_Away = Peak_Theory_max(Ver_LK_W20_HZ80_Away, Ver_Column)

Hor_maxAnaly_HZ10_Away = Peak_Theory_max(Hor_LK_W20_HZ10_Away, Hor_Column) # Hor_maxLK20_HZ10_Away
Hor_maxAnaly_HZ20_Away = Peak_Theory_max(Hor_LK_W20_HZ20_Away, Hor_Column) # Hor_maxLK20_HZ20_Away
Hor_maxAnaly_HZ40_Away = Peak_Theory_max(Hor_LK_W20_HZ40_Away, Hor_Column)
Hor_maxAnaly_HZ80_Away = Peak_Theory_max(Hor_LK_W20_HZ80_Away, Hor_Column)

Roc_maxAnaly_HZ10_Away = Peak_Theory_max(Roc_LK_W20_HZ10_Away, Ver_Column) # Roc_maxLK20_HZ10_Away
Roc_maxAnaly_HZ20_Away = Peak_Theory_max(Roc_LK_W20_HZ20_Away, Ver_Column) # Roc_maxLK20_HZ20_Away
Roc_maxAnaly_HZ40_Away = Peak_Theory_max(Roc_LK_W20_HZ40_Away, Ver_Column)
Roc_maxAnaly_HZ80_Away = Peak_Theory_max(Roc_LK_W20_HZ80_Away, Ver_Column)

# ---------- Middle Node -------------
# ======================================= Vertical Loading ===================================
Ver_Tie20_err = np.zeros((len(Frequency_Size),2))
Ver_LK20_err = np.zeros((len(Frequency_Size),2))
Ver_BeamType_20err = np.zeros((len(Frequency_Size),2))

Ver_Tie10_err = np.zeros((len(Frequency_Size),2))
Ver_LK10_err = np.zeros((len(Frequency_Size),2))
Ver_BeamType_10err = np.zeros((len(Frequency_Size),2))

Ver_Tie5_err = np.zeros((len(Frequency_Size),2))
Ver_LK5_err = np.zeros((len(Frequency_Size),2))
Ver_BeamType_5err = np.zeros((len(Frequency_Size),2))

Ver_Tie2_err = np.zeros((len(Frequency_Size),2))
Ver_LK2_err = np.zeros((len(Frequency_Size),2))
Ver_BeamType_2err = np.zeros((len(Frequency_Size),2))

# ======================================= Horizon Loading ===================================
Hor_Tie20_err = np.zeros((len(Frequency_Size),2))
Hor_LK20_err = np.zeros((len(Frequency_Size),2))
Hor_BeamType_20err = np.zeros((len(Frequency_Size),2))

Hor_Tie10_err = np.zeros((len(Frequency_Size),2))
Hor_LK10_err = np.zeros((len(Frequency_Size),2))
Hor_BeamType_10err = np.zeros((len(Frequency_Size),2))

Hor_Tie5_err = np.zeros((len(Frequency_Size),2))
Hor_LK5_err = np.zeros((len(Frequency_Size),2))
Hor_BeamType_5err = np.zeros((len(Frequency_Size),2))

Hor_Tie2_err = np.zeros((len(Frequency_Size),2))
Hor_LK2_err = np.zeros((len(Frequency_Size),2))
Hor_BeamType_2err = np.zeros((len(Frequency_Size),2))

# ======================================= Rocking Loading ===================================
Roc_Tie20_err = np.zeros((len(Frequency_Size),2))
Roc_LK20_err = np.zeros((len(Frequency_Size),2))
Roc_BeamType_20err = np.zeros((len(Frequency_Size),2))

Roc_Tie10_err = np.zeros((len(Frequency_Size),2))
Roc_LK10_err = np.zeros((len(Frequency_Size),2))
Roc_BeamType_10err = np.zeros((len(Frequency_Size),2))

Roc_Tie5_err = np.zeros((len(Frequency_Size),2))
Roc_LK5_err = np.zeros((len(Frequency_Size),2))
Roc_BeamType_5err = np.zeros((len(Frequency_Size),2))

Roc_Tie2_err = np.zeros((len(Frequency_Size),2))
Roc_LK2_err = np.zeros((len(Frequency_Size),2))
Roc_BeamType_2err = np.zeros((len(Frequency_Size),2))

# ---------- 1m away from middle Node -------------
# ======================================= Vertical Loading ===================================
Ver_Tie20_err_Away = np.zeros((len(Frequency_Size),2))
Ver_LK20_err_Away = np.zeros((len(Frequency_Size),2))
Ver_BeamType_20err_Away = np.zeros((len(Frequency_Size),2))

Ver_Tie10_err_Away = np.zeros((len(Frequency_Size),2))
Ver_LK10_err_Away = np.zeros((len(Frequency_Size),2))
Ver_BeamType_10err_Away = np.zeros((len(Frequency_Size),2))

Ver_Tie5_err_Away = np.zeros((len(Frequency_Size),2))
Ver_LK5_err_Away = np.zeros((len(Frequency_Size),2))
Ver_BeamType_5err_Away = np.zeros((len(Frequency_Size),2))

Ver_Tie2_err_Away = np.zeros((len(Frequency_Size),2))
Ver_LK2_err_Away = np.zeros((len(Frequency_Size),2))
Ver_BeamType_2err_Away = np.zeros((len(Frequency_Size),2))

# ======================================= Horizon Loading ===================================
Hor_Tie20_err_Away = np.zeros((len(Frequency_Size),2))
Hor_LK20_err_Away = np.zeros((len(Frequency_Size),2))
Hor_BeamType_20err_Away = np.zeros((len(Frequency_Size),2))

Hor_Tie10_err_Away = np.zeros((len(Frequency_Size),2))
Hor_LK10_err_Away = np.zeros((len(Frequency_Size),2))
Hor_BeamType_10err_Away = np.zeros((len(Frequency_Size),2))

Hor_Tie5_err_Away = np.zeros((len(Frequency_Size),2))
Hor_LK5_err_Away = np.zeros((len(Frequency_Size),2))
Hor_BeamType_5err_Away = np.zeros((len(Frequency_Size),2))

Hor_Tie2_err_Away = np.zeros((len(Frequency_Size),2))
Hor_LK2_err_Away = np.zeros((len(Frequency_Size),2))
Hor_BeamType_2err_Away = np.zeros((len(Frequency_Size),2))

# ======================================= Rocking Loading ===================================
Roc_Tie20_err_Away = np.zeros((len(Frequency_Size),2))
Roc_LK20_err_Away = np.zeros((len(Frequency_Size),2))
Roc_BeamType_20err_Away = np.zeros((len(Frequency_Size),2))

Roc_Tie10_err_Away = np.zeros((len(Frequency_Size),2))
Roc_LK10_err_Away = np.zeros((len(Frequency_Size),2))
Roc_BeamType_10err_Away = np.zeros((len(Frequency_Size),2))

Roc_Tie5_err_Away = np.zeros((len(Frequency_Size),2))
Roc_LK5_err_Away = np.zeros((len(Frequency_Size),2))
Roc_BeamType_5err_Away = np.zeros((len(Frequency_Size),2))

Roc_Tie2_err_Away = np.zeros((len(Frequency_Size),2))
Roc_LK2_err_Away = np.zeros((len(Frequency_Size),2))
Roc_BeamType_2err_Away = np.zeros((len(Frequency_Size),2))

def Calculate_Error(TieErr, Tie_error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80):
    TieErr[:,0] = Tie_error[:,0]
# # ------------------------- Absolute Relative Error ------------------        
#     TieErr[0,1] = ((Tie_error[0,1] - maxAnaly_HZ10)/maxAnaly_HZ10)*100
#     TieErr[1,1] = ((Tie_error[1,1] - maxAnaly_HZ20)/maxAnaly_HZ20)*100
#     TieErr[2,1] = ((Tie_error[2,1] - maxAnaly_HZ40)/maxAnaly_HZ40)*100
#     TieErr[3,1] = ((Tie_error[3,1] - maxAnaly_HZ80)/maxAnaly_HZ80)*100
    
# -------------------------Wave Refection Letter Relative Error ------------------        
    TieErr[0,1] = ((Tie_error[0,1] - 0)/maxAnaly_HZ10)*100 
    TieErr[1,1] = ((Tie_error[1,1] - 0)/maxAnaly_HZ20)*100
    TieErr[2,1] = ((Tie_error[2,1] - 0)/maxAnaly_HZ40)*100
    TieErr[3,1] = ((Tie_error[3,1] - 0)/maxAnaly_HZ80)*100

# ----------- Middle Node -----------------
# ======================================= Vertical Loading ===================================
Calculate_Error(Ver_Tie20_err, Ver_Tie20_error, Ver_maxAnaly_HZ10, Ver_maxAnaly_HZ20, Ver_maxAnaly_HZ40, Ver_maxAnaly_HZ80)
Calculate_Error(Ver_LK20_err, Ver_LK20_error, Ver_maxAnaly_HZ10, Ver_maxAnaly_HZ20, Ver_maxAnaly_HZ40, Ver_maxAnaly_HZ80) # *****
Calculate_Error(Ver_BeamType_20err, Ver_BeamType_20error, Ver_maxAnaly_HZ10, Ver_maxAnaly_HZ20, Ver_maxAnaly_HZ40, Ver_maxAnaly_HZ80)

Calculate_Error(Ver_Tie10_err, Ver_Tie10_error, Ver_maxAnaly_HZ10, Ver_maxAnaly_HZ20, Ver_maxAnaly_HZ40, Ver_maxAnaly_HZ80)
Calculate_Error(Ver_LK10_err, Ver_LK10_error, Ver_maxAnaly_HZ10, Ver_maxAnaly_HZ20, Ver_maxAnaly_HZ40, Ver_maxAnaly_HZ80)
Calculate_Error(Ver_BeamType_10err, Ver_BeamType_10error, Ver_maxAnaly_HZ10, Ver_maxAnaly_HZ20, Ver_maxAnaly_HZ40, Ver_maxAnaly_HZ80)

Calculate_Error(Ver_Tie5_err, Ver_Tie5_error, Ver_maxAnaly_HZ10, Ver_maxAnaly_HZ20, Ver_maxAnaly_HZ40, Ver_maxAnaly_HZ80)
Calculate_Error(Ver_LK5_err, Ver_LK5_error, Ver_maxAnaly_HZ10, Ver_maxAnaly_HZ20, Ver_maxAnaly_HZ40, Ver_maxAnaly_HZ80)
Calculate_Error(Ver_BeamType_5err, Ver_BeamType_5error, Ver_maxAnaly_HZ10, Ver_maxAnaly_HZ20, Ver_maxAnaly_HZ40, Ver_maxAnaly_HZ80)

Calculate_Error(Ver_Tie2_err, Ver_Tie2_error, Ver_maxAnaly_HZ10, Ver_maxAnaly_HZ20, Ver_maxAnaly_HZ40, Ver_maxAnaly_HZ80)
Calculate_Error(Ver_LK2_err, Ver_LK2_error, Ver_maxAnaly_HZ10, Ver_maxAnaly_HZ20, Ver_maxAnaly_HZ40, Ver_maxAnaly_HZ80)
Calculate_Error(Ver_BeamType_2err, Ver_BeamType_2error, Ver_maxAnaly_HZ10, Ver_maxAnaly_HZ20, Ver_maxAnaly_HZ40, Ver_maxAnaly_HZ80)

# ======================================= Horizon Loading ===================================
Calculate_Error(Hor_Tie20_err, Hor_Tie20_error, Hor_maxAnaly_HZ10, Hor_maxAnaly_HZ20, Hor_maxAnaly_HZ40, Hor_maxAnaly_HZ80)
Calculate_Error(Hor_LK20_err, Hor_LK20_error, Hor_maxAnaly_HZ10, Hor_maxAnaly_HZ20, Hor_maxAnaly_HZ40, Hor_maxAnaly_HZ80) # *****
Calculate_Error(Hor_BeamType_20err, Hor_BeamType_20error, Hor_maxAnaly_HZ10, Hor_maxAnaly_HZ20, Hor_maxAnaly_HZ40, Hor_maxAnaly_HZ80)

Calculate_Error(Hor_Tie10_err, Hor_Tie10_error, Hor_maxAnaly_HZ10, Hor_maxAnaly_HZ20, Hor_maxAnaly_HZ40, Hor_maxAnaly_HZ80)
Calculate_Error(Hor_LK10_err, Hor_LK10_error, Hor_maxAnaly_HZ10, Hor_maxAnaly_HZ20, Hor_maxAnaly_HZ40, Hor_maxAnaly_HZ80)
Calculate_Error(Hor_BeamType_10err, Hor_BeamType_10error, Hor_maxAnaly_HZ10, Hor_maxAnaly_HZ20, Hor_maxAnaly_HZ40, Hor_maxAnaly_HZ80)

Calculate_Error(Hor_Tie5_err, Hor_Tie5_error, Hor_maxAnaly_HZ10, Hor_maxAnaly_HZ20, Hor_maxAnaly_HZ40, Hor_maxAnaly_HZ80)
Calculate_Error(Hor_LK5_err, Hor_LK5_error, Hor_maxAnaly_HZ10, Hor_maxAnaly_HZ20, Hor_maxAnaly_HZ40, Hor_maxAnaly_HZ80)
Calculate_Error(Hor_BeamType_5err, Hor_BeamType_5error, Hor_maxAnaly_HZ10, Hor_maxAnaly_HZ20, Hor_maxAnaly_HZ40, Hor_maxAnaly_HZ80)

Calculate_Error(Hor_Tie2_err, Hor_Tie2_error, Hor_maxAnaly_HZ10, Hor_maxAnaly_HZ20, Hor_maxAnaly_HZ40, Hor_maxAnaly_HZ80)
Calculate_Error(Hor_LK2_err, Hor_LK2_error, Hor_maxAnaly_HZ10, Hor_maxAnaly_HZ20, Hor_maxAnaly_HZ40, Hor_maxAnaly_HZ80)
Calculate_Error(Hor_BeamType_2err, Hor_BeamType_2error, Hor_maxAnaly_HZ10, Hor_maxAnaly_HZ20, Hor_maxAnaly_HZ40, Hor_maxAnaly_HZ80)

# ======================================= Rocking Loading ===================================
Calculate_Error(Roc_Tie20_err, Roc_Tie20_error, Roc_maxAnaly_HZ10, Roc_maxAnaly_HZ20, Roc_maxAnaly_HZ40, Roc_maxAnaly_HZ80)
Calculate_Error(Roc_LK20_err, Roc_LK20_error, Roc_maxAnaly_HZ10, Roc_maxAnaly_HZ20, Roc_maxAnaly_HZ40, Roc_maxAnaly_HZ80) # *****
Calculate_Error(Roc_BeamType_20err, Roc_BeamType_20error, Roc_maxAnaly_HZ10, Roc_maxAnaly_HZ20, Roc_maxAnaly_HZ40, Roc_maxAnaly_HZ80)

Calculate_Error(Roc_Tie10_err, Roc_Tie10_error, Roc_maxAnaly_HZ10, Roc_maxAnaly_HZ20, Roc_maxAnaly_HZ40, Roc_maxAnaly_HZ80)
Calculate_Error(Roc_LK10_err, Roc_LK10_error, Roc_maxAnaly_HZ10, Roc_maxAnaly_HZ20, Roc_maxAnaly_HZ40, Roc_maxAnaly_HZ80)
Calculate_Error(Roc_BeamType_10err, Roc_BeamType_10error, Roc_maxAnaly_HZ10, Roc_maxAnaly_HZ20, Roc_maxAnaly_HZ40, Roc_maxAnaly_HZ80)

Calculate_Error(Roc_Tie5_err, Roc_Tie5_error, Roc_maxAnaly_HZ10, Roc_maxAnaly_HZ20, Roc_maxAnaly_HZ40, Roc_maxAnaly_HZ80)
Calculate_Error(Roc_LK5_err, Roc_LK5_error, Roc_maxAnaly_HZ10, Roc_maxAnaly_HZ20, Roc_maxAnaly_HZ40, Roc_maxAnaly_HZ80)
Calculate_Error(Roc_BeamType_5err, Roc_BeamType_5error, Roc_maxAnaly_HZ10, Roc_maxAnaly_HZ20, Roc_maxAnaly_HZ40, Roc_maxAnaly_HZ80)

Calculate_Error(Roc_Tie2_err, Roc_Tie2_error, Roc_maxAnaly_HZ10, Roc_maxAnaly_HZ20, Roc_maxAnaly_HZ40, Roc_maxAnaly_HZ80)
Calculate_Error(Roc_LK2_err, Roc_LK2_error, Roc_maxAnaly_HZ10, Roc_maxAnaly_HZ20, Roc_maxAnaly_HZ40, Roc_maxAnaly_HZ80)
Calculate_Error(Roc_BeamType_2err, Roc_BeamType_2error, Roc_maxAnaly_HZ10, Roc_maxAnaly_HZ20, Roc_maxAnaly_HZ40, Roc_maxAnaly_HZ80)


# ---------- 1m away from middle Node -------------
# ======================================= Vertical Loading ===================================
Calculate_Error(Ver_Tie20_err_Away, Ver_Tie20_error_Away, Ver_maxAnaly_HZ10_Away, Ver_maxAnaly_HZ20_Away, Ver_maxAnaly_HZ40_Away, Ver_maxAnaly_HZ80_Away)
Calculate_Error(Ver_LK20_err_Away, Ver_LK20_error_Away, Ver_maxAnaly_HZ10_Away, Ver_maxAnaly_HZ20_Away, Ver_maxAnaly_HZ40_Away, Ver_maxAnaly_HZ80_Away) # *****
Calculate_Error(Ver_BeamType_20err_Away, Ver_BeamType_20error_Away, Ver_maxAnaly_HZ10_Away, Ver_maxAnaly_HZ20_Away, Ver_maxAnaly_HZ40_Away, Ver_maxAnaly_HZ80_Away)

Calculate_Error(Ver_Tie10_err_Away, Ver_Tie10_error_Away, Ver_maxAnaly_HZ10_Away, Ver_maxAnaly_HZ20_Away, Ver_maxAnaly_HZ40_Away, Ver_maxAnaly_HZ80_Away)
Calculate_Error(Ver_LK10_err_Away, Ver_LK10_error_Away, Ver_maxAnaly_HZ10_Away, Ver_maxAnaly_HZ20_Away, Ver_maxAnaly_HZ40_Away, Ver_maxAnaly_HZ80_Away) 
Calculate_Error(Ver_BeamType_10err_Away, Ver_BeamType_10error_Away, Ver_maxAnaly_HZ10_Away, Ver_maxAnaly_HZ20_Away, Ver_maxAnaly_HZ40_Away, Ver_maxAnaly_HZ80_Away)

Calculate_Error(Ver_Tie5_err_Away, Ver_Tie5_error_Away, Ver_maxAnaly_HZ10_Away, Ver_maxAnaly_HZ20_Away, Ver_maxAnaly_HZ40_Away, Ver_maxAnaly_HZ80_Away)
Calculate_Error(Ver_LK5_err_Away, Ver_LK5_error_Away, Ver_maxAnaly_HZ10_Away, Ver_maxAnaly_HZ20_Away, Ver_maxAnaly_HZ40_Away, Ver_maxAnaly_HZ80_Away) 
Calculate_Error(Ver_BeamType_5err_Away, Ver_BeamType_5error_Away, Ver_maxAnaly_HZ10_Away, Ver_maxAnaly_HZ20_Away, Ver_maxAnaly_HZ40_Away, Ver_maxAnaly_HZ80_Away)

Calculate_Error(Ver_Tie2_err_Away, Ver_Tie2_error_Away, Ver_maxAnaly_HZ10_Away, Ver_maxAnaly_HZ20_Away, Ver_maxAnaly_HZ40_Away, Ver_maxAnaly_HZ80_Away)
Calculate_Error(Ver_LK2_err_Away, Ver_LK2_error_Away, Ver_maxAnaly_HZ10_Away, Ver_maxAnaly_HZ20_Away, Ver_maxAnaly_HZ40_Away, Ver_maxAnaly_HZ80_Away) 
Calculate_Error(Ver_BeamType_2err_Away, Ver_BeamType_2error_Away, Ver_maxAnaly_HZ10_Away, Ver_maxAnaly_HZ20_Away, Ver_maxAnaly_HZ40_Away, Ver_maxAnaly_HZ80_Away)

# ======================================= Horizon Loading ===================================
Calculate_Error(Hor_Tie20_err_Away, Hor_Tie20_error_Away, Hor_maxAnaly_HZ10_Away, Hor_maxAnaly_HZ20_Away, Hor_maxAnaly_HZ40_Away, Hor_maxAnaly_HZ80_Away)
Calculate_Error(Hor_LK20_err_Away, Hor_LK20_error_Away, Hor_maxAnaly_HZ10_Away, Hor_maxAnaly_HZ20_Away, Hor_maxAnaly_HZ40_Away, Hor_maxAnaly_HZ80_Away) # *****
Calculate_Error(Hor_BeamType_20err_Away, Hor_BeamType_20error_Away, Hor_maxAnaly_HZ10_Away, Hor_maxAnaly_HZ20_Away, Hor_maxAnaly_HZ40_Away, Hor_maxAnaly_HZ80_Away)

Calculate_Error(Hor_Tie10_err_Away, Hor_Tie10_error_Away, Hor_maxAnaly_HZ10_Away, Hor_maxAnaly_HZ20_Away, Hor_maxAnaly_HZ40_Away, Hor_maxAnaly_HZ80_Away)
Calculate_Error(Hor_LK10_err_Away, Hor_LK10_error_Away, Hor_maxAnaly_HZ10_Away, Hor_maxAnaly_HZ20_Away, Hor_maxAnaly_HZ40_Away, Hor_maxAnaly_HZ80_Away) 
Calculate_Error(Hor_BeamType_10err_Away, Hor_BeamType_10error_Away, Hor_maxAnaly_HZ10_Away, Hor_maxAnaly_HZ20_Away, Hor_maxAnaly_HZ40_Away, Hor_maxAnaly_HZ80_Away)

Calculate_Error(Hor_Tie5_err_Away, Hor_Tie5_error_Away, Hor_maxAnaly_HZ10_Away, Hor_maxAnaly_HZ20_Away, Hor_maxAnaly_HZ40_Away, Hor_maxAnaly_HZ80_Away)
Calculate_Error(Hor_LK5_err_Away, Hor_LK5_error_Away, Hor_maxAnaly_HZ10_Away, Hor_maxAnaly_HZ20_Away, Hor_maxAnaly_HZ40_Away, Hor_maxAnaly_HZ80_Away) 
Calculate_Error(Hor_BeamType_5err_Away, Hor_BeamType_5error_Away, Hor_maxAnaly_HZ10_Away, Hor_maxAnaly_HZ20_Away, Hor_maxAnaly_HZ40_Away, Hor_maxAnaly_HZ80_Away)

Calculate_Error(Hor_Tie2_err_Away, Hor_Tie2_error_Away, Hor_maxAnaly_HZ10_Away, Hor_maxAnaly_HZ20_Away, Hor_maxAnaly_HZ40_Away, Hor_maxAnaly_HZ80_Away)
Calculate_Error(Hor_LK2_err_Away, Hor_LK2_error_Away, Hor_maxAnaly_HZ10_Away, Hor_maxAnaly_HZ20_Away, Hor_maxAnaly_HZ40_Away, Hor_maxAnaly_HZ80_Away) 
Calculate_Error(Hor_BeamType_2err_Away, Hor_BeamType_2error_Away, Hor_maxAnaly_HZ10_Away, Hor_maxAnaly_HZ20_Away, Hor_maxAnaly_HZ40_Away, Hor_maxAnaly_HZ80_Away)

# ======================================= Rocking Loading ===================================
Calculate_Error(Roc_Tie20_err_Away, Roc_Tie20_error_Away, Roc_maxAnaly_HZ10_Away, Roc_maxAnaly_HZ20_Away, Roc_maxAnaly_HZ40_Away, Roc_maxAnaly_HZ80_Away)
Calculate_Error(Roc_LK20_err_Away, Roc_LK20_error_Away, Roc_maxAnaly_HZ10_Away, Roc_maxAnaly_HZ20_Away, Roc_maxAnaly_HZ40_Away, Roc_maxAnaly_HZ80_Away) # *****
Calculate_Error(Roc_BeamType_20err_Away, Roc_BeamType_20error_Away, Roc_maxAnaly_HZ10_Away, Roc_maxAnaly_HZ20_Away, Roc_maxAnaly_HZ40_Away, Roc_maxAnaly_HZ80_Away)

Calculate_Error(Roc_Tie10_err_Away, Roc_Tie10_error_Away, Roc_maxAnaly_HZ10_Away, Roc_maxAnaly_HZ20_Away, Roc_maxAnaly_HZ40_Away, Roc_maxAnaly_HZ80_Away)
Calculate_Error(Roc_LK10_err_Away, Roc_LK10_error_Away, Roc_maxAnaly_HZ10_Away, Roc_maxAnaly_HZ20_Away, Roc_maxAnaly_HZ40_Away, Roc_maxAnaly_HZ80_Away) 
Calculate_Error(Roc_BeamType_10err_Away, Roc_BeamType_10error_Away, Roc_maxAnaly_HZ10_Away, Roc_maxAnaly_HZ20_Away, Roc_maxAnaly_HZ40_Away, Roc_maxAnaly_HZ80_Away)

Calculate_Error(Roc_Tie5_err_Away, Roc_Tie5_error_Away, Roc_maxAnaly_HZ10_Away, Roc_maxAnaly_HZ20_Away, Roc_maxAnaly_HZ40_Away, Roc_maxAnaly_HZ80_Away)
Calculate_Error(Roc_LK5_err_Away, Roc_LK5_error_Away, Roc_maxAnaly_HZ10_Away, Roc_maxAnaly_HZ20_Away, Roc_maxAnaly_HZ40_Away, Roc_maxAnaly_HZ80_Away) 
Calculate_Error(Roc_BeamType_5err_Away, Roc_BeamType_5error_Away, Roc_maxAnaly_HZ10_Away, Roc_maxAnaly_HZ20_Away, Roc_maxAnaly_HZ40_Away, Roc_maxAnaly_HZ80_Away)

Calculate_Error(Roc_Tie2_err_Away, Roc_Tie2_error_Away, Roc_maxAnaly_HZ10_Away, Roc_maxAnaly_HZ20_Away, Roc_maxAnaly_HZ40_Away, Roc_maxAnaly_HZ80_Away)
Calculate_Error(Roc_LK2_err_Away, Roc_LK2_error_Away, Roc_maxAnaly_HZ10_Away, Roc_maxAnaly_HZ20_Away, Roc_maxAnaly_HZ40_Away, Roc_maxAnaly_HZ80_Away) 
Calculate_Error(Roc_BeamType_2err_Away, Roc_BeamType_2error_Away, Roc_maxAnaly_HZ10_Away, Roc_maxAnaly_HZ20_Away, Roc_maxAnaly_HZ40_Away, Roc_maxAnaly_HZ80_Away)

# ==================Draw Relative error : Dy/WaveLength =============================
def DifferTime_RelativeError2(Hor_LKErr, Hor_ProposedErr, Ver_LKErr, Ver_ProposedErr, Roc_LKErr, Roc_ProposedErr):
    # ------------ Horizon --------------------------
    plt.plot(Dy_lambP[:], Hor_LKErr[:,1],marker = '^',markersize=16,markerfacecolor = 'white',label = 'LK Dashpot', color = 'red', linewidth = 3.0)
    plt.plot(Dy_lambP[:], Hor_ProposedErr[:,1],marker = 'p',markersize=12,markerfacecolor = 'white',label = 'Proposed', color = 'red', linewidth = 3.0)
   
  # ----------------Vertical------------------------------
    plt.plot(Dy_lambS[:], Ver_LKErr[:,1],marker = '^',markersize=16,markerfacecolor = 'white', color = 'blue', linewidth = 3.0)
    plt.plot(Dy_lambS[:], Ver_ProposedErr[:,1],marker = 'p',markersize=12,markerfacecolor = 'white', color = 'blue', linewidth = 3.0) # , ls = '--'

    # ----------------Rocking------------------------------
    plt.plot(Dy_lambS[:], Roc_LKErr[:,1],marker = '^',markersize=16,markerfacecolor = 'white', color = 'darkgrey', linewidth = 3.0)
    plt.plot(Dy_lambS[:], Roc_ProposedErr[:,1],marker = 'p',markersize=12,markerfacecolor = 'white', color = 'darkgrey', linewidth = 3.0) # , ls = '--'
    
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)

    plt.ylim(-2, 15)  # Middle: -20, 20 ; 0, 8 (0.2s) / Away: -30, 85 ; -2, 15 (0.2s)
    plt.grid(True)
    
    ax = plt.gca()
    # -------------- Consider X-axis  -----------------------
    ax.set_xscale('log', base=10)
    ax.set_xticks([], minor=False)
    ax.set_xticks([], minor=True)
    x_ticks_Num = np.array([0.01, 0.02, 0.04, 0.06, 0.08, 0.1])  # td = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1] ; Dy/lamb = [0.01, 0.02, 0.04, 0.06, 0.08, 0.1]
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.2f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='both', labelsize=20)
    
figsize = (10,10)   
# fig1, (ax1,ax2,ax3,ax4) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# fig1.text(0.13,0.85, "Middle Node", color = "black", fontsize=22)

# # fig1.text(0.02,0.5, 'Peak Velocity Error '+ r"$\ E^{0\,\mathrm{to}\,0.2}_{Max}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=25)
# fig1.text(0.02,0.5, 'Peak Velocity Error '+ r"$\ E^{0.2\,\mathrm{to}\,0.4}_{Max}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=25)

# fig1.text(0.45,0.060, r'$\Delta_c/\lambda$', va= 'center', fontsize=25)

# ax1 = plt.subplot(411)
# DifferTime_RelativeError2(Hor_LK20_err, Hor_BeamType_20err, Ver_LK20_err, Ver_BeamType_20err, Roc_LK20_err, Roc_BeamType_20err)
# ax1.set_title(r"$w=$ $\mathrm{20m}$",fontsize =25, x=0.87, y=0.80)

# ax2 = plt.subplot(412)
# DifferTime_RelativeError2(Hor_LK10_err, Hor_BeamType_10err, Ver_LK10_err, Ver_BeamType_10err, Roc_LK10_err, Roc_BeamType_10err)
# ax2.set_title(r"$w=$ $\mathrm{10m}$",fontsize =25, x=0.87, y=0.80)

# ax3 = plt.subplot(413)
# DifferTime_RelativeError2(Hor_LK5_err, Hor_BeamType_5err, Ver_LK5_err, Ver_BeamType_5err, Roc_LK5_err, Roc_BeamType_5err)
# ax3.set_title(r"$w=$ $\mathrm{5m}$",fontsize =25, x=0.87, y=0.80)

# ax4 = plt.subplot(414)
# DifferTime_RelativeError2(Hor_LK2_err, Hor_BeamType_2err, Ver_LK2_err, Ver_BeamType_2err, Roc_LK2_err, Roc_BeamType_2err)
# ax4.set_title(r"$w=$ $\mathrm{2m}$",fontsize =25, x=0.87, y=0.80)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting
# legend_elements = [Line2D([0], [0], color='red', lw=2, label= f'Horizon Loading'),
#                 Line2D([0], [0], color='blue', lw=2, label= f'Vertical Loading'),
#                 ] # Line2D([0], [0], color='darkgrey', lw=2, label= f'Rocking Loading')

# legend_elements2 =  [Line2D([0], [0], color='black',marker = '^',markersize=16,markerfacecolor = 'white', label= 'LK Dashpot'),
#                     Line2D([0], [0], color='black',marker = 'p',markersize=12,markerfacecolor = 'white', label= 'Proposed')]

# lines, labels = fig1.axes[-1].get_legend_handles_labels()
# legend1 = fig1.legend(handles=legend_elements, loc=(0.30, 0.88) ,prop=font_props) # , title="Legend 1"
# fig1.add_artist(legend1)

# legend2 = fig1.legend(handles=legend_elements2, loc=(0.60, 0.88) ,prop=font_props)

# fig2, (ax5,ax6,ax7,ax8) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# fig2.text(0.13,0.85, "Node 1 m away from the midpoint", color = "black", fontsize=22)

# # fig2.text(0.02,0.5, 'Peak Velocity Error '+ r"$\ E^{0\,\mathrm{to}\,0.2}_{Max}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=25)
# fig2.text(0.02,0.5, 'Peak Velocity Error '+ r"$\ E^{0.2\,\mathrm{to}\,0.4}_{Max}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=25)

# fig2.text(0.45,0.060, r'$\Delta_c/\lambda$', va= 'center', fontsize=25)

# ax5 = plt.subplot(411)
# DifferTime_RelativeError2(Hor_LK20_err_Away, Hor_BeamType_20err_Away, Ver_LK20_err_Away, Ver_BeamType_20err_Away, Roc_LK20_err_Away, Roc_BeamType_20err_Away)
# ax5.set_title(r"$w=$ $\mathrm{20m}$",fontsize =25, x=0.87, y=0.80)

# ax6 = plt.subplot(412)
# DifferTime_RelativeError2(Hor_LK10_err_Away, Hor_BeamType_10err_Away, Ver_LK10_err_Away, Ver_BeamType_10err_Away, Roc_LK10_err_Away, Roc_BeamType_10err_Away)
# ax6.set_title(r"$w=$ $\mathrm{10m}$",fontsize =25, x=0.87, y=0.80)

# ax7 = plt.subplot(413)
# DifferTime_RelativeError2(Hor_LK5_err_Away, Hor_BeamType_5err_Away, Ver_LK5_err_Away, Ver_BeamType_5err_Away, Roc_LK5_err_Away, Roc_BeamType_5err_Away)
# ax7.set_title(r"$w=$ $\mathrm{5m}$",fontsize =25, x=0.87, y=0.80)

# ax8 = plt.subplot(414)
# DifferTime_RelativeError2(Hor_LK2_err_Away, Hor_BeamType_2err_Away, Ver_LK2_err_Away, Ver_BeamType_2err_Away, Roc_LK2_err_Away, Roc_BeamType_2err_Away)
# ax8.set_title(r"$w=$ $\mathrm{2m}$",fontsize =25, x=0.87, y=0.80)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting
# legend_elements = [Line2D([0], [0], color='red', lw=2, label= f'Horizon Loading'),
#                 Line2D([0], [0], color='blue', lw=2, label= f'Vertical Loading'),
#                 Line2D([0], [0], color='darkgrey', lw=2, label= f'Rocking Loading')] 

# legend_elements2 =  [Line2D([0], [0], color='black',marker = '^',markersize=16,markerfacecolor = 'white', label= 'LK Dashpot'),
#                     Line2D([0], [0], color='black',marker = 'p',markersize=12,markerfacecolor = 'white', label= 'Proposed')]

# lines, labels = fig2.axes[-1].get_legend_handles_labels()
# legend1 = fig2.legend(handles=legend_elements, loc=(0.30, 0.88) ,prop=font_props) # , title="Legend 1"
# fig2.add_artist(legend1)

# legend2 = fig2.legend(handles=legend_elements2, loc=(0.60, 0.88) ,prop=font_props)

# ================================== Prepare L2-Norm Error ============================
# ---------- Find Different Data in 40 row Same Time ---------------------
Analysis_Time = Ver_LK_W20_HZ40[:, 0]
Theory_Time = Ver_Tie_W20_HZ40[:, 0]

L2_Start = 0.20 # 0.00 / 0.20
L2_End  = 0.60 # 0.20 / 0.80
# ================= Calculate_2NormError Normalization ===============================
def Calculate_RelativeL2norm(TheoryTime,TheoryData, Analysis_Time,Tie_W20_HZ40_Mid, Column_Index, time_range=(L2_Start, L2_End)):
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

# ===================== Draw L2 Norm in (0.2s to 0.4s) Error ===============================================
def Calculate_RelativeL2norm_Letter(TheoryTime,TheoryData, Analysis_Time,Tie_W20_HZ40_Mid, Column_Index, time_range=(L2_Start, L2_End)): # 0.2, 0.40
# ------------------------- L-2 Norm Error ------------------------
    common80 = set(TheoryTime) & set(Analysis_Time)
    filtered_common80 = [value for value in common80 if time_range[0] <= value <= time_range[1]]
    
    differences = []
    Mom = []

    for common_value in filtered_common80 :
        index1 = np.where(Analysis_Time == common_value)[0][0]
        index2 = np.where(TheoryTime == common_value)[0][0]

        diff = (Tie_W20_HZ40_Mid[index1, Column_Index] - 0) # TheoryData[index2, Column_Index]
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

def Add_Err(MidTieErr20,Tie20_error, LK_W20_HZ10_Mid, LK_W20_HZ20_Mid, LK_W20_HZ40_Mid, LK_W20_HZ80_Mid, Tie_W20_HZ10_Mid, Tie_W20_HZ20_Mid, Tie_W20_HZ40_Mid, Tie_W20_HZ80_Mid, Column_Index):
    MidTieErr20[:,0] = Tie20_error[:,0] 
# # ===================================== Calculate_L2NormError Normalization : Middle Node============================================================
#     MidTieErr20[0,1], MidTieErr20[0,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ10_Mid, Analysis_Time,Tie_W20_HZ10_Mid, Column_Index, time_range=(L2_Start, L2_End))
#     MidTieErr20[1,1], MidTieErr20[1,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ20_Mid, Analysis_Time,Tie_W20_HZ20_Mid, Column_Index, time_range=(L2_Start, L2_End))
#     MidTieErr20[2,1], MidTieErr20[2,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ40_Mid, Analysis_Time,Tie_W20_HZ40_Mid, Column_Index, time_range=(L2_Start, L2_End))
#     MidTieErr20[3,1], MidTieErr20[3,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ80_Mid, Analysis_Time,Tie_W20_HZ80_Mid, Column_Index, time_range=(L2_Start, L2_End))

# =====================================Letter Calculate_L2NormError Normalization : Middle Node============================================================
    MidTieErr20[0,1], MidTieErr20[0,2] = Calculate_RelativeL2norm_Letter(Theory_Time,LK_W20_HZ10_Mid, Analysis_Time,Tie_W20_HZ10_Mid, Column_Index, time_range=(L2_Start, L2_End))
    MidTieErr20[1,1], MidTieErr20[1,2] = Calculate_RelativeL2norm_Letter(Theory_Time,LK_W20_HZ20_Mid, Analysis_Time,Tie_W20_HZ20_Mid, Column_Index, time_range=(L2_Start, L2_End))
    MidTieErr20[2,1], MidTieErr20[2,2] = Calculate_RelativeL2norm_Letter(Theory_Time,LK_W20_HZ40_Mid, Analysis_Time,Tie_W20_HZ40_Mid, Column_Index, time_range=(L2_Start, L2_End))
    MidTieErr20[3,1], MidTieErr20[3,2] = Calculate_RelativeL2norm_Letter(Theory_Time,LK_W20_HZ80_Mid, Analysis_Time,Tie_W20_HZ80_Mid, Column_Index, time_range=(L2_Start, L2_End))
    
# ----------- Middle Node -----------------
# ======================================= Vertical Loading ===================================
# -------------- W = 20m-------------------------------
Ver_Tie20Err_L2 = np.zeros((4,3))
Add_Err(Ver_Tie20Err_L2, Ver_Tie20_error, Ver_LK_W20_HZ10, Ver_LK_W20_HZ20, Ver_LK_W20_HZ40, Ver_LK_W20_HZ80, Ver_Tie_W20_HZ10, Ver_Tie_W20_HZ20, Ver_Tie_W20_HZ40, Ver_Tie_W20_HZ80, Ver_Column)

Ver_LK20Err_L2 = np.zeros((4,3))
Add_Err(Ver_LK20Err_L2, Ver_LK20_error, Ver_LK_W20_HZ10, Ver_LK_W20_HZ20, Ver_LK_W20_HZ40, Ver_LK_W20_HZ80, Ver_LK_W20_HZ10, Ver_LK_W20_HZ20, Ver_LK_W20_HZ40, Ver_LK_W20_HZ80, Ver_Column)

Ver_BeamType_W20Err_L2 = np.zeros((4,3))
Add_Err(Ver_BeamType_W20Err_L2, Ver_BeamType_20error, Ver_LK_W20_HZ10, Ver_LK_W20_HZ20, Ver_LK_W20_HZ40, Ver_LK_W20_HZ80, Ver_BeamType_W20_HZ10, Ver_BeamType_W20_HZ20, Ver_BeamType_W20_HZ40, Ver_BeamType_W20_HZ80, Ver_Column)
# -------------- W = 10m-------------------------------
Ver_Tie10Err_L2 = np.zeros((4,3))
Add_Err(Ver_Tie10Err_L2, Ver_Tie10_error, Ver_LK_W20_HZ10, Ver_LK_W20_HZ20, Ver_LK_W20_HZ40, Ver_LK_W20_HZ80, Ver_Tie_W10_HZ10, Ver_Tie_W10_HZ20, Ver_Tie_W10_HZ40, Ver_Tie_W10_HZ80, Ver_Column)

Ver_LK10Err_L2 = np.zeros((4,3))
Add_Err(Ver_LK10Err_L2, Ver_LK10_error, Ver_LK_W20_HZ10, Ver_LK_W20_HZ20, Ver_LK_W20_HZ40, Ver_LK_W20_HZ80, Ver_LK_W10_HZ10, Ver_LK_W10_HZ20, Ver_LK_W10_HZ40, Ver_LK_W10_HZ80, Ver_Column)

Ver_BeamType_W10Err_L2 = np.zeros((4,3))
Add_Err(Ver_BeamType_W10Err_L2, Ver_BeamType_10error, Ver_LK_W20_HZ10, Ver_LK_W20_HZ20, Ver_LK_W20_HZ40, Ver_LK_W20_HZ80, Ver_BeamType_W10_HZ10, Ver_BeamType_W10_HZ20, Ver_BeamType_W10_HZ40, Ver_BeamType_W10_HZ80, Ver_Column)
# -------------- W = 5m-------------------------------
Ver_Tie5Err_L2 = np.zeros((4,3))
Add_Err(Ver_Tie5Err_L2, Ver_Tie5_error, Ver_LK_W20_HZ10, Ver_LK_W20_HZ20, Ver_LK_W20_HZ40, Ver_LK_W20_HZ80, Ver_Tie_W5_HZ10, Ver_Tie_W5_HZ20, Ver_Tie_W5_HZ40, Ver_Tie_W5_HZ80, Ver_Column)

Ver_LK5Err_L2 = np.zeros((4,3))
Add_Err(Ver_LK5Err_L2, Ver_LK5_error, Ver_LK_W20_HZ10, Ver_LK_W20_HZ20, Ver_LK_W20_HZ40, Ver_LK_W20_HZ80, Ver_LK_W5_HZ10, Ver_LK_W5_HZ20, Ver_LK_W5_HZ40, Ver_LK_W5_HZ80, Ver_Column)

Ver_BeamType_W5Err_L2 = np.zeros((4,3))
Add_Err(Ver_BeamType_W5Err_L2, Ver_BeamType_5error, Ver_LK_W20_HZ10, Ver_LK_W20_HZ20, Ver_LK_W20_HZ40, Ver_LK_W20_HZ80, Ver_BeamType_W5_HZ10, Ver_BeamType_W5_HZ20, Ver_BeamType_W5_HZ40, Ver_BeamType_W5_HZ80, Ver_Column)
# -------------- W = 2m-------------------------------
Ver_Tie2Err_L2 = np.zeros((4,3))
Add_Err(Ver_Tie2Err_L2, Ver_Tie2_error, Ver_LK_W20_HZ10, Ver_LK_W20_HZ20, Ver_LK_W20_HZ40, Ver_LK_W20_HZ80, Ver_Tie_W2_HZ10, Ver_Tie_W2_HZ20, Ver_Tie_W2_HZ40, Ver_Tie_W2_HZ80, Ver_Column)

Ver_LK2Err_L2 = np.zeros((4,3))
Add_Err(Ver_LK2Err_L2, Ver_LK2_error, Ver_LK_W20_HZ10, Ver_LK_W20_HZ20, Ver_LK_W20_HZ40, Ver_LK_W20_HZ80, Ver_LK_W2_HZ10, Ver_LK_W2_HZ20, Ver_LK_W2_HZ40, Ver_LK_W2_HZ80, Ver_Column)

Ver_BeamType_W2Err_L2 = np.zeros((4,3))
Add_Err(Ver_BeamType_W2Err_L2, Ver_BeamType_2error, Ver_LK_W20_HZ10, Ver_LK_W20_HZ20, Ver_LK_W20_HZ40, Ver_LK_W20_HZ80, Ver_BeamType_W2_HZ10, Ver_BeamType_W2_HZ20, Ver_BeamType_W2_HZ40, Ver_BeamType_W2_HZ80, Ver_Column)

# ======================================= Horizon Loading ===================================
# -------------- W = 20m-------------------------------
Hor_Tie20Err_L2 = np.zeros((4,3))
Add_Err(Hor_Tie20Err_L2, Hor_Tie20_error, Hor_LK_W20_HZ10, Hor_LK_W20_HZ20, Hor_LK_W20_HZ40, Hor_LK_W20_HZ80, Hor_Tie_W20_HZ10, Hor_Tie_W20_HZ20, Hor_Tie_W20_HZ40, Hor_Tie_W20_HZ80, Hor_Column)

Hor_LK20Err_L2 = np.zeros((4,3))
Add_Err(Hor_LK20Err_L2, Hor_LK20_error, Hor_LK_W20_HZ10, Hor_LK_W20_HZ20, Hor_LK_W20_HZ40, Hor_LK_W20_HZ80, Hor_LK_W20_HZ10, Hor_LK_W20_HZ20, Hor_LK_W20_HZ40, Hor_LK_W20_HZ80, Hor_Column)

Hor_BeamType_W20Err_L2 = np.zeros((4,3))
Add_Err(Hor_BeamType_W20Err_L2, Hor_BeamType_20error, Hor_LK_W20_HZ10, Hor_LK_W20_HZ20, Hor_LK_W20_HZ40, Hor_LK_W20_HZ80, Hor_BeamType_W20_HZ10, Hor_BeamType_W20_HZ20, Hor_BeamType_W20_HZ40, Hor_BeamType_W20_HZ80, Hor_Column)
# -------------- W = 10m-------------------------------
Hor_Tie10Err_L2 = np.zeros((4,3))
Add_Err(Hor_Tie10Err_L2, Hor_Tie10_error, Hor_LK_W20_HZ10, Hor_LK_W20_HZ20, Hor_LK_W20_HZ40, Hor_LK_W20_HZ80, Hor_Tie_W10_HZ10, Hor_Tie_W10_HZ20, Hor_Tie_W10_HZ40, Hor_Tie_W10_HZ80, Hor_Column)

Hor_LK10Err_L2 = np.zeros((4,3))
Add_Err(Hor_LK10Err_L2, Hor_LK10_error, Hor_LK_W20_HZ10, Hor_LK_W20_HZ20, Hor_LK_W20_HZ40, Hor_LK_W20_HZ80, Hor_LK_W10_HZ10, Hor_LK_W10_HZ20, Hor_LK_W10_HZ40, Hor_LK_W10_HZ80, Hor_Column)

Hor_BeamType_W10Err_L2 = np.zeros((4,3))
Add_Err(Hor_BeamType_W10Err_L2, Hor_BeamType_10error, Hor_LK_W20_HZ10, Hor_LK_W20_HZ20, Hor_LK_W20_HZ40, Hor_LK_W20_HZ80, Hor_BeamType_W10_HZ10, Hor_BeamType_W10_HZ20, Hor_BeamType_W10_HZ40, Hor_BeamType_W10_HZ80, Hor_Column)
# -------------- W = 5m-------------------------------
Hor_Tie5Err_L2 = np.zeros((4,3))
Add_Err(Hor_Tie5Err_L2, Hor_Tie5_error, Hor_LK_W20_HZ10, Hor_LK_W20_HZ20, Hor_LK_W20_HZ40, Hor_LK_W20_HZ80, Hor_Tie_W5_HZ10, Hor_Tie_W5_HZ20, Hor_Tie_W5_HZ40, Hor_Tie_W5_HZ80, Hor_Column)

Hor_LK5Err_L2 = np.zeros((4,3))
Add_Err(Hor_LK5Err_L2, Hor_LK5_error, Hor_LK_W20_HZ10, Hor_LK_W20_HZ20, Hor_LK_W20_HZ40, Hor_LK_W20_HZ80, Hor_LK_W5_HZ10, Hor_LK_W5_HZ20, Hor_LK_W5_HZ40, Hor_LK_W5_HZ80, Hor_Column)

Hor_BeamType_W5Err_L2 = np.zeros((4,3))
Add_Err(Hor_BeamType_W5Err_L2, Hor_BeamType_5error, Hor_LK_W20_HZ10, Hor_LK_W20_HZ20, Hor_LK_W20_HZ40, Hor_LK_W20_HZ80, Hor_BeamType_W5_HZ10, Hor_BeamType_W5_HZ20, Hor_BeamType_W5_HZ40, Hor_BeamType_W5_HZ80, Hor_Column)
# -------------- W = 2m-------------------------------
Hor_Tie2Err_L2 = np.zeros((4,3))
Add_Err(Hor_Tie2Err_L2, Hor_Tie2_error, Hor_LK_W20_HZ10, Hor_LK_W20_HZ20, Hor_LK_W20_HZ40, Hor_LK_W20_HZ80, Hor_Tie_W2_HZ10, Hor_Tie_W2_HZ20, Hor_Tie_W2_HZ40, Hor_Tie_W2_HZ80, Hor_Column)

Hor_LK2Err_L2 = np.zeros((4,3))
Add_Err(Hor_LK2Err_L2, Hor_LK2_error, Hor_LK_W20_HZ10, Hor_LK_W20_HZ20, Hor_LK_W20_HZ40, Hor_LK_W20_HZ80, Hor_LK_W2_HZ10, Hor_LK_W2_HZ20, Hor_LK_W2_HZ40, Hor_LK_W2_HZ80, Hor_Column)

Hor_BeamType_W2Err_L2 = np.zeros((4,3))
Add_Err(Hor_BeamType_W2Err_L2, Hor_BeamType_2error, Hor_LK_W20_HZ10, Hor_LK_W20_HZ20, Hor_LK_W20_HZ40, Hor_LK_W20_HZ80, Hor_BeamType_W2_HZ10, Hor_BeamType_W2_HZ20, Hor_BeamType_W2_HZ40, Hor_BeamType_W2_HZ80, Hor_Column)

# ======================================= Rocking Loading ===================================
# -------------- W = 20m-------------------------------
Roc_Tie20Err_L2 = np.zeros((4,3))
Add_Err(Roc_Tie20Err_L2, Roc_Tie20_error, Roc_LK_W20_HZ10, Roc_LK_W20_HZ20, Roc_LK_W20_HZ40, Roc_LK_W20_HZ80, Roc_Tie_W20_HZ10, Roc_Tie_W20_HZ20, Roc_Tie_W20_HZ40, Roc_Tie_W20_HZ80, Ver_Column)

Roc_LK20Err_L2 = np.zeros((4,3))
Add_Err(Roc_LK20Err_L2, Roc_LK20_error, Roc_LK_W20_HZ10, Roc_LK_W20_HZ20, Roc_LK_W20_HZ40, Roc_LK_W20_HZ80, Roc_LK_W20_HZ10, Roc_LK_W20_HZ20, Roc_LK_W20_HZ40, Roc_LK_W20_HZ80, Ver_Column)

Roc_BeamType_W20Err_L2 = np.zeros((4,3))
Add_Err(Roc_BeamType_W20Err_L2, Roc_BeamType_20error, Roc_LK_W20_HZ10, Roc_LK_W20_HZ20, Roc_LK_W20_HZ40, Roc_LK_W20_HZ80, Roc_BeamType_W20_HZ10, Roc_BeamType_W20_HZ20, Roc_BeamType_W20_HZ40, Roc_BeamType_W20_HZ80, Ver_Column)
# -------------- W = 10m-------------------------------
Roc_Tie10Err_L2 = np.zeros((4,3))
Add_Err(Roc_Tie10Err_L2, Roc_Tie10_error, Roc_LK_W20_HZ10, Roc_LK_W20_HZ20, Roc_LK_W20_HZ40, Roc_LK_W20_HZ80, Roc_Tie_W10_HZ10, Roc_Tie_W10_HZ20, Roc_Tie_W10_HZ40, Roc_Tie_W10_HZ80, Ver_Column)

Roc_LK10Err_L2 = np.zeros((4,3))
Add_Err(Roc_LK10Err_L2, Roc_LK10_error, Roc_LK_W20_HZ10, Roc_LK_W20_HZ20, Roc_LK_W20_HZ40, Roc_LK_W20_HZ80, Roc_LK_W10_HZ10, Roc_LK_W10_HZ20, Roc_LK_W10_HZ40, Roc_LK_W10_HZ80, Ver_Column)

Roc_BeamType_W10Err_L2 = np.zeros((4,3))
Add_Err(Roc_BeamType_W10Err_L2, Roc_BeamType_10error, Roc_LK_W20_HZ10, Roc_LK_W20_HZ20, Roc_LK_W20_HZ40, Roc_LK_W20_HZ80, Roc_BeamType_W10_HZ10, Roc_BeamType_W10_HZ20, Roc_BeamType_W10_HZ40, Roc_BeamType_W10_HZ80, Ver_Column)
# -------------- W = 5m-------------------------------
Roc_Tie5Err_L2 = np.zeros((4,3))
Add_Err(Roc_Tie5Err_L2, Roc_Tie5_error, Roc_LK_W20_HZ10, Roc_LK_W20_HZ20, Roc_LK_W20_HZ40, Roc_LK_W20_HZ80, Roc_Tie_W5_HZ10, Roc_Tie_W5_HZ20, Roc_Tie_W5_HZ40, Roc_Tie_W5_HZ80, Ver_Column)

Roc_LK5Err_L2 = np.zeros((4,3))
Add_Err(Roc_LK5Err_L2, Roc_LK5_error, Roc_LK_W20_HZ10, Roc_LK_W20_HZ20, Roc_LK_W20_HZ40, Roc_LK_W20_HZ80, Roc_LK_W5_HZ10, Roc_LK_W5_HZ20, Roc_LK_W5_HZ40, Roc_LK_W5_HZ80, Ver_Column)

Roc_BeamType_W5Err_L2 = np.zeros((4,3))
Add_Err(Roc_BeamType_W5Err_L2, Roc_BeamType_5error, Roc_LK_W20_HZ10, Roc_LK_W20_HZ20, Roc_LK_W20_HZ40, Roc_LK_W20_HZ80, Roc_BeamType_W5_HZ10, Roc_BeamType_W5_HZ20, Roc_BeamType_W5_HZ40, Roc_BeamType_W5_HZ80, Ver_Column)
# -------------- W = 2m-------------------------------
Roc_Tie2Err_L2 = np.zeros((4,3))
Add_Err(Roc_Tie2Err_L2, Roc_Tie2_error, Roc_LK_W20_HZ10, Roc_LK_W20_HZ20, Roc_LK_W20_HZ40, Roc_LK_W20_HZ80, Roc_Tie_W2_HZ10, Roc_Tie_W2_HZ20, Roc_Tie_W2_HZ40, Roc_Tie_W2_HZ80, Ver_Column)

Roc_LK2Err_L2 = np.zeros((4,3))
Add_Err(Roc_LK2Err_L2, Roc_LK2_error, Roc_LK_W20_HZ10, Roc_LK_W20_HZ20, Roc_LK_W20_HZ40, Roc_LK_W20_HZ80, Roc_LK_W2_HZ10, Roc_LK_W2_HZ20, Roc_LK_W2_HZ40, Roc_LK_W2_HZ80, Ver_Column)

Roc_BeamType_W2Err_L2 = np.zeros((4,3))
Add_Err(Roc_BeamType_W2Err_L2, Roc_BeamType_2error, Roc_LK_W20_HZ10, Roc_LK_W20_HZ20, Roc_LK_W20_HZ40, Roc_LK_W20_HZ80, Roc_BeamType_W2_HZ10, Roc_BeamType_W2_HZ20, Roc_BeamType_W2_HZ40, Roc_BeamType_W2_HZ80, Ver_Column)

def Add_Err2(AwayTieErr20, Tie20_error, LK_W20_HZ10_Away, LK_W20_HZ20_Away, LK_W20_HZ40_Away, LK_W20_HZ80_Away, Tie_W20_HZ10_Away, Tie_W20_HZ20_Away, Tie_W20_HZ40_Away, Tie_W20_HZ80_Away, Column_Index):
    AwayTieErr20[:,0] = Tie20_error[:,0] 
# # ===================================== Calculate_L2NormError Normalization : 1m away from Middle Node============================================================
#     AwayTieErr20[0,1], AwayTieErr20[0,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ10_Away, Analysis_Time,Tie_W20_HZ10_Away, Column_Index, time_range=(L2_Start, L2_End))
#     AwayTieErr20[1,1], AwayTieErr20[1,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ20_Away, Analysis_Time,Tie_W20_HZ20_Away, Column_Index, time_range=(L2_Start, L2_End))
#     AwayTieErr20[2,1], AwayTieErr20[2,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ40_Away, Analysis_Time,Tie_W20_HZ40_Away, Column_Index, time_range=(L2_Start, L2_End))
#     AwayTieErr20[3,1], AwayTieErr20[3,2] = Calculate_RelativeL2norm(Theory_Time,LK_W20_HZ80_Away, Analysis_Time,Tie_W20_HZ80_Away, Column_Index, time_range=(L2_Start, L2_End))

# =====================================Letter Calculate_L2NormError Normalization : 1m away from Middle Node============================================================
    AwayTieErr20[0,1], AwayTieErr20[0,2] = Calculate_RelativeL2norm_Letter(Theory_Time,LK_W20_HZ10_Away, Analysis_Time,Tie_W20_HZ10_Away, Column_Index, time_range=(L2_Start, L2_End))
    AwayTieErr20[1,1], AwayTieErr20[1,2] = Calculate_RelativeL2norm_Letter(Theory_Time,LK_W20_HZ20_Away, Analysis_Time,Tie_W20_HZ20_Away, Column_Index, time_range=(L2_Start, L2_End))
    AwayTieErr20[2,1], AwayTieErr20[2,2] = Calculate_RelativeL2norm_Letter(Theory_Time,LK_W20_HZ40_Away, Analysis_Time,Tie_W20_HZ40_Away, Column_Index, time_range=(L2_Start, L2_End))
    AwayTieErr20[3,1], AwayTieErr20[3,2] = Calculate_RelativeL2norm_Letter(Theory_Time,LK_W20_HZ80_Away, Analysis_Time,Tie_W20_HZ80_Away, Column_Index, time_range=(L2_Start, L2_End))

# ---------- 1m away from middle Node -------------
# ======================================= Vertical Loading ===================================
# -------------- W = 20m-------------------------------
Ver_Tie20Err_L2Away = np.zeros((4,3))
Add_Err2(Ver_Tie20Err_L2Away, Ver_Tie20_error_Away, Ver_LK_W20_HZ10_Away, Ver_LK_W20_HZ20_Away, Ver_LK_W20_HZ40_Away, Ver_LK_W20_HZ80_Away, Ver_Tie_W20_HZ10_Away, Ver_Tie_W20_HZ20_Away, Ver_Tie_W20_HZ40_Away, Ver_Tie_W20_HZ80_Away, Ver_Column)

Ver_LK20Err_L2Away = np.zeros((4,3))
Add_Err2(Ver_LK20Err_L2Away, Ver_LK20_error_Away, Ver_LK_W20_HZ10_Away, Ver_LK_W20_HZ20_Away, Ver_LK_W20_HZ40_Away, Ver_LK_W20_HZ80_Away, Ver_LK_W20_HZ10_Away, Ver_LK_W20_HZ20_Away, Ver_LK_W20_HZ40_Away, Ver_LK_W20_HZ80_Away, Ver_Column)

Ver_BeamType_W20Err_L2Away = np.zeros((4,3))
Add_Err2(Ver_BeamType_W20Err_L2Away, Ver_BeamType_20error_Away, Ver_LK_W20_HZ10_Away, Ver_LK_W20_HZ20_Away, Ver_LK_W20_HZ40_Away, Ver_LK_W20_HZ80_Away, Ver_BeamType_W20_HZ10_Away, Ver_BeamType_W20_HZ20_Away, Ver_BeamType_W20_HZ40_Away, Ver_BeamType_W20_HZ80_Away, Ver_Column)
# -------------- W = 10m-------------------------------
Ver_Tie10Err_L2Away = np.zeros((4,3))
Add_Err2(Ver_Tie10Err_L2Away, Ver_Tie10_error_Away, Ver_LK_W20_HZ10_Away, Ver_LK_W20_HZ20_Away, Ver_LK_W20_HZ40_Away, Ver_LK_W20_HZ80_Away, Ver_Tie_W10_HZ10_Away, Ver_Tie_W10_HZ20_Away, Ver_Tie_W10_HZ40_Away, Ver_Tie_W10_HZ80_Away, Ver_Column)

Ver_LK10Err_L2Away = np.zeros((4,3))
Add_Err2(Ver_LK10Err_L2Away, Ver_LK10_error_Away, Ver_LK_W20_HZ10_Away, Ver_LK_W20_HZ20_Away, Ver_LK_W20_HZ40_Away, Ver_LK_W20_HZ80_Away, Ver_LK_W10_HZ10_Away, Ver_LK_W10_HZ20_Away, Ver_LK_W10_HZ40_Away, Ver_LK_W10_HZ80_Away, Ver_Column)

Ver_BeamType_W10Err_L2Away = np.zeros((4,3))
Add_Err2(Ver_BeamType_W10Err_L2Away, Ver_BeamType_10error_Away, Ver_LK_W20_HZ10_Away, Ver_LK_W20_HZ20_Away, Ver_LK_W20_HZ40_Away, Ver_LK_W20_HZ80_Away, Ver_BeamType_W10_HZ10_Away, Ver_BeamType_W10_HZ20_Away, Ver_BeamType_W10_HZ40_Away, Ver_BeamType_W10_HZ80_Away, Ver_Column)
# -------------- W = 5m-------------------------------
Ver_Tie5Err_L2Away = np.zeros((4,3))
Add_Err2(Ver_Tie5Err_L2Away, Ver_Tie5_error_Away, Ver_LK_W20_HZ10_Away, Ver_LK_W20_HZ20_Away, Ver_LK_W20_HZ40_Away, Ver_LK_W20_HZ80_Away, Ver_Tie_W5_HZ10_Away, Ver_Tie_W5_HZ20_Away, Ver_Tie_W5_HZ40_Away, Ver_Tie_W5_HZ80_Away, Ver_Column)

Ver_LK5Err_L2Away = np.zeros((4,3))
Add_Err2(Ver_LK5Err_L2Away, Ver_LK5_error_Away, Ver_LK_W20_HZ10_Away, Ver_LK_W20_HZ20_Away, Ver_LK_W20_HZ40_Away, Ver_LK_W20_HZ80_Away, Ver_LK_W5_HZ10_Away, Ver_LK_W5_HZ20_Away, Ver_LK_W5_HZ40_Away, Ver_LK_W5_HZ80_Away, Ver_Column)

Ver_BeamType_W5Err_L2Away = np.zeros((4,3))
Add_Err2(Ver_BeamType_W5Err_L2Away, Ver_BeamType_5error_Away, Ver_LK_W20_HZ10_Away, Ver_LK_W20_HZ20_Away, Ver_LK_W20_HZ40_Away, Ver_LK_W20_HZ80_Away, Ver_BeamType_W5_HZ10_Away, Ver_BeamType_W5_HZ20_Away, Ver_BeamType_W5_HZ40_Away, Ver_BeamType_W5_HZ80_Away, Ver_Column)
# -------------- W = 2m-------------------------------
Ver_Tie2Err_L2Away = np.zeros((4,3))
Add_Err2(Ver_Tie2Err_L2Away, Ver_Tie2_error_Away, Ver_LK_W20_HZ10_Away, Ver_LK_W20_HZ20_Away, Ver_LK_W20_HZ40_Away, Ver_LK_W20_HZ80_Away, Ver_Tie_W2_HZ10_Away, Ver_Tie_W2_HZ20_Away, Ver_Tie_W2_HZ40_Away, Ver_Tie_W2_HZ80_Away, Ver_Column)

Ver_LK2Err_L2Away = np.zeros((4,3))
Add_Err2(Ver_LK2Err_L2Away, Ver_LK2_error_Away, Ver_LK_W20_HZ10_Away, Ver_LK_W20_HZ20_Away, Ver_LK_W20_HZ40_Away, Ver_LK_W20_HZ80_Away, Ver_LK_W2_HZ10_Away, Ver_LK_W2_HZ20_Away, Ver_LK_W2_HZ40_Away, Ver_LK_W2_HZ80_Away, Ver_Column)

Ver_BeamType_W2Err_L2Away = np.zeros((4,3))
Add_Err2(Ver_BeamType_W2Err_L2Away, Ver_BeamType_2error_Away, Ver_LK_W20_HZ10_Away, Ver_LK_W20_HZ20_Away, Ver_LK_W20_HZ40_Away, Ver_LK_W20_HZ80_Away, Ver_BeamType_W2_HZ10_Away, Ver_BeamType_W2_HZ20_Away, Ver_BeamType_W2_HZ40_Away, Ver_BeamType_W2_HZ80_Away, Ver_Column)

# ======================================= Horizon Loading ===================================
# -------------- W = 20m-------------------------------
Hor_Tie20Err_L2Away = np.zeros((4,3))
Add_Err2(Hor_Tie20Err_L2Away, Hor_Tie20_error_Away, Hor_LK_W20_HZ10_Away, Hor_LK_W20_HZ20_Away, Hor_LK_W20_HZ40_Away, Hor_LK_W20_HZ80_Away, Hor_Tie_W20_HZ10_Away, Hor_Tie_W20_HZ20_Away, Hor_Tie_W20_HZ40_Away, Hor_Tie_W20_HZ80_Away, Hor_Column)

Hor_LK20Err_L2Away = np.zeros((4,3))
Add_Err2(Hor_LK20Err_L2Away, Hor_LK20_error_Away, Hor_LK_W20_HZ10_Away, Hor_LK_W20_HZ20_Away, Hor_LK_W20_HZ40_Away, Hor_LK_W20_HZ80_Away, Hor_LK_W20_HZ10_Away, Hor_LK_W20_HZ20_Away, Hor_LK_W20_HZ40_Away, Hor_LK_W20_HZ80_Away, Hor_Column)

Hor_BeamType_W20Err_L2Away = np.zeros((4,3))
Add_Err2(Hor_BeamType_W20Err_L2Away, Hor_BeamType_20error_Away, Hor_LK_W20_HZ10_Away, Hor_LK_W20_HZ20_Away, Hor_LK_W20_HZ40_Away, Hor_LK_W20_HZ80_Away, Hor_BeamType_W20_HZ10_Away, Hor_BeamType_W20_HZ20_Away, Hor_BeamType_W20_HZ40_Away, Hor_BeamType_W20_HZ80_Away, Hor_Column)
# -------------- W = 10m-------------------------------
Hor_Tie10Err_L2Away = np.zeros((4,3))
Add_Err2(Hor_Tie10Err_L2Away, Hor_Tie10_error_Away, Hor_LK_W20_HZ10_Away, Hor_LK_W20_HZ20_Away, Hor_LK_W20_HZ40_Away, Hor_LK_W20_HZ80_Away, Hor_Tie_W10_HZ10_Away, Hor_Tie_W10_HZ20_Away, Hor_Tie_W10_HZ40_Away, Hor_Tie_W10_HZ80_Away, Hor_Column)

Hor_LK10Err_L2Away = np.zeros((4,3))
Add_Err2(Hor_LK10Err_L2Away, Hor_LK10_error_Away, Hor_LK_W20_HZ10_Away, Hor_LK_W20_HZ20_Away, Hor_LK_W20_HZ40_Away, Hor_LK_W20_HZ80_Away, Hor_LK_W10_HZ10_Away, Hor_LK_W10_HZ20_Away, Hor_LK_W10_HZ40_Away, Hor_LK_W10_HZ80_Away, Hor_Column)

Hor_BeamType_W10Err_L2Away = np.zeros((4,3))
Add_Err2(Hor_BeamType_W10Err_L2Away, Hor_BeamType_10error_Away, Hor_LK_W20_HZ10_Away, Hor_LK_W20_HZ20_Away, Hor_LK_W20_HZ40_Away, Hor_LK_W20_HZ80_Away, Hor_BeamType_W10_HZ10_Away, Hor_BeamType_W10_HZ20_Away, Hor_BeamType_W10_HZ40_Away, Hor_BeamType_W10_HZ80_Away, Hor_Column)
# -------------- W = 5m-------------------------------
Hor_Tie5Err_L2Away = np.zeros((4,3))
Add_Err2(Hor_Tie5Err_L2Away, Hor_Tie5_error_Away, Hor_LK_W20_HZ10_Away, Hor_LK_W20_HZ20_Away, Hor_LK_W20_HZ40_Away, Hor_LK_W20_HZ80_Away, Hor_Tie_W5_HZ10_Away, Hor_Tie_W5_HZ20_Away, Hor_Tie_W5_HZ40_Away, Hor_Tie_W5_HZ80_Away, Hor_Column)

Hor_LK5Err_L2Away = np.zeros((4,3))
Add_Err2(Hor_LK5Err_L2Away, Hor_LK5_error_Away, Hor_LK_W20_HZ10_Away, Hor_LK_W20_HZ20_Away, Hor_LK_W20_HZ40_Away, Hor_LK_W20_HZ80_Away, Hor_LK_W5_HZ10_Away, Hor_LK_W5_HZ20_Away, Hor_LK_W5_HZ40_Away, Hor_LK_W5_HZ80_Away, Hor_Column)

Hor_BeamType_W5Err_L2Away = np.zeros((4,3))
Add_Err2(Hor_BeamType_W5Err_L2Away, Hor_BeamType_5error_Away, Hor_LK_W20_HZ10_Away, Hor_LK_W20_HZ20_Away, Hor_LK_W20_HZ40_Away, Hor_LK_W20_HZ80_Away, Hor_BeamType_W5_HZ10_Away, Hor_BeamType_W5_HZ20_Away, Hor_BeamType_W5_HZ40_Away, Hor_BeamType_W5_HZ80_Away, Hor_Column)
# -------------- W = 2m-------------------------------
Hor_Tie2Err_L2Away = np.zeros((4,3))
Add_Err2(Hor_Tie2Err_L2Away, Hor_Tie2_error_Away, Hor_LK_W20_HZ10_Away, Hor_LK_W20_HZ20_Away, Hor_LK_W20_HZ40_Away, Hor_LK_W20_HZ80_Away, Hor_Tie_W2_HZ10_Away, Hor_Tie_W2_HZ20_Away, Hor_Tie_W2_HZ40_Away, Hor_Tie_W2_HZ80_Away, Hor_Column)

Hor_LK2Err_L2Away = np.zeros((4,3))
Add_Err2(Hor_LK2Err_L2Away, Hor_LK2_error_Away, Hor_LK_W20_HZ10_Away, Hor_LK_W20_HZ20_Away, Hor_LK_W20_HZ40_Away, Hor_LK_W20_HZ80_Away, Hor_LK_W2_HZ10_Away, Hor_LK_W2_HZ20_Away, Hor_LK_W2_HZ40_Away, Hor_LK_W2_HZ80_Away, Hor_Column)

Hor_BeamType_W2Err_L2Away = np.zeros((4,3))
Add_Err2(Hor_BeamType_W2Err_L2Away, Hor_BeamType_2error_Away, Hor_LK_W20_HZ10_Away, Hor_LK_W20_HZ20_Away, Hor_LK_W20_HZ40_Away, Hor_LK_W20_HZ80_Away, Hor_BeamType_W2_HZ10_Away, Hor_BeamType_W2_HZ20_Away, Hor_BeamType_W2_HZ40_Away, Hor_BeamType_W2_HZ80_Away, Hor_Column)

# ======================================= Rocking Loading ===================================
# -------------- W = 20m-------------------------------
Roc_Tie20Err_L2Away = np.zeros((4,3))
Add_Err2(Roc_Tie20Err_L2Away, Roc_Tie20_error_Away, Roc_LK_W20_HZ10_Away, Roc_LK_W20_HZ20_Away, Roc_LK_W20_HZ40_Away, Roc_LK_W20_HZ80_Away, Roc_Tie_W20_HZ10_Away, Roc_Tie_W20_HZ20_Away, Roc_Tie_W20_HZ40_Away, Roc_Tie_W20_HZ80_Away, Ver_Column)

Roc_LK20Err_L2Away = np.zeros((4,3))
Add_Err2(Roc_LK20Err_L2Away, Roc_LK20_error_Away, Roc_LK_W20_HZ10_Away, Roc_LK_W20_HZ20_Away, Roc_LK_W20_HZ40_Away, Roc_LK_W20_HZ80_Away, Roc_LK_W20_HZ10_Away, Roc_LK_W20_HZ20_Away, Roc_LK_W20_HZ40_Away, Roc_LK_W20_HZ80_Away, Ver_Column)

Roc_BeamType_W20Err_L2Away = np.zeros((4,3))
Add_Err2(Roc_BeamType_W20Err_L2Away, Roc_BeamType_20error_Away, Roc_LK_W20_HZ10_Away, Roc_LK_W20_HZ20_Away, Roc_LK_W20_HZ40_Away, Roc_LK_W20_HZ80_Away, Roc_BeamType_W20_HZ10_Away, Roc_BeamType_W20_HZ20_Away, Roc_BeamType_W20_HZ40_Away, Roc_BeamType_W20_HZ80_Away, Ver_Column)
# -------------- W = 10m-------------------------------
Roc_Tie10Err_L2Away = np.zeros((4,3))
Add_Err2(Roc_Tie10Err_L2Away, Roc_Tie10_error_Away, Roc_LK_W20_HZ10_Away, Roc_LK_W20_HZ20_Away, Roc_LK_W20_HZ40_Away, Roc_LK_W20_HZ80_Away, Roc_Tie_W10_HZ10_Away, Roc_Tie_W10_HZ20_Away, Roc_Tie_W10_HZ40_Away, Roc_Tie_W10_HZ80_Away, Ver_Column)

Roc_LK10Err_L2Away = np.zeros((4,3))
Add_Err2(Roc_LK10Err_L2Away, Roc_LK10_error_Away, Roc_LK_W20_HZ10_Away, Roc_LK_W20_HZ20_Away, Roc_LK_W20_HZ40_Away, Roc_LK_W20_HZ80_Away, Roc_LK_W10_HZ10_Away, Roc_LK_W10_HZ20_Away, Roc_LK_W10_HZ40_Away, Roc_LK_W10_HZ80_Away, Ver_Column)

Roc_BeamType_W10Err_L2Away = np.zeros((4,3))
Add_Err2(Roc_BeamType_W10Err_L2Away, Roc_BeamType_10error_Away, Roc_LK_W20_HZ10_Away, Roc_LK_W20_HZ20_Away, Roc_LK_W20_HZ40_Away, Roc_LK_W20_HZ80_Away, Roc_BeamType_W10_HZ10_Away, Roc_BeamType_W10_HZ20_Away, Roc_BeamType_W10_HZ40_Away, Roc_BeamType_W10_HZ80_Away, Ver_Column)
# -------------- W = 5m-------------------------------
Roc_Tie5Err_L2Away = np.zeros((4,3))
Add_Err2(Roc_Tie5Err_L2Away, Roc_Tie5_error_Away, Roc_LK_W20_HZ10_Away, Roc_LK_W20_HZ20_Away, Roc_LK_W20_HZ40_Away, Roc_LK_W20_HZ80_Away, Roc_Tie_W5_HZ10_Away, Roc_Tie_W5_HZ20_Away, Roc_Tie_W5_HZ40_Away, Roc_Tie_W5_HZ80_Away, Ver_Column)

Roc_LK5Err_L2Away = np.zeros((4,3))
Add_Err2(Roc_LK5Err_L2Away, Roc_LK5_error_Away, Roc_LK_W20_HZ10_Away, Roc_LK_W20_HZ20_Away, Roc_LK_W20_HZ40_Away, Roc_LK_W20_HZ80_Away, Roc_LK_W5_HZ10_Away, Roc_LK_W5_HZ20_Away, Roc_LK_W5_HZ40_Away, Roc_LK_W5_HZ80_Away, Ver_Column)

Roc_BeamType_W5Err_L2Away = np.zeros((4,3))
Add_Err2(Roc_BeamType_W5Err_L2Away, Roc_BeamType_5error_Away, Roc_LK_W20_HZ10_Away, Roc_LK_W20_HZ20_Away, Roc_LK_W20_HZ40_Away, Roc_LK_W20_HZ80_Away, Roc_BeamType_W5_HZ10_Away, Roc_BeamType_W5_HZ20_Away, Roc_BeamType_W5_HZ40_Away, Roc_BeamType_W5_HZ80_Away, Ver_Column)
# -------------- W = 2m-------------------------------
Roc_Tie2Err_L2Away = np.zeros((4,3))
Add_Err2(Roc_Tie2Err_L2Away, Roc_Tie2_error_Away, Roc_LK_W20_HZ10_Away, Roc_LK_W20_HZ20_Away, Roc_LK_W20_HZ40_Away, Roc_LK_W20_HZ80_Away, Roc_Tie_W2_HZ10_Away, Roc_Tie_W2_HZ20_Away, Roc_Tie_W2_HZ40_Away, Roc_Tie_W2_HZ80_Away, Ver_Column)

Roc_LK2Err_L2Away = np.zeros((4,3))
Add_Err2(Roc_LK2Err_L2Away, Roc_LK2_error_Away, Roc_LK_W20_HZ10_Away, Roc_LK_W20_HZ20_Away, Roc_LK_W20_HZ40_Away, Roc_LK_W20_HZ80_Away, Roc_LK_W2_HZ10_Away, Roc_LK_W2_HZ20_Away, Roc_LK_W2_HZ40_Away, Roc_LK_W2_HZ80_Away, Ver_Column)

Roc_BeamType_W2Err_L2Away = np.zeros((4,3))
Add_Err2(Roc_BeamType_W2Err_L2Away, Roc_BeamType_2error_Away, Roc_LK_W20_HZ10_Away, Roc_LK_W20_HZ20_Away, Roc_LK_W20_HZ40_Away, Roc_LK_W20_HZ80_Away, Roc_BeamType_W2_HZ10_Away, Roc_BeamType_W2_HZ20_Away, Roc_BeamType_W2_HZ40_Away, Roc_BeamType_W2_HZ80_Away, Ver_Column)

# ==================Draw L2 Norm error : Middele point (td) =============================
def DifferTime_L2Error2(Hor_LKErr, Hor_ProposedErr, Ver_LKErr, Ver_ProposedErr, Roc_LKErr, Roc_ProposedErr):
    # ------------ Horizon --------------------------
    plt.plot(Dy_lambP[:], Hor_LKErr[:,1],marker = '^',markersize=16,markerfacecolor = 'white',label = 'LK Dashpot', color = 'red', linewidth = 3.0)
    plt.plot(Dy_lambP[:], Hor_ProposedErr[:,1],marker = 'p',markersize=12,markerfacecolor = 'white',label = 'Proposed', color = 'red', linewidth = 3.0)
   
  # ----------------Vertical------------------------------
    plt.plot(Dy_lambS[:], Ver_LKErr[:,1],marker = '^',markersize=16,markerfacecolor = 'white', color = 'blue', linewidth = 3.0)
    plt.plot(Dy_lambS[:], Ver_ProposedErr[:,1],marker = 'p',markersize=12,markerfacecolor = 'white', color = 'blue', linewidth = 3.0) # , ls = '--'

    # ----------------Rocking------------------------------
    plt.plot(Dy_lambS[:], Roc_LKErr[:,1],marker = '^',markersize=16,markerfacecolor = 'white', color = 'darkgrey', linewidth = 3.0)
    plt.plot(Dy_lambS[:], Roc_ProposedErr[:,1],marker = 'p',markersize=12,markerfacecolor = 'white', color = 'darkgrey', linewidth = 3.0) # , ls = '--'
    
    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 18)

    # plt.xlim(0.0, 0.20)
    plt.grid(True)
    
    ax = plt.gca()
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.125))
    # -------------- Consider X-axis  -----------------------
    ax.set_xscale('log', base=10)
    ax.set_xticks([], minor=False)
    ax.set_xticks([], minor=True)
    x_ticks_Num = np.array([0.01, 0.02, 0.04, 0.06, 0.08, 0.1])
    ax.set_xticks(x_ticks_Num)
    # ------- Miner ticks -----------------
    ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='x', which='minor', length=4, color='gray')
    
    ax.set_xticklabels([f'{tick:.2f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='both', labelsize= 17)
    # -------------- Consider Y-axis  ----------------------- 
#--- Mid: 0.02, 0.04, 0.06, 0.08, 0.20, 0.40, 0.60, 0.80 / Away: 0.08, 0.20, 0.40, 0.60, 0.80, 1.0, 2.0 --#    
    ax.set_yscale('log', base=10)
    ax.set_yticks([], minor=False)
    ax.set_yticks([], minor=True)
    y_ticks_Num = np.array([0.08, 0.20, 0.40, 0.60, 0.80, 2.0, 4.0])
    ax.set_yticks(y_ticks_Num)
    ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks_Num], rotation=0, fontsize=12)
    ax.tick_params(axis='y', which='both', labelsize=15)
    # ------- Miner ticks -----------------
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='y', which='minor', length=4, color='gray')
    
# fig3, (ax9,ax10,ax11, ax12) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# fig3.text(0.13,0.85, "Middle Node", color = "black", fontsize=22)

# # fig3.text(0.02,0.5, 'Normalized L2 Norm Error '+ r"$\ E_{L2}$", va= 'center', rotation= 'vertical', fontsize=25)
# fig3.text(0.02,0.5, 'Normalized L2 Norm Error '+ r"$\ E^{0.2\,\mathrm{to}\,0.4}_{L2}$", va= 'center', rotation= 'vertical', fontsize=25)

# fig3.text(0.45,0.060, r'$\Delta_c/\lambda$', va= 'center', fontsize=25)

# ax9 = plt.subplot(411)
# DifferTime_L2Error2(Hor_LK20Err_L2, Hor_BeamType_W20Err_L2, Ver_LK20Err_L2, Ver_BeamType_W20Err_L2, Roc_LK20Err_L2, Roc_BeamType_W20Err_L2)
# ax9.set_title(r"$w=$ $\mathrm{20m}$",fontsize =25, x=0.87, y=0.80)

# ax10 = plt.subplot(412) # 311 / 412
# DifferTime_L2Error2(Hor_LK10Err_L2, Hor_BeamType_W10Err_L2, Ver_LK10Err_L2, Ver_BeamType_W10Err_L2, Roc_LK10Err_L2, Roc_BeamType_W10Err_L2)
# ax10.set_title(r"$w=$ $\mathrm{10m}$",fontsize =25, x=0.87, y=0.80)

# ax11 = plt.subplot(413) # 312 / 413
# DifferTime_L2Error2(Hor_LK5Err_L2, Hor_BeamType_W5Err_L2, Ver_LK5Err_L2, Ver_BeamType_W5Err_L2, Roc_LK5Err_L2, Roc_BeamType_W5Err_L2)
# ax11.set_title(r"$w=$ $\mathrm{5m}$",fontsize =25, x=0.87, y=0.80)

# ax12 = plt.subplot(414) # 313 / 414
# DifferTime_L2Error2(Hor_LK2Err_L2, Hor_BeamType_W2Err_L2, Ver_LK2Err_L2, Ver_BeamType_W2Err_L2, Roc_LK2Err_L2, Roc_BeamType_W2Err_L2)
# ax12.set_title(r"$w=$ $\mathrm{2m}$",fontsize =25, x=0.87, y=0.80)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting
# legend_elements = [Line2D([0], [0], color='red', lw=2, label= f'Horizon Loading'),
#                 Line2D([0], [0], color='blue', lw=2, label= f'Vertical Loading'),
#                 ] # Line2D([0], [0], color='darkgrey', lw=2, label= f'Rocking Loading')

# legend_elements2 =  [Line2D([0], [0], color='black',marker = '^',markersize=16,markerfacecolor = 'white', label= 'LK Dashpot'),
#                     Line2D([0], [0], color='black',marker = 'p',markersize=12,markerfacecolor = 'white', label= 'Proposed')]

# lines, labels = fig3.axes[-1].get_legend_handles_labels()
# legend1 = fig3.legend(handles=legend_elements, loc=(0.30, 0.88) ,prop=font_props) # , title="Legend 1"
# fig3.add_artist(legend1)

# legend2 = fig3.legend(handles=legend_elements2, loc=(0.60, 0.88) ,prop=font_props)

# fig4, (ax13,ax14,ax15, ax16) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# fig4.text(0.13,0.85, "Node 1 m away from the midpoint", color = "black", fontsize=22)

# # fig4.text(0.02,0.5, 'Normalized L2 Norm Error '+ r"$\ E_{L2}$", va= 'center', rotation= 'vertical', fontsize=25)
# fig4.text(0.02,0.5, 'Normalized L2 Norm Error '+ r"$\ E^{0.2\,\mathrm{to}\,0.4}_{L2}$", va= 'center', rotation= 'vertical', fontsize=25)

# fig4.text(0.45,0.060, r'$\Delta_c/\lambda$', va= 'center', fontsize=25)

# ax5 = plt.subplot(411)
# DifferTime_L2Error2(Hor_LK20Err_L2Away, Hor_BeamType_W20Err_L2Away, Ver_LK20Err_L2Away, Ver_BeamType_W20Err_L2Away, Roc_LK20Err_L2Away, Roc_BeamType_W20Err_L2Away)
# ax5.set_title(r"$w=$ $\mathrm{20m}$",fontsize =25, x=0.87, y=0.80)

# ax12 = plt.subplot(412) # 311 / 412
# DifferTime_L2Error2(Hor_LK10Err_L2Away, Hor_BeamType_W10Err_L2Away, Ver_LK10Err_L2Away, Ver_BeamType_W10Err_L2Away, Roc_LK10Err_L2Away, Roc_BeamType_W10Err_L2Away)
# ax12.set_title(r"$w=$ $\mathrm{10m}$",fontsize =25, x=0.87, y=0.80)

# ax13 = plt.subplot(413) # 312 / 413
# DifferTime_L2Error2(Hor_LK5Err_L2Away, Hor_BeamType_W5Err_L2Away, Ver_LK5Err_L2Away, Ver_BeamType_W5Err_L2Away, Roc_LK5Err_L2Away, Roc_BeamType_W5Err_L2Away)
# ax13.set_title(r"$w=$ $\mathrm{5m}$",fontsize =25, x=0.87, y=0.80)

# ax14 = plt.subplot(414) # 313 / 414
# DifferTime_L2Error2(Hor_LK2Err_L2Away, Hor_BeamType_W2Err_L2Away, Ver_LK2Err_L2Away, Ver_BeamType_W2Err_L2Away, Roc_LK2Err_L2Away, Roc_BeamType_W2Err_L2Away)
# ax14.set_title(r"$w=$ $\mathrm{2m}$",fontsize =25, x=0.87, y=0.80)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting
# legend_elements = [Line2D([0], [0], color='red', lw=2, label= f'Horizon Loading'),
#                 Line2D([0], [0], color='blue', lw=2, label= f'Vertical Loading'),
#                 Line2D([0], [0], color='darkgrey', lw=2, label= f'Rocking Loading')] 

# legend_elements2 =  [Line2D([0], [0], color='black',marker = '^',markersize=16,markerfacecolor = 'white', label= 'LK Dashpot'),
#                     Line2D([0], [0], color='black',marker = 'p',markersize=12,markerfacecolor = 'white', label= 'Proposed')]

# lines, labels = fig4.axes[-1].get_legend_handles_labels()
# legend1 = fig4.legend(handles=legend_elements, loc=(0.30, 0.88) ,prop=font_props) # , title="Legend 1"
# fig4.add_artist(legend1)

# legend2 = fig4.legend(handles=legend_elements2, loc=(0.60, 0.88) ,prop=font_props)
