# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 15:19:07 2024

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
wp_20HZ =  pi/10 # 0 to 20m = 0 to 2*pi => x = pi/10
wp_10HZ =  pi/20 # 0 to 40m = 0 to 2*pi => x = pi/20
wp_40HZ =  pi/5 # 0 to 10m = 0 to 2*pi => x = pi/5

wp_80HZ =  (2*pi)/5 # 0 to 5m = 0 to 2*pi => x = 2*pi/5
wp_160HZ =  (4*pi)/5 # 0 to 2.5m = 0 to 2*pi => x = 4*pi/5
wp_320HZ =  (8*pi)/5 # 0 to 1.25m = 0 to 2*pi => x = 8*pi/5

fp_40HZ = 40
fp_80HZ = 80
fp_160HZ = 160
fp_320HZ = 320

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
            # if total_time[t] < Input_Time: # total_time[t] < 0.025
            #     Pwave[to+t,g] = (Pwave[to+t,g] + Cp_vel_Coefficient*XIn[to+t,g])  # original wave transport
                
            if total_time[t] >= 0.025 and total_time[t] <= (0.025+Input_Time):
                Pwave[to+t,End_Ele-g] = Pwave[to+t,End_Ele-g] + 2*Cp_vel_Coefficient*XIn[t-to,End_Ele-g]   # XOut[t-to,End_Ele-g
    return L, Pwave, total_time

lamb80, HZ80_Pwave, total_time_HZ80 = Cal_Theory(fp_80HZ, wp_80HZ)
lamb160, HZ160_Pwave, total_time_HZ160 = Cal_Theory(fp_160HZ, wp_160HZ)
lamb320, HZ320_Pwave, total_time_HZ320 = Cal_Theory(fp_320HZ, wp_320HZ)

lamb40, HZ40_Pwave, total_time_HZ40 = Cal_Theory(fp_40HZ, wp_40HZ)

Integrator = f'NewMark_Linear' # NewMark_Constant / NewMark_Linear
# --------------- Numerical Data ------------------------------
Compare = f"Test_Integrator/{Integrator}/Test/Dt_1.0" 
Condition1 =  f'HZ_80'
file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare}/{Condition1}/row80/Velocity/node161.out"
file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare}/{Condition1}/row40/Velocity/node81.out"
file3 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare}/{Condition1}/row20/Velocity/node41.out"
file4 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare}/{Condition1}/row10/Velocity/node21.out"

HZ80_80row = rdnumpy(file1)
HZ80_40row = rdnumpy(file2)
HZ80_20row = rdnumpy(file3)
HZ80_10row = rdnumpy(file4)

Condition2 =  f'HZ_160'
file5 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare}/{Condition2}/row80/Velocity/node161.out"
file6 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare}/{Condition2}/row40/Velocity/node81.out"
file7 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare}/{Condition2}/row20/Velocity/node41.out"
file8 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare}/{Condition2}/row10/Velocity/node21.out"

HZ160_80row = rdnumpy(file5)
HZ160_40row = rdnumpy(file6)
HZ160_20row = rdnumpy(file7)
HZ160_10row = rdnumpy(file8)

Condition3 =  f'HZ_320'
file9 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare}/{Condition3}/row80/Velocity/node161.out"
file10 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare}/{Condition3}/row40/Velocity/node81.out"
file11 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare}/{Condition3}/row20/Velocity/node41.out"
file12 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare}/{Condition3}/row10/Velocity/node21.out"

HZ320_80row = rdnumpy(file9)
HZ320_40row = rdnumpy(file10)
HZ320_20row = rdnumpy(file11)
HZ320_10row = rdnumpy(file12)

# --------------- Compare fp = 40HZ Numerical Data  ------------------------
Compare2 = f'Test_Integrator/{Integrator}/Dt_1.0'
file13 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare2}/row80/Velocity/node161.out"
file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare2}/row40/Velocity/node81.out"
file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare2}/row20/Velocity/node41.out"
file16 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Compare2}/row10/Velocity/node21.out"

HZ40_80row = rdnumpy(file13)
HZ40_40row = rdnumpy(file14)
HZ40_20row = rdnumpy(file15)
HZ40_10row = rdnumpy(file16)

