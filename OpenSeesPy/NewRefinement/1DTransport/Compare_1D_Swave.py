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

Nele = Soil_80row # Soil_80row
End_Ele = Nele-1
cs = 200 # m/s
L = 10 # m(Soil_Depth)
nu = (1/3)  #  0.3 -> (epsilon_z /=0)
rho = 2000 # kg/m3 
G = (cs*cs)*rho  # N/m^2 = Kg/(m*s^2)
E =  G*2*(1+nu)  # N/m^2 = Kg/(m*s^2)
cp = (E*(1-nu)/((1+nu)*(1-2*nu)*rho))**(0.5)

A = 0.1# 0.1
# ======== Different frequency to Control Ws and Wp (v = f * lambda)======================
ws_40HZ =  (2*pi)/5 # 0 to 5m = 0 to 2*pi => x = 2*pi/5
ws_20HZ =  pi/5  # 0 to 10m = 0 to 2*pi => x = pi/5
ws_10HZ =  pi/10 # 0 to 20m = 0 to 2*pi => x = pi/10

# wp_20HZ =  pi/10 # 0 to 20m = 0 to 2*pi => x = pi/10
# wp_10HZ =  pi/20 # 0 to 40m = 0 to 2*pi => x = pi/20
# wp_40HZ =  pi/5 # 0 to 10m = 0 to 2*pi => x = pi/5

Swave_HZ = ws_40HZ

HZ = 40
# calculate eace step time
tns = L/cs # wave transport time
dcell = tns/Nele #each cell time
dt = dcell*0.1 #eace cell have 10 steps
print(f"Swave travel = {tns} ;dcell = {dcell} ;dt = {dt}")

time_cs = np.arange(0.0,0.050005,dt)
timeCs_Node = np.arange(0.0,0.050005,dt)
Nt = len(time_cs)
#----------- Soil Coordinate --------------
x = cs*time_cs #m
def Incoming_wave(w, x, cs, t):  #事實上為（xi,yi,t），空間跟時間資訊全寫進去，目前只用到yi的空間
    return np.sin(w*(x-cs*t)) # Normal：np.sin(w*(x-cs*t))

def Outgoing_wave(w, x, cs, t):
    return np.sin(w*(x+cs*t)) # Norrmal： np.sin(w*(x+cs*t))

Nnode = Nele + 1
End_Node = Nele
dy = L/Nele # 1, 0.1
dx= dy/10 # 0.1, 0.01 each element have 10 step dx

total_Transport = np.arange(0.0,20.1, dx)

# ---------- Incoming wave (Beam distributed load)------------------
XIn = np.zeros((len(total_Transport),Nele))
# X = 0~10 m 
for j in range(Nele): #100 
    tin = time_cs[10*j+5]
    x0 = x[10*j+5]  # 0.05,0.15,0.25....,9.95
    # print(x0,cs*tin)
    for i in range(len(time_cs)):      
        xii = x0 + dx*i 
        XIn[5+10*j+i,j] = Incoming_wave(Swave_HZ, xii, cs, tin)  #from 0.05m to 9.95m

# ---------- Outcoming wave (Beam distributed load)-------------------
XOut = np.zeros((len(total_Transport),Nele))
Output_disp = 5 # 9.95
End_disp = 10*Nele-5
# X = 10m ~ 20m
for j in range(Nele):# 100 Nele
    tout = time_cs[Output_disp+10*j] 
    x0 = (L-(dy/2))-dy*j   #9.5/9.75/9.875/9.9375/9.95-dy*j 
    # print(x0,cs*tout)
    for i in range(len(time_cs)):      
        xoo = x0 + dx*i 
        XOut[End_disp-10*j+i,End_Ele-j] = Outgoing_wave(Swave_HZ, xoo, cs, tout)  #from 9.95m to 0.05m      
        
total_time = np.arange(0.0,0.4001,dt)
Swave = np.zeros((len(total_time),Nele))

