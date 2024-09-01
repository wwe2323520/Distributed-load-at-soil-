# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:50:48 2024

@author: User
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

def Incoming_wave(w, x, cp, t):  #事實上為（xi,yi,t），空間跟時間資訊全寫進去，目前只用到yi的空間
    return np.sin(w*(x-cp*t)) # Normal：np.sin(w*(x-cs*t))

def Outgoing_wave(w, x, cp, t):
    return np.sin(w*(x+cp*t)) # Norrmal： np.sin(w*(x+cs*t))


def Cal_Theory(fp_HZ, Pwave_HZ):
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
                
            if total_time[t] >= 0.025 and total_time[t] < (0.025+Input_Time):
                Pwave[to+t,End_Ele-g] = Pwave[to+t,End_Ele-g] + Cp_vel_Coefficient*XIn[t-to,End_Ele-g]   # XOut[t-to,End_Ele-g
    return L, Pwave, total_time

lamb10, HZ10_Pwave, total_time_HZ10 = Cal_Theory(fp_10HZ, wp_10HZ)
lamb20, HZ20_Pwave, total_time_HZ20 = Cal_Theory(fp_20HZ, wp_20HZ)
lamb40, HZ40_Pwave, total_time_HZ40 = Cal_Theory(fp_40HZ, wp_40HZ)
lamb80, HZ80_Pwave, total_time_HZ80 = Cal_Theory(fp_80HZ, wp_80HZ)

Analysis_Column = Nele-1
def CompareDt_DiffVel(titleName, total_time_HZ10,HZ10_Pwave, total_time_HZ20,HZ20_Pwave, total_time_HZ40,HZ40_Pwave, total_time_HZ80,HZ80_Pwave):
    plt.figure(figsize=(10,8))
    plt.title(titleName, fontsize = 25)
    #  ------------------- Theory ------------------------------
    plt.plot(total_time_HZ10[:], HZ10_Pwave[:, Analysis_Column], label = r'$\lambda_{10} = \mathrm{40m}$ $(\mathrm{10HZ})$', color= 'limegreen', linewidth = 6.0) # , ls = '--' 
    plt.plot(total_time_HZ20[:], HZ20_Pwave[:, Analysis_Column], label = r'$\lambda_{20} = \mathrm{20m}$ $(\mathrm{20HZ})$', color= 'orange', ls = '-.',  linewidth = 5.0) # , ls = '-.'
    plt.plot(total_time_HZ40[:], HZ40_Pwave[:, Analysis_Column], label = r'$\lambda_{40} = \mathrm{10m}$ $(\mathrm{40HZ})$', color= 'purple', linewidth = 4.0) # , ls = ':'
    plt.plot(total_time_HZ80[:], HZ80_Pwave[:, Analysis_Column], label = r'$\lambda_{80} = \mathrm{5m}$ $(\mathrm{80HZ})$', color= 'red',  linewidth = 3.0) # , ls = '-.'
    
    plt.grid(True)
    plt.legend(loc='lower right',fontsize=18)
    
    plt.xlim(0, 0.2)
    plt.ylim(-0.75, 0.75)
    
    plt.xlabel(r"$\mathrm {time}$ ${t}$ $\mathrm {(s)}$", fontsize = 25) # r"$G^{'}/G$"
    plt.ylabel(r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", fontsize = 25)  # r"$m_{x'}/m_{x}$"
    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 18)
    
    ax = plt.gca()
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
    ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    ax.yaxis.get_offset_text().set(size=20)
    
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.025))
    ax.xaxis.get_offset_text().set(size=20)
    
# CompareDt_DiffVel(f'Different Frequency', total_time_HZ10,HZ10_Pwave, total_time_HZ20,HZ20_Pwave, total_time_HZ40,HZ40_Pwave, total_time_HZ80,HZ80_Pwave)

# ====================== Read File From Numerical ==================================
# soilwidth = int(2.0)
# ny = int(40) # 80, 40, 20. 10
# HZ = 20
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
        
        # # print('================ Middle Left And Right 1m Node ====================')
        # Top_CenterLeft = UpperN_Center - int(1.0/Dw)
        # Top_CenterRight = UpperN_Center + int(1.0/Dw)
        # # print(f'Top_CenterLeft Node = {Top_CenterLeft}; Top_CenterRight Node = {Top_CenterRight}')
        
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
# ---------- Consider Mesh = 40 row ----------------------------------
W2_Mid40row = Find_Middle(int(2.0), YMesh)
W10_Mid40row = Find_Middle(int(10.0), YMesh)
W20_Mid40row = Find_Middle(int(20.0), YMesh)

Wave_Choose = f'1D_Transport/Newmark_Linear/Pwave'
# ----------------- f = 10HZ --------------------------------
HZ10 = f'HZ_10'
# ============================ SoilWidth = 2.0 m (HZ = 10)=======================================
Condition1 = f'{Wave_Choose}/W_2m/{HZ10}'
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

Tie_W2_HZ10_Mid = rdnumpy(file1)
LK_W2_HZ10_Mid = rdnumpy(file2)
Type1_W2_HZ10_Mid = rdnumpy(file3)
Type2_W2_HZ10_Mid = rdnumpy(file4)
Type3_W2_HZ10_Mid = rdnumpy(file5)

# ============================ SoilWidth = 10.0 m (HZ = 10)=======================================
Condition2 = f'{Wave_Choose}/W_10m/{HZ10}'
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

Tie_W10_HZ10_Mid = rdnumpy(file6)
LK_W10_HZ10_Mid = rdnumpy(file7)
Type1_W10_HZ10_Mid = rdnumpy(file8)
Type2_W10_HZ10_Mid = rdnumpy(file9)
Type3_W10_HZ10_Mid = rdnumpy(file10)

# ============================ SoilWidth = 20.0 m (HZ = 10)=======================================
Condition3 = f'{Wave_Choose}/W_20m/{HZ10}'
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

Tie_W20_HZ10_Mid = rdnumpy(file11)
LK_W20_HZ10_Mid = rdnumpy(file12)
Type1_W20_HZ10_Mid = rdnumpy(file13)
Type2_W20_HZ10_Mid = rdnumpy(file14)
Type3_W20_HZ10_Mid = rdnumpy(file15)

# ----------------- f = 20HZ --------------------------------
HZ20 = f'HZ_20'
# ============================ SoilWidth = 2.0 m (HZ = 20)=======================================
Condition4 = f'{Wave_Choose}/W_2m/{HZ20}'
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

Tie_W2_HZ20_Mid = rdnumpy(file16)
LK_W2_HZ20_Mid = rdnumpy(file17)
Type1_W2_HZ20_Mid = rdnumpy(file18)
Type2_W2_HZ20_Mid = rdnumpy(file19)
Type3_W2_HZ20_Mid = rdnumpy(file20)
# ============================ SoilWidth = 10.0 m (HZ = 20)=======================================
Condition5 = f'{Wave_Choose}/W_10m/{HZ20}'
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

