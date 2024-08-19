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

# ===================== Theory Pwave =============================================
Soil_80row= 80 # dt= 6.25e-05   #cpdt = 3.34e-05
Soil_40row= 40

Nele = Soil_40row # Soil_80row
End_Ele = Nele-1
cs = 200 # m/s
soilLength = 10 # m(Soil_Depth)

nu = (1/3)  #  0.3 -> (epsilon_z /=0)
rho = 2000 # kg/m3 
G = (cs*cs)*rho  # N/m^2 = Kg/(m*s^2)
E =  G*2*(1+nu)  # N/m^2 = Kg/(m*s^2)
cp = (E*(1-nu)/((1+nu)*(1-2*nu)*rho))**(0.5)

A = 0.1# 0.1
# ======== Different frequency to Control Ws and Wp (v = f * lambda)======================
# ws_40HZ =  (2*pi)/5 # 0 to 5m = 0 to 2*pi => x = 2*pi/5
# ws_20HZ =  pi/5  # 0 to 10m = 0 to 2*pi => x = pi/5
# ws_10HZ =  pi/10 # 0 to 20m = 0 to 2*pi => x = pi/10

wp_20HZ =  pi/10 # 0 to 20m = 0 to 2*pi => x = pi/10
wp_10HZ =  pi/20 # 0 to 40m = 0 to 2*pi => x = pi/20
wp_40HZ =  pi/5 # 0 to 10m = 0 to 2*pi => x = pi/5

fp_20HZ = 20
fp_10HZ = 10
fp_40HZ = 40

# ******************** Input which Frequency you want to Draw ********************************
HZ = fp_40HZ
Pwave_HZ = wp_40HZ

# ============================== Consider PWave ======================================
L = cp/HZ # ***
# calculate eace step time
tns_cp = soilLength/cp # wave transport time
dcell_cp = tns_cp/Nele #each cell time
dt_cp = dcell_cp*0.1 #eace cell have 10 steps
print(f"Pwave travel = {tns_cp} ;dcell = {dcell_cp} ;dt = {dt_cp}")

Input_Time = L/cp

time_cp = np.arange(0.0, Input_Time + dt_cp, dt_cp)
Nt_cp = len(time_cp)

#----------- Soil Coordinate --------------
x = cp*time_cp #m
def Incoming_wave(w, x, cp, t):  #事實上為（xi,yi,t），空間跟時間資訊全寫進去，目前只用到yi的空間
    return np.sin(w*(x-cp*t)) # Normal：np.sin(w*(x-cs*t))

def Outgoing_wave(w, x, cp, t):
    return np.sin(w*(x+cp*t)) # Norrmal： np.sin(w*(x+cs*t))

Nnode = Nele + 1
End_Node = Nele
dy = soilLength/Nele 
dx= dy/10 # 0.1, 0.01 each element have 10 step dx

total_Transport_cp = np.arange(0.0, 2*L+0.1, dx)

# ---------- Incoming wave (Beam distributed load)------------------
XIn = np.zeros((len(total_Transport_cp), Nele))
# X = 0~10 m 
for j in range(Nele): #100 
    tin = time_cp[10*j+5]
    x0 = x[10*j+5]  # 0.05,0.15,0.25....,9.95
    # print(x0,cp*tin)
    for i in range(len(time_cp)):      
        xii = x0 + dx*i 
        XIn[5+10*j+i,j] = Incoming_wave(Pwave_HZ, xii, cp, tin)  #from 0.05m to 9.95m

# ---------- Outcoming wave (Beam distributed load)-------------------
XOut = np.zeros((len(total_Transport_cp), Nele))
Output_disp = 5 # 9.95
End_disp = 10*Nele-5
# X = 10m ~ 20m
for j in range(Nele):# 100 Nele
    tout = time_cp[Output_disp+10*j] 
    x0 = (L-(dy/2))-dy*j   #9.5/9.75/9.875/9.9375/9.95-dy*j 
    # print(x0,cp*tout)
    for i in range(len(time_cp)):      
        xoo = x0 + dx*i 
        XOut[End_disp-10*j+i,End_Ele-j] = Outgoing_wave(Pwave_HZ, xoo, cp, tout)  #from 9.95m to 0.05m      
    
total_time = np.arange(0.0,0.40003,dt_cp)
Pwave = np.zeros((len(total_time),Nele))

# ===== New BC Sideforce on Left and Right ==============
PSideforce_y = np.zeros((len(total_time),Nele))  # 10
PSideforce_x = np.zeros((len(total_time),Nele))  # 10

# ----- 事實上是算 taux、tauy ------------------
Cp_vel_Coefficient =  2*1e4/(A*rho*cp)

# Pwave Hz=10 => Xin + Xin (入射波跟回彈波都一樣 xin)
# ===== Input Incoming Wave and Outcoming Wave to wave1 =======================
for g in range(Nele): #Nele
    to = 5 + 10*g
    for t in range(len(total_time)):
        if total_time[t] < Input_Time: # total_time[t] < 0.025
            Pwave[to+t,g] = (Pwave[to+t,g] + Cp_vel_Coefficient*XIn[to+t,g])  # original wave transport
            
        if total_time[t] >= 0.025 and total_time[t] < (0.025+Input_Time): # total_time[t] >= 0.025 and total_time[t] < 0.050
            Pwave[to+t,End_Ele-g] = Pwave[to+t,End_Ele-g] + Cp_vel_Coefficient*XIn[t-to,End_Ele-g]   # XOut[t-to,End_Ele-g]

# plt.plot(total_time, Pwave[:, Nele-1], linewidth = 3.0)
# plt.xlim(0,0.2)
# plt.grid(True)

# ====================== Read File From Numerical ==================================
# soilwidth = int(2.0)
# ny = int(40) # 80, 40, 20. 10
# HZ = 20

YMesh = np.array([40]) # 80, 40, 20, 10

def Find_Middle(soilwidth, YMesh):
    Dw = soilLength/80 # soilLength/80 , soilLength/ny
    
    nx = int(soilwidth/Dw)
    MiddelNode = []
    # ------ Recorde Node/Element ID -----------------------------------------------
    for i in range(len(YMesh)):
        ny = int(YMesh[i])
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
# ---------- Consider Mesh = 80, 40, 20, 10 row -----------------
# W2_Mid80row, W2_Mid40row, W2_Mid20row, W2_Mid10row = Find_Middle(int(2.0), YMesh)
# W10_Mid80row, W10_Mid40row, W10_Mid20row, W10_Mid10row = Find_Middle(int(10.0), YMesh)
# W20_Mid80row, W20_Mid40row, W20_Mid20row, W20_Mid10row = Find_Middle(int(20.0), YMesh)

# ---------- Consider Mesh = 40 row -----------------
W2_Mid40row = Find_Middle(int(2.0), YMesh)
W10_Mid40row = Find_Middle(int(10.0), YMesh)
W20_Mid40row = Find_Middle(int(20.0), YMesh)

Wave_Choose = f'1D_Transport/Newmark_Linear/Pwave'
# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
Condition1 = f'{Wave_Choose}/W_2m/HZ_{HZ}'
# --------- Tie Boundary Condition ----------------
file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/TieBC_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file3 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file4 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType2_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file5 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType3_40row/Velocity/node{W2_Mid40row}.out"

Tie_W2_Mid40row = rdnumpy(file1)
LK_W2_Mid40row = rdnumpy(file2)
Tyep1_W2_Mid40row = rdnumpy(file3)
Tyep2_W2_Mid40row = rdnumpy(file4)
Tyep3_W2_Mid40row = rdnumpy(file5)

# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
Condition2 = f'{Wave_Choose}/W_10m/HZ_{HZ}'
# --------- Tie Boundary Condition ----------------
file6 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file7 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file8 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file9 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file10 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_40row/Velocity/node{W10_Mid40row}.out"

Tie_W10_Mid40row = rdnumpy(file6)
LK_W10_Mid40row = rdnumpy(file7)
Tyep1_W10_Mid40row = rdnumpy(file8)
Tyep2_W10_Mid40row = rdnumpy(file9)
Tyep3_W10_Mid40row = rdnumpy(file10)

# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
Condition3 = f'{Wave_Choose}/W_20m/HZ_{HZ}'
# --------- Tie Boundary Condition ----------------
file11 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/TieBC_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file12 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file13 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType2_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType3_40row/Velocity/node{W20_Mid40row}.out"

Tie_W20_Mid40row = rdnumpy(file11)
LK_W20_Mid40row = rdnumpy(file12)
Tyep1_W20_Mid40row = rdnumpy(file13)
Tyep2_W20_Mid40row = rdnumpy(file14)
Tyep3_W20_Mid40row = rdnumpy(file15)