def CompareDt_DiffVel(titleName,total_time, Pwave, HZ80_80row, HZ80_40row, HZ80_20row, HZ80_10row):
    plt.figure(figsize=(10,8))
    plt.title(titleName, fontsize = 25)
    # ------------------- Theory ------------------------------
    plt.plot(total_time, Pwave[:,79],label =r'$\mathrm{Analytical}$',color= 'black',linewidth= 4.0)
        
    # # -----------------Differ Mesh Pwave  -------------------------   
    plt.plot(HZ80_80row[:,0], HZ80_80row[:, 2], label = r'$\Delta_{c} = 0.0125H$', color= 'limegreen', linewidth = 6.0) # , ls = '--' 
    plt.plot(HZ80_40row[:,0], HZ80_40row[:, 2], label = r'$\Delta_{c} = 0.025H$', color= 'orange', ls = '-.',  linewidth = 5.0) # , ls = '-.'
    plt.plot(HZ80_20row[:,0], HZ80_20row[:, 2], label = r'$\Delta_{c} = 0.050H$', color= 'purple', linewidth = 4.0) # , ls = ':'
    plt.plot(HZ80_10row[:,0], HZ80_10row[:, 2], label = r'$\Delta_{c} = 0.10H$', color= 'red',  linewidth = 3.0) # , ls = '-.'
    
    plt.grid(True)
    plt.legend(loc='lower right',fontsize= 20)
    
    plt.xlim(0, 0.2)
    plt.ylim(-0.75, 0.75)
    
    plt.xlabel(r"$\mathrm {time}$ ${t}$ $\mathrm {(s)}$", fontsize = 25) # r"$G^{'}/G$"
    plt.ylabel(r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", fontsize = 25)  # r"$m_{x'}/m_{x}$"
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    
    ax = plt.gca()
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
    # ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    ax.yaxis.get_offset_text().set(size=20)
    
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.025))
    ax.xaxis.get_offset_text().set(size=20)

# CompareDt_DiffVel(r'Wave Length$\mathrm{=5m}$ ($t_d=0.0125$ $\mathrm{s}$)',total_time_HZ80, HZ80_Pwave, HZ80_80row, HZ80_40row, HZ80_20row, HZ80_10row)
# CompareDt_DiffVel(r'Wave Length$\mathrm{=2.5m}$ ($t_d=6.25$ $\times 10^{-3}$ $\mathrm{s}$)',total_time_HZ160, HZ160_Pwave, HZ160_80row, HZ160_40row, HZ160_20row, HZ160_10row)
# CompareDt_DiffVel(r'Wave Length$\mathrm{=1.25m}$ ($t_d=3.125$ $\times 10^{-3}$ $\mathrm{s}$)',total_time_HZ320, HZ320_Pwave, HZ320_80row, HZ320_40row, HZ320_20row, HZ320_10row)

# CompareDt_DiffVel(r'Wave Length$\mathrm{=10m}$ $(\mathrm{40HZ})$',total_time_HZ40, HZ40_Pwave, HZ40_80row, HZ40_40row, HZ40_20row, HZ40_10row)
# ================================== Prepare Relative Error and Absolute Error ============================
def process_column(matrix, column_index):
    column = matrix[:, column_index]
    abs_column = np.abs(column)
    
    max_index = np.argmax(abs_column)
    max_peak = np.max(abs_column)
    
    
    print(f'max_value= {max_peak}; max_index= {max_index}')
    return max_peak

# =========== Find Grounf Surface Max/ Min Peak Value ==========================
column_index = 2 # Pwave = 2 (yaxis)
Analysis_column = 79

# ------------ HZ = 80 -----------------------
maxHZ80_80row = process_column(HZ80_80row, column_index)
maxHZ80_40row = process_column(HZ80_40row, column_index)
maxHZ80_20row = process_column(HZ80_20row, column_index)
maxHZ80_10row = process_column(HZ80_10row, column_index)

# ------------ HZ = 160 -----------------------
maxHZ160_80row = process_column(HZ160_80row, column_index)
maxHZ160_40row = process_column(HZ160_40row, column_index)
maxHZ160_20row = process_column(HZ160_20row, column_index)
maxHZ160_10row = process_column(HZ160_10row, column_index)

# # ------------ HZ = 320 -----------------------
maxHZ320_80row = process_column(HZ320_80row, column_index)
maxHZ320_40row = process_column(HZ320_40row, column_index)
maxHZ320_20row = process_column(HZ320_20row, column_index)
maxHZ320_10row = process_column(HZ320_10row, column_index)