Tie_W10_HZ20_Mid = rdnumpy(file21)
LK_W10_HZ20_Mid = rdnumpy(file22)
Type1_W10_HZ20_Mid = rdnumpy(file23)
Type2_W10_HZ20_Mid = rdnumpy(file24)
Type3_W10_HZ20_Mid = rdnumpy(file25)
# ============================ SoilWidth = 20.0 m (HZ = 20)=======================================
Condition6 = f'{Wave_Choose}/W_20m/{HZ20}'
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

Tie_W20_HZ20_Mid = rdnumpy(file26)
LK_W20_HZ20_Mid = rdnumpy(file27)
Type1_W20_HZ20_Mid = rdnumpy(file28)
Type2_W20_HZ20_Mid = rdnumpy(file29)
Type3_W20_HZ20_Mid = rdnumpy(file30)

# ----------------- f = 40HZ --------------------------------
HZ40 = f'HZ_40'
# ============================ SoilWidth = 2.0 m (HZ = 40)=======================================
Condition7 = f'{Wave_Choose}/W_2m/{HZ40}'
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

Tie_W2_HZ40_Mid = rdnumpy(file31)
LK_W2_HZ40_Mid = rdnumpy(file32)
Type1_W2_HZ40_Mid = rdnumpy(file33)
Type2_W2_HZ40_Mid = rdnumpy(file34)
Type3_W2_HZ40_Mid = rdnumpy(file35)
# ============================ SoilWidth = 10.0 m (HZ = 40)=======================================
Condition8 = f'{Wave_Choose}/W_10m/{HZ40}'
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

Tie_W10_HZ40_Mid = rdnumpy(file36)
LK_W10_HZ40_Mid = rdnumpy(file37)
Type1_W10_HZ40_Mid = rdnumpy(file38)
Type2_W10_HZ40_Mid = rdnumpy(file39)
Type3_W10_HZ40_Mid = rdnumpy(file40)
# ============================ SoilWidth = 20.0 m (HZ = 40)=======================================
Condition9 = f'{Wave_Choose}/W_20m/{HZ40}'
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

Tie_W20_HZ40_Mid = rdnumpy(file41)
LK_W20_HZ40_Mid = rdnumpy(file42)
Type1_W20_HZ40_Mid = rdnumpy(file43)
Type2_W20_HZ40_Mid = rdnumpy(file44)
Type3_W20_HZ40_Mid = rdnumpy(file45)

# ----------------- f = 80HZ --------------------------------
HZ80 = f'HZ_80'
# ============================ SoilWidth = 2.0 m (HZ = 80)=======================================
Condition10 = f'{Wave_Choose}/W_2m/{HZ80}'
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

Tie_W2_HZ80_Mid = rdnumpy(file46)
LK_W2_HZ80_Mid = rdnumpy(file47)
Type1_W2_HZ80_Mid = rdnumpy(file48)
Type2_W2_HZ80_Mid = rdnumpy(file49)
Type3_W2_HZ80_Mid = rdnumpy(file50)
# ============================ SoilWidth = 10.0 m (HZ = 80)=======================================
Condition11 = f'{Wave_Choose}/W_10m/{HZ80}'
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

Tie_W10_HZ80_Mid = rdnumpy(file51)
LK_W10_HZ80_Mid = rdnumpy(file52)
Type1_W10_HZ80_Mid = rdnumpy(file53)
Type2_W10_HZ80_Mid = rdnumpy(file54)
Type3_W10_HZ80_Mid = rdnumpy(file55)
# ============================ SoilWidth = 20.0 m (HZ = 80)=======================================
Condition12 = f'{Wave_Choose}/W_20m/{HZ80}'
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

Tie_W20_HZ80_Mid = rdnumpy(file56)
LK_W20_HZ80_Mid = rdnumpy(file57)
Type1_W20_HZ80_Mid = rdnumpy(file58)
Type2_W20_HZ80_Mid = rdnumpy(file59)
Type3_W20_HZ80_Mid = rdnumpy(file60)

def Find_Quarter(soilwidth, YMesh):
    Dw = SoilLength/80 # SoilLength/80 , SoilLength/ny
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

plt_axis2 = 2
# # ------- wave put into the timeSeries ---------------
def Differ_BCVel(total_time, Pwave, Tie, LKDash, BeamType1, BeamType2, BeamType3):
    # font_props = {'family': 'Arial', 'size': 12}
    plt.plot(total_time, Pwave[:, Nele-1],label =r'$\mathrm{Analytical}$',color= 'black',linewidth=6.0)
    plt.plot(Tie[:,0], Tie[:,plt_axis2],label ='Tie', ls = '-',color= 'limegreen',linewidth=6.0)
    plt.plot(LKDash[:,0], LKDash[:,plt_axis2],label ='LK Dashpot', ls = '-.',color= 'orange',linewidth=5.0)
    plt.plot(BeamType1[:,0], BeamType1[:,plt_axis2],label ='Beam_Base ', ls = ':',color= 'purple',linewidth=4.0)
    plt.plot(BeamType2[:,0], BeamType2[:,plt_axis2],label ='Hybrid', ls = '--',color= 'blue',linewidth=3.0)
    plt.plot(BeamType3[:,0], BeamType3[:,plt_axis2],label ='Node_Base',color= 'red',linewidth= 2.0)

    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 17)
    plt.xlim(0.0, 0.20) 
    plt.ylim(-0.75, 0.75)
    plt.grid(True)
    
    ax = plt.gca()
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
    # ax.yaxis.get_offset_text().set(size=17)

x_axis = 0.25

# row_heights = [3,3,3]
# fig1, (ax1,ax2,ax3) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# fig1.suptitle(f'Different Boundary Compare',x=0.50,y =0.95,fontsize = 20)
# fig1.text(0.40,0.89, "(Middle Node)", color = "red", fontsize=20)
# fig1.text(0.58,0.68, f'P wave '+ r"($t_d=0.1$ $\mathrm {s}$)", color = "blue", fontsize=22)
# fig1.text(0.01,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
# fig1.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

# ax1 = plt.subplot(311)
# Differ_BCVel(total_time_HZ10, HZ10_Pwave, Tie_W20_HZ10_Mid, LK_W20_HZ10_Mid, Type1_W20_HZ10_Mid, Type2_W20_HZ10_Mid, Type3_W20_HZ10_Mid)
# ax1.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.50, y=0.78)

# ax2 = plt.subplot(312)
# Differ_BCVel(total_time_HZ10, HZ10_Pwave, Tie_W10_HZ10_Mid, LK_W10_HZ10_Mid, Type1_W10_HZ10_Mid, Type2_W10_HZ10_Mid, Type3_W10_HZ10_Mid)
# ax2.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.50, y=0.78)

