# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 17:28:11 2024

@author: User
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import LogLocator, NullFormatter, LogFormatter
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator

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
SoilLength = 10 #m
Soil_80row= 80 # dt= 6.25e-05   #cpdt = 3.34e-05

Nele = Soil_80row # Soil_80row
End_Ele = Nele-1
cs = 200 # m/s
# L = 10 # m(Soil_Depth)
nu = (1/3)  #  0.3 -> (epsilon_z /=0)
rho = 2000 # kg/m3 
G = (cs*cs)*rho  # N/m^2 = Kg/(m*s^2)
E =  G*2*(1+nu)  # N/m^2 = Kg/(m*s^2)
cp = (E*(1-nu)/((1+nu)*(1-2*nu)*rho))**(0.5)

A = 0.1# 0.1
# ======== Different frequency to Control Ws and Wp (v = f * lambda)======================
wp_10HZ =  pi/20 # 0 to 40m = 0 to 2*pi => x = pi/20
wp_20HZ =  pi/10 # 0 to 20m = 0 to 2*pi => x = pi/10
wp_40HZ =  pi/5 # 0 to 10m = 0 to 2*pi => x = pi/5
wp_80HZ =  (2*pi)/5 # 0 to 5m = 0 to 2*pi => x = 2*pi/5

fp_10HZ = 10
fp_20HZ = 20
fp_40HZ = 40
fp_80HZ = 80

def Incoming_Pwave(w, x, cp, t):  #事實上為（xi,yi,t），空間跟時間資訊全寫進去，目前只用到yi的空間
    return np.sin(w*(x-cp*t)) # Normal：np.sin(w*(x-cs*t))

def Outgoing_Pwave(w, x, cp, t):
    return np.sin(w*(x+cp*t)) # Norrmal： np.sin(w*(x+cs*t))


def Calfp_Theory(fp_HZ, Pwave_HZ):
    # ------------ Consider SolilLength --------------
    L = cp/fp_HZ # wave Length
    
    # ============================== Consider PWave ======================================
    # calculate eace step time
    tns_cp = SoilLength/cp # wave transport time
    dcell_cp = tns_cp/Nele #each cell time
    dt_cp = dcell_cp*0.1 #eace cell have 10 steps
    print(f"Pwave travel = {tns_cp} ;dcell = {dcell_cp} ;dt = {dt_cp}")
    
    Input_Time = L/cp
    
    time_cp = np.arange(0.0, 8*Input_Time+dt_cp, dt_cp)
    Nt_cp = len(time_cp)
    
    #----------- Soil Coordinate --------------
    x = cp*time_cp #m
    
    Nnode = Nele + 1
    End_Node = Nele
    dy = SoilLength/Nele # 1, 0.1
    dx= dy/10 # 0.1, 0.01 each element have 10 step dx
    
    total_Transport_cp = np.arange(0.0, 16*L+0.1, dx)
    
    # ---------- Incoming wave (Beam distributed load)------------------
    XIn = np.zeros((len(total_Transport_cp), Nele))
    # X = 0~10 m 
    for j in range(Nele): #100 
        tin = time_cp[10*j+5]
        x0 = x[10*j+5]  # 0.05,0.15,0.25....,9.95
        # print(x0,cp*tin)
        for i in range(len(time_cp)):      
            xii = x0 + dx*i 
            XIn[5+10*j+i,j] = Incoming_Pwave(Pwave_HZ, xii, cp, tin)  #from 0.05m to 9.95m
    
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
            XOut[End_disp-10*j+i,End_Ele-j] = Outgoing_Pwave(Pwave_HZ, xoo, cp, tout)  #from 9.95m to 0.05m      
        
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
                
            if total_time[t] >= 0.025 and total_time[t] < (0.025+Input_Time):
                Pwave[to+t,End_Ele-g] = Pwave[to+t,End_Ele-g] + Cp_vel_Coefficient*XIn[t-to,End_Ele-g]   # XOut[t-to,End_Ele-g
    return L, Pwave, total_time

Plamb10, HZ10_Pwave, total_Ptime_HZ10 = Calfp_Theory(fp_10HZ, wp_10HZ)
Plamb20, HZ20_Pwave, total_Ptime_HZ20 = Calfp_Theory(fp_20HZ, wp_20HZ)
Plamb40, HZ40_Pwave, total_Ptime_HZ40 = Calfp_Theory(fp_40HZ, wp_40HZ)
Plamb80, HZ80_Pwave, total_Ptime_HZ80 = Calfp_Theory(fp_80HZ, wp_80HZ)

# ======== Different frequency to Control Ws and Wp (v = f * lambda)======================
ws_80HZ =  (4*pi)/5 # 0 to 5m = 0 to 2*pi => x = 4*pi/5
ws_40HZ =  (2*pi)/5 # 0 to 5m = 0 to 2*pi => x = 2*pi/5
ws_20HZ =  pi/5  # 0 to 10m = 0 to 2*pi => x = pi/5
ws_10HZ =  pi/10 # 0 to 20m = 0 to 2*pi => x = pi/10

fs_10HZ = 10
fs_20HZ = 20
fs_40HZ = 40
fs_80HZ = 80

def Incoming_Swave(w, x, cs, t):  #事實上為（xi,yi,t），空間跟時間資訊全寫進去，目前只用到yi的空間
    return np.sin(w*(x-cs*t)) # Normal：np.sin(w*(x-cs*t))

def Outgoing_Swave(w, x, cs, t):
    return np.sin(w*(x+cs*t)) # Norrmal： np.sin(w*(x+cs*t))

def Calfs_Theory(fs_HZ, Swave_HZ):
    # ------------ Consider SolilLength --------------
    L = cs/fs_HZ # wave Length
    
    # ============================== Consider PWave ======================================
    # calculate eace step time
    tns_cs = SoilLength/cs # wave transport time L/cp
    dcell_cs = tns_cs/Nele #each cell time
    dt_cs = dcell_cs*0.1 #eace cell have 10 steps
    print(f"Swave travel = {tns_cs} ;dcell = {dcell_cs} ;dt = {dt_cs}")
    
    Input_Time = L/cs
    
    time_cs = np.arange(0.0, 4*Input_Time + dt_cs, dt_cs) # 0.0,0.050005,dt
    timecs_Node = np.arange(0.0, 4*Input_Time + dt_cs, dt_cs) # 0.0,0.050005,dt
    Nt_cs = len(time_cs)
        
    #----------- Soil Coordinate --------------
    x = cs*time_cs #m
    
    Nnode = Nele + 1
    End_Node = Nele
    dy = SoilLength/Nele # L/Nele
    dx= dy/10 # 0.1, 0.01 each element have 10 step dx
    
    total_Transport_cs = np.arange(0.0, 8*L+0.1, dx) # 0.0,20.1, dx
        
    # ---------- Incoming wave (Beam distributed load)------------------
    XIn = np.zeros((len(total_Transport_cs), Nele))
    # X = 0~10 m 
    for j in range(Nele): #100 
        tin = time_cs[10*j+5]
        x0 = x[10*j+5]  # 0.05,0.15,0.25....,9.95
        # print(x0,cs*tin)
        for i in range(len(time_cs)):      
            xii = x0 + dx*i 
            XIn[5+10*j+i,j] = Incoming_Swave(Swave_HZ, xii, cs, tin)  #from 0.05m to 9.95m
    
    # ---------- Outcoming wave (Beam distributed load)-------------------
    XOut = np.zeros((len(total_Transport_cs), Nele))
    Output_disp = 5 # 9.95
    End_disp = 10*Nele-5
    # X = 10m ~ 20m
    for j in range(Nele):# 100 Nele
        tout = time_cs[Output_disp+10*j] 
        x0 = (L-(dy/2))-dy*j   #9.5/9.75/9.875/9.9375/9.95-dy*j 
        # print(x0,cs*tout)
        for i in range(len(time_cs)):      
            xoo = x0 + dx*i 
            XOut[End_disp-10*j+i,End_Ele-j] = Outgoing_Swave(Swave_HZ, xoo, cs, tout)  #from 9.95m to 0.05m          
        
    total_time = np.arange(0.0,0.40003,dt_cs)
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
            if total_time[t] < Input_Time: # total_time[t] < 0.025
                Swave[to+t,g] = (Swave[to+t,g] + Cs_vel_Coefficient*XIn[to+t,g])  # original wave transport
                
            if total_time[t] >= 0.050 and total_time[t] < (0.050+Input_Time):
                Swave[to+t,End_Ele-g] = Swave[to+t,End_Ele-g] + Cs_vel_Coefficient*XIn[t-to,End_Ele-g]   # XOut[t-to,End_Ele-g
    return L, Swave, total_time

Slamb10, HZ10_Swave, total_Stime_HZ10 = Calfs_Theory(fs_10HZ, ws_10HZ)
Slamb20, HZ20_Swave, total_Stime_HZ20 = Calfs_Theory(fs_20HZ, ws_20HZ)
Slamb40, HZ40_Swave, total_Stime_HZ40 = Calfs_Theory(fs_40HZ, ws_40HZ)
Slamb80, HZ80_Swave, total_Stime_HZ80 = Calfs_Theory(fs_80HZ, ws_80HZ)

YMesh = np.array([40]) # 80, 40, 20, 10
def Find_Middle(soilwidth, YMesh):
    Dw = SoilLength/80 # soilLength/80 , soilLength/ny
    
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
        
        # -------- Quarter(3/4) Node ------------------------
        LowerN_RQuarter = int((3*nx/4)+1)
        UpperrN_RQuarter = int(LowerN_RQuarter + (nx+1)* ny)
        print(f"LowerN_RQuarter = {LowerN_RQuarter} ,UpperrN_RQuarter = {UpperrN_RQuarter}")
        
        MiddelNode.append(UpperN_Center)
    
    Mid40row = MiddelNode[0]
    
    return Mid40row

# ---------- Consider Mesh = 40 row ----------------------------------
W2_Mid40row = Find_Middle(int(2.0), YMesh)
W10_Mid40row = Find_Middle(int(10.0), YMesh)
W20_Mid40row = Find_Middle(int(20.0), YMesh)

# ===================================== P Wave ========================================================
PWave_Choose = f'1D_Transport/Newmark_Linear/Pwave'
# ----------------- f = 10HZ --------------------------------
HZ10 = f'HZ_10'
# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
Condition1 = f'{PWave_Choose}/W_2m/{HZ10}'
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

Tie_W2_HZ10_P = rdnumpy(file1)
LK_W2_HZ10_P = rdnumpy(file2)
Type1_W2_HZ10_P = rdnumpy(file3)
Type2_W2_HZ10_P = rdnumpy(file4)
Type3_W2_HZ10_P = rdnumpy(file5)

# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
Condition2 = f'{PWave_Choose}/W_10m/{HZ10}'
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

Tie_W10_HZ10_P = rdnumpy(file6)
LK_W10_HZ10_P = rdnumpy(file7)
Type1_W10_HZ10_P = rdnumpy(file8)
Type2_W10_HZ10_P = rdnumpy(file9)
Type3_W10_HZ10_P = rdnumpy(file10)

# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
Condition3 = f'{PWave_Choose}/W_20m/{HZ10}'
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