# ===== New BC Sideforce on Left and Right ==============
SSideforce_y = np.zeros((len(total_time),Nele))  # 10
SSideforce_x = np.zeros((len(total_time),Nele))  # 10

# ----- 事實上是算 taux、tauy ------------------
Cs_vel_Coefficient =  2*1e4/(A*rho*cs)
# ===== Input Incoming Wave and Outcoming Wave to wave1 =======================
for g in range(Nele): #Nele
    to = 5 + 10*g
    for t in range(len(total_time)):
        if total_time[t] < 0.05:
            Swave[to+t,g] = (Swave[to+t,g] + Cs_vel_Coefficient* XIn[to+t,g])  # original wave transport
            
        if total_time[t] >= 0.05 and total_time[t] < 0.1:
            Swave[to+t,End_Ele-g] = Swave[to+t,End_Ele-g] + Cs_vel_Coefficient* XIn[t-to,End_Ele-g]   # XOut

# plt.plot(total_time, Swave[:, 79])
# plt.xlim(0,0.2)
# plt.grid(True)

# ====================== Read File From Numerical ==================================
soilLength = 10 #m
# soilwidth = int(2.0)
# ny = int(40) # 80, 40, 20. 10
# HZ = 20

YMesh = np.array([80, 40, 20, 10])

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
        
    Mid80row = MiddelNode[0]
    Mid40row = MiddelNode[1]
    Mid20row = MiddelNode[2]
    Mid10row = MiddelNode[3]
    
    return Mid80row, Mid40row, Mid20row, Mid10row

W2_Mid80row, W2_Mid40row, W2_Mid20row, W2_Mid10row = Find_Middle(int(2.0), YMesh)
W10_Mid80row, W10_Mid40row, W10_Mid20row, W10_Mid10row = Find_Middle(int(10.0), YMesh)
W20_Mid80row, W20_Mid40row, W20_Mid20row, W20_Mid10row = Find_Middle(int(20.0), YMesh)


# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
Condition1 = f'1D_Transport/Swave/W_2m/HZ_{HZ}'
file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/TieBC_80row/Velocity/node{W2_Mid80row}.out"
file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/TieBC_40row/Velocity/node{W2_Mid40row}.out"
file3 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/TieBC_20row/Velocity/node{W2_Mid20row}.out"
file4 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/TieBC_10row/Velocity/node{W2_Mid10row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file5 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_80row/Velocity/node{W2_Mid80row}.out"
file6 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_40row/Velocity/node{W2_Mid40row}.out"
file7 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_20row/Velocity/node{W2_Mid20row}.out"
file8 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_10row/Velocity/node{W2_Mid10row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file9 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_80row/Velocity/node{W2_Mid80row}.out"
file10 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_40row/Velocity/node{W2_Mid40row}.out"
file11 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_20row/Velocity/node{W2_Mid20row}.out"
file12 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_10row/Velocity/node{W2_Mid10row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file13 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType2_80row/Velocity/node{W2_Mid80row}.out"
file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType2_40row/Velocity/node{W2_Mid40row}.out"
file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType2_20row/Velocity/node{W2_Mid20row}.out"
file16 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType2_10row/Velocity/node{W2_Mid10row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file17 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType3_80row/Velocity/node{W2_Mid80row}.out"
file18 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType3_40row/Velocity/node{W2_Mid40row}.out"
file19 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType3_20row/Velocity/node{W2_Mid20row}.out"
file20 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType3_10row/Velocity/node{W2_Mid10row}.out"

Tie_W2_Mid80row = rdnumpy(file1)
Tie_W2_Mid40row = rdnumpy(file2)
Tie_W2_Mid20row = rdnumpy(file3)
Tie_W2_Mid10row = rdnumpy(file4)

LK_W2_Mid80row = rdnumpy(file5)
LK_W2_Mid40row = rdnumpy(file6)
LK_W2_Mid20row = rdnumpy(file7)
LK_W2_Mid10row = rdnumpy(file8)

Tyep1_W2_Mid80row = rdnumpy(file9)
Tyep1_W2_Mid40row = rdnumpy(file10)
Tyep1_W2_Mid20row = rdnumpy(file11)
Tyep1_W2_Mid10row = rdnumpy(file12)

Tyep2_W2_Mid80row = rdnumpy(file13)
Tyep2_W2_Mid40row = rdnumpy(file14)
Tyep2_W2_Mid20row = rdnumpy(file15)
Tyep2_W2_Mid10row = rdnumpy(file16)

Tyep3_W2_Mid80row = rdnumpy(file17)
Tyep3_W2_Mid40row = rdnumpy(file18)
Tyep3_W2_Mid20row = rdnumpy(file19)
Tyep3_W2_Mid10row = rdnumpy(file20)
# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
Condition2 = f'1D_Transport/Swave/W_10m/HZ_{HZ}'
file21 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_80row/Velocity/node{W10_Mid80row}.out"
file22 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_40row/Velocity/node{W10_Mid40row}.out"
file23 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_20row/Velocity/node{W10_Mid20row}.out"
file24 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_10row/Velocity/node{W10_Mid10row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file25 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_80row/Velocity/node{W10_Mid80row}.out"
file26 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_40row/Velocity/node{W10_Mid40row}.out"
file27 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_20row/Velocity/node{W10_Mid20row}.out"
file28 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_10row/Velocity/node{W10_Mid10row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file29 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_80row/Velocity/node{W10_Mid80row}.out"
file30 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_40row/Velocity/node{W10_Mid40row}.out"
file31 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_20row/Velocity/node{W10_Mid20row}.out"
file32 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_10row/Velocity/node{W10_Mid10row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file33 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_80row/Velocity/node{W10_Mid80row}.out"
file34 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_40row/Velocity/node{W10_Mid40row}.out"
file35 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_20row/Velocity/node{W10_Mid20row}.out"
file36 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_10row/Velocity/node{W10_Mid10row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file37 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_80row/Velocity/node{W10_Mid80row}.out"
file38 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_40row/Velocity/node{W10_Mid40row}.out"
file39 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_20row/Velocity/node{W10_Mid20row}.out"
file40 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_10row/Velocity/node{W10_Mid10row}.out"

Tie_W10_Mid80row = rdnumpy(file21)
Tie_W10_Mid40row = rdnumpy(file22)
Tie_W10_Mid20row = rdnumpy(file23)
Tie_W10_Mid10row = rdnumpy(file24)

LK_W10_Mid80row = rdnumpy(file25)
LK_W10_Mid40row = rdnumpy(file26)
LK_W10_Mid20row = rdnumpy(file27)
LK_W10_Mid10row = rdnumpy(file28)

Tyep1_W10_Mid80row = rdnumpy(file29)
Tyep1_W10_Mid40row = rdnumpy(file30)
Tyep1_W10_Mid20row = rdnumpy(file31)
Tyep1_W10_Mid10row = rdnumpy(file32)

Tyep2_W10_Mid80row = rdnumpy(file33)
Tyep2_W10_Mid40row = rdnumpy(file34)
Tyep2_W10_Mid20row = rdnumpy(file35)
Tyep2_W10_Mid10row = rdnumpy(file36)

Tyep3_W10_Mid80row = rdnumpy(file37)
Tyep3_W10_Mid40row = rdnumpy(file38)
Tyep3_W10_Mid20row = rdnumpy(file39)
Tyep3_W10_Mid10row = rdnumpy(file40)

# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
Condition3 = f'1D_Transport/Swave/W_20m/HZ_{HZ}'
file41 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/TieBC_80row/Velocity/node{W20_Mid80row}.out"
file42 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/TieBC_40row/Velocity/node{W20_Mid40row}.out"
file43 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/TieBC_20row/Velocity/node{W20_Mid20row}.out"
file44 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/TieBC_10row/Velocity/node{W20_Mid10row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file45 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_80row/Velocity/node{W20_Mid80row}.out"
file46 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_40row/Velocity/node{W20_Mid40row}.out"
file47 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_20row/Velocity/node{W20_Mid20row}.out"
file48 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_10row/Velocity/node{W20_Mid10row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file49 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_80row/Velocity/node{W20_Mid80row}.out"
file50 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_40row/Velocity/node{W20_Mid40row}.out"
file51 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_20row/Velocity/node{W20_Mid20row}.out"
file52 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_10row/Velocity/node{W20_Mid10row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file53 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType2_80row/Velocity/node{W20_Mid80row}.out"
file54 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType2_40row/Velocity/node{W20_Mid40row}.out"
file55 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType2_20row/Velocity/node{W20_Mid20row}.out"
file56 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType2_10row/Velocity/node{W20_Mid10row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file57 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType3_80row/Velocity/node{W20_Mid80row}.out"
file58 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType3_40row/Velocity/node{W20_Mid40row}.out"
file59 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType3_20row/Velocity/node{W20_Mid20row}.out"
file60 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType3_10row/Velocity/node{W20_Mid10row}.out"

Tie_W20_Mid80row = rdnumpy(file41)
Tie_W20_Mid40row = rdnumpy(file42)
Tie_W20_Mid20row = rdnumpy(file43)
Tie_W20_Mid10row = rdnumpy(file44)

LK_W20_Mid80row = rdnumpy(file45)
LK_W20_Mid40row = rdnumpy(file46)
LK_W20_Mid20row = rdnumpy(file47)
LK_W20_Mid10row = rdnumpy(file48)

Tyep1_W20_Mid80row = rdnumpy(file49)
Tyep1_W20_Mid40row = rdnumpy(file50)
Tyep1_W20_Mid20row = rdnumpy(file51)
Tyep1_W20_Mid10row = rdnumpy(file52)

Tyep2_W20_Mid80row = rdnumpy(file53)
Tyep2_W20_Mid40row = rdnumpy(file54)
Tyep2_W20_Mid20row = rdnumpy(file55)
Tyep2_W20_Mid10row = rdnumpy(file56)

Tyep3_W20_Mid80row = rdnumpy(file57)
Tyep3_W20_Mid40row = rdnumpy(file58)
Tyep3_W20_Mid20row = rdnumpy(file59)
Tyep3_W20_Mid10row = rdnumpy(file60)

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
        
    Qua80row = QuarterNode[0]
    Qua40row = QuarterNode[1]
    Qua20row = QuarterNode[2]
    Qua10row = QuarterNode[3]
    
    return Qua80row, Qua40row, Qua20row, Qua10row

W2_Qua80row, W2_Qua40row, W2_Qua20row, W2_Qua10row = Find_Quarter(int(2.0), YMesh)
W10_Qua80row, W10_Qua40row, W10_Qua20row, W10_Qua10row = Find_Quarter(int(10.0), YMesh)
W20_Qua80row, W20_Qua40row, W20_Qua20row, W20_Qua10row = Find_Quarter(int(20.0), YMesh)

# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
file61 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/TieBC_80row/Velocity/node{W2_Qua80row}.out"
file62 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/TieBC_40row/Velocity/node{W2_Qua40row}.out"
file63 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/TieBC_20row/Velocity/node{W2_Qua20row}.out"
file64 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/TieBC_10row/Velocity/node{W2_Qua10row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file65 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_80row/Velocity/node{W2_Qua80row}.out"
file66 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_40row/Velocity/node{W2_Qua40row}.out"
file67 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_20row/Velocity/node{W2_Qua20row}.out"
file68 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/LKDash_10row/Velocity/node{W2_Qua10row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file69 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_80row/Velocity/node{W2_Qua80row}.out"
file70 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_40row/Velocity/node{W2_Qua40row}.out"
file71 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_20row/Velocity/node{W2_Qua20row}.out"
file72 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType1_10row/Velocity/node{W2_Qua10row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file73 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType2_80row/Velocity/node{W2_Qua80row}.out"
file74 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType2_40row/Velocity/node{W2_Qua40row}.out"
file75 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType2_20row/Velocity/node{W2_Qua20row}.out"
file76 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType2_10row/Velocity/node{W2_Qua10row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file77 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType3_80row/Velocity/node{W2_Qua80row}.out"
file78 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType3_40row/Velocity/node{W2_Qua40row}.out"
file79 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType3_20row/Velocity/node{W2_Qua20row}.out"
file80 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/BeamType3_10row/Velocity/node{W2_Qua10row}.out"

Tie_W2_Qua80row = rdnumpy(file61)
Tie_W2_Qua40row = rdnumpy(file62)
Tie_W2_Qua20row = rdnumpy(file63)
Tie_W2_Qua10row = rdnumpy(file64)

LK_W2_Qua80row = rdnumpy(file65)
LK_W2_Qua40row = rdnumpy(file66)
LK_W2_Qua20row = rdnumpy(file67)
LK_W2_Qua10row = rdnumpy(file68)

Tyep1_W2_Qua80row = rdnumpy(file69)
Tyep1_W2_Qua40row = rdnumpy(file70)
Tyep1_W2_Qua20row = rdnumpy(file71)
Tyep1_W2_Qua10row = rdnumpy(file72)

Tyep2_W2_Qua80row = rdnumpy(file73)
Tyep2_W2_Qua40row = rdnumpy(file74)
Tyep2_W2_Qua20row = rdnumpy(file75)
Tyep2_W2_Qua10row = rdnumpy(file76)

Tyep3_W2_Qua80row = rdnumpy(file77)
Tyep3_W2_Qua40row = rdnumpy(file78)
Tyep3_W2_Qua20row = rdnumpy(file79)
Tyep3_W2_Qua10row = rdnumpy(file80)

# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
file81 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_80row/Velocity/node{W10_Qua80row}.out"
file82 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_40row/Velocity/node{W10_Qua40row}.out"
file83 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_20row/Velocity/node{W10_Qua20row}.out"
file84 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_10row/Velocity/node{W10_Qua10row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file85 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_80row/Velocity/node{W10_Qua80row}.out"
file86 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_40row/Velocity/node{W10_Qua40row}.out"
file87 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_20row/Velocity/node{W10_Qua20row}.out"
file88 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_10row/Velocity/node{W10_Qua10row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file89 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_80row/Velocity/node{W10_Qua80row}.out"
file90 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_40row/Velocity/node{W10_Qua40row}.out"
file91 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_20row/Velocity/node{W10_Qua20row}.out"
file92 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_10row/Velocity/node{W10_Qua10row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file93 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_80row/Velocity/node{W10_Qua80row}.out"
file94 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_40row/Velocity/node{W10_Qua40row}.out"
file95 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_20row/Velocity/node{W10_Qua20row}.out"
file96 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_10row/Velocity/node{W10_Qua10row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file97 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_80row/Velocity/node{W10_Qua80row}.out"
file98 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_40row/Velocity/node{W10_Qua40row}.out"
file99 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_20row/Velocity/node{W10_Qua20row}.out"
file100 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_10row/Velocity/node{W10_Qua10row}.out"

Tie_W10_Qua80row = rdnumpy(file81)
Tie_W10_Qua40row = rdnumpy(file82)
Tie_W10_Qua20row = rdnumpy(file83)
Tie_W10_Qua10row = rdnumpy(file84)

LK_W10_Qua80row = rdnumpy(file85)
LK_W10_Qua40row = rdnumpy(file86)
LK_W10_Qua20row = rdnumpy(file87)
LK_W10_Qua10row = rdnumpy(file88)

Tyep1_W10_Qua80row = rdnumpy(file89)
Tyep1_W10_Qua40row = rdnumpy(file90)
Tyep1_W10_Qua20row = rdnumpy(file91)
Tyep1_W10_Qua10row = rdnumpy(file92)

Tyep2_W10_Qua80row = rdnumpy(file93)
Tyep2_W10_Qua40row = rdnumpy(file94)
Tyep2_W10_Qua20row = rdnumpy(file95)
Tyep2_W10_Qua10row = rdnumpy(file96)

Tyep3_W10_Qua80row = rdnumpy(file97)
Tyep3_W10_Qua40row = rdnumpy(file98)
Tyep3_W10_Qua20row = rdnumpy(file99)
Tyep3_W10_Qua10row = rdnumpy(file100)
# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
file81 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_80row/Velocity/node{W10_Qua80row}.out"
file82 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_40row/Velocity/node{W10_Qua40row}.out"
file83 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_20row/Velocity/node{W10_Qua20row}.out"
file84 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/TieBC_10row/Velocity/node{W10_Qua10row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file85 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_80row/Velocity/node{W10_Qua80row}.out"
file86 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_40row/Velocity/node{W10_Qua40row}.out"
file87 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_20row/Velocity/node{W10_Qua20row}.out"
file88 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/LKDash_10row/Velocity/node{W10_Qua10row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file89 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_80row/Velocity/node{W10_Qua80row}.out"
file90 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_40row/Velocity/node{W10_Qua40row}.out"
file91 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_20row/Velocity/node{W10_Qua20row}.out"
file92 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType1_10row/Velocity/node{W10_Qua10row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file93 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_80row/Velocity/node{W10_Qua80row}.out"
file94 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_40row/Velocity/node{W10_Qua40row}.out"
file95 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_20row/Velocity/node{W10_Qua20row}.out"
file96 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType2_10row/Velocity/node{W10_Qua10row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file97 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_80row/Velocity/node{W10_Qua80row}.out"
file98 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_40row/Velocity/node{W10_Qua40row}.out"
file99 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_20row/Velocity/node{W10_Qua20row}.out"
file100 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/BeamType3_10row/Velocity/node{W10_Qua10row}.out"

Tie_W10_Qua80row = rdnumpy(file81)
Tie_W10_Qua40row = rdnumpy(file82)
Tie_W10_Qua20row = rdnumpy(file83)
Tie_W10_Qua10row = rdnumpy(file84)

LK_W10_Qua80row = rdnumpy(file85)
LK_W10_Qua40row = rdnumpy(file86)
LK_W10_Qua20row = rdnumpy(file87)
LK_W10_Qua10row = rdnumpy(file88)

Tyep1_W10_Qua80row = rdnumpy(file89)
Tyep1_W10_Qua40row = rdnumpy(file90)
Tyep1_W10_Qua20row = rdnumpy(file91)
Tyep1_W10_Qua10row = rdnumpy(file92)

Tyep2_W10_Qua80row = rdnumpy(file93)
Tyep2_W10_Qua40row = rdnumpy(file94)
Tyep2_W10_Qua20row = rdnumpy(file95)
Tyep2_W10_Qua10row = rdnumpy(file96)

Tyep3_W10_Qua80row = rdnumpy(file97)
Tyep3_W10_Qua40row = rdnumpy(file98)
Tyep3_W10_Qua20row = rdnumpy(file99)
Tyep3_W10_Qua10row = rdnumpy(file100)
# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
# --------- Tie Boundary Condition ----------------
file101 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/TieBC_80row/Velocity/node{W20_Qua80row}.out"
file102 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/TieBC_40row/Velocity/node{W20_Qua40row}.out"
file103 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/TieBC_20row/Velocity/node{W20_Qua20row}.out"
file104 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/TieBC_10row/Velocity/node{W20_Qua10row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file105 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_80row/Velocity/node{W20_Qua80row}.out"
file106 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_40row/Velocity/node{W20_Qua40row}.out"
file107 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_20row/Velocity/node{W20_Qua20row}.out"
file108 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/LKDash_10row/Velocity/node{W20_Qua10row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file109 =  f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_80row/Velocity/node{W20_Qua80row}.out"
file110 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_40row/Velocity/node{W20_Qua40row}.out"
file111 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_20row/Velocity/node{W20_Qua20row}.out"
file112 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType1_10row/Velocity/node{W20_Qua10row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file113 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType2_80row/Velocity/node{W20_Qua80row}.out"
file114 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType2_40row/Velocity/node{W20_Qua40row}.out"
file115 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType2_20row/Velocity/node{W20_Qua20row}.out"
file116 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType2_10row/Velocity/node{W20_Qua10row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file117 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType3_80row/Velocity/node{W20_Qua80row}.out"
file118 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType3_40row/Velocity/node{W20_Qua40row}.out"
file119 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType3_20row/Velocity/node{W20_Qua20row}.out"
file120 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/BeamType3_10row/Velocity/node{W20_Qua10row}.out"

Tie_W20_Qua80row = rdnumpy(file101)
Tie_W20_Qua40row = rdnumpy(file102)
Tie_W20_Qua20row = rdnumpy(file103)
Tie_W20_Qua10row = rdnumpy(file104)

LK_W20_Qua80row = rdnumpy(file105)
LK_W20_Qua40row = rdnumpy(file106)
LK_W20_Qua20row = rdnumpy(file107)
LK_W20_Qua10row = rdnumpy(file108)

Tyep1_W20_Qua80row = rdnumpy(file109)
Tyep1_W20_Qua40row = rdnumpy(file110)
Tyep1_W20_Qua20row = rdnumpy(file111)
Tyep1_W20_Qua10row = rdnumpy(file112)

Tyep2_W20_Qua80row = rdnumpy(file113)
Tyep2_W20_Qua40row = rdnumpy(file114)
Tyep2_W20_Qua20row = rdnumpy(file115)
Tyep2_W20_Qua10row = rdnumpy(file116)

Tyep3_W20_Qua80row = rdnumpy(file117)
Tyep3_W20_Qua40row = rdnumpy(file118)
Tyep3_W20_Qua20row = rdnumpy(file119)
Tyep3_W20_Qua10row = rdnumpy(file120)

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

plt_axis2 = 1 # Swave
# # ------- wave put into the timeSeries ---------------
def Differ_BCVel(total_time, Swave, Tie, LKDash, BeamType1, BeamType2, BeamType3):
    # font_props = {'family': 'Arial', 'size': 12}
    plt.plot(total_time, Swave[:,79],label =r'$\mathrm{Analytical}$',color= 'black',linewidth=6.0)
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
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.50))
    ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    ax.yaxis.get_offset_text().set(size=18)

x_axis = 0.25 # 0.1 0.05 **** 10 Times the x axis ******

row_heights = [3,3,3]
fig1, (ax1,ax2,ax3) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig1.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.125' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig1.text(0.40,0.89, "(Middle Node)", color = "red", fontsize=20)
fig1.text(0.55,0.80, r"$\mathrm {Swave}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig1.text(0.02,0.5, r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig1.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax1 = plt.subplot(311)
Differ_BCVel(total_time,Swave, Tie_W20_Mid80row, LK_W20_Mid80row, Tyep1_W20_Mid80row, Tyep2_W20_Mid80row, Tyep3_W20_Mid80row)
ax1.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.60, y=0.78)

ax2 = plt.subplot(312)
Differ_BCVel(total_time,Swave, Tie_W10_Mid80row, LK_W10_Mid80row, Tyep1_W10_Mid80row, Tyep2_W10_Mid80row, Tyep3_W10_Mid80row)
ax2.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.60, y=0.78)

ax3 = plt.subplot(313)
Differ_BCVel(total_time,Swave, Tie_W2_Mid80row, LK_W2_Mid80row, Tyep1_W2_Mid80row, Tyep2_W2_Mid80row, Tyep3_W2_Mid80row)
ax3.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.60, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig1.axes[-1].get_legend_handles_labels()
fig1.legend(lines, labels, loc = 'center right',prop=font_props)

row_heights = [3,3,3]
fig2, (ax4,ax5,ax6) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig2.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.25' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig2.text(0.40,0.89, "(Middle Node)", color = "red", fontsize=20)
fig2.text(0.55,0.80, r"$\mathrm {Swave}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig2.text(0.02,0.5, r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig2.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax4 = plt.subplot(311)
Differ_BCVel(total_time,Swave, Tie_W20_Mid40row, LK_W20_Mid40row, Tyep1_W20_Mid40row, Tyep2_W20_Mid40row, Tyep3_W20_Mid40row)
ax4.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.60, y=0.78)

ax5 = plt.subplot(312)
Differ_BCVel(total_time,Swave, Tie_W10_Mid40row, LK_W10_Mid40row, Tyep1_W10_Mid40row, Tyep2_W10_Mid40row, Tyep3_W10_Mid40row)
ax5.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.60, y=0.78)

ax6 = plt.subplot(313)
Differ_BCVel(total_time,Swave, Tie_W2_Mid40row, LK_W2_Mid40row, Tyep1_W2_Mid40row, Tyep2_W2_Mid40row, Tyep3_W2_Mid40row)
ax6.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.60, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig2.axes[-1].get_legend_handles_labels()
fig2.legend(lines, labels, loc = 'center right',prop=font_props)

row_heights = [3,3,3]
fig3, (ax7,ax8,ax9) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig3.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '0.50' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig3.text(0.40,0.89, "(Middle Node)", color = "red", fontsize=20)
fig3.text(0.55,0.80, r"$\mathrm {Swave}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig3.text(0.02,0.5, r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig3.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax7 = plt.subplot(311)
Differ_BCVel(total_time,Swave, Tie_W20_Mid20row, LK_W20_Mid20row, Tyep1_W20_Mid20row, Tyep2_W20_Mid20row, Tyep3_W20_Mid20row)
ax7.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.60, y=0.78)

ax8 = plt.subplot(312)
Differ_BCVel(total_time,Swave, Tie_W10_Mid20row, LK_W10_Mid20row, Tyep1_W10_Mid20row, Tyep2_W10_Mid20row, Tyep3_W10_Mid20row)
ax8.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.60, y=0.78)

ax9 = plt.subplot(313)
Differ_BCVel(total_time,Swave, Tie_W2_Mid20row, LK_W2_Mid20row, Tyep1_W2_Mid20row, Tyep2_W2_Mid20row, Tyep3_W2_Mid20row)
ax9.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.60, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig3.axes[-1].get_legend_handles_labels()
fig3.legend(lines, labels, loc = 'center right',prop=font_props)

row_heights = [3,3,3]
fig4, (ax10,ax11,ax12) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig4.suptitle(f'Different Boundary '+ r'$\Delta_y='+ '1.0' + r'\mathrm{m}$',x=0.50,y =0.95,fontsize = 20)
fig4.text(0.40,0.89, "(Middle Node)", color = "red", fontsize=20)
fig4.text(0.57,0.80, r"$\mathrm {Swave}$ $(t_{d} = 1/40)$", color = "blue", fontsize=22)
fig4.text(0.02,0.5, r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig4.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

ax10 = plt.subplot(311)
Differ_BCVel(total_time,Swave, Tie_W20_Mid10row, LK_W20_Mid10row, Tyep1_W20_Mid10row, Tyep2_W20_Mid10row, Tyep3_W20_Mid10row)
ax10.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.60, y=0.78)

ax11 = plt.subplot(312)
Differ_BCVel(total_time,Swave, Tie_W10_Mid10row, LK_W10_Mid10row, Tyep1_W10_Mid10row, Tyep2_W10_Mid10row, Tyep3_W10_Mid10row)
ax11.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.60, y=0.78)

ax12 = plt.subplot(313)
Differ_BCVel(total_time,Swave, Tie_W2_Mid10row, LK_W2_Mid10row, Tyep1_W2_Mid10row, Tyep2_W2_Mid10row, Tyep3_W2_Mid10row)
ax12.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.60, y=0.78)

font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

lines, labels = fig4.axes[-1].get_legend_handles_labels()
fig4.legend(lines, labels, loc = 'center right',prop=font_props)