# ax3 = plt.subplot(313)
# Differ_BCVel(total_time_HZ10, HZ10_Pwave, Tie_W2_HZ10_Mid, LK_W2_HZ10_Mid, Type1_W2_HZ10_Mid, Type2_W2_HZ10_Mid, Type3_W2_HZ10_Mid)
# ax3.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.48, y=0.78)

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig1.axes[-1].get_legend_handles_labels()
# fig1.legend(lines, labels, loc = (0.75, 0.80), prop=font_props)

# row_heights = [3,3,3]
# fig2, (ax4,ax5,ax6) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# fig2.suptitle(f'Different Boundary Compare',x=0.50,y =0.95,fontsize = 20)
# fig2.text(0.40,0.89, "(Middle Node)", color = "red", fontsize=20)
# fig2.text(0.54,0.68, f'P wave '+ r"($t_d=0.05$ $\mathrm {s}$)", color = "blue", fontsize=22)
# fig2.text(0.01,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
# fig2.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

# ax4 = plt.subplot(311)
# Differ_BCVel(total_time_HZ20, HZ20_Pwave, Tie_W20_HZ20_Mid, LK_W20_HZ20_Mid, Type1_W20_HZ20_Mid, Type2_W20_HZ20_Mid, Type3_W20_HZ20_Mid)
# ax4.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.50, y=0.78)

# ax5 = plt.subplot(312)
# Differ_BCVel(total_time_HZ20, HZ20_Pwave, Tie_W10_HZ20_Mid, LK_W10_HZ20_Mid, Type1_W10_HZ20_Mid, Type2_W10_HZ20_Mid, Type3_W10_HZ20_Mid)
# ax5.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.50, y=0.78)

# ax6 = plt.subplot(313)
# Differ_BCVel(total_time_HZ20, HZ20_Pwave, Tie_W2_HZ20_Mid, LK_W2_HZ20_Mid, Type1_W2_HZ20_Mid, Type2_W2_HZ20_Mid, Type3_W2_HZ20_Mid)
# ax6.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.48, y=0.78)

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig2.axes[-1].get_legend_handles_labels()
# fig2.legend(lines, labels, loc = (0.75, 0.80), prop=font_props)

# row_heights = [3,3,3]
# fig3, (ax7,ax8,ax9) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# fig3.suptitle(f'Different Boundary Compare',x=0.50,y =0.95,fontsize = 20)
# fig3.text(0.40,0.89, "(Middle Node)", color = "red", fontsize=20)
# fig3.text(0.53,0.68, f'P wave '+ r"($t_d=0.025$ $\mathrm {s}$)", color = "blue", fontsize=22)
# fig3.text(0.01,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
# fig3.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

# ax7 = plt.subplot(311)
# Differ_BCVel(total_time_HZ40, HZ40_Pwave, Tie_W20_HZ40_Mid, LK_W20_HZ40_Mid, Type1_W20_HZ40_Mid, Type2_W20_HZ40_Mid, Type3_W20_HZ40_Mid)
# ax7.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.50, y=0.78)

# ax8 = plt.subplot(312)
# Differ_BCVel(total_time_HZ40, HZ40_Pwave, Tie_W10_HZ40_Mid, LK_W10_HZ40_Mid, Type1_W10_HZ40_Mid, Type2_W10_HZ40_Mid, Type3_W10_HZ40_Mid)
# ax8.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.50, y=0.78)

# ax9 = plt.subplot(313)
# Differ_BCVel(total_time_HZ40, HZ40_Pwave, Tie_W2_HZ40_Mid, LK_W2_HZ40_Mid, Type1_W2_HZ40_Mid, Type2_W2_HZ40_Mid, Type3_W2_HZ40_Mid)
# ax9.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.48, y=0.78)

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig3.axes[-1].get_legend_handles_labels()
# fig3.legend(lines, labels, loc = (0.75, 0.80), prop=font_props)

# row_heights = [3,3,3]
# fig4, (ax10,ax11,ax12) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# fig4.suptitle(f'Different Boundary Compare',x=0.50,y =0.95,fontsize = 20)
# fig4.text(0.40,0.89, "(Middle Node)", color = "red", fontsize=20)
# fig4.text(0.50,0.68, f'P wave '+ r"($t_d=0.0125$ $\mathrm {s}$)", color = "blue", fontsize=22)
# fig4.text(0.01,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
# fig4.text(0.42,0.05, r"$\mathrm {time}$ ${t}$ $(s)$", va= 'center', fontsize=20) # $(10^{-1}\,s)$

# ax10 = plt.subplot(311)
# Differ_BCVel(total_time_HZ80, HZ80_Pwave, Tie_W20_HZ80_Mid, LK_W20_HZ80_Mid, Type1_W20_HZ80_Mid, Type2_W20_HZ80_Mid, Type3_W20_HZ80_Mid)
# ax10.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.50, y=0.78)

# ax11 = plt.subplot(312)
# Differ_BCVel(total_time_HZ80, HZ80_Pwave, Tie_W10_HZ80_Mid, LK_W10_HZ80_Mid, Type1_W10_HZ80_Mid, Type2_W10_HZ80_Mid, Type3_W10_HZ80_Mid)
# ax11.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.50, y=0.78)

# ax12 = plt.subplot(313)
# Differ_BCVel(total_time_HZ80, HZ80_Pwave, Tie_W2_HZ80_Mid, LK_W2_HZ80_Mid, Type1_W2_HZ80_Mid, Type2_W2_HZ80_Mid, Type3_W2_HZ80_Mid)
# ax12.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.48, y=0.78)

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig4.axes[-1].get_legend_handles_labels()
# fig4.legend(lines, labels, loc = (0.75, 0.80), prop=font_props)

# ================================== Prepare Relative Error and Absolute Error ============================
def Find_ColMaxValue(column_index, ele80_Mid):
    column = ele80_Mid[:, column_index]
    max_value = np.max(column)
    max_index = np.argmax(column)
    
    min_value = np.min(column)
    min_index = np.argmin(column)

    print(f'max_value= {max_value}; max_index= {max_index}; min_value= {min_value}; min_index= {min_index}')
    return(max_value)
# ---------- Find Analysis data Peak Value -----------------
maxAnaly_HZ10 = Find_ColMaxValue(Analysis_Column, HZ10_Pwave)
maxAnaly_HZ20 = Find_ColMaxValue(Analysis_Column, HZ20_Pwave)
maxAnaly_HZ40 = Find_ColMaxValue(Analysis_Column, HZ40_Pwave)
maxAnaly_HZ80 = Find_ColMaxValue(Analysis_Column, HZ80_Pwave)