Tie_W20_HZ10_P = rdnumpy(file11)
LK_W20_HZ10_P = rdnumpy(file12)
Type1_W20_HZ10_P = rdnumpy(file13)
Type2_W20_HZ10_P = rdnumpy(file14)
Type3_W20_HZ10_P = rdnumpy(file15)

# ----------------- f = 20HZ --------------------------------
HZ20 = f'HZ_20'
# ============================ SoilWidth = 2.0 m (HZ = 20)=======================================
Condition4 = f'{PWave_Choose}/W_2m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file16 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/TieBC_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file17 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/LKDash_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file18 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/BeamType1_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file19 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/BeamType2_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file20 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/BeamType3_40row/Velocity/node{W2_Mid40row}.out"

Tie_W2_HZ20_P = rdnumpy(file16)
LK_W2_HZ20_P = rdnumpy(file17)
Type1_W2_HZ20_P = rdnumpy(file18)
Type2_W2_HZ20_P = rdnumpy(file19)
Type3_W2_HZ20_P = rdnumpy(file20)
# ============================ SoilWidth = 10.0 m (HZ = 20)=======================================
Condition5 = f'{PWave_Choose}/W_10m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file21 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/TieBC_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file22 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/LKDash_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file23 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/BeamType1_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file24 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/BeamType2_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file25 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/BeamType3_40row/Velocity/node{W10_Mid40row}.out"

Tie_W10_HZ20_P = rdnumpy(file21)
LK_W10_HZ20_P = rdnumpy(file22)
Type1_W10_HZ20_P = rdnumpy(file23)
Type2_W10_HZ20_P = rdnumpy(file24)
Type3_W10_HZ20_P = rdnumpy(file25)
# ============================ SoilWidth = 20.0 m (HZ = 20)=======================================
Condition6 = f'{PWave_Choose}/W_20m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file26 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/TieBC_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file27 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/LKDash_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file28 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/BeamType1_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file29 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/BeamType2_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file30 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/BeamType3_40row/Velocity/node{W20_Mid40row}.out"

Tie_W20_HZ20_P = rdnumpy(file26)
LK_W20_HZ20_P = rdnumpy(file27)
Type1_W20_HZ20_P = rdnumpy(file28)
Type2_W20_HZ20_P = rdnumpy(file29)
Type3_W20_HZ20_P = rdnumpy(file30)

# ----------------- f = 40HZ --------------------------------
HZ40 = f'HZ_40'
# ============================ SoilWidth = 2.0 m (HZ = 40)=======================================
Condition7 = f'{PWave_Choose}/W_2m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file31 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/TieBC_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file32 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/LKDash_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file33 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/BeamType1_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file34 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/BeamType2_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file35 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/BeamType3_40row/Velocity/node{W2_Mid40row}.out"

Tie_W2_HZ40_P = rdnumpy(file31)
LK_W2_HZ40_P = rdnumpy(file32)
Type1_W2_HZ40_P = rdnumpy(file33)
Type2_W2_HZ40_P = rdnumpy(file34)
Type3_W2_HZ40_P = rdnumpy(file35)
# ============================ SoilWidth = 10.0 m (HZ = 40)=======================================
Condition8 = f'{PWave_Choose}/W_10m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file36 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/TieBC_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file37 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/LKDash_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file38 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/BeamType1_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file39 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/BeamType2_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file40 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/BeamType3_40row/Velocity/node{W10_Mid40row}.out"

Tie_W10_HZ40_P = rdnumpy(file36)
LK_W10_HZ40_P = rdnumpy(file37)
Type1_W10_HZ40_P = rdnumpy(file38)
Type2_W10_HZ40_P = rdnumpy(file39)
Type3_W10_HZ40_P = rdnumpy(file40)
# ============================ SoilWidth = 20.0 m (HZ = 40)=======================================
Condition9 = f'{PWave_Choose}/W_20m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file41 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/TieBC_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file42 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/LKDash_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file43 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/BeamType1_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file44 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/BeamType2_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file45 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/BeamType3_40row/Velocity/node{W20_Mid40row}.out"

Tie_W20_HZ40_P = rdnumpy(file41)
LK_W20_HZ40_P = rdnumpy(file42)
Type1_W20_HZ40_P = rdnumpy(file43)
Type2_W20_HZ40_P = rdnumpy(file44)
Type3_W20_HZ40_P = rdnumpy(file45)

# ----------------- f = 80HZ --------------------------------
HZ80 = f'HZ_80'
# ============================ SoilWidth = 2.0 m (HZ = 80)=======================================
Condition10 = f'{PWave_Choose}/W_2m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file46 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/TieBC_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file47 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/LKDash_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file48 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/BeamType1_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file49 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/BeamType2_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file50 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/BeamType3_40row/Velocity/node{W2_Mid40row}.out"

Tie_W2_HZ80_P = rdnumpy(file46)
LK_W2_HZ80_P = rdnumpy(file47)
Type1_W2_HZ80_P = rdnumpy(file48)
Type2_W2_HZ80_P = rdnumpy(file49)
Type3_W2_HZ80_P = rdnumpy(file50)
# ============================ SoilWidth = 10.0 m (HZ = 80)=======================================
Condition11 = f'{PWave_Choose}/W_10m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file51 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/TieBC_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file52 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/LKDash_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file53 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/BeamType1_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file54 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/BeamType2_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file55 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/BeamType3_40row/Velocity/node{W10_Mid40row}.out"

Tie_W10_HZ80_P = rdnumpy(file51)
LK_W10_HZ80_P = rdnumpy(file52)
Type1_W10_HZ80_P = rdnumpy(file53)
Type2_W10_HZ80_P = rdnumpy(file54)
Type3_W10_HZ80_P = rdnumpy(file55)
# ============================ SoilWidth = 20.0 m (HZ = 80)=======================================
Condition12 = f'{PWave_Choose}/W_20m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file56 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/TieBC_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file57 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/LKDash_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file58 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/BeamType1_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file59 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/BeamType2_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file60 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/BeamType3_40row/Velocity/node{W20_Mid40row}.out"

Tie_W20_HZ80_P = rdnumpy(file56)
LK_W20_HZ80_P = rdnumpy(file57)
Type1_W20_HZ80_P = rdnumpy(file58)
Type2_W20_HZ80_P = rdnumpy(file59)
Type3_W20_HZ80_P = rdnumpy(file60)

# ===================================== S Wave ========================================================
SWave_Choose = f'1D_Transport/Newmark_Linear/Swave'
# ----------------- f = 10HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
Condition13 = f'{SWave_Choose}/W_2m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file61 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/TieBC_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file62 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/LKDash_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file63 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/BeamType1_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file64 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/BeamType2_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file65 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/BeamType3_40row/Velocity/node{W2_Mid40row}.out"

Tie_W2_HZ10_S = rdnumpy(file61)
LK_W2_HZ10_S = rdnumpy(file62)
Type1_W2_HZ10_S = rdnumpy(file63)
Type2_W2_HZ10_S = rdnumpy(file64)
Type3_W2_HZ10_S = rdnumpy(file65)

# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
Condition14 = f'{SWave_Choose}/W_10m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file66 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/TieBC_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file67 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/LKDash_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file68 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/BeamType1_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file69 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/BeamType2_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file70 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/BeamType3_40row/Velocity/node{W10_Mid40row}.out"

Tie_W10_HZ10_S = rdnumpy(file66)
LK_W10_HZ10_S = rdnumpy(file67)
Type1_W10_HZ10_S = rdnumpy(file68)
Type2_W10_HZ10_S = rdnumpy(file69)
Type3_W10_HZ10_S = rdnumpy(file70)

# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
Condition15 = f'{SWave_Choose}/W_20m/{HZ10}'
# --------- Tie Boundary Condition ----------------
file71 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/TieBC_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file72 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/LKDash_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file73 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/BeamType1_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file74 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/BeamType2_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file75 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/BeamType3_40row/Velocity/node{W20_Mid40row}.out"

Tie_W20_HZ10_S = rdnumpy(file71)
LK_W20_HZ10_S = rdnumpy(file72)
Type1_W20_HZ10_S = rdnumpy(file73)
Type2_W20_HZ10_S = rdnumpy(file74)
Type3_W20_HZ10_S = rdnumpy(file75)

# ----------------- f = 20HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 20)=======================================
Condition16 = f'{SWave_Choose}/W_2m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file76 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/TieBC_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file77 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/LKDash_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file78 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/BeamType1_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file79 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/BeamType2_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file80 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/BeamType3_40row/Velocity/node{W2_Mid40row}.out"

Tie_W2_HZ20_S = rdnumpy(file76)
LK_W2_HZ20_S = rdnumpy(file77)
Type1_W2_HZ20_S = rdnumpy(file78)
Type2_W2_HZ20_S = rdnumpy(file79)
Type3_W2_HZ20_S = rdnumpy(file80)
# ============================ SoilWidth = 10.0 m (HZ = 20)=======================================
Condition17 = f'{SWave_Choose}/W_10m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file81 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition17}/TieBC_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file82 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition17}/LKDash_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file83 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition17}/BeamType1_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file84 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition17}/BeamType2_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file85 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition17}/BeamType3_40row/Velocity/node{W10_Mid40row}.out"

Tie_W10_HZ20_S = rdnumpy(file81)
LK_W10_HZ20_S = rdnumpy(file82)
Type1_W10_HZ20_S = rdnumpy(file83)
Type2_W10_HZ20_S = rdnumpy(file84)
Type3_W10_HZ20_S = rdnumpy(file85)
# ============================ SoilWidth = 20.0 m (HZ = 20)=======================================
Condition18 = f'{SWave_Choose}/W_20m/{HZ20}'
# --------- Tie Boundary Condition ----------------
file86 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition18}/TieBC_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file87 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition18}/LKDash_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file88 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition18}/BeamType1_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file89 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition18}/BeamType2_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file90 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition18}/BeamType3_40row/Velocity/node{W20_Mid40row}.out"

Tie_W20_HZ20_S = rdnumpy(file86)
LK_W20_HZ20_S = rdnumpy(file87)
Type1_W20_HZ20_S = rdnumpy(file88)
Type2_W20_HZ20_S = rdnumpy(file89)
Type3_W20_HZ20_S = rdnumpy(file90)

# ----------------- f = 40HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 40)=======================================
Condition19 = f'{SWave_Choose}/W_2m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file91 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition19}/TieBC_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file92 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition19}/LKDash_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file93 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition19}/BeamType1_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file94 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition19}/BeamType2_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file95 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition19}/BeamType3_40row/Velocity/node{W2_Mid40row}.out"

Tie_W2_HZ40_S = rdnumpy(file91)
LK_W2_HZ40_S = rdnumpy(file92)
Type1_W2_HZ40_S = rdnumpy(file93)
Type2_W2_HZ40_S = rdnumpy(file94)
Type3_W2_HZ40_S = rdnumpy(file95)
# ============================ SoilWidth = 10.0 m (HZ = 40)=======================================
Condition20 = f'{SWave_Choose}/W_10m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file96 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition20}/TieBC_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file97 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition20}/LKDash_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file98 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition20}/BeamType1_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file99 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition20}/BeamType2_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file100 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition20}/BeamType3_40row/Velocity/node{W10_Mid40row}.out"