def Find_Quarter(soilwidth, YMesh):
    Dw = soilLength/80 # soilLength/80 , soilLength/ny
    nx = int(soilwidth/Dw)
    
    QuarterNode = []
    # ------ Recorde Node/Element ID -----------------------------------------------
    for i in range(len(YMesh)):
        ny = int(YMesh[i])
        
        # -------- Quarter(3/4) Node ------------------------
        LowerN_RQuarter = int((3*nx/4)+1)
        UpperrN_RQuarter = int(LowerN_RQuarter + (nx+1)* ny)
        # print(f"LowerN_RQuarter = {LowerN_RQuarter} ,UpperrN_RQuarter = {UpperrN_RQuarter}")
        
        QuarterNode.append(UpperrN_RQuarter)
    
    Qua40row = QuarterNode[0]
    
    # Qua80row = QuarterNode[0]
    # Qua40row = QuarterNode[1]
    # Qua20row = QuarterNode[2]
    # Qua10row = QuarterNode[3]
    
    return Qua40row

W2_Qua40row = Find_Quarter(int(2.0), YMesh)
W10_Qua40roww = Find_Quarter(int(10.0), YMesh)
W20_Qua40row = Find_Quarter(int(20.0), YMesh)

# # ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
# # --------- Tie Boundary Condition ----------------
# file61 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/TieBC_80row/Velocity/node{W2_Qua80row}.out"
# file62 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/TieBC_40row/Velocity/node{W2_Qua40row}.out"
# file63 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/TieBC_20row/Velocity/node{W2_Qua20row}.out"
# file64 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/TieBC_10row/Velocity/node{W2_Qua10row}.out"
# # --------- LK Dashpot Boundary Condition ----------------
# file65 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_80row/Velocity/node{W2_Qua80row}.out"
# file66 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_40row/Velocity/node{W2_Qua40row}.out"
# file67 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_20row/Velocity/node{W2_Qua20row}.out"
# file68 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_10row/Velocity/node{W2_Qua10row}.out"
# # --------- Type 1 ：Distributed Beam Boundary Condition ----------------
# file69 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_80row/Velocity/node{W2_Qua80row}.out"
# file70 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_40row/Velocity/node{W2_Qua40row}.out"
# file71 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_20row/Velocity/node{W2_Qua20row}.out"
# file72 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_10row/Velocity/node{W2_Qua10row}.out"
# # --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
# file73 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType2_80row/Velocity/node{W2_Qua80row}.out"
# file74 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType2_40row/Velocity/node{W2_Qua40row}.out"
# file75 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType2_20row/Velocity/node{W2_Qua20row}.out"
# file76 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType2_10row/Velocity/node{W2_Qua10row}.out"
# # --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
# file77 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType3_80row/Velocity/node{W2_Qua80row}.out"
# file78 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType3_40row/Velocity/node{W2_Qua40row}.out"
# file79 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType3_20row/Velocity/node{W2_Qua20row}.out"
# file80 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType3_10row/Velocity/node{W2_Qua10row}.out"

# Tie_W2_Qua80row = rdnumpy(file61)
# Tie_W2_Qua40row = rdnumpy(file62)
# Tie_W2_Qua20row = rdnumpy(file63)
# Tie_W2_Qua10row = rdnumpy(file64)

# LK_W2_Qua80row = rdnumpy(file65)
# LK_W2_Qua40row = rdnumpy(file66)
# LK_W2_Qua20row = rdnumpy(file67)
# LK_W2_Qua10row = rdnumpy(file68)

# Tyep1_W2_Qua80row = rdnumpy(file69)
# Tyep1_W2_Qua40row = rdnumpy(file70)
# Tyep1_W2_Qua20row = rdnumpy(file71)
# Tyep1_W2_Qua10row = rdnumpy(file72)

# Tyep2_W2_Qua80row = rdnumpy(file73)
# Tyep2_W2_Qua40row = rdnumpy(file74)
# Tyep2_W2_Qua20row = rdnumpy(file75)
# Tyep2_W2_Qua10row = rdnumpy(file76)

# Tyep3_W2_Qua80row = rdnumpy(file77)
# Tyep3_W2_Qua40row = rdnumpy(file78)
# Tyep3_W2_Qua20row = rdnumpy(file79)
# Tyep3_W2_Qua10row = rdnumpy(file80)

# # ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
# # --------- Tie Boundary Condition ----------------
# file81 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_80row/Velocity/node{W10_Qua80row}.out"
# file82 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_40row/Velocity/node{W10_Qua40row}.out"
# file83 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_20row/Velocity/node{W10_Qua20row}.out"
# file84 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_10row/Velocity/node{W10_Qua10row}.out"
# # --------- LK Dashpot Boundary Condition ----------------
# file85 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_80row/Velocity/node{W10_Qua80row}.out"
# file86 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_40row/Velocity/node{W10_Qua40row}.out"
# file87 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_20row/Velocity/node{W10_Qua20row}.out"
# file88 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_10row/Velocity/node{W10_Qua10row}.out"
# # --------- Type 1 ：Distributed Beam Boundary Condition ----------------
# file89 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_80row/Velocity/node{W10_Qua80row}.out"
# file90 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_40row/Velocity/node{W10_Qua40row}.out"
# file91 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_20row/Velocity/node{W10_Qua20row}.out"
# file92 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_10row/Velocity/node{W10_Qua10row}.out"
# # --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
# file93 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_80row/Velocity/node{W10_Qua80row}.out"
# file94 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_40row/Velocity/node{W10_Qua40row}.out"
# file95 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_20row/Velocity/node{W10_Qua20row}.out"
# file96 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_10row/Velocity/node{W10_Qua10row}.out"
# # --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
# file97 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_80row/Velocity/node{W10_Qua80row}.out"
# file98 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_40row/Velocity/node{W10_Qua40row}.out"
# file99 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_20row/Velocity/node{W10_Qua20row}.out"
# file100 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_10row/Velocity/node{W10_Qua10row}.out"

# Tie_W10_Qua80row = rdnumpy(file81)
# Tie_W10_Qua40row = rdnumpy(file82)
# Tie_W10_Qua20row = rdnumpy(file83)
# Tie_W10_Qua10row = rdnumpy(file84)

# LK_W10_Qua80row = rdnumpy(file85)
# LK_W10_Qua40row = rdnumpy(file86)
# LK_W10_Qua20row = rdnumpy(file87)
# LK_W10_Qua10row = rdnumpy(file88)

# Tyep1_W10_Qua80row = rdnumpy(file89)
# Tyep1_W10_Qua40row = rdnumpy(file90)
# Tyep1_W10_Qua20row = rdnumpy(file91)
# Tyep1_W10_Qua10row = rdnumpy(file92)

# Tyep2_W10_Qua80row = rdnumpy(file93)
# Tyep2_W10_Qua40row = rdnumpy(file94)
# Tyep2_W10_Qua20row = rdnumpy(file95)
# Tyep2_W10_Qua10row = rdnumpy(file96)

# Tyep3_W10_Qua80row = rdnumpy(file97)
# Tyep3_W10_Qua40row = rdnumpy(file98)
# Tyep3_W10_Qua20row = rdnumpy(file99)
# Tyep3_W10_Qua10row = rdnumpy(file100)
# # ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
# # --------- Tie Boundary Condition ----------------
# file81 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_80row/Velocity/node{W10_Qua80row}.out"
# file82 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_40row/Velocity/node{W10_Qua40row}.out"
# file83 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_20row/Velocity/node{W10_Qua20row}.out"
# file84 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_10row/Velocity/node{W10_Qua10row}.out"
# # --------- LK Dashpot Boundary Condition ----------------
# file85 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_80row/Velocity/node{W10_Qua80row}.out"
# file86 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_40row/Velocity/node{W10_Qua40row}.out"
# file87 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_20row/Velocity/node{W10_Qua20row}.out"
# file88 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_10row/Velocity/node{W10_Qua10row}.out"
# # --------- Type 1 ：Distributed Beam Boundary Condition ----------------
# file89 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_80row/Velocity/node{W10_Qua80row}.out"
# file90 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_40row/Velocity/node{W10_Qua40row}.out"
# file91 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_20row/Velocity/node{W10_Qua20row}.out"
# file92 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_10row/Velocity/node{W10_Qua10row}.out"
# # --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
# file93 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_80row/Velocity/node{W10_Qua80row}.out"
# file94 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_40row/Velocity/node{W10_Qua40row}.out"
# file95 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_20row/Velocity/node{W10_Qua20row}.out"
# file96 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_10row/Velocity/node{W10_Qua10row}.out"
# # --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
# file97 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_80row/Velocity/node{W10_Qua80row}.out"
# file98 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_40row/Velocity/node{W10_Qua40row}.out"
# file99 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_20row/Velocity/node{W10_Qua20row}.out"
# file100 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_10row/Velocity/node{W10_Qua10row}.out"