def process_column(matrix, column_index):
    column = matrix[:, column_index]
    abs_column = np.abs(column)
    
    max_index = np.argmax(abs_column)
    max_peak = np.max(abs_column)
    
    print(f'max_value= {max_peak}; max_index= {max_index}')
    return max_peak

column_index = 2 # Pwave = 2 (yaxis)
# ------------ 10HZ --------------------
maxTie2_HZ10 = process_column(Tie_W2_HZ10_Mid, column_index)
maxLK2_HZ10 = process_column(LK_W2_HZ10_Mid, column_index)
maxType1_2_HZ10 = process_column(Type1_W2_HZ10_Mid, column_index)
maxType2_2_HZ10 = process_column(Type2_W2_HZ10_Mid, column_index)
maxType3_2_HZ10 = process_column(Type3_W2_HZ10_Mid, column_index)

maxTie10_HZ10 = process_column(Tie_W10_HZ10_Mid, column_index)
maxLK10_HZ10 = process_column(LK_W10_HZ10_Mid, column_index)
maxType1_10_HZ10 = process_column(Type1_W10_HZ10_Mid, column_index)
maxType2_10_HZ10 = process_column(Type2_W10_HZ10_Mid, column_index)
maxType3_10_HZ10 = process_column(Type3_W10_HZ10_Mid, column_index)

maxTie20_HZ10 = process_column(Tie_W20_HZ10_Mid, column_index)
maxLK20_HZ10 = process_column(LK_W20_HZ10_Mid, column_index)
maxType1_20_HZ10 = process_column(Type1_W20_HZ10_Mid, column_index)
maxType2_20_HZ10 = process_column(Type2_W20_HZ10_Mid, column_index)
maxType3_20_HZ10 = process_column(Type3_W20_HZ10_Mid, column_index)

# ------------ 20HZ --------------------
maxTie2_HZ20 = process_column(Tie_W2_HZ20_Mid, column_index)
maxLK2_HZ20 = process_column(LK_W2_HZ20_Mid, column_index)
maxType1_2_HZ20 = process_column(Type1_W2_HZ20_Mid, column_index)
maxType2_2_HZ20 = process_column(Type2_W2_HZ20_Mid, column_index)
maxType3_2_HZ20 = process_column(Type3_W2_HZ20_Mid, column_index)

maxTie10_HZ20 = process_column(Tie_W10_HZ20_Mid, column_index)
maxLK10_HZ20 = process_column(LK_W10_HZ20_Mid, column_index)
maxType1_10_HZ20 = process_column(Type1_W10_HZ20_Mid, column_index)
maxType2_10_HZ20 = process_column(Type2_W10_HZ20_Mid, column_index)
maxType3_10_HZ20 = process_column(Type3_W10_HZ20_Mid, column_index)

maxTie20_HZ20 = process_column(Tie_W20_HZ20_Mid, column_index)
maxLK20_HZ20 = process_column(LK_W20_HZ20_Mid, column_index)
maxType1_20_HZ20 = process_column(Type1_W20_HZ20_Mid, column_index)
maxType2_20_HZ20 = process_column(Type2_W20_HZ20_Mid, column_index)
maxType3_20_HZ20 = process_column(Type3_W20_HZ20_Mid, column_index)

# ------------ 40HZ --------------------
maxTie2_HZ40 = process_column(Tie_W2_HZ40_Mid, column_index)
maxLK2_HZ40 = process_column(LK_W2_HZ40_Mid, column_index)
maxType1_2_HZ40 = process_column(Type1_W2_HZ40_Mid, column_index)
maxType2_2_HZ40 = process_column(Type2_W2_HZ40_Mid, column_index)
maxType3_2_HZ40 = process_column(Type3_W2_HZ40_Mid, column_index)

maxTie10_HZ40 = process_column(Tie_W10_HZ40_Mid, column_index)
maxLK10_HZ40 = process_column(LK_W10_HZ40_Mid, column_index)
maxType1_10_HZ40 = process_column(Type1_W10_HZ40_Mid, column_index)
maxType2_10_HZ40 = process_column(Type2_W10_HZ40_Mid, column_index)
maxType3_10_HZ40 = process_column(Type3_W10_HZ40_Mid, column_index)

maxTie20_HZ40 = process_column(Tie_W20_HZ40_Mid, column_index)
maxLK20_HZ40 = process_column(LK_W20_HZ40_Mid, column_index)
maxType1_20_HZ40 = process_column(Type1_W20_HZ40_Mid, column_index)
maxType2_20_HZ40 = process_column(Type2_W20_HZ40_Mid, column_index)
maxType3_20_HZ40 = process_column(Type3_W20_HZ40_Mid, column_index)

# ------------ 80HZ --------------------
maxTie2_HZ80 = process_column(Tie_W2_HZ80_Mid, column_index)
maxLK2_HZ80 = process_column(LK_W2_HZ80_Mid, column_index)
maxType1_2_HZ80 = process_column(Type1_W2_HZ80_Mid, column_index)
maxType2_2_HZ80 = process_column(Type2_W2_HZ80_Mid, column_index)
maxType3_2_HZ80 = process_column(Type3_W2_HZ80_Mid, column_index)

maxTie10_HZ80 = process_column(Tie_W10_HZ80_Mid, column_index)
maxLK10_HZ80 = process_column(LK_W10_HZ80_Mid, column_index)
maxType1_10_HZ80 = process_column(Type1_W10_HZ80_Mid, column_index)
maxType2_10_HZ80 = process_column(Type2_W10_HZ80_Mid, column_index)
maxType3_10_HZ80 = process_column(Type3_W10_HZ80_Mid, column_index)

maxTie20_HZ80 = process_column(Tie_W20_HZ80_Mid, column_index)
maxLK20_HZ80 = process_column(LK_W20_HZ80_Mid, column_index)
maxType1_20_HZ80 = process_column(Type1_W20_HZ80_Mid, column_index)
maxType2_20_HZ80 = process_column(Type2_W20_HZ80_Mid, column_index)
maxType3_20_HZ80 = process_column(Type3_W20_HZ80_Mid, column_index)

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

Type1_20error = np.zeros((len(Frequency_Size),2))
errMatrix(Type1_20error, maxType1_20_HZ10, maxType1_20_HZ20, maxType1_20_HZ40, maxType1_20_HZ80)

Type2_20error = np.zeros((len(Frequency_Size),2))
errMatrix(Type2_20error, maxType2_20_HZ10, maxType2_20_HZ20, maxType2_20_HZ40, maxType2_20_HZ80)

Type3_20error = np.zeros((len(Frequency_Size),2))
errMatrix(Type3_20error, maxType3_20_HZ10, maxType3_20_HZ20, maxType3_20_HZ40, maxType3_20_HZ80)