# # ------------ HZ = 40 -----------------------
maxHZ40_80row = process_column(HZ40_80row, column_index)
maxHZ40_40row = process_column(HZ40_40row, column_index)
maxHZ40_20row = process_column(HZ40_20row, column_index)
maxHZ40_10row = process_column(HZ40_10row, column_index)

def Find_ColMaxValue(column_index, ele80_Mid):
    column = ele80_Mid[:, column_index]
    max_value = np.max(column)
    max_index = np.argmax(column)
    
    min_value = np.min(column)
    min_index = np.argmin(column)

    print(f'max_value= {max_value}; max_index= {max_index}; min_value= {min_value}; min_index= {min_index}')
    return(max_value)

# ------------- Theory Max Value ---------------------
maxAnaly_HZ80 = Find_ColMaxValue(Analysis_column, HZ80_Pwave)
maxAnaly_HZ160 = Find_ColMaxValue(Analysis_column, HZ160_Pwave)
maxAnaly_HZ320 = Find_ColMaxValue(Analysis_column, HZ320_Pwave)

maxAnaly_HZ40 = Find_ColMaxValue(Analysis_column, HZ40_Pwave)

Mesh_Size = np.zeros(4)
ele = 80 
for m in range(len(Mesh_Size)):
    if m == 0 :    
        Mesh_Size[m] = SoilLength/ (ele)
    if m > 0:    
        Mesh_Size[m] = Mesh_Size[m-1]*2

def errMatrix(error_dc, maxDt02_80row, maxDt02_40row, maxDt02_20row, maxDt02_10row):
    error_dc[:,0] = Mesh_Size[:]
    
    error_dc[0,1] = maxDt02_80row
    error_dc[1,1] = maxDt02_40row
    error_dc[2,1] = maxDt02_20row
    error_dc[3,1] = maxDt02_10row

    return error_dc

# ============================= Middle Node ========================================
# ------------HZ = 80 Error Peak Value-----------------------
HZ80_error = np.zeros((4,2))
errMatrix(HZ80_error, maxHZ80_80row, maxHZ80_40row, maxHZ80_20row, maxHZ80_10row)
# ------------HZ = 160 Error Peak Value-----------------------
HZ160_error = np.zeros((4,2))
errMatrix(HZ160_error, maxHZ160_80row, maxHZ160_40row, maxHZ160_20row, maxHZ160_10row)
# ------------HZ = 320 Error Peak Value-----------------------
HZ320_error = np.zeros((4,2))
errMatrix(HZ320_error, maxHZ320_80row, maxHZ320_40row, maxHZ320_20row, maxHZ320_10row)

# ------------HZ = 40 Error Peak Value-----------------------
HZ40_error = np.zeros((4,2))
errMatrix(HZ40_error, maxHZ40_80row, maxHZ40_40row, maxHZ40_20row, maxHZ40_10row)

# calculate_Error()
HZ80_err = np.zeros((4,2))
HZ160_err = np.zeros((4,2))
HZ320_err = np.zeros((4,2))

HZ40_err = np.zeros((4,2))

def Calculate_Error(TieErr, Tie_error, maxAnaly):
    for i in range(len(Mesh_Size)):
        TieErr[:,0] = Tie_error[:,0]
# ------------------------- Absolute Relative Error ------------------        
        TieErr[i,1] = ((Tie_error[i,1] - maxAnaly)/maxAnaly)*100
        
Calculate_Error(HZ80_err, HZ80_error, maxAnaly_HZ80)
Calculate_Error(HZ160_err, HZ160_error, maxAnaly_HZ160)
Calculate_Error(HZ320_err, HZ320_error, maxAnaly_HZ320)