Tie_W10_HZ40_S = rdnumpy(file96)
LK_W10_HZ40_S = rdnumpy(file97)
Type1_W10_HZ40_S = rdnumpy(file98)
Type2_W10_HZ40_S = rdnumpy(file99)
Type3_W10_HZ40_S = rdnumpy(file100)
# ============================ SoilWidth = 20.0 m (HZ = 40)=======================================
Condition21 = f'{SWave_Choose}/W_20m/{HZ40}'
# --------- Tie Boundary Condition ----------------
file101 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition21}/TieBC_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file102 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition21}/LKDash_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file103 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition21}/BeamType1_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file104 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition21}/BeamType2_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file105 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition21}/BeamType3_40row/Velocity/node{W20_Mid40row}.out"

Tie_W20_HZ40_S = rdnumpy(file101)
LK_W20_HZ40_S = rdnumpy(file102)
Type1_W20_HZ40_S = rdnumpy(file103)
Type2_W20_HZ40_S = rdnumpy(file104)
Type3_W20_HZ40_S = rdnumpy(file105)

# ----------------- f = 80HZ --------------------------------
# ============================ SoilWidth = 2.0 m (HZ = 80)=======================================
Condition22 = f'{SWave_Choose}/W_2m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file106 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition22}/TieBC_40row/Velocity/node{W2_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file107 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition22}/LKDash_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file108 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition22}/BeamType1_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file109 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition22}/BeamType2_40row/Velocity/node{W2_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file110 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition22}/BeamType3_40row/Velocity/node{W2_Mid40row}.out"

Tie_W2_HZ80_S = rdnumpy(file106)
LK_W2_HZ80_S = rdnumpy(file107)
Type1_W2_HZ80_S = rdnumpy(file108)
Type2_W2_HZ80_S = rdnumpy(file109)
Type3_W2_HZ80_S = rdnumpy(file110)
# ============================ SoilWidth = 10.0 m (HZ = 80)=======================================
Condition23 = f'{SWave_Choose}/W_10m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file111 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition23}/TieBC_40row/Velocity/node{W10_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file112 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition23}/LKDash_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file113 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition23}/BeamType1_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file114 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition23}/BeamType2_40row/Velocity/node{W10_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file115 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition23}/BeamType3_40row/Velocity/node{W10_Mid40row}.out"

Tie_W10_HZ80_S = rdnumpy(file111)
LK_W10_HZ80_S = rdnumpy(file112)
Type1_W10_HZ80_S = rdnumpy(file113)
Type2_W10_HZ80_S = rdnumpy(file114)
Type3_W10_HZ80_S = rdnumpy(file115)
# ============================ SoilWidth = 20.0 m (HZ = 80)=======================================
Condition24 = f'{SWave_Choose}/W_20m/{HZ80}'
# --------- Tie Boundary Condition ----------------
file116 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition24}/TieBC_40row/Velocity/node{W20_Mid40row}.out"
# --------- LK Dashpot Boundary Condition ----------------
file117 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition24}/LKDash_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 1 ：Distributed Beam Boundary Condition ----------------
file118 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition24}/BeamType1_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 2 ：Distributed Beam and Node Boundary Condition ----------------
file119 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition24}/BeamType2_40row/Velocity/node{W20_Mid40row}.out"
# --------- Type 3 ：Distributed Beam and Node Boundary Condition ----------------
file120 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition24}/BeamType3_40row/Velocity/node{W20_Mid40row}.out"

Tie_W20_HZ80_S = rdnumpy(file116)
LK_W20_HZ80_S = rdnumpy(file117)
Type1_W20_HZ80_S = rdnumpy(file118)
Type2_W20_HZ80_S = rdnumpy(file119)
Type3_W20_HZ80_S = rdnumpy(file120)

# ================================== Prepare Relative Error and Absolute Error ============================
def Find_ColMaxValue(column_index, ele80_Mid):
    column = ele80_Mid[:, column_index]
    max_value = np.max(column)
    max_index = np.argmax(column)
    
    min_value = np.min(column)
    min_index = np.argmin(column)

    print(f'max_value= {max_value}; max_index= {max_index}; min_value= {min_value}; min_index= {min_index}')
    return(max_value)

Analysis_Column = Nele-1
# ---------- Find Analysis data Peak Value -----------------
maxAnaly_PHZ10 = Find_ColMaxValue(Analysis_Column, HZ10_Pwave)
maxAnaly_PHZ20 = Find_ColMaxValue(Analysis_Column, HZ20_Pwave)
maxAnaly_PHZ40 = Find_ColMaxValue(Analysis_Column, HZ40_Pwave)
maxAnaly_PHZ80 = Find_ColMaxValue(Analysis_Column, HZ80_Pwave)

maxAnaly_SHZ10 = Find_ColMaxValue(Analysis_Column, HZ10_Swave)
maxAnaly_SHZ20 = Find_ColMaxValue(Analysis_Column, HZ20_Swave)
maxAnaly_SHZ40 = Find_ColMaxValue(Analysis_Column, HZ40_Swave)
maxAnaly_SHZ80 = Find_ColMaxValue(Analysis_Column, HZ80_Swave)

def process_column(matrix, column_index):
    column = matrix[:, column_index]
    abs_column = np.abs(column)
    
    max_index = np.argmax(abs_column)
    max_peak = np.max(abs_column)
    
    print(f'max_value= {max_peak}; max_index= {max_index}')
    return max_peak

Pcolumn_index = 2 # Pwave = 2 (yaxis)
# ------------ 10HZ --------------------
maxTie2_PHZ10 = process_column(Tie_W2_HZ10_P, Pcolumn_index)
maxLK2_PHZ10 = process_column(LK_W2_HZ10_P, Pcolumn_index)
maxType1_2_PHZ10 = process_column(Type1_W2_HZ10_P, Pcolumn_index)
maxType2_2_PHZ10 = process_column(Type2_W2_HZ10_P, Pcolumn_index)
maxType3_2_PHZ10 = process_column(Type3_W2_HZ10_P, Pcolumn_index)

maxTie10_PHZ10 = process_column(Tie_W10_HZ10_P, Pcolumn_index)
maxLK10_PHZ10 = process_column(LK_W10_HZ10_P, Pcolumn_index)
maxType1_10_PHZ10 = process_column(Type1_W10_HZ10_P, Pcolumn_index)
maxType2_10_PHZ10 = process_column(Type2_W10_HZ10_P, Pcolumn_index)
maxType3_10_PHZ10 = process_column(Type3_W10_HZ10_P, Pcolumn_index)

maxTie20_PHZ10 = process_column(Tie_W20_HZ10_P, Pcolumn_index)
maxLK20_PHZ10 = process_column(LK_W20_HZ10_P, Pcolumn_index)
maxType1_20_PHZ10 = process_column(Type1_W20_HZ10_P, Pcolumn_index)
maxType2_20_PHZ10 = process_column(Type2_W20_HZ10_P, Pcolumn_index)
maxType3_20_PHZ10 = process_column(Type3_W20_HZ10_P, Pcolumn_index)

# ------------ 20HZ --------------------
maxTie2_PHZ20 = process_column(Tie_W2_HZ20_P, Pcolumn_index)
maxLK2_PHZ20 = process_column(LK_W2_HZ20_P, Pcolumn_index)
maxType1_2_PHZ20 = process_column(Type1_W2_HZ20_P, Pcolumn_index)
maxType2_2_PHZ20 = process_column(Type2_W2_HZ20_P, Pcolumn_index)
maxType3_2_PHZ20 = process_column(Type3_W2_HZ20_P, Pcolumn_index)

maxTie10_PHZ20 = process_column(Tie_W10_HZ20_P, Pcolumn_index)
maxLK10_PHZ20 = process_column(LK_W10_HZ20_P, Pcolumn_index)
maxType1_10_PHZ20 = process_column(Type1_W10_HZ20_P, Pcolumn_index)
maxType2_10_PHZ20 = process_column(Type2_W10_HZ20_P, Pcolumn_index)
maxType3_10_PHZ20 = process_column(Type3_W10_HZ20_P, Pcolumn_index)

maxTie20_PHZ20 = process_column(Tie_W20_HZ20_P, Pcolumn_index)
maxLK20_PHZ20 = process_column(LK_W20_HZ20_P, Pcolumn_index)
maxType1_20_PHZ20 = process_column(Type1_W20_HZ20_P, Pcolumn_index)
maxType2_20_PHZ20 = process_column(Type2_W20_HZ20_P, Pcolumn_index)
maxType3_20_PHZ20 = process_column(Type3_W20_HZ20_P, Pcolumn_index)

# ------------ 40HZ --------------------
maxTie2_PHZ40 = process_column(Tie_W2_HZ40_P, Pcolumn_index)
maxLK2_PHZ40 = process_column(LK_W2_HZ40_P, Pcolumn_index)
maxType1_2_PHZ40 = process_column(Type1_W2_HZ40_P, Pcolumn_index)
maxType2_2_PHZ40 = process_column(Type2_W2_HZ40_P, Pcolumn_index)
maxType3_2_PHZ40 = process_column(Type3_W2_HZ40_P, Pcolumn_index)

maxTie10_PHZ40 = process_column(Tie_W10_HZ40_P, Pcolumn_index)
maxLK10_PHZ40 = process_column(LK_W10_HZ40_P, Pcolumn_index)
maxType1_10_PHZ40 = process_column(Type1_W10_HZ40_P, Pcolumn_index)
maxType2_10_PHZ40 = process_column(Type2_W10_HZ40_P, Pcolumn_index)
maxType3_10_PHZ40 = process_column(Type3_W10_HZ40_P, Pcolumn_index)

maxTie20_PHZ40 = process_column(Tie_W20_HZ40_P, Pcolumn_index)
maxLK20_PHZ40 = process_column(LK_W20_HZ40_P, Pcolumn_index)
maxType1_20_PHZ40 = process_column(Type1_W20_HZ40_P, Pcolumn_index)
maxType2_20_PHZ40 = process_column(Type2_W20_HZ40_P, Pcolumn_index)
maxType3_20_PHZ40 = process_column(Type3_W20_HZ40_P, Pcolumn_index)

# ------------ 80HZ --------------------
maxTie2_PHZ80 = process_column(Tie_W2_HZ80_P, Pcolumn_index)
maxLK2_PHZ80 = process_column(LK_W2_HZ80_P, Pcolumn_index)
maxType1_2_PHZ80 = process_column(Type1_W2_HZ80_P, Pcolumn_index)
maxType2_2_PHZ80 = process_column(Type2_W2_HZ80_P, Pcolumn_index)
maxType3_2_PHZ80 = process_column(Type3_W2_HZ80_P, Pcolumn_index)

maxTie10_PHZ80 = process_column(Tie_W10_HZ80_P, Pcolumn_index)
maxLK10_PHZ80 = process_column(LK_W10_HZ80_P, Pcolumn_index)
maxType1_10_PHZ80 = process_column(Type1_W10_HZ80_P, Pcolumn_index)
maxType2_10_PHZ80 = process_column(Type2_W10_HZ80_P, Pcolumn_index)
maxType3_10_PHZ80 = process_column(Type3_W10_HZ80_P, Pcolumn_index)