# ------------W10m Error Peak Value-----------------------
Tie10_error = np.zeros((len(Frequency_Size),2))
errMatrix(Tie10_error, maxTie10_HZ10, maxTie10_HZ20, maxTie10_HZ40, maxTie10_HZ80)

LK10_error = np.zeros((len(Frequency_Size),2))
errMatrix(LK10_error, maxLK10_HZ10, maxLK10_HZ20, maxLK10_HZ40, maxLK10_HZ80)

Type1_10error = np.zeros((len(Frequency_Size),2))
errMatrix(Type1_10error, maxType1_10_HZ10, maxType1_10_HZ20, maxType1_10_HZ40, maxType1_10_HZ80)

Type2_10error = np.zeros((len(Frequency_Size),2))
errMatrix(Type2_10error, maxType2_10_HZ10, maxType2_10_HZ20, maxType2_10_HZ40, maxType2_10_HZ80)

Type3_10error = np.zeros((len(Frequency_Size),2))
errMatrix(Type3_10error, maxType3_10_HZ10, maxType3_10_HZ20, maxType3_10_HZ40, maxType3_10_HZ80)

# ------------W2m Error Peak Value-----------------------
Tie2_error = np.zeros((len(Frequency_Size),2))
errMatrix(Tie2_error, maxTie2_HZ10, maxTie2_HZ20, maxTie2_HZ40, maxTie2_HZ80)

LK2_error = np.zeros((len(Frequency_Size),2))
errMatrix(LK2_error, maxLK2_HZ10, maxLK2_HZ20, maxLK2_HZ40, maxLK2_HZ80)

Type1_2error = np.zeros((len(Frequency_Size),2))
errMatrix(Type1_2error, maxType1_2_HZ10, maxType1_2_HZ20, maxType1_2_HZ40, maxType1_2_HZ80)

Type2_2error = np.zeros((len(Frequency_Size),2))
errMatrix(Type2_2error, maxType2_2_HZ10, maxType2_2_HZ20, maxType2_2_HZ40, maxType2_2_HZ80)

Type3_2error = np.zeros((len(Frequency_Size),2))
errMatrix(Type3_2error, maxType3_2_HZ10, maxType3_2_HZ20, maxType3_2_HZ40, maxType3_2_HZ80)

#  ---------- calculate Relative Error ----------------------------
Tie20_err = np.zeros((len(Frequency_Size),2))
LK20_err = np.zeros((len(Frequency_Size),2))
Type1_W20_err = np.zeros((len(Frequency_Size),2))
Type2_W20_err = np.zeros((len(Frequency_Size),2))
Type3_W20_err = np.zeros((len(Frequency_Size),2))

Tie10_err = np.zeros((len(Frequency_Size),2))
LK10_err = np.zeros((len(Frequency_Size),2))
Type1_W10_err = np.zeros((len(Frequency_Size),2))
Type2_W10_err = np.zeros((len(Frequency_Size),2))
Type3_W10_err = np.zeros((len(Frequency_Size),2))

Tie2_err = np.zeros((len(Frequency_Size),2))
LK2_err = np.zeros((len(Frequency_Size),2))
Type1_W2_err = np.zeros((len(Frequency_Size),2))
Type2_W2_err = np.zeros((len(Frequency_Size),2))
Type3_W2_err = np.zeros((len(Frequency_Size),2))

def Calculate_Error(TieErr, Tie_error): # , maxAnaly_HZ10, maxAnaly_HZ20, maxAnaly_HZ40, maxAnaly_HZ80
    TieErr[:,0] = Tie_error[:,0]
# ------------------------- Absolute Relative Error ------------------        
    TieErr[0,1] = ((Tie_error[0,1] - maxAnaly_HZ10)/maxAnaly_HZ10)*100
    TieErr[1,1] = ((Tie_error[1,1] - maxAnaly_HZ20)/maxAnaly_HZ20)*100
    TieErr[2,1] = ((Tie_error[2,1] - maxAnaly_HZ40)/maxAnaly_HZ40)*100
    TieErr[3,1] = ((Tie_error[3,1] - maxAnaly_HZ80)/maxAnaly_HZ80)*100
        
Calculate_Error(Tie20_err, Tie20_error)
Calculate_Error(LK20_err, LK20_error)
Calculate_Error(Type1_W20_err, Type1_20error)
Calculate_Error(Type2_W20_err, Type2_20error)
Calculate_Error(Type3_W20_err, Type3_20error)

Calculate_Error(Tie10_err, Tie10_error)
Calculate_Error(LK10_err, LK10_error)
Calculate_Error(Type1_W10_err, Type1_10error)
Calculate_Error(Type2_W10_err, Type2_10error)
Calculate_Error(Type3_W10_err, Type3_10error)

Calculate_Error(Tie2_err, Tie2_error)
Calculate_Error(LK2_err, LK2_error)
Calculate_Error(Type1_W2_err, Type1_2error)
Calculate_Error(Type2_W2_err, Type2_2error)
Calculate_Error(Type3_W2_err, Type3_2error)

# ------------------------------- Time Increment Relative Error: 20、10、1m (Middle point)-------------------- 
# ==================Draw Relative error : Middele point =============================
def DifferTime_RelativeError(Peak,TieErr, LKErr, Type1Err, Type2Err, Type3Err):
    # font_props = {'family': 'Arial', 'size': 14}
    plt.plot(TieErr[:,0], TieErr[:,Peak],marker = '^',markersize=12,markerfacecolor = 'white',label = 'Tie')
    # plt.plot(LKErr[:,0], LKErr[:,Peak],marker = 'o',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot')
    plt.plot(Type1Err[:,0], Type1Err[:,Peak],marker = '<',markersize=8,markerfacecolor = 'white',label = 'Beam_Base')
    plt.plot(Type2Err[:,0], Type2Err[:,Peak],marker = 's',markersize=6,markerfacecolor = 'white',label = 'Hybrid')
    plt.plot(Type3Err[:,0], Type3Err[:,Peak],marker = 'p',markersize=4,markerfacecolor = 'white',label = 'Node_Base')

    # plt.legend(loc='center left',prop=font_props) #ncol=2,fontsize=16 frameon=False
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)

    plt.ylim(0, 5.0)  # 0,12
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

figsize = (10,10)
# # ----------------- Middle Node Relative Error -------------------------
# # ----------------- Draw Relative error : td (1/HZ) ------------------- 
# fig5, (ax13,ax14,ax15) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# fig5.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig5.text(0.43,0.89, "(Middle Node)", color = "red", fontsize=20)
# fig5.text(0.15,0.85, f'P wave', color = "blue", fontsize=30)

# fig5.text(0.045,0.5, 'Peak Velocity Error: '+ r"$\ E_{Max}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=20)
# fig5.text(0.41,0.060,  f'Critical Time ' + r'$t_d$', va= 'center', fontsize=20)