Calculate_Error(HZ40_err, HZ40_error, maxAnaly_HZ40)
# ==================Draw Relative error : Middele point =============================
def DifferTime_elemetError(HZ40_err, HZ80_err, HZ160_err, HZ320_err):
    plt.figure(figsize=(10,8))
    plt.title(f'Different Wave Length Relative Error: ' + f'{Integrator}', fontsize = 25) # Compare / Integrator
    
    font_props = {'family': 'Arial', 'size': 18}
    # ----------- Compare Original fp = 40 HZ ------------------------------
    plt.plot(HZ40_err[:,0], HZ40_err[:,1],marker = '*',markersize=14,markerfacecolor = 'white',label = r'$t_d=0.025$ $\mathrm{s}$', linewidth = 3.0)
    
    plt.plot(HZ80_err[:,0], HZ80_err[:,1],marker = '^',markersize=12,markerfacecolor = 'white',label = r'$t_d=0.0125$ $\mathrm{s}$', linewidth = 3.0)
    plt.plot(HZ160_err[:,0], HZ160_err[:,1],marker = 'o',markersize=11,markerfacecolor = 'white',label = r'$t_d=6.25$ $\times 10^{-3}$ $\mathrm{s}$', linewidth = 3.0)
    plt.plot(HZ320_err[:,0], HZ320_err[:,1],marker = '<',markersize=10,markerfacecolor = 'white',label = r'$t_d=3.125$ $\times 10^{-3}$ $\mathrm{s}$', linewidth = 3.0)
    
    plt.legend(ncol=1,prop=font_props, loc='lower left') #ncol=2,fontsize=16 frameon=False , loc='upper right'
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    
    plt.xlabel(r'$\Delta_c/\lambda_p$', fontsize = 25) # f'Mesh size ' + r'$\Delta_y$ $\mathrm {(m)}$' / r'$\Delta_c/\lambda_p$'
    plt.ylabel('Peak Velocity Error: '+ r"$\ E_{Max}$" + r" (%)", fontsize = 25)

    plt.ylim(-100, 20) # -15.0, 15.0 / -80, 20
    plt.grid(True)
    
    ax = plt.gca()
    # -------------- Consider X-axis  -----------------------
    ax.set_xscale('log', base=10)
    ax.set_xticks([], minor=False)
    ax.set_xticks([], minor=True)
    x_ticks_Num = np.array([0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4, 0.6])  # Dy: [0.125, 0.25, 0.50, 1.0] / Dy/H: [0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4, 0.6]
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.2f}' for tick in x_ticks_Num], rotation=0, fontsize=12) # Dy: .3f / Dy/H: .1f
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='both', labelsize=17)
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.125))
    # ------- Miner ticks -----------------
    ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='x', which='minor', length=4, color='gray')
    

# ---------- Compare Dy/lambda_p -----------------
HZ80_err[:,0] = HZ80_err[:,0]/lamb80
HZ160_err[:,0] = HZ160_err[:,0]/lamb160
HZ320_err[:,0] = HZ320_err[:,0]/lamb320

HZ40_err[:,0] = HZ40_err[:,0]/lamb40

# DifferTime_elemetError(HZ40_err, HZ80_err, HZ160_err, HZ320_err)

# ================================== Prepare L2-Norm Error ============================
# # ---------- Find Different Dt in 80, 40, 20, 10 row Same Time ---------------------
def Find_TimeCol(HZ80_80row, HZ80_40row, HZ80_20row, HZ80_10row):
    Ele80_Time = HZ80_80row[:,0]
    Ele40_Time = HZ80_40row[:,0]
    Ele20_Time = HZ80_20row[:,0]
    Ele10_Time = HZ80_10row[:,0]
    
    return Ele80_Time, Ele40_Time, Ele20_Time, Ele10_Time

# TheoryTime = total_time[:] total_time_HZ80
# ------------ Original fp = 40 HZ data ----------------------
HZ40_ele80, HZ40_ele40, HZ40_ele20, HZ40_ele10 = Find_TimeCol(HZ40_80row, HZ40_40row, HZ40_20row, HZ40_10row)
HZ80_ele80, HZ80_ele40, HZ80_ele20, HZ80_ele10 = Find_TimeCol(HZ80_80row, HZ80_40row, HZ80_20row, HZ80_10row)
HZ160_ele80, HZ160_ele40, HZ160_ele20, HZ160_ele10 = Find_TimeCol(HZ160_80row, HZ160_40row, HZ160_20row, HZ160_10row)
HZ320_ele80, HZ320_ele40, HZ320_ele20, HZ320_ele10 = Find_TimeCol(HZ320_80row, HZ320_40row, HZ320_20row, HZ320_10row)