# Tie_W10_Qua80row = rdnumpy(file81)
# Tie_W10_Qua40row = rdnumpy(file82)
# Tie_W10_Qua20row = rdnumpy(file83)
# Tie_W10_Qua10row = rdnumpy(file84)

# LK_W10_Qua80row = rdnumpy(file85)
# LK_W10_Qua40row = rdnumpy(file86)
# LK_W10_Qua20row = rdnumpy(file87)
# LK_W10_Qua10row = rdnumpy(file88)

# Tyep1_W10_Qua80row = rdnumpy(file89)
# Tyep1_W10_Qua40row = rdnumpy(file90)
# Tyep1_W10_Qua20row = rdnumpy(file91)
# Tyep1_W10_Qua10row = rdnumpy(file92)

# Tyep2_W10_Qua80row = rdnumpy(file93)
# Tyep2_W10_Qua40row = rdnumpy(file94)
# Tyep2_W10_Qua20row = rdnumpy(file95)
# Tyep2_W10_Qua10row = rdnumpy(file96)

# Tyep3_W10_Qua80row = rdnumpy(file97)
# Tyep3_W10_Qua40row = rdnumpy(file98)
# Tyep3_W10_Qua20row = rdnumpy(file99)
# Tyep3_W10_Qua10row = rdnumpy(file100)
# # ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
# # --------- Tie Boundary Condition ----------------
# file101 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/TieBC_80row/Velocity/node{W20_Qua80row}.out"
# file102 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/TieBC_40row/Velocity/node{W20_Qua40row}.out"
# file103 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/TieBC_20row/Velocity/node{W20_Qua20row}.out"
# file104 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/TieBC_10row/Velocity/node{W20_Qua10row}.out"
# # --------- LK Dashpot Boundary Condition ----------------
# file105 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_80row/Velocity/node{W20_Qua80row}.out"
# file106 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_40row/Velocity/node{W20_Qua40row}.out"
# file107 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_20row/Velocity/node{W20_Qua20row}.out"
# file108 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_10row/Velocity/node{W20_Qua10row}.out"
# # --------- Type 1 ：Distributed Beam Boundary Condition ----------------
# file109 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_80row/Velocity/node{W20_Qua80row}.out"
# file110 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_40row/Velocity/node{W20_Qua40row}.out"
# file111 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_20row/Velocity/node{W20_Qua20row}.out"
# file112 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_10row/Velocity/node{W20_Qua10row}.out"
# # --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
# file113 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType2_80row/Velocity/node{W20_Qua80row}.out"
# file114 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType2_40row/Velocity/node{W20_Qua40row}.out"
# file115 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType2_20row/Velocity/node{W20_Qua20row}.out"
# file116 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType2_10row/Velocity/node{W20_Qua10row}.out"
# # --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
# file117 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType3_80row/Velocity/node{W20_Qua80row}.out"
# file118 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType3_40row/Velocity/node{W20_Qua40row}.out"
# file119 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType3_20row/Velocity/node{W20_Qua20row}.out"
# file120 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType3_10row/Velocity/node{W20_Qua10row}.out"

# Tie_W20_Qua80row = rdnumpy(file101)
# Tie_W20_Qua40row = rdnumpy(file102)
# Tie_W20_Qua20row = rdnumpy(file103)
# Tie_W20_Qua10row = rdnumpy(file104)

# LK_W20_Qua80row = rdnumpy(file105)
# LK_W20_Qua40row = rdnumpy(file106)
# LK_W20_Qua20row = rdnumpy(file107)
# LK_W20_Qua10row = rdnumpy(file108)

# Tyep1_W20_Qua80row = rdnumpy(file109)
# Tyep1_W20_Qua40row = rdnumpy(file110)
# Tyep1_W20_Qua20row = rdnumpy(file111)
# Tyep1_W20_Qua10row = rdnumpy(file112)

# Tyep2_W20_Qua80row = rdnumpy(file113)
# Tyep2_W20_Qua40row = rdnumpy(file114)
# Tyep2_W20_Qua20row = rdnumpy(file115)
# Tyep2_W20_Qua10row = rdnumpy(file116)

# Tyep3_W20_Qua80row = rdnumpy(file117)
# Tyep3_W20_Qua40row = rdnumpy(file118)
# Tyep3_W20_Qua20row = rdnumpy(file119)
# Tyep3_W20_Qua10row = rdnumpy(file120)

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
def Differ_BCVel(total_time, Pwave, Tie, LKDash, BeamType1, BeamType2, BeamType3):
    # font_props = {'family': 'Arial', 'size': 12}
    plt.plot(total_time, Pwave[:, Nele-1],label =r'$\mathrm{Analytical}$',color= 'black',linewidth=6.0)
    plt.plot(Tie[:,0], Tie[:,plt_axis2],label ='Tie BC', ls = '-',color= 'limegreen',linewidth=6.0)
    plt.plot(LKDash[:,0], LKDash[:,plt_axis2],label ='LK Dashpot', ls = '-.',color= 'orange',linewidth=5.0)
    plt.plot(BeamType1[:,0], BeamType1[:,plt_axis2],label ='Beam Type1', ls = ':',color= 'purple',linewidth=4.0)
    plt.plot(BeamType2[:,0], BeamType2[:,plt_axis2],label ='Beam Type2', ls = '--',color= 'blue',linewidth=3.0)
    plt.plot(BeamType3[:,0], BeamType3[:,plt_axis2],label ='Node BC',color= 'red',linewidth= 2.0)

    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xlim(0.0, 0.20) 
    plt.grid(True)
    
    ax = plt.gca()
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
    ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    ax.yaxis.get_offset_text().set(size=18)

x_axis = 0.25 # 0.1 0.05 **** 10 Times the x axis ******

row_heights = [3,3,3]
fig1, (ax1,ax2,ax3) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig1.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.25' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig1.text(0.40,0.89, "(Middle Node)", color = "red", fontsize=20)
fig1.text(0.50,0.68, r"$\mathrm {Pwave}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig1.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig1.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax1 = plt.subplot(311)
Differ_BCVel(total_time,Pwave, Tie_W20_Mid40row, LK_W20_Mid40row, Tyep1_W20_Mid40row, Tyep2_W20_Mid40row, Tyep3_W20_Mid40row)
ax1.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.50, y=0.78)

ax2 = plt.subplot(312)
Differ_BCVel(total_time,Pwave, Tie_W10_Mid40row, LK_W10_Mid40row, Tyep1_W10_Mid40row, Tyep2_W10_Mid40row, Tyep3_W10_Mid40row)
ax2.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.50, y=0.78)

ax3 = plt.subplot(313)
Differ_BCVel(total_time,Pwave, Tie_W2_Mid40row, LK_W2_Mid40row, Tyep1_W2_Mid40row, Tyep2_W2_Mid40row, Tyep3_W2_Mid40row)
ax3.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.48, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig1.axes[-1].get_legend_handles_labels()
fig1.legend(lines, labels, loc = 'center right',prop=font_props)

# # # ------- wave put into the timeSeries ---------------
# def Differ_elemetVel(total_time, Pwave, Mid80row, Mid40row, Mid20row, Mid10row):
#     plt.plot(total_time, Pwave[:,79],label =r'$\mathrm{Analytical}$',color= 'black',linewidth=4.0)
#     plt.plot(Mid80row[:,0],Mid80row[:,plt_axis2],label =r'$\Delta_y=0.125\, \mathrm{m}$', ls = '-',color= 'limegreen',linewidth=6.0)
#     plt.plot(Mid40row[:,0],Mid40row[:,plt_axis2],label =r'$\Delta_y=0.25\, \mathrm{m}$', ls = '-.',color= 'orange',linewidth=4.0)
#     plt.plot(Mid20row[:,0],Mid20row[:,plt_axis2],label =r'$\Delta_y=0.50\, \mathrm{m}$', ls = ':',color= 'purple',linewidth=3.0)
#     plt.plot(Mid10row[:,0],Mid10row[:,plt_axis2],label =r'$\Delta_y=1\, \mathrm{m}$', ls = '--',color= 'red',linewidth=2.0)
    
#     plt.xticks(fontsize = 16)
#     plt.yticks(fontsize = 16)
#     plt.xlim(0.0, 0.20)  # original x axis (totalTime = 0~0.4 s)
#     plt.grid(True)
    
#     ax = plt.gca()
#     ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
#     ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
#     ax.yaxis.get_offset_text().set(size=18)