maxTie20_PHZ80 = process_column(Tie_W20_HZ80_P, Pcolumn_index)
maxLK20_PHZ80 = process_column(LK_W20_HZ80_P, Pcolumn_index)
maxType1_20_PHZ80 = process_column(Type1_W20_HZ80_P, Pcolumn_index)
maxType2_20_PHZ80 = process_column(Type2_W20_HZ80_P, Pcolumn_index)
maxType3_20_PHZ80 = process_column(Type3_W20_HZ80_P, Pcolumn_index)

Scolumn_index = 1 # Swave = 1 (Xaxis)
# ------------ 10HZ --------------------
maxTie2_SHZ10 = process_column(Tie_W2_HZ10_S, Scolumn_index)
maxLK2_SHZ10 = process_column(LK_W2_HZ10_S, Scolumn_index)
maxType1_2_SHZ10 = process_column(Type1_W2_HZ10_S, Scolumn_index)
maxType2_2_SHZ10 = process_column(Type2_W2_HZ10_S, Scolumn_index)
maxType3_2_SHZ10 = process_column(Type3_W2_HZ10_S, Scolumn_index)

maxTie10_SHZ10 = process_column(Tie_W10_HZ10_S, Scolumn_index)
maxLK10_SHZ10 = process_column(LK_W10_HZ10_S, Scolumn_index)
maxType1_10_SHZ10 = process_column(Type1_W10_HZ10_S, Scolumn_index)
maxType2_10_SHZ10 = process_column(Type2_W10_HZ10_S, Scolumn_index)
maxType3_10_SHZ10 = process_column(Type3_W10_HZ10_S, Scolumn_index)

maxTie20_SHZ10 = process_column(Tie_W20_HZ10_S, Scolumn_index)
maxLK20_SHZ10 = process_column(LK_W20_HZ10_S, Scolumn_index)
maxType1_20_SHZ10 = process_column(Type1_W20_HZ10_S, Scolumn_index)
maxType2_20_SHZ10 = process_column(Type2_W20_HZ10_S, Scolumn_index)
maxType3_20_SHZ10 = process_column(Type3_W20_HZ10_S, Scolumn_index)

# ------------ 20HZ --------------------
maxTie2_SHZ20 = process_column(Tie_W2_HZ20_S, Scolumn_index)
maxLK2_SHZ20 = process_column(LK_W2_HZ20_S, Scolumn_index)
maxType1_2_SHZ20 = process_column(Type1_W2_HZ20_S, Scolumn_index)
maxType2_2_SHZ20 = process_column(Type2_W2_HZ20_S, Scolumn_index)
maxType3_2_SHZ20 = process_column(Type3_W2_HZ20_S, Scolumn_index)

maxTie10_SHZ20 = process_column(Tie_W10_HZ20_S, Scolumn_index)
maxLK10_SHZ20 = process_column(LK_W10_HZ20_S, Scolumn_index)
maxType1_10_SHZ20 = process_column(Type1_W10_HZ20_S, Scolumn_index)
maxType2_10_SHZ20 = process_column(Type2_W10_HZ20_S, Scolumn_index)
maxType3_10_SHZ20 = process_column(Type3_W10_HZ20_S, Scolumn_index)

maxTie20_SHZ20 = process_column(Tie_W20_HZ20_S, Scolumn_index)
maxLK20_SHZ20 = process_column(LK_W20_HZ20_S, Scolumn_index)
maxType1_20_SHZ20 = process_column(Type1_W20_HZ20_S, Scolumn_index)
maxType2_20_SHZ20 = process_column(Type2_W20_HZ20_S, Scolumn_index)
maxType3_20_SHZ20 = process_column(Type3_W20_HZ20_S, Scolumn_index)

# ------------ 40HZ --------------------
maxTie2_SHZ40 = process_column(Tie_W2_HZ40_S, Scolumn_index)
maxLK2_SHZ40 = process_column(LK_W2_HZ40_S, Scolumn_index)
maxType1_2_SHZ40 = process_column(Type1_W2_HZ40_S, Scolumn_index)
maxType2_2_SHZ40 = process_column(Type2_W2_HZ40_S, Scolumn_index)
maxType3_2_SHZ40 = process_column(Type3_W2_HZ40_S, Scolumn_index)

maxTie10_SHZ40 = process_column(Tie_W10_HZ40_S, Scolumn_index)
maxLK10_SHZ40 = process_column(LK_W10_HZ40_S, Scolumn_index)
maxType1_10_SHZ40 = process_column(Type1_W10_HZ40_S, Scolumn_index)
maxType2_10_SHZ40 = process_column(Type2_W10_HZ40_S, Scolumn_index)
maxType3_10_SHZ40 = process_column(Type3_W10_HZ40_S, Scolumn_index)

maxTie20_SHZ40 = process_column(Tie_W20_HZ40_S, Scolumn_index)
maxLK20_SHZ40 = process_column(LK_W20_HZ40_S, Scolumn_index)
maxType1_20_SHZ40 = process_column(Type1_W20_HZ40_S, Scolumn_index)
maxType2_20_SHZ40 = process_column(Type2_W20_HZ40_S, Scolumn_index)
maxType3_20_SHZ40 = process_column(Type3_W20_HZ40_S, Scolumn_index)

# ------------ 80HZ --------------------
maxTie2_SHZ80 = process_column(Tie_W2_HZ80_S, Scolumn_index)
maxLK2_SHZ80 = process_column(LK_W2_HZ80_S, Scolumn_index)
maxType1_2_SHZ80 = process_column(Type1_W2_HZ80_S, Scolumn_index)
maxType2_2_SHZ80 = process_column(Type2_W2_HZ80_S, Scolumn_index)
maxType3_2_SHZ80 = process_column(Type3_W2_HZ80_S, Scolumn_index)

maxTie10_SHZ80 = process_column(Tie_W10_HZ80_S, Scolumn_index)
maxLK10_SHZ80 = process_column(LK_W10_HZ80_S, Scolumn_index)
maxType1_10_SHZ80 = process_column(Type1_W10_HZ80_S, Scolumn_index)
maxType2_10_SHZ80 = process_column(Type2_W10_HZ80_S, Scolumn_index)
maxType3_10_SHZ80 = process_column(Type3_W10_HZ80_S, Scolumn_index)

maxTie20_SHZ80 = process_column(Tie_W20_HZ80_S, Scolumn_index)
maxLK20_SHZ80 = process_column(LK_W20_HZ80_S, Scolumn_index)
maxType1_20_SHZ80 = process_column(Type1_W20_HZ80_S, Scolumn_index)
maxType2_20_SHZ80 = process_column(Type2_W20_HZ80_S, Scolumn_index)
maxType3_20_SHZ80 = process_column(Type3_W20_HZ80_S, Scolumn_index)

Frequency_Size = np.array([1/10, 1/20, 1/40, 1/80])

def errMatrix(error_dc, maxTie2_HZ10, maxTie2_HZ20, maxTie2_HZ40, maxTie2_HZ80):
    error_dc[:,0] = Frequency_Size[:]
    error_dc[0,1] = maxTie2_HZ10
    error_dc[1,1] = maxTie2_HZ20
    error_dc[2,1] = maxTie2_HZ40
    error_dc[3,1] = maxTie2_HZ80
    return error_dc

# ============================= Middle Node (Pwave) ========================================
# ------------W20m Error Peak Value-----------------------
Tie20_Perror = np.zeros((len(Frequency_Size),2))
errMatrix(Tie20_Perror, maxTie20_PHZ10, maxTie20_PHZ20, maxTie20_PHZ40, maxTie20_PHZ80)

LK20_Perror = np.zeros((len(Frequency_Size),2))
errMatrix(LK20_Perror, maxLK20_PHZ10, maxLK20_PHZ20, maxLK20_PHZ40, maxLK20_PHZ80)

Type1_P20error = np.zeros((len(Frequency_Size),2))
errMatrix(Type1_P20error, maxType1_20_PHZ10, maxType1_20_PHZ20, maxType1_20_PHZ40, maxType1_20_PHZ80)

Type2_P20error = np.zeros((len(Frequency_Size),2))
errMatrix(Type2_P20error, maxType2_20_PHZ10, maxType2_20_PHZ20, maxType2_20_PHZ40, maxType2_20_PHZ80)

Type3_P20error = np.zeros((len(Frequency_Size),2))
errMatrix(Type3_P20error, maxType3_20_PHZ10, maxType3_20_PHZ20, maxType3_20_PHZ40, maxType3_20_PHZ80)

# ------------W10m Error Peak Value-----------------------
Tie10_Perror = np.zeros((len(Frequency_Size),2))
errMatrix(Tie10_Perror, maxTie10_PHZ10, maxTie10_PHZ20, maxTie10_PHZ40, maxTie10_PHZ80)

LK10_Perror = np.zeros((len(Frequency_Size),2))
errMatrix(LK10_Perror, maxLK10_PHZ10, maxLK10_PHZ20, maxLK10_PHZ40, maxLK10_PHZ80)

Type1_P10error = np.zeros((len(Frequency_Size),2))
errMatrix(Type1_P10error, maxType1_10_PHZ10, maxType1_10_PHZ20, maxType1_10_PHZ40, maxType1_10_PHZ80)

Type2_P10error = np.zeros((len(Frequency_Size),2))
errMatrix(Type2_P10error, maxType2_10_PHZ10, maxType2_10_PHZ20, maxType2_10_PHZ40, maxType2_10_PHZ80)

Type3_P10error = np.zeros((len(Frequency_Size),2))
errMatrix(Type3_P10error, maxType3_10_PHZ10, maxType3_10_PHZ20, maxType3_10_PHZ40, maxType3_10_PHZ80)

# ------------W2m Error Peak Value-----------------------
Tie2_Perror = np.zeros((len(Frequency_Size),2))
errMatrix(Tie2_Perror, maxTie2_PHZ10, maxTie2_PHZ20, maxTie2_PHZ40, maxTie2_PHZ80)

LK2_Perror = np.zeros((len(Frequency_Size),2))
errMatrix(LK2_Perror, maxLK2_PHZ10, maxLK2_PHZ20, maxLK2_PHZ40, maxLK2_PHZ80)

Type1_P2error = np.zeros((len(Frequency_Size),2))
errMatrix(Type1_P2error, maxType1_2_PHZ10, maxType1_2_PHZ20, maxType1_2_PHZ40, maxType1_2_PHZ80)

Type2_P2error = np.zeros((len(Frequency_Size),2))
errMatrix(Type2_P2error, maxType2_2_PHZ10, maxType2_2_PHZ20, maxType2_2_PHZ40, maxType2_2_PHZ80)

Type3_P2error = np.zeros((len(Frequency_Size),2))
errMatrix(Type3_P2error, maxType3_2_PHZ10, maxType3_2_PHZ20, maxType3_2_PHZ40, maxType3_2_PHZ80)

#  ---------- calculate Relative Error ----------------------------
Tie20_Perr = np.zeros((len(Frequency_Size),2))
LK20_Perr = np.zeros((len(Frequency_Size),2))
Type1_W20_Perr = np.zeros((len(Frequency_Size),2))
Type2_W20_Perr = np.zeros((len(Frequency_Size),2))
Type3_W20_Perr = np.zeros((len(Frequency_Size),2))