# ================= Calculate_2NormError ===============================
def Calculate_2NormError(TheoryTime,Pwave, Element80,Tie_W20_Mid80row, time_range=(0, 0.20)):
# ------------------------- L-2 Norm Error ------------------------
    common80 = set(TheoryTime) & set(Element80)
    filtered_common80 = [value for value in common80 if time_range[0] <= value <= time_range[1]]
    differences = []
    
    # for common_value in common80:
    for common_value in filtered_common80:
        index1 = np.where(Element80 == common_value)[0][0]
        index2 = np.where(TheoryTime == common_value)[0][0]
        # print(index1,index2)
        diff = Tie_W20_Mid80row[index1, column_index] - Pwave[index2, Analysis_column]
        differences.append(diff)
        
    compare = np.array(differences)
    squared_values = np.square(compare)
    sum_of_squares = np.sum(squared_values)
    result = np.sqrt(sum_of_squares)
    return result, len(compare)

# ================= Calculate_2NormError Normalization ===============================
def Calculate_RelativeL2norm(TheoryTime,Pwave, Element80,Tie_W20_Mid80row, time_range=(0, 0.20)):
# ------------------------- L-2 Norm Error ------------------------
    common80 = set(TheoryTime) & set(Element80)
    filtered_common80 = [value for value in common80 if time_range[0] <= value <= time_range[1]]
    
    differences = []
    Mom = []

    for common_value in common80:
        index1 = np.where(Element80 == common_value)[0][0]
        index2 = np.where(TheoryTime == common_value)[0][0]

        diff = (Tie_W20_Mid80row[index1, column_index] - Pwave[index2, Analysis_column])
        differences.append(diff)
        
        Mother =  Pwave[index2, Analysis_column]
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

def Add_Err(Index,MidTieErr20,MidTie20_error,TheoryTime,Pwave, Element80, Tie_W20_Mid80row, Element40,Tie_W20_Mid40row, Element20,Tie_W20_Mid20row, Element10,Tie_W20_Mid10row):
    MidTieErr20[:,0] = MidTie20_error[:,0] 
# # ===================================== Calculate_L2NormError ============================================================
#     MidTieErr20[0,Index], MidTieErr20[0,2] = Calculate_2NormError(TheoryTime,Pwave, Element80,Tie_W20_Mid80row)
#     MidTieErr20[1,Index], MidTieErr20[1,2] = Calculate_2NormError(TheoryTime,Pwave, Element40,Tie_W20_Mid40row)
#     MidTieErr20[2,Index], MidTieErr20[2,2] = Calculate_2NormError(TheoryTime,Pwave, Element20,Tie_W20_Mid20row)
#     MidTieErr20[3,Index], MidTieErr20[3,2] = Calculate_2NormError(TheoryTime,Pwave, Element10,Tie_W20_Mid10row)
    
# ===================================== Calculate_L2NormError Normalization ============================================================
    MidTieErr20[0,Index], MidTieErr20[0,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Element80,Tie_W20_Mid80row)
    MidTieErr20[1,Index], MidTieErr20[1,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Element40,Tie_W20_Mid40row)
    MidTieErr20[2,Index], MidTieErr20[2,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Element20,Tie_W20_Mid20row)
    MidTieErr20[3,Index], MidTieErr20[3,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Element10,Tie_W20_Mid10row)

HZ40Err_L2 = np.zeros((4,3))
HZ80Err_L2 = np.zeros((4,3))
HZ160Err_L2 = np.zeros((4,3))
HZ320Err_L2 = np.zeros((4,3))

# -----------------L2- Norm Error Calculate-------------------------------------    
Add_Err(1,HZ40Err_L2, HZ40_error, total_time_HZ40, HZ40_Pwave, HZ40_ele80,HZ40_80row, HZ40_ele40,HZ40_40row, HZ40_ele20,HZ40_20row, HZ40_ele10,HZ40_10row)

Add_Err(1,HZ80Err_L2, HZ80_error, total_time_HZ80, HZ80_Pwave, HZ80_ele80,HZ80_80row, HZ80_ele40,HZ80_40row, HZ80_ele20,HZ80_20row, HZ80_ele10,HZ80_10row)
Add_Err(1,HZ160Err_L2, HZ160_error, total_time_HZ160, HZ160_Pwave, HZ160_ele80,HZ160_80row, HZ160_ele40,HZ160_40row, HZ160_ele20,HZ160_20row, HZ160_ele10,HZ160_10row)
Add_Err(1,HZ320Err_L2, HZ320_error, total_time_HZ320, HZ320_Pwave, HZ320_ele80,HZ320_80row, HZ320_ele40,HZ320_40row, HZ320_ele20,HZ320_20row, HZ320_ele10,HZ320_10row)