# # fig5, (ax13,ax14,ax15) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8,8))
# # fig5.suptitle(f'Tie Boundary',x=0.50,y =0.95,fontsize = 20)
# # fig5.text(0.40,0.89, "(Middle node)", color = "red", fontsize=20)
# # fig5.text(0.55,0.80, r"$\mathrm {Pwave}$ $(t_{d} = 1/10)$", color = "blue", fontsize=20)
# # fig5.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig5.text(0.40,0.04, r"$\mathrm {time}$ ${t}$  $(10^{-1}\,s)$", va= 'center', fontsize=20)

# # ax13 = plt.subplot(311)
# # Differ_elemetVel(total_time,Pwave ,Tie_W20_Mid80row, Tie_W20_Mid40row, Tie_W20_Mid20row, Tie_W20_Mid10row)
# # ax13.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.55, y=0.78)

# # ax14 = plt.subplot(312)
# # Differ_elemetVel(total_time,Pwave ,Tie_W10_Mid80row, Tie_W10_Mid40row, Tie_W10_Mid20row, Tie_W10_Mid10row)
# # ax14.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.55, y=0.78)

# # ax15 = plt.subplot(313)
# # Differ_elemetVel(total_time,Pwave ,Tie_W2_Mid80row, Tie_W2_Mid40row, Tie_W2_Mid20row, Tie_W2_Mid10row)
# # ax15.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.55, y=0.78)

# # font_props = {'family': 'Arial', 'size': 15}  #Legend Setting
# # lines, labels = fig5.axes[-1].get_legend_handles_labels()
# # fig5.legend(lines, labels, loc = 'center right',prop=font_props)

# # fig6, (ax16,ax17,ax18) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8,8))
# # fig6.suptitle(f'Node Boundary',x=0.50,y =0.95,fontsize = 20)
# # fig6.text(0.40,0.89, "(Middle node)", color = "red", fontsize=20)
# # fig6.text(0.55,0.80, r"$\mathrm {Pwave}$ $(t_{d} = 1/10)$", color = "blue", fontsize=20)
# # fig6.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig6.text(0.40,0.04, r"$\mathrm {time}$ ${t}$  $(10^{-1}\,s)$", va= 'center', fontsize=20)

# # ax16 = plt.subplot(311)
# # Differ_elemetVel(total_time,Pwave ,Tyep3_W20_Mid80row, Tyep3_W20_Mid40row, Tyep3_W20_Mid20row, Tyep3_W20_Mid10row)
# # ax16.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.55, y=0.78)

# # ax17 = plt.subplot(312)
# # Differ_elemetVel(total_time,Pwave ,Tyep3_W10_Mid80row, Tyep3_W10_Mid40row, Tyep3_W10_Mid20row, Tyep3_W10_Mid10row)
# # ax17.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.55, y=0.78)

# # ax18 = plt.subplot(313)
# # Differ_elemetVel(total_time,Pwave ,Tyep3_W2_Mid80row, Tyep3_W2_Mid40row, Tyep3_W2_Mid20row, Tyep3_W2_Mid10row)
# # ax18.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.55, y=0.78)

# # font_props = {'family': 'Arial', 'size': 15}  #Legend Setting
# # lines, labels = fig6.axes[-1].get_legend_handles_labels()
# # fig6.legend(lines, labels, loc = 'center right',prop=font_props)

# # ================================== Prepare Relative Error and Absolute Error ============================
# def Find_ColMaxValue(column_index,ele80_Mid):
#     column = ele80_Mid[:, column_index]
#     max_value = np.max(column)
#     max_index = np.argmax(column)
    
#     min_value = np.min(column)
#     min_index = np.argmin(column)

#     print(f'max_value= {max_value}; max_index= {max_index}; min_value= {min_value}; min_index= {min_index}')
#     return(max_value,min_value)
# # =========== Find Grounf Surface Max/ Min Peak Value ==========================
# column_index = 2 # Pwave = 2 (yaxis)
# Analysis_column = 79

# # =================================== Middle Node ===================================
# # ------------ Tie Boundary Condition -----------------------
# maxTie20_Mid80, minTie20_Mid80 = Find_ColMaxValue(column_index,Tie_W20_Mid80row)
# maxTie20_Mid40, minTie20_Mid40 = Find_ColMaxValue(column_index,Tie_W20_Mid40row)
# maxTie20_Mid20, minTie20_Mid20 = Find_ColMaxValue(column_index,Tie_W20_Mid20row)
# maxTie20_Mid10, minTie20_Mid10 = Find_ColMaxValue(column_index,Tie_W20_Mid10row)

# maxTie10_Mid80, minTie10_Mid80 = Find_ColMaxValue(column_index,Tie_W10_Mid80row)
# maxTie10_Mid40, minTie10_Mid40 = Find_ColMaxValue(column_index,Tie_W10_Mid40row)
# maxTie10_Mid20, minTie10_Mid20 = Find_ColMaxValue(column_index,Tie_W10_Mid20row)
# maxTie10_Mid10, minTie10_Mid10 = Find_ColMaxValue(column_index,Tie_W10_Mid10row)

# maxTie2_Mid80, minTie2_Mid80 = Find_ColMaxValue(column_index,Tie_W2_Mid80row)
# maxTie2_Mid40, minTie2_Mid40 = Find_ColMaxValue(column_index,Tie_W2_Mid40row)
# maxTie2_Mid20, minTie2_Mid20 = Find_ColMaxValue(column_index,Tie_W2_Mid20row)
# maxTie2_Mid10, minTie2_Mid10 = Find_ColMaxValue(column_index,Tie_W2_Mid10row)

# # ------------ LK Dashpot Boundary Condition -----------------------
# maxLK20_Mid80, minLK20_Mid80 = Find_ColMaxValue(column_index,LK_W20_Mid80row)
# maxLK20_Mid40, minLK20_Mid40 = Find_ColMaxValue(column_index,LK_W20_Mid40row)
# maxLK20_Mid20, minLK20_Mid20 = Find_ColMaxValue(column_index,LK_W20_Mid20row)
# maxLK20_Mid10, minLK20_Mid10 = Find_ColMaxValue(column_index,LK_W20_Mid10row)

# maxLK10_Mid80, minLK10_Mid80 = Find_ColMaxValue(column_index,LK_W10_Mid80row)
# maxLK10_Mid40, minLK10_Mid40 = Find_ColMaxValue(column_index,LK_W10_Mid40row)
# maxLK10_Mid20, minLK10_Mid20 = Find_ColMaxValue(column_index,LK_W10_Mid20row)
# maxLK10_Mid10, minLK10_Mid10 = Find_ColMaxValue(column_index,LK_W10_Mid10row)

# maxLK2_Mid80, minLK2_Mid80 = Find_ColMaxValue(column_index,LK_W2_Mid80row)
# maxLK2_Mid40, minLK2_Mid40 = Find_ColMaxValue(column_index,LK_W2_Mid40row)
# maxLK2_Mid20, minLK2_Mid20 = Find_ColMaxValue(column_index,LK_W2_Mid20row)
# maxLK2_Mid10, minLK2_Mid10 = Find_ColMaxValue(column_index,LK_W2_Mid10row)

# # ------------ Type1：Distributed Beam Boundary Condition -----------------------
# maxType1_20_Mid80, minType1_20_Mid80 = Find_ColMaxValue(column_index,Tyep1_W20_Mid80row)
# maxType1_20_Mid40, minType1_20_Mid40 = Find_ColMaxValue(column_index,Tyep1_W20_Mid40row)
# maxType1_20_Mid20, minType1_20_Mid20 = Find_ColMaxValue(column_index,Tyep1_W20_Mid20row)
# maxType1_20_Mid10, minType1_20_Mid10 = Find_ColMaxValue(column_index,Tyep1_W20_Mid10row)

# maxType1_10_Mid80, minType1_10_Mid80 = Find_ColMaxValue(column_index,Tyep1_W10_Mid80row)
# maxType1_10_Mid40, minType1_10_Mid40 = Find_ColMaxValue(column_index,Tyep1_W10_Mid40row)
# maxType1_10_Mid20, minType1_10_Mid20 = Find_ColMaxValue(column_index,Tyep1_W10_Mid20row)
# maxType1_10_Mid10, minType1_10_Mid10 = Find_ColMaxValue(column_index,Tyep1_W10_Mid10row)

# maxType1_2_Mid80, minType1_2_Mid80 = Find_ColMaxValue(column_index,Tyep1_W2_Mid80row)
# maxType1_2_Mid40, minType1_2_Mid40 = Find_ColMaxValue(column_index,Tyep1_W2_Mid40row)
# maxType1_2_Mid20, minType1_2_Mid20 = Find_ColMaxValue(column_index,Tyep1_W2_Mid20row)
# maxType1_2_Mid10, minType1_2_Mid10 = Find_ColMaxValue(column_index,Tyep1_W2_Mid10row)