Tie10_Perr = np.zeros((len(Frequency_Size),2))
LK10_Perr = np.zeros((len(Frequency_Size),2))
Type1_W10_Perr = np.zeros((len(Frequency_Size),2))
Type2_W10_Perr = np.zeros((len(Frequency_Size),2))
Type3_W10_Perr = np.zeros((len(Frequency_Size),2))

Tie2_Perr = np.zeros((len(Frequency_Size),2))
LK2_Perr = np.zeros((len(Frequency_Size),2))
Type1_W2_Perr = np.zeros((len(Frequency_Size),2))
Type2_W2_Perr = np.zeros((len(Frequency_Size),2))
Type3_W2_Perr = np.zeros((len(Frequency_Size),2))

# ============================= Middle Node (Swave) ========================================
# ------------W20m Error Peak Value-----------------------
Tie20_Serror = np.zeros((len(Frequency_Size),2))
errMatrix(Tie20_Serror, maxTie20_SHZ10, maxTie20_SHZ20, maxTie20_SHZ40, maxTie20_SHZ80)

LK20_Serror = np.zeros((len(Frequency_Size),2))
errMatrix(LK20_Serror, maxLK20_SHZ10, maxLK20_SHZ20, maxLK20_SHZ40, maxLK20_SHZ80)

Type1_S20error = np.zeros((len(Frequency_Size),2))
errMatrix(Type1_S20error, maxType1_20_SHZ10, maxType1_20_SHZ20, maxType1_20_SHZ40, maxType1_20_SHZ80)

Type2_S20error = np.zeros((len(Frequency_Size),2))
errMatrix(Type2_S20error, maxType2_20_SHZ10, maxType2_20_SHZ20, maxType2_20_SHZ40, maxType2_20_SHZ80)

Type3_S20error = np.zeros((len(Frequency_Size),2))
errMatrix(Type3_S20error, maxType3_20_SHZ10, maxType3_20_SHZ20, maxType3_20_SHZ40, maxType3_20_SHZ80)

# ------------W10m Error Peak Value-----------------------
Tie10_Serror = np.zeros((len(Frequency_Size),2))
errMatrix(Tie10_Serror, maxTie10_SHZ10, maxTie10_SHZ20, maxTie10_SHZ40, maxTie10_SHZ80)

LK10_Serror = np.zeros((len(Frequency_Size),2))
errMatrix(LK10_Serror, maxLK10_SHZ10, maxLK10_SHZ20, maxLK10_SHZ40, maxLK10_SHZ80)

Type1_S10error = np.zeros((len(Frequency_Size),2))
errMatrix(Type1_S10error, maxType1_10_SHZ10, maxType1_10_SHZ20, maxType1_10_SHZ40, maxType1_10_SHZ80)

Type2_S10error = np.zeros((len(Frequency_Size),2))
errMatrix(Type2_S10error, maxType2_10_SHZ10, maxType2_10_SHZ20, maxType2_10_SHZ40, maxType2_10_SHZ80)

Type3_S10error = np.zeros((len(Frequency_Size),2))
errMatrix(Type3_S10error, maxType3_10_SHZ10, maxType3_10_SHZ20, maxType3_10_SHZ40, maxType3_10_SHZ80)

# ------------W2m Error Peak Value-----------------------
Tie2_Serror = np.zeros((len(Frequency_Size),2))
errMatrix(Tie2_Serror, maxTie2_SHZ10, maxTie2_SHZ20, maxTie2_SHZ40, maxTie2_SHZ80)

LK2_Serror = np.zeros((len(Frequency_Size),2))
errMatrix(LK2_Serror, maxLK2_SHZ10, maxLK2_SHZ20, maxLK2_SHZ40, maxLK2_SHZ80)

Type1_S2error = np.zeros((len(Frequency_Size),2))
errMatrix(Type1_S2error, maxType1_2_SHZ10, maxType1_2_SHZ20, maxType1_2_SHZ40, maxType1_2_SHZ80)

Type2_S2error = np.zeros((len(Frequency_Size),2))
errMatrix(Type2_S2error, maxType2_2_SHZ10, maxType2_2_SHZ20, maxType2_2_SHZ40, maxType2_2_SHZ80)

Type3_S2error = np.zeros((len(Frequency_Size),2))
errMatrix(Type3_S2error, maxType3_2_SHZ10, maxType3_2_SHZ20, maxType3_2_SHZ40, maxType3_2_SHZ80)

#  ---------- calculate Relative Error ----------------------------
Tie20_Serr = np.zeros((len(Frequency_Size),2))
LK20_Serr = np.zeros((len(Frequency_Size),2))
Type1_W20_Serr = np.zeros((len(Frequency_Size),2))
Type2_W20_Serr = np.zeros((len(Frequency_Size),2))
Type3_W20_Serr = np.zeros((len(Frequency_Size),2))

Tie10_Serr = np.zeros((len(Frequency_Size),2))
LK10_Serr = np.zeros((len(Frequency_Size),2))
Type1_W10_Serr = np.zeros((len(Frequency_Size),2))
Type2_W10_Serr = np.zeros((len(Frequency_Size),2))
Type3_W10_Serr = np.zeros((len(Frequency_Size),2))

Tie2_Serr = np.zeros((len(Frequency_Size),2))
LK2_Serr = np.zeros((len(Frequency_Size),2))
Type1_W2_Serr = np.zeros((len(Frequency_Size),2))
Type2_W2_Serr = np.zeros((len(Frequency_Size),2))
Type3_W2_Serr = np.zeros((len(Frequency_Size),2))

def Calculate_Error(TieErr, Tie_error, maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80): # 
    TieErr[:,0] = Tie_error[:,0]
# ------------------------- Absolute Relative Error ------------------        
    TieErr[0,1] = ((Tie_error[0,1] - maxAnaly_HZ10)/maxAnaly_HZ10)*100
    TieErr[1,1] = ((Tie_error[1,1] - maxAnaly_HZ20)/maxAnaly_HZ20)*100
    TieErr[2,1] = ((Tie_error[2,1] - maxAnaly_HZ40)/maxAnaly_HZ40)*100
    TieErr[3,1] = ((Tie_error[3,1] - maxAnaly_HZ80)/maxAnaly_HZ80)*100
    
# ============================= Middle Node (Pwave) ========================================      
Calculate_Error(Tie20_Perr, Tie20_Perror, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)
Calculate_Error(LK20_Perr, LK20_Perror, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)
Calculate_Error(Type1_W20_Perr, Type1_P20error, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)
Calculate_Error(Type2_W20_Perr, Type2_P20error, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)
Calculate_Error(Type3_W20_Perr, Type3_P20error, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)

Calculate_Error(Tie10_Perr, Tie10_Perror, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)
Calculate_Error(LK10_Perr, LK10_Perror, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)
Calculate_Error(Type1_W10_Perr, Type1_P10error, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)
Calculate_Error(Type2_W10_Perr, Type2_P10error, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)
Calculate_Error(Type3_W10_Perr, Type3_P10error, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)

Calculate_Error(Tie2_Perr, Tie2_Perror, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)
Calculate_Error(LK2_Perr, LK2_Perror, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)
Calculate_Error(Type1_W2_Perr, Type1_P2error, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)
Calculate_Error(Type2_W2_Perr, Type2_P2error, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)
Calculate_Error(Type3_W2_Perr, Type3_P2error, maxAnaly_PHZ10, maxAnaly_PHZ20, maxAnaly_PHZ40, maxAnaly_PHZ80)

# ============================= Middle Node (Swave) ========================================
Calculate_Error(Tie20_Serr, Tie20_Serror, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)
Calculate_Error(LK20_Serr, LK20_Serror, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)
Calculate_Error(Type1_W20_Serr, Type1_S20error, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)
Calculate_Error(Type2_W20_Serr, Type2_S20error, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)
Calculate_Error(Type3_W20_Serr, Type3_S20error, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)

Calculate_Error(Tie10_Serr, Tie10_Serror, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)
Calculate_Error(LK10_Serr, LK10_Serror, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)
Calculate_Error(Type1_W10_Serr, Type1_S10error, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)
Calculate_Error(Type2_W10_Serr, Type2_S10error, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)
Calculate_Error(Type3_W10_Serr, Type3_S10error, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)

Calculate_Error(Tie2_Serr, Tie2_Serror, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)
Calculate_Error(LK2_Serr, LK2_Serror, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)
Calculate_Error(Type1_W2_Serr, Type1_S2error, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)
Calculate_Error(Type2_W2_Serr, Type2_S2error, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)
Calculate_Error(Type3_W2_Serr, Type3_S2error, maxAnaly_SHZ10, maxAnaly_SHZ20, maxAnaly_SHZ40, maxAnaly_SHZ80)

# --------------- Draw Relative error: Dc/WaveLength --------------------------
Dy = 0.25 # m
Dy_lamb_Pwave = np.array([Dy/Plamb10, Dy/Plamb20, Dy/Plamb40, Dy/Plamb80])
Dy_lamb_Swave = np.array([Dy/Slamb10, Dy/Slamb20, Dy/Slamb40, Dy/Slamb80])

marksize = 14
# ==================Draw Relative error : Dy/WaveLength =============================
def DifferTime_RelativeError2(TiePErr, Type1PErr, Type2PErr, Type3PErr, TieSErr, Type1SErr, Type2SErr, Type3SErr):
    # ------------ P wave --------------------------
    plt.plot(Dy_lamb_Pwave[:], TiePErr[:,1],marker = '^',markersize=marksize,markerfacecolor = 'none',label = 'Tie', color = 'crimson', linewidth = 3.0)
    # plt.plot(Dy_lamb_Pwave[:,0], LKErr[:,Peak],marker = 'p',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot')
    plt.plot(Dy_lamb_Pwave[:], Type1PErr[:,1],marker = 'o',markersize=marksize,markerfacecolor = 'none',label = 'Beam-based', color = 'crimson', linewidth = 3.0)
    plt.plot(Dy_lamb_Pwave[:], Type2PErr[:,1],marker = '<',markersize=marksize,markerfacecolor = 'none',label = 'Hybrid', color = 'crimson', linewidth = 3.0)
    plt.plot(Dy_lamb_Pwave[:], Type3PErr[:,1],marker = 's',markersize=marksize,markerfacecolor = 'none',label = 'Node-based', color = 'crimson', linewidth = 3.0)
    
 # ----------------S wave------------------------------
    plt.plot(Dy_lamb_Swave[:], TieSErr[:,1],marker = '^',markersize=marksize,markerfacecolor = 'none', color = 'dimgrey', linewidth = 3.0)
    # plt.plot(Dy_lamb_Swave[:,0], LKErr[:,1],marker = 'p',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot')
    plt.plot(Dy_lamb_Swave[:], Type1SErr[:,1],marker = 'o',markersize=marksize,markerfacecolor = 'none', color = 'dimgrey', linewidth = 3.0) # , ls = '--'
    plt.plot(Dy_lamb_Swave[:], Type2SErr[:,1],marker = '<',markersize=marksize,markerfacecolor = 'none', color = 'dimgrey', linewidth = 3.0) # , ls =':'
    plt.plot(Dy_lamb_Swave[:], Type3SErr[:,1],marker = 's',markersize=marksize,markerfacecolor = 'none', color = 'dimgrey', linewidth = 3.0) # , ls = '-.'
 
    plt.xticks(fontsize = 20, fontweight='bold', color='black')
    plt.yticks(fontsize = 20, fontweight='bold', color='black')

    # plt.ylim(0, 5.0) 
    # plt.grid(True)
    # ========== set up figure thick ============================
    bwidth = 2
    TK = plt.gca()
    TK.spines['bottom'].set_linewidth(bwidth)
    TK.spines['left'].set_linewidth(bwidth)
    TK.spines['top'].set_linewidth(bwidth)
    TK.spines['right'].set_linewidth(bwidth)
    
    ax = plt.gca()
    # -------------- Consider X-axis  -----------------------
    ax.set_xscale('log', base=10)
    ax.set_xticks([], minor=False)
    ax.set_xticks([], minor=True)
    x_ticks_Num = np.array([0.01, 0.02, 0.04, 0.06, 0.08, 0.1])  # td = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1] ; Dy/lamb = [0.01, 0.02, 0.04, 0.06, 0.08, 0.1]
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.2f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='major', labelsize= 20, length=8, width=2)
    
    # -------------- Consider y-axis  -----------------------
    ax.yaxis.set_major_locator(MultipleLocator(2.5))
    ax.tick_params(axis='y', which='major', labelsize= 20, length=8, width=2)
    
    