# ax13 = plt.subplot(311)
# DifferTime_RelativeError(1, Tie20_err, LK20_err, Type1_W20_err, Type2_W20_err, Type3_W20_err)
# ax13.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.50, y=0.65)

# ax14 = plt.subplot(312)
# DifferTime_RelativeError(1, Tie10_err, LK10_err, Type1_W10_err, Type2_W10_err, Type3_W10_err)
# ax14.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.50, y=0.65)

# ax15 = plt.subplot(313)
# DifferTime_RelativeError(1, Tie2_err, LK2_err, Type1_W2_err, Type2_W2_err, Type3_W2_err)
# ax15.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.50, y=0.65)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting

# lines, labels = fig5.axes[-1].get_legend_handles_labels()
# fig5.legend(lines, labels, loc = (0.77,0.80) ,prop=font_props)

def LK_RelativeError(Peak,LK2, LK10, LK20):
    plt.figure(figsize=(10, 8))
    font_props = {'family': 'Arial', 'size': 18}
    plt.title('LK Dashpot Different Soilwidth Error Compare', fontsize = 20)
    plt.xlabel(f'Critical Time ' + r'$t_d$', fontsize = 20)
    plt.ylabel('Peak Velocity Error: '+ r"$\ E_{Max}$" + r" (%)", fontsize = 20)
    
    plt.plot(LK2[:,0], LK2[:,Peak],marker = '^',markersize=12,markerfacecolor = 'white',label = r"$w=$ $\mathrm{2m}$")
    plt.plot(LK10[:,0], LK10[:,Peak],marker = 'o',markersize=10,markerfacecolor = 'white',label = r"$w=$ $\mathrm{10m}$")
    plt.plot(LK20[:,0], LK20[:,Peak],marker = '<',markersize=8,markerfacecolor = 'white',label = r"$w=$ $\mathrm{20m}$")

    plt.legend(loc='center left',prop=font_props) #ncol=2,fontsize=16 frameon=False
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)

    plt.ylim(-100, 20.0)
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

# LK_RelativeError(1, LK2_err, LK10_err, LK20_err)
    
Dy = 0.25 # m
Dy_lamb = np.array([Dy/lamb10, Dy/lamb20, Dy/lamb40, Dy/lamb80])

# ==================Draw Relative error : Dy/WaveLength =============================
def DifferTime_RelativeError2(Peak,TieErr, LKErr, Type1Err, Type2Err, Type3Err):
    # font_props = {'family': 'Arial', 'size': 14}
    plt.plot(Dy_lamb[:], TieErr[:,Peak],marker = '^',markersize=12,markerfacecolor = 'white',label = 'Tie BC')
    # plt.plot(Dy_lamb[:,0], LKErr[:,Peak],marker = 'o',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot')
    plt.plot(Dy_lamb[:], Type1Err[:,Peak],marker = '<',markersize=8,markerfacecolor = 'white',label = 'Beam_Base')
    plt.plot(Dy_lamb[:], Type2Err[:,Peak],marker = 's',markersize=6,markerfacecolor = 'white',label = 'Hybrid')
    plt.plot(Dy_lamb[:], Type3Err[:,Peak],marker = 'p',markersize=4,markerfacecolor = 'white',label = 'Node_Base')

    # plt.legend(loc='center left',prop=font_props) #ncol=2,fontsize=16 frameon=False
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)

    plt.ylim(0, 5.0) 
    plt.grid(True)
    
    ax = plt.gca()
    # -------------- Consider X-axis  -----------------------
    ax.set_xscale('log', base=10)
    ax.set_xticks([], minor=False)
    ax.set_xticks([], minor=True)
    x_ticks_Num = np.array([0.006,0.01, 0.02, 0.03, 0.04, 0.05])  # td = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1] ; Dy/lamb = []
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.3f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='both', labelsize=20)
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.125))

# figsize = (10,10)   
# fig6, (ax16,ax17,ax18) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# fig6.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig6.text(0.41,0.89, "(Middle Node)", color = "red", fontsize=20)
# fig6.text(0.15,0.85, r"$\mathrm {Pwave}$", color = "blue", fontsize=22)

# fig6.text(0.045,0.5, 'Peak Velocity Error: '+ r"$\ E_{Max}$" + r" (%)", va= 'center', rotation= 'vertical', fontsize=20)
# fig6.text(0.50,0.060, r'$\Delta_y/\lambda_p$', va= 'center', fontsize=20)

# ax16 = plt.subplot(311)
# DifferTime_RelativeError2(1, Tie20_err, LK20_err, Type1_W20_err, Type2_W20_err, Type3_W20_err)
# ax16.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.50, y=0.65)

# ax17 = plt.subplot(312)
# DifferTime_RelativeError2(1, Tie10_err, LK10_err, Type1_W10_err, Type2_W10_err, Type3_W10_err)
# ax17.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.50, y=0.65)

# ax18 = plt.subplot(313)
# DifferTime_RelativeError2(1, Tie2_err, LK2_err, Type1_W2_err, Type2_W2_err, Type3_W2_err)
# ax18.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.50, y=0.65)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting

# lines, labels = fig6.axes[-1].get_legend_handles_labels()
# fig6.legend(lines, labels, loc = (0.77,0.82) ,prop=font_props)

# ================================== Prepare L2-Norm Error (Normalization) ============================
# ---------- Find Different Data in 40 row Same Time ---------------------
Analysis_Time = Tie_W20_HZ40_Mid[:,0]
Theory_Time = total_time_HZ80

# ================= Calculate_2NormError Normalization ===============================
def Calculate_RelativeL2norm(TheoryTime,Pwave, Analysis_Time,Tie_W20_HZ40_Mid, time_range=(0, 0.20)):
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

def Add_Err(Index, MidTieErr20,Tie20_error, Tie_W20_HZ10_Mid, Tie_W20_HZ20_Mid, Tie_W20_HZ40_Mid, Tie_W20_HZ80_Mid):
    MidTieErr20[:,0] = Tie20_error[:,0] 
# ===================================== Calculate_L2NormError Normalization ============================================================
    MidTieErr20[0,Index], MidTieErr20[0,2] = Calculate_RelativeL2norm(Theory_Time,HZ10_Pwave, Analysis_Time,Tie_W20_HZ10_Mid, time_range=(0, 0.20))
    MidTieErr20[1,Index], MidTieErr20[1,2] = Calculate_RelativeL2norm(Theory_Time,HZ20_Pwave, Analysis_Time,Tie_W20_HZ20_Mid, time_range=(0, 0.20))
    MidTieErr20[2,Index], MidTieErr20[2,2] = Calculate_RelativeL2norm(Theory_Time,HZ40_Pwave, Analysis_Time,Tie_W20_HZ40_Mid, time_range=(0, 0.20))
    MidTieErr20[3,Index], MidTieErr20[3,2] = Calculate_RelativeL2norm(Theory_Time,HZ80_Pwave, Analysis_Time,Tie_W20_HZ80_Mid, time_range=(0, 0.20))