# # ------------ Type2： Beam and Node Boundary Condition -----------------------
# maxType2_20_Mid80, minType2_20_Mid80 = Find_ColMaxValue(column_index,Tyep2_W20_Mid80row)
# maxType2_20_Mid40, minType2_20_Mid40 = Find_ColMaxValue(column_index,Tyep2_W20_Mid40row)
# maxType2_20_Mid20, minType2_20_Mid20 = Find_ColMaxValue(column_index,Tyep2_W20_Mid20row)
# maxType2_20_Mid10, minType2_20_Mid10 = Find_ColMaxValue(column_index,Tyep2_W20_Mid10row)

# maxType2_10_Mid80, minType2_10_Mid80 = Find_ColMaxValue(column_index,Tyep2_W10_Mid80row)
# maxType2_10_Mid40, minType2_10_Mid40 = Find_ColMaxValue(column_index,Tyep2_W10_Mid40row)
# maxType2_10_Mid20, minType2_10_Mid20 = Find_ColMaxValue(column_index,Tyep2_W10_Mid20row)
# maxType2_10_Mid10, minType2_10_Mid10 = Find_ColMaxValue(column_index,Tyep2_W10_Mid10row)

# maxType2_2_Mid80, minType2_2_Mid80 = Find_ColMaxValue(column_index,Tyep2_W2_Mid80row)
# maxType2_2_Mid40, minType2_2_Mid40 = Find_ColMaxValue(column_index,Tyep2_W2_Mid40row)
# maxType2_2_Mid20, minType2_2_Mid20 = Find_ColMaxValue(column_index,Tyep2_W2_Mid20row)
# maxType2_2_Mid10, minType2_2_Mid10 = Find_ColMaxValue(column_index,Tyep2_W2_Mid10row)

# # ------------ Type3：Node Boundary Condition -----------------------
# maxType3_20_Mid80, minType3_20_Mid80 = Find_ColMaxValue(column_index,Tyep3_W20_Mid80row)
# maxType3_20_Mid40, minType3_20_Mid40 = Find_ColMaxValue(column_index,Tyep3_W20_Mid40row)
# maxType3_20_Mid20, minType3_20_Mid20 = Find_ColMaxValue(column_index,Tyep3_W20_Mid20row)
# maxType3_20_Mid10, minType3_20_Mid10 = Find_ColMaxValue(column_index,Tyep3_W20_Mid10row)

# maxType3_10_Mid80, minType3_10_Mid80 = Find_ColMaxValue(column_index,Tyep3_W10_Mid80row)
# maxType3_10_Mid40, minType3_10_Mid40 = Find_ColMaxValue(column_index,Tyep3_W10_Mid40row)
# maxType3_10_Mid20, minType3_10_Mid20 = Find_ColMaxValue(column_index,Tyep3_W10_Mid20row)
# maxType3_10_Mid10, minType3_10_Mid10 = Find_ColMaxValue(column_index,Tyep3_W10_Mid10row)

# maxType3_2_Mid80, minType3_2_Mid80 = Find_ColMaxValue(column_index,Tyep3_W2_Mid80row)
# maxType3_2_Mid40, minType3_2_Mid40 = Find_ColMaxValue(column_index,Tyep3_W2_Mid40row)
# maxType3_2_Mid20, minType3_2_Mid20 = Find_ColMaxValue(column_index,Tyep3_W2_Mid20row)
# maxType3_2_Mid10, minType3_2_Mid10 = Find_ColMaxValue(column_index,Tyep3_W2_Mid10row)

# maxAnaly, minAnaly = Find_ColMaxValue(Analysis_column,Pwave)
# Mesh_Size = np.zeros(4)
# ele = 80 
# for m in range(len(Mesh_Size)):
#     if m == 0 :    
#         Mesh_Size[m] = L/ (ele)
#     if m > 0:    
#         Mesh_Size[m] = Mesh_Size[m-1]*2

# def errMatrix(error_dc,maxTie20_Mid80,minTie20_Mid80,maxTie20_Mid40,minTie20_Mid40,maxTie20_Mid20,minTie20_Mid20,maxTie20_Mid10,minTie20_Mid10):
#     error_dc[:,0] = Mesh_Size[:]
#     error_dc[0,1] = maxTie20_Mid80
#     error_dc[0,2] = minTie20_Mid80
#     error_dc[1,1] = maxTie20_Mid40
#     error_dc[1,2] = minTie20_Mid40
#     error_dc[2,1] = maxTie20_Mid20
#     error_dc[2,2] = minTie20_Mid20
#     error_dc[3,1] = maxTie20_Mid10
#     error_dc[3,2] = minTie20_Mid10
#     return error_dc

# # ============================= Middle Node ========================================
# # ------------W20m Tie BC Error Peak Value-----------------------
# MidTie20_error = np.zeros((4,3))
# errMatrix(MidTie20_error,maxTie20_Mid80,minTie20_Mid80,maxTie20_Mid40,minTie20_Mid40,maxTie20_Mid20,minTie20_Mid20,maxTie20_Mid10,minTie20_Mid10)
# # ------------W20m LK BC Error Peak Value-----------------------
# MidLK20_error = np.zeros((4,3))
# errMatrix(MidLK20_error,maxLK20_Mid80,minLK20_Mid80,maxLK20_Mid40,minLK20_Mid40,maxLK20_Mid20,minLK20_Mid20,maxLK20_Mid10,minLK20_Mid10)
# # ------------W20m Type1 ：Distributed Beam BC Error Peak Value-----------------------
# MidType1_20_error = np.zeros((4,3))
# errMatrix(MidType1_20_error,maxType1_20_Mid80,minType1_20_Mid80,maxType1_20_Mid40,minType1_20_Mid40,maxType1_20_Mid20,minType1_20_Mid20,maxType1_20_Mid10,minType1_20_Mid10)
# # ------------W20m Type2： Beam and Node BC Error Peak Value-----------------------
# MidType2_20_error = np.zeros((4,3))
# errMatrix(MidType2_20_error,maxType2_20_Mid80,minType2_20_Mid80,maxType2_20_Mid40,minType2_20_Mid40,maxType2_20_Mid20,minType2_20_Mid20,maxType2_20_Mid10,minType2_20_Mid10)
# # ------------W20m Type3： Node BC Error Peak Value-----------------------
# MidType3_20_error = np.zeros((4,3))
# errMatrix(MidType3_20_error,maxType3_20_Mid80,minType3_20_Mid80,maxType3_20_Mid40,minType3_20_Mid40,maxType3_20_Mid20,minType3_20_Mid20,maxType3_20_Mid10,minType3_20_Mid10)

# # ------------W10m Tie BC Error Peak Value-----------------------
# MidTie10_error = np.zeros((4,3))
# errMatrix(MidTie10_error, maxTie10_Mid80,minTie10_Mid80, maxTie10_Mid40,minTie10_Mid40, maxTie10_Mid20,minTie10_Mid20, maxTie10_Mid10,minTie10_Mid10)
# # ------------W10m LK BC Error Peak Value-----------------------
# MidLK10_error = np.zeros((4,3))
# errMatrix(MidLK10_error, maxLK10_Mid80,minLK10_Mid80, maxLK10_Mid40,minLK10_Mid40, maxLK10_Mid20,minLK10_Mid20, maxLK10_Mid10,minLK10_Mid10)
# # ------------W10m Type1 ：Distributed Beam BC Error Peak Value-----------------------
# MidType1_10_error = np.zeros((4,3))
# errMatrix(MidType1_10_error, maxType1_10_Mid80,minType1_10_Mid80, maxType1_10_Mid40,minType1_10_Mid40, maxType1_10_Mid20,minType1_10_Mid20, maxType1_10_Mid10,minType1_10_Mid10)
# # # ------------W10m Type2：Beam and Node BC Error Peak Value-----------------------
# MidType2_10_error = np.zeros((4,3))
# errMatrix(MidType2_10_error, maxType2_10_Mid80,minType2_10_Mid80, maxType2_10_Mid40,minType2_10_Mid40, maxType2_10_Mid20,minType2_10_Mid20, maxType2_10_Mid10,minType2_10_Mid10)
# # # ------------W10m Type3：Node BC Error Peak Value-----------------------
# MidType3_10_error = np.zeros((4,3))
# errMatrix(MidType3_10_error, maxType3_10_Mid80,minType3_10_Mid80, maxType3_10_Mid40,minType3_10_Mid40, maxType3_10_Mid20,minType3_10_Mid20, maxType3_10_Mid10,minType3_10_Mid10)