# figsize = (10,10)   
# fig1, (ax1,ax2,ax3) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# # fig1.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig1.text(0.13,0.85, "Middle Node", color = "black", fontsize=25)

# fig1.text(0.02,0.5, 'Peak Velocity Error '+ r"$\ E_{Max}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=28)
# fig1.text(0.45,0.040, r'$\Delta_c/\lambda$', va= 'center', fontsize=25)

# ax1 = plt.subplot(311)
# DifferTime_RelativeError2(Tie20_Perr, Type1_W20_Perr, Type2_W20_Perr, Type3_W20_Perr, Tie20_Serr, Type1_W20_Serr, Type2_W20_Serr, Type3_W20_Serr)
# ax1.set_title(r"$w=$ $\mathrm{20m}$",fontsize =25, x=0.12, y=0.65)

# ax2 = plt.subplot(312)
# DifferTime_RelativeError2(Tie10_Perr, Type1_W10_Perr, Type2_W10_Perr, Type3_W10_Perr, Tie10_Serr, Type1_W10_Serr, Type2_W10_Serr, Type3_W10_Serr)
# ax2.set_title(r"$w=$ $\mathrm{10m}$",fontsize =25, x=0.12, y=0.80)

# ax3 = plt.subplot(313)
# DifferTime_RelativeError2(Tie2_Perr, Type1_W2_Perr, Type2_W2_Perr, Type3_W2_Perr, Tie2_Serr, Type1_W2_Serr, Type2_W2_Serr, Type3_W2_Serr)
# ax3.set_title(r"$w=$ $\mathrm{2m}$",fontsize =25, x=0.12, y=0.80)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting
# legend_elements = [Line2D([0], [0], color='crimson', lw=2, label= f'P wave'),
#                 Line2D([0], [0], color='dimgrey', lw=2, label='S wave'),]

# legend_elements2 =  [Line2D([0], [0], color='black',marker = '^',markersize=marksize,markerfacecolor = 'none', label= 'Tie'),
#                     Line2D([0], [0], color='black',marker = 'o',markersize=marksize,markerfacecolor = 'none', label= 'Beam-based'),
#                     Line2D([0], [0], color='black',marker = '<',markersize=marksize,markerfacecolor = 'none', label= 'Hybrid'),
#                     Line2D([0], [0], color='black',marker = 's',markersize=marksize,markerfacecolor = 'none', label= 'Node-based')]

# lines, labels = fig1.axes[-1].get_legend_handles_labels()
# legend1 = fig1.legend(handles=legend_elements, loc=(0.30, 0.90) ,prop=font_props) # , title="Legend 1"
# legend1.get_frame().set_edgecolor('grey')
# legend1.get_frame().set_linewidth(2)  # 設置外框寬度
# fig1.add_artist(legend1)

# legend2 = fig1.legend(handles=legend_elements2, loc=(0.50, 0.85) ,prop=font_props)
# legend2.get_frame().set_edgecolor('grey')
# legend2.get_frame().set_linewidth(2)  # 設置外框寬度

# ==================Draw Relative error : td =============================
def DifferTime_RelativeError(TiePErr, Type1PErr, Type2PErr, Type3PErr, TieSErr, Type1SErr, Type2SErr, Type3SErr):
    # ------------ P wave --------------------------
    plt.plot(TiePErr[:,0], TiePErr[:,1],marker = '^',markersize=16,markerfacecolor = 'white',label = 'Tie', color = 'red', linewidth = 3.0)
    # plt.plot(LKErr[:,0], LKErr[:,Peak],marker = 'p',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot')
    plt.plot(Type1PErr[:,0], Type1PErr[:,1],marker = 'o',markersize=12,markerfacecolor = 'white',label = 'Beam-based', color = 'red', linewidth = 3.0)
    plt.plot(Type2PErr[:,0], Type2PErr[:,1],marker = '<',markersize=8,markerfacecolor = 'white',label = 'Hybrid', color = 'red', linewidth = 3.0)
    plt.plot(Type3PErr[:,0], Type3PErr[:,1],marker = 's',markersize=6,markerfacecolor = 'white',label = 'Node-based', color = 'red', linewidth = 3.0)
    
 # ----------------S wave------------------------------
    plt.plot(TieSErr[:,0], TieSErr[:,1],marker = '^',markersize=16,markerfacecolor = 'white', color = 'darkgrey', linewidth = 3.0)
    # plt.plot(Dy_lamb_Swave[:,0], LKErr[:,1],marker = 'p',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot')
    plt.plot(Type1SErr[:,0], Type1SErr[:,1],marker = 'p',markersize=12,markerfacecolor = 'white', color = 'darkgrey', linewidth = 3.0) # , ls = '--'
    plt.plot(Type2SErr[:,0], Type2SErr[:,1],marker = '<',markersize=8,markerfacecolor = 'white', color = 'darkgrey', linewidth = 3.0) # , ls =':'
    plt.plot(Type3SErr[:,0], Type3SErr[:,1],marker = 's',markersize=6,markerfacecolor = 'white', color = 'darkgrey', linewidth = 3.0) # , ls = '-.'
 
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)

    # plt.ylim(0, 5.0) 
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
    ax.tick_params(axis='x', which='both', labelsize=17)

# figsize = (10,10)   
# fig2, (ax4,ax5,ax6) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# # fig1.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig2.text(0.70,0.82, "Middle Node", color = "black", fontsize=25)

# fig2.text(0.02,0.5, 'Peak Velocity Error '+ r"$\ E_{Max}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=25)
# fig2.text(0.45,0.060, f'Duration ' + r'$t_d$', va= 'center', fontsize=25)

# ax4 = plt.subplot(311)
# DifferTime_RelativeError(Tie20_Perr, Type1_W20_Perr, Type2_W20_Perr, Type3_W20_Perr, Tie20_Serr, Type1_W20_Serr, Type2_W20_Serr, Type3_W20_Serr)
# ax4.set_title(r"$w=$ $\mathrm{20m}$",fontsize =25, x=0.85, y=0.55)

# ax5 = plt.subplot(312)
# DifferTime_RelativeError(Tie10_Perr, Type1_W10_Perr, Type2_W10_Perr, Type3_W10_Perr, Tie10_Serr, Type1_W10_Serr, Type2_W10_Serr, Type3_W10_Serr)
# ax5.set_title(r"$w=$ $\mathrm{10m}$",fontsize =25, x=0.85, y=0.80)

# ax6 = plt.subplot(313)
# DifferTime_RelativeError(Tie2_Perr, Type1_W2_Perr, Type2_W2_Perr, Type3_W2_Perr, Tie2_Serr, Type1_W2_Serr, Type2_W2_Serr, Type3_W2_Serr)
# ax6.set_title(r"$w=$ $\mathrm{2m}$",fontsize =25, x=0.85, y=0.80)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting
# legend_elements = [Line2D([0], [0], color='red', lw=2, label= f'P wave'),
#                 Line2D([0], [0], color='darkgrey', lw=2, label='S wave'),]

# legend_elements2 =  [Line2D([0], [0], color='black',marker = '^',markersize=16,markerfacecolor = 'white', label= 'Tie'),
#                     Line2D([0], [0], color='black',marker = 'o',markersize=12,markerfacecolor = 'white', label= 'Beam-based'),
#                     Line2D([0], [0], color='black',marker = '<',markersize=8,markerfacecolor = 'white', label= 'Hybrid'),
#                     Line2D([0], [0], color='black',marker = 's',markersize=6,markerfacecolor = 'white', label= 'Node-based')]

# lines, labels = fig2.axes[-1].get_legend_handles_labels()
# legend1 = fig2.legend(handles=legend_elements, loc=(0.30, 0.90) ,prop=font_props) # , title="Legend 1"
# fig2.add_artist(legend1)

# legend2 = fig2.legend(handles=legend_elements2, loc=(0.50, 0.85) ,prop=font_props)

# ================= Calculate_2NormError Normalization ===============================
Theory_PTime = total_Ptime_HZ80
Analysis_PTime = Tie_W20_HZ40_P[:,0]

Theory_STime = total_Stime_HZ80
Analysis_STime = Tie_W20_HZ40_S[:,0]

def Calculate_RelativeL2norm(column_index, TheoryTime, Pwave, Analysis_Time, Tie_W20_HZ40_Mid, time_range=(0, 0.20)):
# ------------------------- L-2 Norm Error ------------------------
    common80 = set(TheoryTime) & set(Analysis_Time)
    filtered_common80 = [value for value in common80 if time_range[0] <= value <= time_range[1]]
    
    differences = []
    Mom = []

    for common_value in common80:
        index1 = np.where(Analysis_Time == common_value)[0][0]
        index2 = np.where(TheoryTime == common_value)[0][0]

        diff = (Tie_W20_HZ40_Mid[index1, column_index] - Pwave[index2, Analysis_Column])
        differences.append(diff)
        
        Mother =  Pwave[index2, Analysis_Column]
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

def Add_PErr(MidTieErr20,Tie20_error, Tie_W20_HZ10_P, Tie_W20_HZ20_P, Tie_W20_HZ40_P, Tie_W20_HZ80_P):
    MidTieErr20[:,0] = Tie20_error[:,0] 