# -------------- W = 20m-------------------------------
Tie20Err_L2 = np.zeros((4,3))
Add_Err(1, Tie20Err_L2,Tie20_error, Tie_W20_HZ10_Mid, Tie_W20_HZ20_Mid, Tie_W20_HZ40_Mid, Tie_W20_HZ80_Mid)

LK20Err_L2 = np.zeros((4,3))
Add_Err(1, LK20Err_L2,LK20_error, LK_W20_HZ10_Mid, LK_W20_HZ20_Mid, LK_W20_HZ40_Mid, LK_W20_HZ80_Mid)

Type1_W20Err_L2 = np.zeros((4,3))
Add_Err(1, Type1_W20Err_L2, Type1_20error, Type1_W20_HZ10_Mid, Type1_W20_HZ20_Mid, Type1_W20_HZ40_Mid, Type1_W20_HZ80_Mid)

Type2_W20Err_L2 = np.zeros((4,3))
Add_Err(1, Type2_W20Err_L2, Type2_20error, Type2_W20_HZ10_Mid, Type2_W20_HZ20_Mid, Type2_W20_HZ40_Mid, Type2_W20_HZ80_Mid)

Type3_W20Err_L2 = np.zeros((4,3))
Add_Err(1, Type3_W20Err_L2, Type3_20error, Type3_W20_HZ10_Mid, Type3_W20_HZ20_Mid, Type3_W20_HZ40_Mid, Type3_W20_HZ80_Mid)

# -------------- W = 10m-------------------------------
Tie10Err_L2 = np.zeros((4,3))
Add_Err(1, Tie10Err_L2,Tie10_error, Tie_W10_HZ10_Mid, Tie_W10_HZ20_Mid, Tie_W10_HZ40_Mid, Tie_W10_HZ80_Mid)

LK10Err_L2 = np.zeros((4,3))
Add_Err(1, LK10Err_L2,LK10_error, LK_W10_HZ10_Mid, LK_W10_HZ20_Mid, LK_W10_HZ40_Mid, LK_W10_HZ80_Mid)

Type1_W10Err_L2 = np.zeros((4,3))
Add_Err(1, Type1_W10Err_L2, Type1_10error, Type1_W10_HZ10_Mid, Type1_W10_HZ20_Mid, Type1_W10_HZ40_Mid, Type1_W10_HZ80_Mid)

Type2_W10Err_L2 = np.zeros((4,3))
Add_Err(1, Type2_W10Err_L2, Type2_10error, Type2_W10_HZ10_Mid, Type2_W10_HZ20_Mid, Type2_W10_HZ40_Mid, Type2_W10_HZ80_Mid)

Type3_W10Err_L2 = np.zeros((4,3))
Add_Err(1, Type3_W10Err_L2, Type3_10error, Type3_W10_HZ10_Mid, Type3_W10_HZ20_Mid, Type3_W10_HZ40_Mid, Type3_W10_HZ80_Mid)

# -------------- W = 2m-------------------------------
Tie2Err_L2 = np.zeros((4,3))
Add_Err(1, Tie2Err_L2,Tie2_error, Tie_W2_HZ10_Mid, Tie_W2_HZ20_Mid, Tie_W2_HZ40_Mid, Tie_W2_HZ80_Mid)

LK2Err_L2 = np.zeros((4,3))
Add_Err(1, LK2Err_L2,LK2_error, LK_W2_HZ10_Mid, LK_W2_HZ20_Mid, LK_W2_HZ40_Mid, LK_W2_HZ80_Mid)

Type1_W2Err_L2 = np.zeros((4,3))
Add_Err(1, Type1_W2Err_L2, Type1_2error, Type1_W2_HZ10_Mid, Type1_W2_HZ20_Mid, Type1_W2_HZ40_Mid, Type1_W2_HZ80_Mid)

Type2_W2Err_L2 = np.zeros((4,3))
Add_Err(1, Type2_W2Err_L2, Type2_2error, Type2_W2_HZ10_Mid, Type2_W2_HZ20_Mid, Type2_W2_HZ40_Mid, Type3_W2_HZ80_Mid)

Type3_W2Err_L2 = np.zeros((4,3))
Add_Err(1, Type3_W2Err_L2, Type3_2error, Type3_W2_HZ10_Mid, Type3_W2_HZ20_Mid, Type3_W2_HZ40_Mid, Type3_W2_HZ80_Mid)

# ==================Draw L2 Norm error : Middele point =============================
def DifferTime_L2Error(Peak,TieErr, LKErr, Type1Err, Type2Err, Type3Err):
    plt.plot(TieErr[:,0],TieErr[:,Peak],marker = '^',markersize=12,markerfacecolor = 'white',label = 'Tie BC')
    # plt.plot(LKErr[:,0],LKErr[:,Peak],marker = 'o',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot')
    plt.plot(Type1Err[:,0],Type1Err[:,Peak],marker = '<',markersize=8,markerfacecolor = 'white',label = 'Beam_Base')
    plt.plot(Type2Err[:,0],Type2Err[:,Peak],marker = 's',markersize=6,markerfacecolor = 'white',label = 'Hybrid')
    plt.plot(Type3Err[:,0],Type3Err[:,Peak],marker = 'p',markersize=4,markerfacecolor = 'white',label = 'Node_Base')

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
    ax.tick_params(axis='x', which='both', labelsize= 18)
    # -------------- Consider Y-axis  -----------------------
    ax.set_yscale('log', base=10)
    ax.set_yticks([], minor=False)
    ax.set_yticks([], minor=True)
    y_ticks_Num = np.array([0.02, 0.04, 0.06, 0.08, 0.20])
    ax.set_yticks(y_ticks_Num)
    ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks_Num], rotation=0, fontsize=12)
    ax.tick_params(axis='y', which='both', labelsize=18)
    # ------- Miner ticks -----------------
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='y', which='minor', length=4, color='gray')
    
    
# # ----------------- Middle Node L2-Norm Error -------------------------
# figsize = (10, 10)
# fig7, (ax19,ax20,ax21) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# fig7.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig7.text(0.43,0.89, "(Middle Node)", color = "red", fontsize=20)
# fig7.text(0.15,0.80, f"P wave", color = "blue", fontsize=30)

# fig7.text(0.01,0.5, 'L2 normalization: '+ r"$\ E_{L2}$", va= 'center', rotation= 'vertical', fontsize=25)