# # ------------W2m Tie BC Error Peak Value-----------------------
# MidTie2_error = np.zeros((4,3))
# errMatrix(MidTie2_error, maxTie2_Mid80,minTie2_Mid80, maxTie2_Mid40,minTie2_Mid40, maxTie2_Mid20,minTie2_Mid20, maxTie2_Mid10,minTie2_Mid10)
# # ------------W2m LK BC Error Peak Value-----------------------
# MidLK2_error = np.zeros((4,3))
# errMatrix(MidLK2_error, maxLK2_Mid80,minLK2_Mid80, maxLK2_Mid40,minLK2_Mid40, maxLK2_Mid20,minLK2_Mid20, maxLK2_Mid10,minLK2_Mid10)
# # ------------W2m Type1 ：Distributed Beam BC Error Peak Value-----------------------
# MidType1_2_error = np.zeros((4,3))
# errMatrix(MidType1_2_error, maxType1_2_Mid80,minType1_2_Mid80, maxType1_2_Mid40,minType1_2_Mid40, maxType1_2_Mid20,minType1_2_Mid20, maxType1_2_Mid10,minType1_2_Mid10)
# # ------------W2m Type2：Beam and Node BC Error Peak Value-----------------------
# MidType2_2_error = np.zeros((4,3))
# errMatrix(MidType2_2_error, maxType2_2_Mid80,minType2_2_Mid80, maxType2_2_Mid40,minType2_2_Mid40, maxType2_2_Mid20,minType2_2_Mid20, maxType2_2_Mid10,minType2_2_Mid10)
# # ------------W10m Type3：Node BC Error Peak Value-----------------------
# MidType3_2_error = np.zeros((4,3))
# errMatrix(MidType3_2_error, maxType3_2_Mid80,minType3_2_Mid80, maxType3_2_Mid40,minType3_2_Mid40, maxType3_2_Mid20,minType3_2_Mid20, maxType3_2_Mid10,minType3_2_Mid10)

# # calculate_Error()
# MidTieErr20 = np.zeros((4,3))
# MidLKErr20 = np.zeros((4,3))
# MidType1Err20 = np.zeros((4,3))
# MidType2Err20 = np.zeros((4,3))
# MidType3Err20 = np.zeros((4,3))

# MidTieErr10 = np.zeros((4,3))
# MidLKErr10 = np.zeros((4,3))
# MidType1Err10 = np.zeros((4,3))
# MidType2Err10 = np.zeros((4,3))
# MidType3Err10 = np.zeros((4,3))

# MidTieErr2 = np.zeros((4,3))
# MidLKErr2 = np.zeros((4,3))
# MidType1Err2 = np.zeros((4,3))
# MidType2Err2 = np.zeros((4,3))
# MidType3Err2 = np.zeros((4,3))

# def Calculate_Error(TieErr,Tie_error):
#     for i in range(len(Mesh_Size)):
#         TieErr[:,0] = Tie_error[:,0]
# # # ------------------------- Relative Error ----------------------
# #         TieErr[i,1] = ((Tie_error[i,1] - maxAnaly)/maxAnaly)*100
# #         TieErr[i,2] = ((Tie_error[i,2] - minAnaly)/minAnaly)*100

# # ------------------------- Absolute Relative Error ------------------        
#         TieErr[i,1] = (abs(Tie_error[i,1] - maxAnaly)/maxAnaly)*100
#         TieErr[i,2] = (abs(Tie_error[i,2] - minAnaly)/minAnaly)*100
        
# # # ------------------------- Absolute Error ----------------------       
# #         TieErr[i,1] = abs(Tie_error[i,1] - maxAnaly)
# #         TieErr[i,2] = abs(Tie_error[i,2] - minAnaly)
        
# # -------- W20 Relative Error --------------   
# Calculate_Error(MidTieErr20, MidTie20_error)
# Calculate_Error(MidLKErr20, MidLK20_error)      
# Calculate_Error(MidType1Err20, MidType1_20_error)
# Calculate_Error(MidType2Err20, MidType2_20_error)   
# Calculate_Error(MidType3Err20, MidType3_20_error)   
# # -------- W10 Relative Error --------------   
# Calculate_Error(MidTieErr10, MidTie10_error)
# Calculate_Error(MidLKErr10, MidLK10_error)      
# Calculate_Error(MidType1Err10, MidType1_10_error)
# Calculate_Error(MidType2Err10, MidType2_10_error)   
# Calculate_Error(MidType3Err10, MidType3_10_error)   
# # -------- W2 Relative Error --------------   
# Calculate_Error(MidTieErr2, MidTie2_error)
# Calculate_Error(MidLKErr2, MidLK2_error)      
# Calculate_Error(MidType1Err2, MidType1_2_error)
# Calculate_Error(MidType2Err2, MidType2_2_error)
# Calculate_Error(MidType3Err2, MidType3_2_error)

# # ------------------------------- Time Increment Relative Error: 20、10、1m (Middle point)-------------------- 
# # ==================Draw Relative error : Middele point =============================
# def DifferTime_elemetError(Peak,TieErr, LKErr, Type1Err, Type2Err, Type3Err):
#     # font_props = {'family': 'Arial', 'size': 14}
#     plt.plot(TieErr[:,0],TieErr[:,Peak],marker = '^',markersize=12,markerfacecolor = 'white',label = 'Tie BC')
#     # plt.plot(LKErr[:,0],LKErr[:,Peak],marker = 'o',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot')
#     plt.plot(Type1Err[:,0],Type1Err[:,Peak],marker = '<',markersize=8,markerfacecolor = 'white',label = 'Beam Type1')
#     plt.plot(Type2Err[:,0],Type2Err[:,Peak],marker = 's',markersize=6,markerfacecolor = 'white',label = 'Beam Type2')
#     plt.plot(Type3Err[:,0],Type3Err[:,Peak],marker = 'p',markersize=4,markerfacecolor = 'white',label = 'Node BC')

#     # plt.legend(loc='center left',prop=font_props) #ncol=2,fontsize=16 frameon=False
#     plt.xticks(fontsize = 15)
#     plt.yticks(fontsize = 15)

#     # plt.xlim(0.0, 0.20)
#     plt.grid(True)
    
# x_axis = 0.125
# figsize = (10,10)
# # # ----------------- Middle Node Relative Error -------------------------
# # # ----------------- Maximum Midpoint Value ------------------- 
# # fig5, (ax13,ax14,ax15) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# # fig5.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# # fig5.text(0.43,0.89, "(Middle Node)", color = "red", fontsize=20)
# # fig5.text(0.15,0.85, r"$\mathrm {Pwave}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)

# # # fig5.text(0.045,0.5, 'Peak Velocity Error: '+ r"$\ E_{Max}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=20)
# # fig5.text(0.045,0.5, 'Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(E_{Max})$", va= 'center', rotation= 'vertical', fontsize=20)

# # # fig5.text(0.045,0.5,'Peak Velocity Error: '+ r"$Max\ E_{abs}$", va= 'center', rotation= 'vertical', fontsize=20)
# # # fig5.text(0.01,0.5,'Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(Max\ E_{abs})$", va= 'center', rotation= 'vertical', fontsize=20)

# # # fig5.text(0.40,0.060,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)
# # fig5.text(0.35,0.056,  f'Mesh size ' + r'$\Delta_y$ $\,(log_{10})\,$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# # ax13 = plt.subplot(311)
# # DifferTime_elemetError(1,MidTieErr20, MidLKErr20, MidType1Err20, MidType2Err20, MidType3Err20)
# # ax13.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.15, y=0.65)

# # ax13.set_xscale('log', base=10)
# # ax13.set_yscale('log', base=10)
# # ax13.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # # ax13.get_xaxis().set_visible(False) # make X-asis tick dissappear

# # ax14 = plt.subplot(312)
# # DifferTime_elemetError(1,MidTieErr10, MidLKErr10, MidType1Err10, MidType2Err10, MidType3Err10)
# # ax14.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.15, y=0.65)

# # ax14.set_xscale('log', base=10)
# # ax14.set_yscale('log', base=10)
# # ax14.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # # ax14.get_xaxis().set_visible(False) # make X-asis tick dissappear

# # ax15 = plt.subplot(313)
# # DifferTime_elemetError(1,MidTieErr2, MidLKErr2, MidType1Err2, MidType2Err2, MidType3Err2)
# # ax15.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.15, y=0.65)

# # ax15.set_xscale('log', base=10)
# # ax15.set_yscale('log', base=10)
# # ax15.tick_params(axis = 'y', which = 'both', labelsize = 17)