# ===================================== Calculate_L2NormError Normalization ============================================================
    MidTieErr20[0,1], MidTieErr20[0,2] = Calculate_RelativeL2norm(Pcolumn_index, Theory_PTime,HZ10_Pwave, Analysis_PTime,Tie_W20_HZ10_P, time_range=(0, 0.20))
    MidTieErr20[1,1], MidTieErr20[1,2] = Calculate_RelativeL2norm(Pcolumn_index, Theory_PTime,HZ20_Pwave, Analysis_PTime,Tie_W20_HZ20_P, time_range=(0, 0.20))
    MidTieErr20[2,1], MidTieErr20[2,2] = Calculate_RelativeL2norm(Pcolumn_index, Theory_PTime,HZ40_Pwave, Analysis_PTime,Tie_W20_HZ40_P, time_range=(0, 0.20))
    MidTieErr20[3,1], MidTieErr20[3,2] = Calculate_RelativeL2norm(Pcolumn_index, Theory_PTime,HZ80_Pwave, Analysis_PTime,Tie_W20_HZ80_P, time_range=(0, 0.20))

# -------------- W = 20m-------------------------------
Tie20Err_PL2 = np.zeros((4,3))
Add_PErr(Tie20Err_PL2, Tie20_Perror, Tie_W20_HZ10_P, Tie_W20_HZ20_P, Tie_W20_HZ40_P, Tie_W20_HZ80_P)

LK20Err_PL2 = np.zeros((4,3))
Add_PErr(LK20Err_PL2, LK20_Perror, LK_W20_HZ10_P, LK_W20_HZ20_P, LK_W20_HZ40_P, LK_W20_HZ80_P)

Type1_W20Err_PL2 = np.zeros((4,3))
Add_PErr(Type1_W20Err_PL2, Type1_P20error, Type1_W20_HZ10_P, Type1_W20_HZ20_P, Type1_W20_HZ40_P, Type1_W20_HZ80_P)

Type2_W20Err_PL2 = np.zeros((4,3))
Add_PErr(Type2_W20Err_PL2, Type2_P20error, Type2_W20_HZ10_P, Type2_W20_HZ20_P, Type2_W20_HZ40_P, Type2_W20_HZ80_P)

Type3_W20Err_PL2 = np.zeros((4,3))
Add_PErr(Type3_W20Err_PL2, Type3_P20error, Type3_W20_HZ10_P, Type3_W20_HZ20_P, Type3_W20_HZ40_P, Type3_W20_HZ80_P)

# -------------- W = 10m-------------------------------
Tie10Err_PL2 = np.zeros((4,3))
Add_PErr(Tie10Err_PL2,Tie10_Perror, Tie_W10_HZ10_P, Tie_W10_HZ20_P, Tie_W10_HZ40_P, Tie_W10_HZ80_P)

LK10Err_PL2 = np.zeros((4,3))
Add_PErr(LK10Err_PL2,LK10_Perror, LK_W10_HZ10_P, LK_W10_HZ20_P, LK_W10_HZ40_P, LK_W10_HZ80_P)

Type1_W10Err_PL2 = np.zeros((4,3))
Add_PErr(Type1_W10Err_PL2, Type1_P10error, Type1_W10_HZ10_P, Type1_W10_HZ20_P, Type1_W10_HZ40_P, Type1_W10_HZ80_P)

Type2_W10Err_PL2 = np.zeros((4,3))
Add_PErr(Type2_W10Err_PL2, Type2_P10error, Type2_W10_HZ10_P, Type2_W10_HZ20_P, Type2_W10_HZ40_P, Type2_W10_HZ80_P)

Type3_W10Err_PL2 = np.zeros((4,3))
Add_PErr(Type3_W10Err_PL2, Type3_P10error, Type3_W10_HZ10_P, Type3_W10_HZ20_P, Type3_W10_HZ40_P, Type3_W10_HZ80_P)

# -------------- W = 2m-------------------------------
Tie2Err_PL2 = np.zeros((4,3))
Add_PErr(Tie2Err_PL2,Tie2_Perror, Tie_W2_HZ10_P, Tie_W2_HZ20_P, Tie_W2_HZ40_P, Tie_W2_HZ80_P)

LK2Err_PL2 = np.zeros((4,3))
Add_PErr(LK2Err_PL2, LK2_Perror, LK_W2_HZ10_P, LK_W2_HZ20_P, LK_W2_HZ40_P, LK_W2_HZ80_P)

Type1_W2Err_PL2 = np.zeros((4,3))
Add_PErr(Type1_W2Err_PL2, Type1_P2error, Type1_W2_HZ10_P, Type1_W2_HZ20_P, Type1_W2_HZ40_P, Type1_W2_HZ80_P)

Type2_W2Err_PL2 = np.zeros((4,3))
Add_PErr(Type2_W2Err_PL2, Type2_P2error, Type2_W2_HZ10_P, Type2_W2_HZ20_P, Type2_W2_HZ40_P, Type3_W2_HZ80_P)

Type3_W2Err_PL2 = np.zeros((4,3))
Add_PErr(Type3_W2Err_PL2, Type3_P2error, Type3_W2_HZ10_P, Type3_W2_HZ20_P, Type3_W2_HZ40_P, Type3_W2_HZ80_P)

def Add_SErr(MidTieErr20,Tie20_error, Tie_W20_HZ10_S, Tie_W20_HZ20_S, Tie_W20_HZ40_S, Tie_W20_HZ80_S):
    MidTieErr20[:,0] = Tie20_error[:,0] 
# ===================================== Calculate_L2NormError Normalization ============================================================
    MidTieErr20[0,1], MidTieErr20[0,2] = Calculate_RelativeL2norm(Scolumn_index, Theory_STime,HZ10_Swave, Analysis_STime,Tie_W20_HZ10_S, time_range=(0, 0.20))
    MidTieErr20[1,1], MidTieErr20[1,2] = Calculate_RelativeL2norm(Scolumn_index, Theory_STime,HZ20_Swave, Analysis_STime,Tie_W20_HZ20_S, time_range=(0, 0.20))
    MidTieErr20[2,1], MidTieErr20[2,2] = Calculate_RelativeL2norm(Scolumn_index, Theory_STime,HZ40_Swave, Analysis_STime,Tie_W20_HZ40_S, time_range=(0, 0.20))
    MidTieErr20[3,1], MidTieErr20[3,2] = Calculate_RelativeL2norm(Scolumn_index, Theory_STime,HZ80_Swave, Analysis_STime,Tie_W20_HZ80_S, time_range=(0, 0.20))
    
# -------------- W = 20m-------------------------------
Tie20Err_SL2 = np.zeros((4,3))
Add_SErr(Tie20Err_SL2,Tie20_Serror, Tie_W20_HZ10_S, Tie_W20_HZ20_S, Tie_W20_HZ40_S, Tie_W20_HZ80_S)

LK20Err_SL2 = np.zeros((4,3))
Add_SErr(LK20Err_SL2,LK20_Serror, LK_W20_HZ10_S, LK_W20_HZ20_S, LK_W20_HZ40_S, LK_W20_HZ80_S)

Type1_W20Err_SL2 = np.zeros((4,3))
Add_SErr(Type1_W20Err_SL2, Type1_S20error, Type1_W20_HZ10_S, Type1_W20_HZ20_S, Type1_W20_HZ40_S, Type1_W20_HZ80_S)

Type2_W20Err_SL2 = np.zeros((4,3))
Add_SErr(Type2_W20Err_SL2, Type2_S20error, Type2_W20_HZ10_S, Type2_W20_HZ20_S, Type2_W20_HZ40_S, Type2_W20_HZ80_S)

Type3_W20Err_SL2 = np.zeros((4,3))
Add_SErr(Type3_W20Err_SL2, Type3_S20error, Type3_W20_HZ10_S, Type3_W20_HZ20_S, Type3_W20_HZ40_S, Type3_W20_HZ80_S)

# -------------- W = 10m-------------------------------
Tie10Err_SL2 = np.zeros((4,3))
Add_SErr(Tie10Err_SL2,Tie10_Serror, Tie_W10_HZ10_S, Tie_W10_HZ20_S, Tie_W10_HZ40_S, Tie_W10_HZ80_S)

LK10Err_SL2 = np.zeros((4,3))
Add_SErr(LK10Err_SL2,LK10_Serror, LK_W10_HZ10_S, LK_W10_HZ20_S, LK_W10_HZ40_S, LK_W10_HZ80_S)

Type1_W10Err_SL2 = np.zeros((4,3))
Add_SErr(Type1_W10Err_SL2, Type1_S10error, Type1_W10_HZ10_S, Type1_W10_HZ20_S, Type1_W10_HZ40_S, Type1_W10_HZ80_S)

Type2_W10Err_SL2 = np.zeros((4,3))
Add_SErr(Type2_W10Err_SL2, Type2_S10error, Type2_W10_HZ10_S, Type2_W10_HZ20_S, Type2_W10_HZ40_S, Type2_W10_HZ80_S)

Type3_W10Err_SL2 = np.zeros((4,3))
Add_SErr(Type3_W10Err_SL2, Type3_S10error, Type3_W10_HZ10_S, Type3_W10_HZ20_S, Type3_W10_HZ40_S, Type3_W10_HZ80_S)

# -------------- W = 2m-------------------------------
Tie2Err_SL2 = np.zeros((4,3))
Add_SErr(Tie2Err_SL2,Tie2_Serror, Tie_W2_HZ10_S, Tie_W2_HZ20_S, Tie_W2_HZ40_S, Tie_W2_HZ80_S)

LK2Err_SL2 = np.zeros((4,3))
Add_SErr(LK2Err_SL2,LK2_Serror, LK_W2_HZ10_S, LK_W2_HZ20_S, LK_W2_HZ40_S, LK_W2_HZ80_S)

Type1_W2Err_SL2 = np.zeros((4,3))
Add_SErr(Type1_W2Err_SL2, Type1_S2error, Type1_W2_HZ10_S, Type1_W2_HZ20_S, Type1_W2_HZ40_S, Type1_W2_HZ80_S)

Type2_W2Err_SL2 = np.zeros((4,3))
Add_SErr(Type2_W2Err_SL2, Type2_S2error, Type2_W2_HZ10_S, Type2_W2_HZ20_S, Type2_W2_HZ40_S, Type3_W2_HZ80_S)

Type3_W2Err_SL2 = np.zeros((4,3))
Add_SErr(Type3_W2Err_SL2, Type3_S2error, Type3_W2_HZ10_S, Type3_W2_HZ20_S, Type3_W2_HZ40_S, Type3_W2_HZ80_S)