# ==================Draw L2 Norm error : Middele point =============================
def DifferTime_L2NormError(Peak, HZ40Err_L2, HZ80Err_L2, HZ160Err_L2, HZ320Err_L2):
    plt.figure(figsize=(10,8))
    plt.title(f'{Integrator} L2-Norm Error', fontsize = 25) # Compare / Integrator
    
    font_props = {'family': 'Arial', 'size': 18}
    plt.plot(HZ40Err_L2[:,0], HZ40Err_L2[:,Peak],marker = '^',markersize=12,markerfacecolor = 'white',label = r'$t_d=0.025$ $\mathrm{s}$', linewidth = 3.0)
    plt.plot(HZ80Err_L2[:,0], HZ80Err_L2[:,Peak],marker = 'o',markersize=11,markerfacecolor = 'white',label =  r'$t_d=0.0125$ $\mathrm{s}$', linewidth = 3.0)
    plt.plot(HZ160Err_L2[:,0], HZ160Err_L2[:,Peak],marker = '<',markersize=10,markerfacecolor = 'white',label = r'$t_d=6.25$ $\times 10^{-3}$ $\mathrm{s}$', linewidth = 3.0)
    plt.plot(HZ320Err_L2[:,0], HZ320Err_L2[:,Peak],marker = 's',markersize=9,markerfacecolor = 'white',label = r'$t_d=3.125$ $\times 10^{-3}$ $\mathrm{s}$', linewidth = 3.0)
    
    plt.legend(ncol=1,prop=font_props, loc='lower right') #ncol=2,fontsize=16 frameon=False , loc='upper left'
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    
    plt.xlabel(r'$\Delta_c/\lambda_p$', fontsize = 25) # f'Mesh size ' + r'$\Delta_c$ $\mathrm {(m)}$' / r'$\Delta_c/\lambda_p$'
    plt.ylabel('L2 normalization: '+ r"$\ E_{L2}$" , fontsize = 25) # 'L2 Norm Error: '+ r"$\ E_{L2}$"  / 'L2 normalization: '+ r"$\ E_{L2N}$" 

    # plt.xlim(0.0, 0.20)
    # plt.ylim(-15.0, 15.0)
    plt.grid(True)
    
    ax = plt.gca()
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.125))
    # -------------- Consider X-axis  -----------------------
    ax.set_xscale('log', base=10)
    ax.set_xticks([], minor=False)
    ax.set_xticks([], minor=True)
    x_ticks_Num = np.array([0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4, 0.6])  ## Dy: [0.125, 0.25, 0.50, 1.0] / Dy/H: [0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4, 0.6]
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.2f}' for tick in x_ticks_Num], rotation=0, fontsize=12) # Dy: .3f / Dy/H: .2f
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='both', labelsize= 17)
    # -------------- Consider Y-axis  -----------------------
    ax.set_yscale('log', base=10)
    ax.set_yticks([], minor=False)
    ax.set_yticks([], minor=True)
    y_ticks_Num = np.array([0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4])  # [0.1, 0.2, 0.3, 0.4, 0.5]
    ax.set_yticks(y_ticks_Num)
    ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks_Num], rotation=0, fontsize=12)
    ax.tick_params(axis='y', which='both', labelsize=20)
    # ------- Miner ticks -----------------
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='y', which='minor', length=4, color='gray')
    

# DifferTime_L2NormError(1, HZ40Err_L2, HZ80Err_L2, HZ160Err_L2, HZ320Err_L2) # Dy

# ---------- Compare Dy/lambda_p -----------------
HZ40Err_L2[:,0] = HZ40Err_L2[:,0]/lamb40
HZ80Err_L2[:,0] = HZ80Err_L2[:,0]/lamb80
HZ160Err_L2[:,0] = HZ160Err_L2[:,0]/lamb160
HZ320Err_L2[:,0] = HZ320Err_L2[:,0]/lamb320

DifferTime_L2NormError(1, HZ40Err_L2, HZ80Err_L2, HZ160Err_L2, HZ320Err_L2) # Dy/H