# # ax15.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
# # ax15.tick_params(axis = 'x', which = 'both', labelsize = 17)

# # font_props = {'family': 'Arial', 'size': 17}  #Legend Setting

# # lines, labels = fig5.axes[-1].get_legend_handles_labels()
# # fig5.legend(lines, labels, loc = (0.77,0.80) ,prop=font_props)

# # # for ax in [ax13,ax14,ax15]:
# # #     formatter = ticker.ScalarFormatter(useMathText =True)
# # #     formatter.set_scientific(True)
# # #     formatter.set_powerlimits((0,0))
    
# # #     ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# # #     # ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# # #     ax.yaxis.get_offset_text().set(size=18)

# # #     # ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# # #     # ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# # #     # ax.xaxis.get_offset_text().set(size=18)

# # # ----------------- Minimum Midpoint Value ------------------- 
# # fig6, (ax16,ax17,ax18) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# # fig6.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# # fig6.text(0.43,0.89, "(Middle Node)", color = "red", fontsize=20)
# # fig6.text(0.15,0.82, r"$\mathrm {Pwave}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)

# # # fig6.text(0.045,0.5, 'Peak Velocity Error: '+ r"$\ E_{Min}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=20)
# # fig6.text(0.045,0.5, 'Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(E_{Min})$", va= 'center', rotation= 'vertical', fontsize=20)

# # # fig6.text(0.045,0.5, 'Peak Velocity Error: '+ r"$Min\ E_{abs}$", va= 'center', rotation= 'vertical', fontsize=20)
# # # fig6.text(0.015,0.5, 'Peak Velocity Error: '+  r'$\log_{10}$'+ r"$(Min\ E_{abs})$", va= 'center', rotation= 'vertical', fontsize=20)

# # # fig6.text(0.40,0.060,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)
# # fig6.text(0.35,0.056,  f'Mesh size ' + r'$\Delta_y$ $\,(log_{10})\,$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# # ax16 = plt.subplot(311)
# # DifferTime_elemetError(2,MidTieErr20, MidLKErr20, MidType1Err20, MidType2Err20, MidType3Err20)
# # ax16.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.15, y=0.50)

# # ax16.set_xscale('log', base=10)
# # # ax16.set_yscale('log', base=10)
# # ax16.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # # ax16.get_xaxis().set_visible(False) # make X-asis tick dissappear

# # ax17 = plt.subplot(312)
# # DifferTime_elemetError(2,MidTieErr10, MidLKErr10, MidType1Err10, MidType2Err10, MidType3Err10)
# # ax17.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.15, y=0.70)

# # ax17.set_xscale('log', base=10)
# # # ax17.set_yscale('log', base=10)
# # ax17.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # # ax17.get_xaxis().set_visible(False) # make X-asis tick dissappear

# # ax18 = plt.subplot(313)
# # DifferTime_elemetError(2,MidTieErr2, MidLKErr2, MidType1Err2, MidType2Err2, MidType3Err2)
# # ax18.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.15, y=0.50)

# # ax18.set_xscale('log', base=10)
# # # ax18.set_yscale('log', base=10)
# # ax18.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
# # ax18.tick_params(axis = 'x', which = 'both', labelsize = 17)

# # ax18.tick_params(axis = 'y', which = 'both', labelsize = 17)

# # lines, labels = fig6.axes[-1].get_legend_handles_labels()
# # fig6.legend(lines, labels, loc = (0.77,0.80),prop=font_props)

# # # for ax in [ax16,ax17,ax18]:
# # #     # formatter = ticker.ScalarFormatter(useMathText =True)
# # #     # formatter.set_scientific(True)
# # #     # formatter.set_powerlimits((0,0))
# # #     ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# # #     ax.yaxis.get_offset_text().set(size=18)
    
# # #     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# # #     ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# # #     ax.xaxis.get_offset_text().set(size=18)

# # ================================== Prepare L2-Norm Error ============================
# # # ---------- Find Same Time ---------------------
# # # 从两个数组中提取要比较的列
# TheoryTime = total_time[:]
# Element80 = Tie_W20_Mid80row[:,0]
# Element40 = Tie_W20_Mid40row[:,0]
# Element20 = Tie_W20_Mid20row[:,0]
# Element10 = Tie_W20_Mid10row[:,0]

# TheoryTime_dt = total_time[1]
# Element80_dt = Tie_W20_Mid80row[0,0]
# Element40_dt = Tie_W20_Mid40row[0,0]
# Element20_dt = Tie_W20_Mid20row[0,0]
# Element10_dt = Tie_W20_Mid10row[0,0]

# # ================= Calculate_2NormError ===============================
# def Calculate_2NormError(TheoryTime,Pwave,Element80,Tie_W20_Mid80row, time_range=(0, 0.20)):
# # ------------------------- L-2 Norm Error ------------------------
#     common80 = set(TheoryTime) & set(Element80)
#     filtered_common80 = [value for value in common80 if time_range[0] <= value <= time_range[1]]
#     differences = []
    
#     # for common_value in common80:
#     for common_value in filtered_common80:
#         index1 = np.where(Element80 == common_value)[0][0]
#         index2 = np.where(TheoryTime == common_value)[0][0]
#         # print(index1,index2)
#         diff = Tie_W20_Mid80row[index1, column_index] - Pwave[index2,79]
#         differences.append(diff)
        
#     compare = np.array(differences)
#     squared_values = np.square(compare)
#     sum_of_squares = np.sum(squared_values)
#     result = np.sqrt(sum_of_squares)
#     return result, len(compare)


# # ================= Calculate_2NormError ===============================
# def Calculate_RelativeL2norm(TheoryTime,Pwave,Element80,Tie_W20_Mid80row, TheoryTime_dt, Element80_dt):
# # ------------------------- L-2 Norm Error ------------------------
#     common80 = set(TheoryTime) & set(Element80)
#     differences = []
#     Mom = []

#     for common_value in common80:
#         index1 = np.where(Element80 == common_value)[0][0]
#         index2 = np.where(TheoryTime == common_value)[0][0]

#         diff = (Tie_W20_Mid80row[index1, column_index] - Pwave[index2,79])
#         # diff = (wave1[index2,99]-Tie_W20_Mid80row[index1, 1])
        
#         Mother =  Pwave[index2,79]
#         differences.append(diff)
#         Mom.append(Mother)
# # ------------- numerator and denominator seperate calculate -------------------- 
#     compare = np.array(differences)
#     Momm = np.array(Mom)
# # ------------- numerator and denominator seperate Square --------------------    
#     squared_values = np.square(compare)
#     squared_value2 = np.square(Momm)
    
#     sum_of_squares = np.sum(squared_values)
#     sum_of_square2 = np.sum(squared_value2)

#     result = np.sqrt((sum_of_squares)/sum_of_square2)
#     return result, len(compare)

# def Add_Err(Index,MidTieErr20,MidTie20_error,Tie_W20_Mid80row,Tie_W20_Mid40row,Tie_W20_Mid20row,Tie_W20_Mid10row):
#     MidTieErr20[:,0] = MidTie20_error[:,0] 
# # ===================================== Calculate_L2NormError ============================================================
#     MidTieErr20[0,Index], MidTieErr20[0,2] = Calculate_2NormError(TheoryTime,Pwave, Element80,Tie_W20_Mid80row)
#     MidTieErr20[1,Index], MidTieErr20[1,2] = Calculate_2NormError(TheoryTime,Pwave, Element40,Tie_W20_Mid40row)
#     MidTieErr20[2,Index], MidTieErr20[2,2] = Calculate_2NormError(TheoryTime,Pwave, Element20,Tie_W20_Mid20row)
#     MidTieErr20[3,Index], MidTieErr20[3,2] = Calculate_2NormError(TheoryTime,Pwave, Element10,Tie_W20_Mid10row)
    
# # # ===================================== Calculate_Relative L2-Norm Error ============================================================
# #     MidTieErr20[0,Index], MidTieErr20[0,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Element80,Tie_W20_Mid80row, TheoryTime_dt, Element80_dt)
# #     MidTieErr20[1,Index], MidTieErr20[1,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Element40,Tie_W20_Mid40row, TheoryTime_dt, Element40_dt)
# #     MidTieErr20[2,Index], MidTieErr20[2,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Element20,Tie_W20_Mid20row, TheoryTime_dt, Element20_dt)
# #     MidTieErr20[3,Index], MidTieErr20[3,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Element10,Tie_W20_Mid10row, TheoryTime_dt, Element10_dt)


# MidTieErr20_L2 = np.zeros((4,3))
# MidLKErr20_L2 = np.zeros((4,3))
# MidType1Err20_L2 = np.zeros((4,3))
# MidType2Err20_L2 = np.zeros((4,3))
# MidType3Err20_L2 = np.zeros((4,3))