# ==================Draw L2 Norm error : Middele point (WaveLength = Dy/Lamb) =============================
def DifferTime_L2Error(TiePErr, Type1PErr, Type2PErr, Type3PErr, TieSErr, Type1SErr, Type2SErr, Type3SErr):
 # ------------ P wave --------------------------
    plt.plot(Dy_lamb_Pwave[:], TiePErr[:,1],marker = '^',markersize=marksize,markerfacecolor = 'none',label = 'Tie', color = 'crimson', linewidth = 3.0)
    # plt.plot(Dy_lamb_Pwave[:,0], LKErr[:,Peak],marker = 'p',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot')
    plt.plot(Dy_lamb_Pwave[:], Type1PErr[:,1],marker = 'o',markersize=marksize,markerfacecolor = 'none',label = 'Beam_Base', color = 'crimson', linewidth = 3.0)
    plt.plot(Dy_lamb_Pwave[:], Type2PErr[:,1],marker = '<',markersize=marksize,markerfacecolor = 'none',label = 'Hybrid', color = 'crimson', linewidth = 3.0)
    plt.plot(Dy_lamb_Pwave[:], Type3PErr[:,1],marker = 's',markersize=marksize,markerfacecolor = 'none',label = 'Node_Base', color = 'crimson', linewidth = 3.0)
       
    # ----------------S wave------------------------------
    plt.plot(Dy_lamb_Swave[:], TieSErr[:,1],marker = '^',markersize=marksize,markerfacecolor = 'none', color = 'dimgrey', linewidth = 3.0)
    # plt.plot(Dy_lamb_Swave[:,0], LKErr[:,1],marker = 'p',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot')
    plt.plot(Dy_lamb_Swave[:], Type1SErr[:,1],marker = 'o',markersize=marksize,markerfacecolor = 'none', color = 'dimgrey', linewidth = 3.0) # , ls = '--'
    plt.plot(Dy_lamb_Swave[:], Type2SErr[:,1],marker = '<',markersize=marksize,markerfacecolor = 'none', color = 'dimgrey', linewidth = 3.0) # , ls =':'
    plt.plot(Dy_lamb_Swave[:], Type3SErr[:,1],marker = 's',markersize=marksize,markerfacecolor = 'none', color = 'dimgrey', linewidth = 3.0) # , ls = '-.'

    plt.xticks(fontsize = 18, fontweight='bold', color='black')
    plt.yticks(fontsize = 18, fontweight='bold', color='black')

    # plt.xlim(0.0, 0.20)
    # plt.grid(True)
    # ========== set up figure thick ============================
    bwidth = 2
    TK = plt.gca()
    TK.spines['bottom'].set_linewidth(bwidth)
    TK.spines['left'].set_linewidth(bwidth)
    TK.spines['top'].set_linewidth(bwidth)
    TK.spines['right'].set_linewidth(bwidth)
    
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
    ax.tick_params(axis='x', which='minor', length=4, width=2, color='gray')
    
    ax.set_xticklabels([f'{tick:.2f}' for tick in x_ticks_Num], rotation=0, fontsize=5)
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='major', labelsize= 20, length=8, width=2)
    # -------------- Consider Y-axis  -----------------------
    ax.set_yscale('log', base=10)
    ax.set_yticks([], minor=False)
    ax.set_yticks([], minor=True)
    y_ticks_Num = np.array([0.02, 0.04, 0.08, 0.20, 0.40, 0.60]) # 0.02, 0.04, 0.06, 0.08, 0.20, 0.40, 0.60
    ax.set_yticks(y_ticks_Num)
    ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks_Num], rotation=0, fontsize=12)
    ax.tick_params(axis='y', which='major', labelsize= 20, length=8, width=2)
    # ------- Miner ticks -----------------
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='y', which='minor', length=4, width=2, color='gray')
    
figsize = (10,10)   
fig3, (ax7,ax8,ax9) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# fig3.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
fig3.text(0.13,0.85, "Middle Node", color = "black", fontsize=25)

fig3.text(0.01,0.5, 'Normalized L2 Norm Error '+ r"$\ E_{L2}$", va= 'center', rotation= 'vertical', fontsize=28)
fig3.text(0.45,0.030, r'$\Delta_c/\lambda$', va= 'center', fontsize=25)

ax7 = plt.subplot(311)
DifferTime_L2Error(Tie20Err_PL2, Type1_W20Err_PL2, Type2_W20Err_PL2, Type3_W20Err_PL2, Tie20Err_SL2, Type1_W20Err_SL2, Type2_W20Err_SL2, Type3_W20Err_SL2)
ax7.set_title(r"$w=$ $\mathrm{20m}$",fontsize =25, x=0.12, y=0.70)

ax8 = plt.subplot(312)
DifferTime_L2Error(Tie10Err_PL2, Type1_W10Err_PL2, Type2_W10Err_PL2, Type3_W10Err_PL2, Tie10Err_SL2, Type1_W10Err_SL2, Type2_W10Err_SL2, Type3_W10Err_SL2)
ax8.set_title(r"$w=$ $\mathrm{10m}$",fontsize =25, x=0.12, y=0.80)

ax9 = plt.subplot(313)
DifferTime_L2Error(Tie2Err_PL2, Type1_W2Err_PL2, Type2_W2Err_PL2, Type3_W2Err_PL2, Tie2Err_SL2, Type1_W2Err_SL2, Type2_W2Err_SL2, Type3_W2Err_SL2)
ax9.set_title(r"$w=$ $\mathrm{2m}$",fontsize =25, x=0.12, y=0.80)

font_props = {'family': 'Arial', 'size': 17}  #Legend Setting
legend_elements = [Line2D([0], [0], color='crimson', lw=2, label= f'P wave'),
                Line2D([0], [0], color='dimgrey', lw=2, label='S wave'),]

legend_elements2 =  [Line2D([0], [0], color='black',marker = '^',markersize=marksize,markerfacecolor = 'none', label= 'Tie'),
                    Line2D([0], [0], color='black',marker = 'o',markersize=marksize,markerfacecolor = 'none', label= 'Beam-based'),
                    Line2D([0], [0], color='black',marker = '<',markersize=marksize,markerfacecolor = 'none', label= 'Hybrid'),
                    Line2D([0], [0], color='black',marker = 's',markersize=marksize,markerfacecolor = 'none', label= 'Node-based')]

lines, labels = fig3.axes[-1].get_legend_handles_labels()
legend1 = fig3.legend(handles=legend_elements, loc=(0.30, 0.90) ,prop=font_props) # , title="Legend 1"
legend1.get_frame().set_edgecolor('grey')
legend1.get_frame().set_linewidth(2)  # 設置外框寬度
fig3.add_artist(legend1)

legend2 = fig3.legend(handles=legend_elements2, loc=(0.50, 0.85) ,prop=font_props)
legend2.get_frame().set_edgecolor('grey')
legend2.get_frame().set_linewidth(2)  # 設置外框寬度

# ==================Draw L2 Norm error : Middele point (td) =============================
def DifferTime_L2Error2(TiePErr, Type1PErr, Type2PErr, Type3PErr, TieSErr, Type1SErr, Type2SErr, Type3SErr):
 # ------------ P wave --------------------------
    plt.plot(TiePErr[:,0], TiePErr[:,1],marker = '^',markersize=16,markerfacecolor = 'white',label = 'Tie', color = 'red', linewidth = 3.0)
    # plt.plot(Dy_lamb_Pwave[:,0], LKErr[:,Peak],marker = 'p',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot')
    plt.plot(Type1PErr[:,0], Type1PErr[:,1],marker = 'o',markersize=12,markerfacecolor = 'white',label = 'Beam_Base', color = 'red', linewidth = 3.0)
    plt.plot(Type2PErr[:,0], Type2PErr[:,1],marker = '<',markersize=8,markerfacecolor = 'white',label = 'Hybrid', color = 'red', linewidth = 3.0)
    plt.plot(Type3PErr[:,0], Type3PErr[:,1],marker = 's',markersize=6,markerfacecolor = 'white',label = 'Node_Base', color = 'red', linewidth = 3.0)
       
    # ----------------S wave------------------------------
    plt.plot(TieSErr[:,0], TieSErr[:,1],marker = '^',markersize=16,markerfacecolor = 'white', color = 'darkgrey', linewidth = 3.0)
    # plt.plot(Dy_lamb_Swave[:,0], LKErr[:,1],marker = 'p',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot')
    plt.plot(Type1SErr[:,0], Type1SErr[:,1],marker = 'o',markersize=12,markerfacecolor = 'white', color = 'darkgrey', linewidth = 3.0) # , ls = '--'
    plt.plot(Type2SErr[:,0], Type2SErr[:,1],marker = '<',markersize=8,markerfacecolor = 'white', color = 'darkgrey', linewidth = 3.0) # , ls =':'
    plt.plot(Type3SErr[:,0], Type3SErr[:,1],marker = 's',markersize=6,markerfacecolor = 'white', color = 'darkgrey', linewidth = 3.0) # , ls = '-.'

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
    ax.set_yscale('log', base=10)
    ax.set_yticks([], minor=False)
    ax.set_yticks([], minor=True)
    y_ticks_Num = np.array([0.02, 0.04, 0.06, 0.08, 0.20, 0.40, 0.60])
    ax.set_yticks(y_ticks_Num)
    ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks_Num], rotation=0, fontsize=12)
    ax.tick_params(axis='y', which='both', labelsize=17)
    # ------- Miner ticks -----------------
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='y', which='minor', length=4, color='gray')
    
# figsize = (10,10)   
# fig4, (ax10,ax11,ax12) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# # fig4.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig4.text(0.70,0.82, "Middle Node", color = "black", fontsize=25)

# fig4.text(0.01,0.5, 'Normalized L2 Norm Error '+ r"$\ E_{L2}$", va= 'center', rotation= 'vertical', fontsize=25)
# fig4.text(0.45,0.060, f'Duration ' + r'$t_d$', va= 'center', fontsize=22)

# ax10 = plt.subplot(311)
# DifferTime_L2Error2(Tie20Err_PL2, Type1_W20Err_PL2, Type2_W20Err_PL2, Type3_W20Err_PL2, Tie20Err_SL2, Type1_W20Err_SL2, Type2_W20Err_SL2, Type3_W20Err_SL2)
# ax10.set_title(r"$w=$ $\mathrm{20m}$",fontsize =25, x=0.85, y=0.55)

# ax11 = plt.subplot(312)
# DifferTime_L2Error2(Tie10Err_PL2, Type1_W10Err_PL2, Type2_W10Err_PL2, Type3_W10Err_PL2, Tie10Err_SL2, Type1_W10Err_SL2, Type2_W10Err_SL2, Type3_W10Err_SL2)
# ax11.set_title(r"$w=$ $\mathrm{10m}$",fontsize =25, x=0.85, y=0.80)

# ax12 = plt.subplot(313)
# DifferTime_L2Error2(Tie2Err_PL2, Type1_W2Err_PL2, Type2_W2Err_PL2, Type3_W2Err_PL2, Tie2Err_SL2, Type1_W2Err_SL2, Type2_W2Err_SL2, Type3_W2Err_SL2)
# ax12.set_title(r"$w=$ $\mathrm{2m}$",fontsize =25, x=0.85, y=0.80)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting
# legend_elements = [Line2D([0], [0], color='red', lw=2, label= f'P wave'),
#                 Line2D([0], [0], color='darkgrey', lw=2, label='S wave'),]

# legend_elements2 =  [Line2D([0], [0], color='black',marker = '^',markersize=16,markerfacecolor = 'white', label= 'Tie'),
#                     Line2D([0], [0], color='black',marker = 'o',markersize=12,markerfacecolor = 'white', label= 'Beam-based'),
#                     Line2D([0], [0], color='black',marker = '<',markersize=8,markerfacecolor = 'white', label= 'Hybrid'),
#                     Line2D([0], [0], color='black',marker = 's',markersize=6,markerfacecolor = 'white', label= 'Node-based')]

# lines, labels = fig4.axes[-1].get_legend_handles_labels()
# legend1 = fig4.legend(handles=legend_elements, loc=(0.30, 0.90) ,prop=font_props) # , title="Legend 1"
# fig4.add_artist(legend1)

# legend2 = fig4.legend(handles=legend_elements2, loc=(0.50, 0.85) ,prop=font_props)