# fig7.text(0.43,0.060,  f'Critical Time ' + r'$t_d$', va= 'center', fontsize=20)

# ax19 = plt.subplot(311)
# DifferTime_L2Error(1, Tie20Err_L2, LK20Err_L2, Type1_W20Err_L2, Type2_W20Err_L2, Type3_W20Err_L2)
# ax19.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.65, y=0.60)

# ax20 = plt.subplot(312)
# DifferTime_L2Error(1, Tie10Err_L2, LK10Err_L2, Type1_W10Err_L2, Type2_W10Err_L2, Type3_W10Err_L2)
# ax20.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.65, y=0.60)

# ax21 = plt.subplot(313)
# DifferTime_L2Error(1, Tie2Err_L2, LK2Err_L2, Type1_W2Err_L2, Type2_W2Err_L2, Type3_W2Err_L2)
# ax21.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.65, y=0.60)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting

# lines, labels = fig7.axes[-1].get_legend_handles_labels()
# fig7.legend(lines, labels, loc = (0.77,0.80) ,prop=font_props)

def LK_L2Error(Peak, LK2, LK10, LK20):
    plt.figure(figsize=(10, 8))
    font_props = {'family': 'Arial', 'size': 18}
    plt.title('LK Dashpot Different Soilwidth Error Compare', fontsize = 20)
    plt.xlabel(f'Critical Time ' + r'$t_d$', fontsize = 20)
    plt.ylabel('L2 normalization: '+ r"$\ E_{L2}$", fontsize = 20)
    
    plt.plot(LK2[:,0], LK2[:,Peak],marker = '^',markersize=12,markerfacecolor = 'white',label = r"$w=$ $\mathrm{2m}$")
    plt.plot(LK10[:,0], LK10[:,Peak],marker = 'o',markersize=10,markerfacecolor = 'white',label = r"$w=$ $\mathrm{10m}$")
    plt.plot(LK20[:,0], LK20[:,Peak],marker = '<',markersize=8,markerfacecolor = 'white',label = r"$w=$ $\mathrm{20m}$")

    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 18)

    # plt.xlim(0.0, 0.20)
    plt.grid(True)
    plt.legend(loc='lower left',prop=font_props) #ncol=2,fontsize=16 frameon=False
    
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
    ax.tick_params(axis='x', which='both', labelsize= 18)
    # -------------- Consider Y-axis  -----------------------
    ax.set_yscale('log', base=10)
    ax.set_yticks([], minor=False)
    ax.set_yticks([], minor=True)
    y_ticks_Num = np.array([0.10, 0.20, 0.40, 0.60, 0.80, 1.0])
    ax.set_yticks(y_ticks_Num)
    ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks_Num], rotation=0, fontsize=12)
    ax.tick_params(axis='y', which='both', labelsize=18)
    # ------- Miner ticks -----------------
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='y', which='minor', length=4, color='gray')

# LK_L2Error(1, LK2Err_L2, LK10Err_L2, LK20Err_L2)

# ==================Draw L2 Norm error : Dy/WaveLength =============================
def DifferTime_L2Error2(Peak,TieErr, LKErr, Type1Err, Type2Err, Type3Err):
    plt.plot(Dy_lamb[:],TieErr[:,Peak],marker = '^',markersize=12,markerfacecolor = 'white',label = 'Tie BC')
    # plt.plot(Dy_lamb[:],LKErr[:,Peak],marker = 'o',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot')
    plt.plot(Dy_lamb[:],Type1Err[:,Peak],marker = '<',markersize=8,markerfacecolor = 'white',label = 'Type1 Beam')
    plt.plot(Dy_lamb[:],Type2Err[:,Peak],marker = 's',markersize=6,markerfacecolor = 'white',label = 'Type2 Beam')
    plt.plot(Dy_lamb[:],Type3Err[:,Peak],marker = 'p',markersize=4,markerfacecolor = 'white',label = 'Type3 Node')

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
    x_ticks_Num = np.array([0.006,0.01, 0.02, 0.03, 0.04, 0.05])
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.2f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='both', labelsize= 18)
    # -------------- Consider Y-axis  -----------------------
    ax.set_yscale('log', base=10)
    ax.set_yticks([], minor=False)
    ax.set_yticks([], minor=True)
    y_ticks_Num = np.array([0.02, 0.04, 0.06, 0.08, 0.20])
    ax.set_yticks(y_ticks_Num)
    ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks_Num], rotation=0, fontsize=12)
    ax.tick_params(axis='y', which='both', labelsize=18)
    
    # # 使用科学计数法显示y轴刻度标签
    # ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    # ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))  # 使用科学计数法格式化

    # ax.set_ylim(0.0, 1.0)  # 例如从0.1到10
    
    # ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
    # ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    # ax.yaxis.get_offset_text().set(size=18)

# # ----------------- Middle Node L2-Norm Error -------------------------
# figsize = (10, 10)
# fig8, (ax22,ax23,ax24) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize) #, sharex=True
# fig8.suptitle(f'Ground Surface Different Boundary Compare',x=0.50,y =0.94,fontsize = 20)
# fig8.text(0.43,0.89, "(Middle Node)", color = "red", fontsize=20)
# fig8.text(0.15,0.85, r"$\mathrm {Pwave}$", color = "blue", fontsize=22)

# fig8.text(0.01,0.5, 'L2 normalization: '+ r"$\ E_{L2}$", va= 'center', rotation= 'vertical', fontsize=25)

# fig8.text(0.45,0.060, r'$\Delta_y/\lambda_p$', va= 'center', fontsize=20)

# ax22 = plt.subplot(311)
# DifferTime_L2Error2(1, Tie20Err_L2, LK20Err_L2, Type1_W20Err_L2, Type2_W20Err_L2, Type3_W20Err_L2)
# ax22.set_title(r"$w=$ $\mathrm{20m}$",fontsize =23, x=0.15, y=0.60)

# ax23 = plt.subplot(312)
# DifferTime_L2Error2(1, Tie10Err_L2, LK10Err_L2, Type1_W10Err_L2, Type2_W10Err_L2, Type3_W10Err_L2)
# ax23.set_title(r"$w=$ $\mathrm{10m}$",fontsize =23, x=0.15, y=0.60)

# ax24 = plt.subplot(313)
# DifferTime_L2Error2(1, Tie2Err_L2, LK2Err_L2, Type1_W2Err_L2, Type2_W2Err_L2, Type3_W2Err_L2)
# ax24.set_title(r"$w=$ $\mathrm{2m}$",fontsize =23, x=0.15, y=0.60)

# font_props = {'family': 'Arial', 'size': 17}  #Legend Setting

# lines, labels = fig8.axes[-1].get_legend_handles_labels()
# fig8.legend(lines, labels, loc = (0.77,0.65) ,prop=font_props)