# MidTieErr10_L2 = np.zeros((4,3))
# MidLKErr10_L2 = np.zeros((4,3))
# MidType1Err10_L2 = np.zeros((4,3))
# MidType2Err10_L2 = np.zeros((4,3))
# MidType3Err10_L2 = np.zeros((4,3))

# MidTieErr2_L2 = np.zeros((4,3))
# MidLKErr2_L2 = np.zeros((4,3))
# MidType1Err2_L2 = np.zeros((4,3))
# MidType2Err2_L2 = np.zeros((4,3))
# MidType3Err2_L2 = np.zeros((4,3))

# # ---------------------------- Middle Node -----------------------------
# # ----------------- Soil Width 20m -------------------------------------    
# Add_Err(1,MidTieErr20_L2, MidTie20_error, Tie_W20_Mid80row, Tie_W20_Mid40row, Tie_W20_Mid20row, Tie_W20_Mid10row)
# Add_Err(1,MidLKErr20_L2, MidLK20_error, LK_W20_Mid80row, LK_W20_Mid40row, LK_W20_Mid20row, LK_W20_Mid10row)
# Add_Err(1,MidType1Err20_L2, MidType1_20_error, Tyep1_W20_Mid80row, Tyep1_W20_Mid40row, Tyep1_W20_Mid20row, Tyep1_W20_Mid10row)
# Add_Err(1,MidType2Err20_L2, MidType2_20_error, Tyep2_W20_Mid80row, Tyep2_W20_Mid40row, Tyep2_W20_Mid20row, Tyep2_W20_Mid10row)
# Add_Err(1,MidType3Err20_L2, MidType3_20_error, Tyep3_W20_Mid80row, Tyep3_W20_Mid40row, Tyep3_W20_Mid20row, Tyep3_W20_Mid10row)

# # # ----------------- Soil Width 10m -------------------------------------
# Add_Err(1,MidTieErr10_L2 , MidTie10_error, Tie_W10_Mid80row, Tie_W10_Mid40row, Tie_W10_Mid20row, Tie_W10_Mid10row)
# Add_Err(1,MidLKErr10_L2, MidLK10_error, LK_W10_Mid80row,LK_W10_Mid40row,LK_W10_Mid20row,LK_W10_Mid10row)
# Add_Err(1,MidType1Err10_L2, MidType1_10_error, Tyep1_W10_Mid80row, Tyep1_W10_Mid40row, Tyep1_W10_Mid20row, Tyep1_W10_Mid10row)
# Add_Err(1,MidType2Err10_L2, MidType2_10_error, Tyep2_W10_Mid80row, Tyep2_W10_Mid40row, Tyep2_W10_Mid20row, Tyep2_W10_Mid10row)
# Add_Err(1,MidType3Err10_L2, MidType3_10_error, Tyep3_W10_Mid80row, Tyep3_W10_Mid40row, Tyep3_W10_Mid20row, Tyep3_W10_Mid10row)

# # # ----------------- Soil Width 2m -------------------------------------
# Add_Err(1,MidTieErr2_L2 , MidTie2_error, Tie_W2_Mid80row, Tie_W2_Mid40row, Tie_W2_Mid20row, Tie_W2_Mid10row)
# Add_Err(1,MidLKErr2_L2, MidLK2_error, LK_W2_Mid80row,LK_W2_Mid40row,LK_W2_Mid20row,LK_W2_Mid10row)
# Add_Err(1,MidType1Err2_L2, MidType1_2_error, Tyep1_W2_Mid80row, Tyep1_W2_Mid40row, Tyep1_W2_Mid20row, Tyep1_W2_Mid10row)
# Add_Err(1,MidType2Err2_L2, MidType2_2_error, Tyep2_W2_Mid80row, Tyep2_W2_Mid40row, Tyep2_W2_Mid20row, Tyep2_W2_Mid10row)
# Add_Err(1,MidType3Err2_L2, MidType3_2_error, Tyep3_W2_Mid80row, Tyep3_W2_Mid40row, Tyep3_W2_Mid20row, Tyep3_W2_Mid10row)

# # ==================Draw L2 Norm error : Middele point =============================
# def DifferTime_elemetError2(Peak,TieErr, LKErr, Type1Err, Type2Err, Type3Err):
#     # font_props = {'family': 'Arial', 'size': 14}
#     plt.plot(TieErr[:,0],TieErr[:,Peak],marker = '^',markersize=12,markerfacecolor = 'white',label = 'Tie BC')
#     # plt.plot(LKErr[:,0],LKErr[:,Peak],marker = 'o',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot')
#     plt.plot(Type1Err[:,0],Type1Err[:,Peak],marker = '<',markersize=8,markerfacecolor = 'white',label = 'Beam Type1')
#     plt.plot(Type2Err[:,0],Type2Err[:,Peak],marker = 's',markersize=6,markerfacecolor = 'white',label = 'Beam Type2')
#     plt.plot(Type3Err[:,0],Type3Err[:,Peak],marker = 'p',markersize=4,markerfacecolor = 'white',label = 'Node BC')

#     # plt.legend(loc='center left',prop=font_props) #ncol=2,fontsize=16 frameon=False
#     plt.xticks(fontsize = 15)
#     plt.yticks(fontsize = 15)

#     # plt.xlim(0.0, 0.20)
#     plt.grid(True)
    
# # # ----------------- Middle Node Relative Error -------------------------
# # figsize = (10, 10)
# # fig7, (ax19,ax20,ax21) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# # fig7.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# # fig7.text(0.43,0.89, "(Middle Node)", color = "red", fontsize=20)
# # fig7.text(0.5,0.85, r"$\mathrm {Pwave}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)

# # # fig7.text(0.04,0.5, 'Peak Velocity Error: '+ r"$E_{L2}$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig7.text(0.01,0.5, 'Peak Velocity Error: '+ r'$\log_{10}$' + r"$(E_{L2})$", va= 'center', rotation= 'vertical', fontsize=20)

# # # fig7.text(0.040,0.5, 'Peak Velocity Error: '+ r"$E_{RL2}$", va= 'center', rotation= 'vertical', fontsize=20)
# # # fig7.text(0.01,0.5, 'Peak Velocity Error: '+ r'$\log_{10}$' + r"$(E_{RL2})$", va= 'center', rotation= 'vertical', fontsize=20)

# # # fig7.text(0.40,0.060,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)
# # fig7.text(0.35,0.056,  f'Mesh size ' + r'$\Delta_y$ $\,(log_{10})\,$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# # ax19 = plt.subplot(311)
# # DifferTime_elemetError2(1,MidTieErr20_L2, MidLKErr20_L2, MidType1Err20_L2, MidType2Err20_L2, MidType3Err20_L2)
# # ax19.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.15, y=0.60)

# # ax19.set_xscale('log', base=10)
# # ax19.set_yscale('log', base=10)
# # ax19.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # # ax19.get_xaxis().set_visible(False) # make X-asis tick dissappear

# # ax20 = plt.subplot(312)
# # DifferTime_elemetError2(1,MidTieErr10_L2, MidLKErr10_L2, MidType1Err10_L2, MidType2Err10_L2, MidType3Err10_L2)
# # ax20.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.15, y=0.60)

# # ax20.set_xscale('log', base=10)
# # ax20.set_yscale('log', base=10)
# # ax20.tick_params(axis = 'y', which = 'both', labelsize = 17)
# # # ax20.get_xaxis().set_visible(False) # make X-asis tick dissappear

# # ax21 = plt.subplot(313)
# # DifferTime_elemetError2(1,MidTieErr2_L2, MidLKErr2_L2, MidType1Err2_L2, MidType2Err2_L2, MidType3Err2_L2)
# # ax21.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.15, y=0.60)

# # ax21.set_xscale('log', base=10)
# # ax21.set_yscale('log', base=10)
# # ax21.tick_params(axis = 'y', which = 'both', labelsize = 17)

# # ax21.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
# # ax21.tick_params(axis = 'x', which = 'both', labelsize = 17)

# # font_props = {'family': 'Arial', 'size': 17}  #Legend Setting

# # lines, labels = fig7.axes[-1].get_legend_handles_labels()
# # fig7.legend(lines, labels, loc = (0.77,0.62) ,prop=font_props)

# # # for ax in [ax19,ax20,ax21]:
# # #     formatter = ticker.ScalarFormatter(useMathText =True)
# # #     formatter.set_scientific(True)
# # #     formatter.set_powerlimits((0,0))
    
# # #     ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# # #     ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# # #     ax.yaxis.get_offset_text().set(size=18)

# # #     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# # #     ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
# # #     ax.xaxis.get_offset_text().set(size=18)


