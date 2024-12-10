# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 11:11:10 2024

@author: User
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
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
# ws_40HZ =  (2*pi)/5 # 0 to 5m = 0 to 2*pi => x = 2*pi/5
# ws_20HZ =  pi/5  # 0 to 10m = 0 to 2*pi => x = pi/5
# ws_10HZ =  pi/10 # 0 to 20m = 0 to 2*pi => x = pi/10

wp_20HZ =  pi/10 # 0 to 20m = 0 to 2*pi => x = pi/10
wp_10HZ =  pi/20 # 0 to 40m = 0 to 2*pi => x = pi/20
wp_40HZ =  pi/5 # 0 to 10m = 0 to 2*pi => x = pi/5

Pwave_HZ = wp_40HZ

HZ = 40
# ============================== Consider PWave ======================================
# calculate eace step time
tns_cp = L/cp # wave transport time
dcell_cp = tns_cp/Nele #each cell time
dt_cp = dcell_cp*0.1 #eace cell have 10 steps
print(f"Pwave travel = {tns_cp} ;dcell = {dcell_cp} ;dt = {dt_cp}")

time_cp = np.arange(0.0, 0.02503,dt_cp)
Nt_cp = len(time_cp)

#----------- Soil Coordinate --------------
x = cp*time_cp #m
def Incoming_wave(w, x, cp, t):  #事實上為（xi,yi,t），空間跟時間資訊全寫進去，目前只用到yi的空間
    return np.sin(w*(x-cp*t)) # Normal：np.sin(w*(x-cs*t))

def Outgoing_wave(w, x, cp, t):
    return np.sin(w*(x+cp*t)) # Norrmal： np.sin(w*(x+cs*t))

Nnode = Nele + 1
End_Node = Nele
dy = L/Nele # 1, 0.1
dx= dy/10 # 0.1, 0.01 each element have 10 step dx

total_Transport_cp = np.arange(0.0,20.1, dx)

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
        if total_time[t] < 0.025:
            Pwave[to+t,g] = (Pwave[to+t,g] + Cp_vel_Coefficient*XIn[to+t,g])  # original wave transport
            
        if total_time[t] >= 0.025 and total_time[t] <= 0.050:
            Pwave[to+t,End_Ele-g] = Pwave[to+t,End_Ele-g] + Cp_vel_Coefficient*XIn[t-to,End_Ele-g]   # XOut[t-to,End_Ele-g]

row80 = f'node161'
row40 = f'node81'
row20 = f'node41'
row10 = f'node21'

Integrator = f'Newmark Constant' # Central Differential / HHT_Alpha / Newmark Linear / Newmark Constant

Condition1 =  f"Test_Integrator/{Integrator}/Dt_0.2"# 
file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/row80/Velocity/{row80}.out"
file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/row40/Velocity/{row40}.out"
file3 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/row20/Velocity/{row20}.out"
file4 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/row10/Velocity/{row10}.out"

Dt02_80row = rdnumpy(file1)
Dt02_40row = rdnumpy(file2)
Dt02_20row = rdnumpy(file3)
Dt02_10row = rdnumpy(file4)

Condition2 =  f"Test_Integrator/{Integrator}/Dt_0.4"# 
file5 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/row80/Velocity/{row80}.out"
file6 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/row40/Velocity/{row40}.out"
file7 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/row20/Velocity/{row20}.out"
file8 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/row10/Velocity/{row10}.out"

Dt04_80row = rdnumpy(file5)
Dt04_40row = rdnumpy(file6)
Dt04_20row = rdnumpy(file7)
Dt04_10row = rdnumpy(file8)

Condition3 =  f"Test_Integrator/{Integrator}/Dt_0.6"# 
file9 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/row80/Velocity/{row80}.out"
file10 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/row40/Velocity/{row40}.out"
file11 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/row20/Velocity/{row20}.out"
file12 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/row10/Velocity/{row10}.out"

Dt06_80row = rdnumpy(file9)
Dt06_40row = rdnumpy(file10)
Dt06_20row = rdnumpy(file11)
Dt06_10row = rdnumpy(file12)

# Integrator2 = f'Test_Newmark_Linear' # ****
Condition4 =  f"Test_Integrator/{Integrator}/Dt_0.8"# 
file13 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/row80/Velocity/{row80}.out"
file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/row40/Velocity/{row40}.out"
file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/row20/Velocity/{row20}.out"
file16 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/row10/Velocity/{row10}.out"

Dt08_80row = rdnumpy(file13)
Dt08_40row = rdnumpy(file14)
Dt08_20row = rdnumpy(file15)
Dt08_10row = rdnumpy(file16)

Condition5 =  f"Test_Integrator/{Integrator}/Dt_1.0"# 
file17 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/row80/Velocity/{row80}.out"
file18 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/row40/Velocity/{row40}.out"
file19 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/row20/Velocity/{row20}.out"
file20 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/row10/Velocity/{row10}.out"

Dt10_80row = rdnumpy(file17)
Dt10_40row = rdnumpy(file18)
Dt10_20row = rdnumpy(file19)
Dt10_10row = rdnumpy(file20)

Condition6 =  f"Test_Integrator/{Integrator}/Dt_1.2"# 
file21 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/row80/Velocity/{row80}.out"
file22 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/row40/Velocity/{row40}.out"
file23 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/row20/Velocity/{row20}.out"
file24 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/row10/Velocity/{row10}.out"

Dt12_80row = rdnumpy(file21)
Dt12_40row = rdnumpy(file22)
Dt12_20row = rdnumpy(file23)
Dt12_10row = rdnumpy(file24)

Condition7 =  f"Test_Integrator/{Integrator}/Dt_1.4"# 
file25 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/row80/Velocity/{row80}.out"
file26 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/row40/Velocity/{row40}.out"
file27 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/row20/Velocity/{row20}.out"
file28 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/row10/Velocity/{row10}.out"

Dt14_80row = rdnumpy(file25)
Dt14_40row = rdnumpy(file26)
Dt14_20row = rdnumpy(file27)
Dt14_10row = rdnumpy(file28)

Condition8 =  f"Test_Integrator/{Integrator}/Dt_1.6"# 
file29 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/row80/Velocity/{row80}.out"
file30 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/row40/Velocity/{row40}.out"
file31 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/row20/Velocity/{row20}.out"
file32 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/row10/Velocity/{row10}.out"

Dt16_80row = rdnumpy(file29)
Dt16_40row = rdnumpy(file30)
Dt16_20row = rdnumpy(file31)
Dt16_10row = rdnumpy(file32)

Condition9 =  f"Test_Integrator/{Integrator}/Dt_1.8"# 
file33 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/row80/Velocity/{row80}.out"
file34 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/row40/Velocity/{row40}.out"
file35 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/row20/Velocity/{row20}.out"
file36 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/row10/Velocity/{row10}.out"

Dt18_80row = rdnumpy(file33)
Dt18_40row = rdnumpy(file34)
Dt18_20row = rdnumpy(file35)
Dt18_10row = rdnumpy(file36)

def CompareDt_DiffVel(titleName, D80_Dt10, D80_Dt11, D80_Dt12, D80_Dt14):
    plt.figure(figsize=(10,8))
    plt.title(titleName, fontsize = 28)
# ------------------- Theory ------------------------------
    plt.plot(total_time, Pwave[:,79],label =r'$\mathrm{Analytical}$',color= 'dimgray',linewidth=3.5)
    
# -----------------Test Integrator Differ Mesh -------------------------   
    plt.plot(D80_Dt10[:,0], D80_Dt10[:, 2], label = r'$\Delta_{c} = 0.0125H$', color= 'limegreen',marker = 'o',markersize=12, markerfacecolor = 'none' , markevery=50, mew=2.0, linewidth=2.0) # , ls = '--' 
    plt.plot(D80_Dt11[:,0], D80_Dt11[:, 2], label = r'$\Delta_{c} = 0.0250H$', color= 'darkorange',marker = '^',markersize=12,markerfacecolor = 'none' , markevery=50, mew=2.0, linewidth=2.0) # , ls = '-.', mediumorchid
    plt.plot(D80_Dt12[:,0], D80_Dt12[:, 2], label = r'$\Delta_{c} = 0.0500H$', color= 'mediumblue',marker = 's',markersize=12,markerfacecolor = 'none' , markevery=52, mew=2.0, linewidth=2.0) # , ls = ':'
    plt.plot(D80_Dt14[:,0], D80_Dt14[:, 2], label = r'$\Delta_{c} = 0.1000H$', color= 'crimson',marker = '<',markersize=12,markerfacecolor = 'none' , markevery=55, mew=2.0, linewidth= 2.0) # , ls = ':'
    
    # plt.grid(True)
    # ========== set up figure thick ============================
    bwidth = 2
    TK = plt.gca()
    TK.spines['bottom'].set_linewidth(bwidth)
    TK.spines['left'].set_linewidth(bwidth)
    TK.spines['top'].set_linewidth(bwidth)
    TK.spines['right'].set_linewidth(bwidth)
    
    legend1 = plt.legend(fontsize=22) # loc='lower left',
    legend1.get_frame().set_edgecolor('grey')
    legend1.get_frame().set_linewidth(2)  # 設置外框寬度
    
    plt.xlim(0, 0.2)
    plt.ylim(-0.75, 0.75)
    
    plt.xlabel(r"$\mathrm {time}$ ${t}$ $\mathrm {(s)}$", fontsize = 28) # r"$G^{'}/G$"
    plt.ylabel(r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", fontsize = 28)  # r"$m_{x'}/m_{x}$"
    plt.xticks(fontsize = 18, fontweight='bold', color='black')
    plt.yticks(fontsize = 18, fontweight='bold', color='black')
    
    ax = plt.gca()
    ax.tick_params(axis='x', which='major', labelsize= 23, length=8, width=2)
    
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.50)) # 0.25
    ax.tick_params(axis='y', which='major', labelsize= 23, length=8, width=2)
    # ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    # ax.yaxis.get_offset_text().set(size=18)

Compare = f'HHT-'+r'$\alpha$'
# # ================ Compare/ Integrator ====
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 0.2$ $\Delta_{tp}$', Dt02_80row, Dt02_40row, Dt02_20row, Dt02_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 0.4$ $\Delta_{tp}$', Dt04_80row, Dt04_40row, Dt04_20row, Dt04_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 0.6$ $\Delta_{tp}$', Dt06_80row, Dt06_40row, Dt06_20row, Dt06_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 0.8$ $\Delta_{tp}$', Dt08_80row, Dt08_40row, Dt08_20row, Dt08_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 1.0$ $\Delta_{tp}$', Dt10_80row, Dt10_40row, Dt10_20row, Dt10_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 1.2$ $\Delta_{tp}$', Dt12_80row, Dt12_40row, Dt12_20row, Dt12_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 1.4$ $\Delta_{tp}$', Dt14_80row, Dt14_40row, Dt14_20row, Dt14_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 1.6$ $\Delta_{tp}$', Dt16_80row, Dt16_40row, Dt16_20row, Dt16_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 1.8$ $\Delta_{tp}$', Dt18_80row, Dt18_40row, Dt18_20row, Dt18_10row)

# ================================== Prepare Relative Error and Absolute Error ============================
# def process_column(matrix, column_index):
#     column = matrix[:, column_index]
#     abs_column = np.abs(column)
    
#     max_index = np.argmax(abs_column)
#     max_peak = np.max(abs_column)
    
    
#     print(f'max_value= {max_peak}; max_index= {max_index}')
#     return max_peak

start_time = 0.0
end_time = 0.20 # 0.035
def process_column(matrix, column_index):
    # 选择在指定时间范围内的数据
    time_column = matrix[:, 0]
    column = matrix[:, column_index]
    
    # 限定在时间范围内
    within_time_range = (time_column >= start_time) & (time_column <= end_time)
    filtered_column = column[within_time_range]
    
    # 计算绝对值并找出最大值
    abs_filtered_column = np.abs(filtered_column)
    max_peak = np.max(abs_filtered_column)
    max_index = np.argmax(abs_filtered_column)
    
    print(f'max_value= {max_peak}; max_index= {max_index}')
    return max_peak

# =========== Find Grounf Surface Max/ Min Peak Value ==========================
column_index = 2 # Pwave = 2 (yaxis)
Analysis_column = 79
# =================================== Middle Node ===================================
# ------------ Dt = 0.2-----------------------
maxDt02_80row = process_column(Dt02_80row, column_index)
maxDt02_40row = process_column(Dt02_40row, column_index)
maxDt02_20row = process_column(Dt02_20row, column_index)
maxDt02_10row = process_column(Dt02_10row, column_index)
# ------------ Dt = 0.4-----------------------
maxDt04_80row = process_column(Dt04_80row, column_index)
maxDt04_40row = process_column(Dt04_40row, column_index)
maxDt04_20row = process_column(Dt04_20row, column_index)
maxDt04_10row = process_column(Dt04_10row, column_index)
# ------------ Dt = 0.6-----------------------
maxDt06_80row = process_column(Dt06_80row, column_index)
maxDt06_40row = process_column(Dt06_40row, column_index)
maxDt06_20row = process_column(Dt06_20row, column_index)
maxDt06_10row = process_column(Dt06_10row, column_index)
# ------------ Dt = 0.8-----------------------
maxDt08_80row = process_column(Dt08_80row, column_index)
maxDt08_40row = process_column(Dt08_40row, column_index)
maxDt08_20row = process_column(Dt08_20row, column_index)
maxDt08_10row = process_column(Dt08_10row, column_index)
# ------------ Dt = 1.0-----------------------
maxDt10_80row = process_column(Dt10_80row, column_index)
maxDt10_40row = process_column(Dt10_40row, column_index)
maxDt10_20row = process_column(Dt10_20row, column_index)
maxDt10_10row = process_column(Dt10_10row, column_index)
# ------------ Dt = 1.2-----------------------
maxDt12_80row = process_column(Dt12_80row, column_index)
maxDt12_40row = process_column(Dt12_40row, column_index)
maxDt12_20row = process_column(Dt12_20row, column_index)
maxDt12_10row = process_column(Dt12_10row, column_index)

# ------------ Dt = 1.4-----------------------
maxDt14_80row = process_column(Dt14_80row, column_index)
maxDt14_40row = process_column(Dt14_40row, column_index)
maxDt14_20row = process_column(Dt14_20row, column_index)
maxDt14_10row = process_column(Dt14_10row, column_index)
# ------------ Dt = 1.6-----------------------
maxDt16_80row = process_column(Dt16_80row, column_index)
maxDt16_40row = process_column(Dt16_40row, column_index)
maxDt16_20row = process_column(Dt16_20row, column_index)
maxDt16_10row = process_column(Dt16_10row, column_index)
# ------------ Dt = 1.8-----------------------
maxDt18_80row = process_column(Dt18_80row, column_index)
maxDt18_40row = process_column(Dt18_40row, column_index)
maxDt18_20row = process_column(Dt18_20row, column_index)
maxDt18_10row = process_column(Dt18_10row, column_index)

def Find_ColMaxValue(column_index,ele80_Mid):
    column = ele80_Mid[:, column_index]
    max_value = np.max(column)
    max_index = np.argmax(column)
    
    min_value = np.min(column)
    min_index = np.argmin(column)

    print(f'max_value= {max_value}; max_index= {max_index}; min_value= {min_value}; min_index= {min_index}')
    return(max_value,min_value)

maxAnaly, minAnaly = Find_ColMaxValue(Analysis_column,Pwave)

Mesh_Size = np.zeros(4)
ele = 80 
for m in range(len(Mesh_Size)):
    if m == 0 :    
        Mesh_Size[m] = L/ (ele)
    if m > 0:    
        Mesh_Size[m] = Mesh_Size[m-1]*2

def errMatrix(error_dc,maxDt02_80row,maxDt02_40row,maxDt02_20row,maxDt02_10row):
    error_dc[:,0] = Mesh_Size[:]
    error_dc[0,1] = maxDt02_80row
    error_dc[1,1] = maxDt02_40row
    error_dc[2,1] = maxDt02_20row
    error_dc[3,1] = maxDt02_10row
    return error_dc

# ============================= Middle Node ========================================
# ------------Dt = 0.2 Error Peak Value-----------------------
Dt02_error = np.zeros((4,2))
errMatrix(Dt02_error, maxDt02_80row, maxDt02_40row, maxDt02_20row, maxDt02_10row)
# ------------Dt = 0.4 Error Peak Value-----------------------
Dt04_error = np.zeros((4,2))
errMatrix(Dt04_error, maxDt04_80row, maxDt04_40row, maxDt04_20row, maxDt04_10row)
# ------------Dt = 0.6 Error Peak Value-----------------------
Dt06_error = np.zeros((4,2))
errMatrix(Dt06_error, maxDt06_80row, maxDt06_40row, maxDt06_20row, maxDt06_10row)
# ------------Dt = 0.8 Error Peak Value-----------------------
Dt08_error = np.zeros((4,2))
errMatrix(Dt08_error, maxDt08_80row, maxDt08_40row, maxDt08_20row, maxDt08_10row)
# ------------Dt = 1.0 Error Peak Value-----------------------
Dt10_error = np.zeros((4,2))
errMatrix(Dt10_error, maxDt10_80row, maxDt10_40row, maxDt10_20row, maxDt10_10row)
# ------------Dt = 1.2 Error Peak Value-----------------------
Dt12_error = np.zeros((4,2))
errMatrix(Dt12_error, maxDt12_80row, maxDt12_40row, maxDt12_20row, maxDt12_10row)

# calculate_Error()
Dt02_err = np.zeros((4,2))
Dt04_err = np.zeros((4,2))
Dt06_err = np.zeros((4,2))
Dt08_err = np.zeros((4,2))
Dt10_err = np.zeros((4,2))
Dt12_err = np.zeros((4,2))

# ------------Dt = 1.4 Error Peak Value-----------------------
Dt14_error = np.zeros((4,2))
errMatrix(Dt14_error, maxDt14_80row, maxDt14_40row, maxDt14_20row, maxDt14_10row)
# ------------Dt = 1.6 Error Peak Value-----------------------
Dt16_error = np.zeros((4,2))
errMatrix(Dt16_error, maxDt16_80row, maxDt16_40row, maxDt16_20row, maxDt16_10row)
# ------------Dt = 1.8 Error Peak Value-----------------------
Dt18_error = np.zeros((4,2))
errMatrix(Dt18_error, maxDt18_80row, maxDt18_40row, maxDt18_20row, maxDt18_10row)

Dt14_err = np.zeros((4,2))
Dt16_err = np.zeros((4,2))
Dt18_err = np.zeros((4,2))

def Calculate_Error(TieErr, Tie_error):
    for i in range(len(Mesh_Size)):
        TieErr[:,0] = Tie_error[:,0]
# ------------------------- Absolute Relative Error ------------------        
        TieErr[i,1] = ((Tie_error[i,1] - maxAnaly)/maxAnaly)*100
        # TieErr[i,2] = ((Tie_error[i,2] - minAnaly)/minAnaly)*100
        
Calculate_Error(Dt02_err, Dt02_error)
Calculate_Error(Dt04_err, Dt04_error)
Calculate_Error(Dt06_err, Dt06_error)
Calculate_Error(Dt08_err, Dt08_error)
Calculate_Error(Dt10_err, Dt10_error)
Calculate_Error(Dt12_err, Dt12_error)

Calculate_Error(Dt14_err, Dt14_error)
Calculate_Error(Dt16_err, Dt16_error)
Calculate_Error(Dt18_err, Dt18_error)

# # -------- For Newmark Linear to deal with Draw ------------------
# Dt18_err[0, 1] = Dt18_err[0, 1]*1e+11
# ==================Draw Relative error : Middele point =============================
def DifferTime_elemetError(Peak, Dt02_err, Dt04_err, Dt06_err, Dt08_err, Dt10_err, Dt12_err, Dt14_err, Dt16_err, Dt18_err): # , Dt12_err, Dt14_err, Dt16_err, Dt18_err
    plt.figure(figsize=(10,8))
    # plt.title(f'{Integrator} Relative Error', fontsize = 25) # Compare / Integrator
    plt.text(0.01, 0.94, f'{Integrator}', fontsize = 28, color= 'black', transform=plt.gca().transAxes) # 0.9 / 0.08
    
    font_props = {'family': 'Arial', 'size': 20}
    plt.plot(Dt02_err[:,0], Dt02_err[:,Peak],marker = '^',markersize=12,markerfacecolor = 'none',label = r'$C = 0.2$', linewidth = 2.0, color = 'dimgray')
    plt.plot(Dt04_err[:,0], Dt04_err[:,Peak],marker = 'o',markersize=12,markerfacecolor = 'none',label = r'$C = 0.4$', linewidth = 2.0, color = 'darkorange')
    plt.plot(Dt06_err[:,0], Dt06_err[:,Peak],marker = '<',markersize=12,markerfacecolor = 'none',label = r'$C = 0.6$', linewidth = 2.0, color = 'limegreen')
    plt.plot(Dt08_err[:,0], Dt08_err[:,Peak],marker = 's',markersize=12,markerfacecolor = 'none',label = r'$C = 0.8$', linewidth = 2.0, color = 'mediumblue')
    plt.plot(Dt10_err[:,0], Dt10_err[:,Peak],marker = 'p',markersize=12,markerfacecolor = 'none',label = r'$C = 1.0$', linewidth = 2.0, color = 'crimson')
    plt.plot(Dt12_err[:,0], Dt12_err[:,Peak],marker = '*',markersize=12,markerfacecolor = 'none',label = r'$C = 1.2$', linewidth = 2.0, color = 'tab:brown')
    plt.plot(Dt14_err[:,0], Dt14_err[:,Peak],marker = '+',markersize=12,markerfacecolor = 'none',label = r'$C = 1.4$', linewidth = 2.0, color = 'darkviolet')
    plt.plot(Dt16_err[:,0], Dt16_err[:,Peak],marker = 'x',markersize=12,markerfacecolor = 'none',label = r'$C = 1.6$', linewidth = 2.0, color = 'goldenrod')
    # plt.plot(Dt18_err[:,0], Dt18_err[:,Peak],marker = 'D',markersize=12,markerfacecolor = 'none',label = r'$C = 1.8$', linewidth = 2.0, color = 'magenta')
    
    legend1 = plt.legend(ncol=2,prop=font_props, loc= (0.02, 0.02)) #ncol=2,fontsize=16 frameon=False , loc='upper left'
    legend1.get_frame().set_edgecolor('grey')
    legend1.get_frame().set_linewidth(2)  # 設置外框寬度
    
    plt.xticks(fontsize = 22, fontweight='bold', color='black')
    plt.yticks(fontsize = 22, fontweight='bold', color='black')
    
    plt.xlabel(f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', fontsize = 26)
    plt.ylabel('Peak Velocity Error '+ r"$\ E_{Max}$" + r" (%)", fontsize = 28)

    # plt.xlim(0.0, 0.20)
    plt.ylim(-15.0, 15.0) # -15.0, 15.0 / -5.0, 5.0
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
    x_ticks_Num = np.array([0.125, 0.25, 0.50, 1.0])  # 设置线性刻度间距为0.125
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.3f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='major', labelsize= 25, length=8, width=2)
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.125))
    
    
    # ax.set_yscale('log', base=10)
    ax.tick_params(axis = 'y', which='major', labelsize= 25, length=8, width=2)
    
    # # ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
    # ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    # ax.yaxis.get_offset_text().set(size=18)

# DifferTime_elemetError(1, Dt02_err, Dt04_err, Dt06_err, Dt08_err, Dt10_err, Dt12_err, Dt14_err, Dt16_err, Dt18_err) # , Dt12_err, Dt14_err, Dt16_err, Dt18_err

# ================================== Prepare L2-Norm Error ============================
# # ---------- Find Different Dt in 80, 40, 20, 10 row Same Time ---------------------
def Find_TimeCol(Dt02_80row, Dt02_40row, Dt02_20row, Dt02_10row):
    Ele80_Time = Dt02_80row[:,0]
    Ele40_Time = Dt02_40row[:,0]
    Ele20_Time = Dt02_20row[:,0]
    Ele10_Time = Dt02_10row[:,0]
    
    return Ele80_Time, Ele40_Time, Ele20_Time, Ele10_Time

TheoryTime = total_time[:]
Dt02_ele80, Dt02_ele40, Dt02_ele20, Dt02_ele10 = Find_TimeCol(Dt02_80row, Dt02_40row, Dt02_20row, Dt02_10row)
Dt04_ele80, Dt04_ele40, Dt04_ele20, Dt04_ele10 = Find_TimeCol(Dt04_80row, Dt04_40row, Dt04_20row, Dt04_10row)
Dt06_ele80, Dt06_ele40, Dt06_ele20, Dt06_ele10 = Find_TimeCol(Dt06_80row, Dt06_40row, Dt06_20row, Dt06_10row)
Dt08_ele80, Dt08_ele40, Dt08_ele20, Dt08_ele10 = Find_TimeCol(Dt08_80row, Dt08_40row, Dt08_20row, Dt08_10row)
Dt10_ele80, Dt10_ele40, Dt10_ele20, Dt10_ele10 = Find_TimeCol(Dt10_80row, Dt10_40row, Dt10_20row, Dt10_10row)

Dt12_ele80, Dt12_ele40, Dt12_ele20, Dt12_ele10 = Find_TimeCol(Dt12_80row, Dt12_40row, Dt12_20row, Dt12_10row)
Dt14_ele80, Dt14_ele40, Dt14_ele20, Dt14_ele10 = Find_TimeCol(Dt14_80row, Dt14_40row, Dt14_20row, Dt14_10row)
Dt16_ele80, Dt16_ele40, Dt16_ele20, Dt16_ele10 = Find_TimeCol(Dt16_80row, Dt16_40row, Dt16_20row, Dt16_10row)
Dt18_ele80, Dt18_ele40, Dt18_ele20, Dt18_ele10 = Find_TimeCol(Dt18_80row, Dt18_40row, Dt18_20row, Dt18_10row)

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

def Add_Err(Index,MidTieErr20,MidTie20_error, Element80, Tie_W20_Mid80row, Element40,Tie_W20_Mid40row, Element20,Tie_W20_Mid20row, Element10,Tie_W20_Mid10row):
    MidTieErr20[:,0] = MidTie20_error[:,0] 
# # ===================================== Calculate_L2NormError ============================================================
#     MidTieErr20[0,Index], MidTieErr20[0,2] = Calculate_2NormError(TheoryTime,Pwave, Element80,Tie_W20_Mid80row)
#     MidTieErr20[1,Index], MidTieErr20[1,2] = Calculate_2NormError(TheoryTime,Pwave, Element40,Tie_W20_Mid40row)
#     MidTieErr20[2,Index], MidTieErr20[2,2] = Calculate_2NormError(TheoryTime,Pwave, Element20,Tie_W20_Mid20row)
#     MidTieErr20[3,Index], MidTieErr20[3,2] = Calculate_2NormError(TheoryTime,Pwave, Element10,Tie_W20_Mid10row)
    
# ===================================== Calculate_L2NormError Normalization ============================================================
    MidTieErr20[0,Index], MidTieErr20[0,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Element80,Tie_W20_Mid80row, time_range=(0, 0.20))
    MidTieErr20[1,Index], MidTieErr20[1,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Element40,Tie_W20_Mid40row, time_range=(0, 0.20))
    MidTieErr20[2,Index], MidTieErr20[2,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Element20,Tie_W20_Mid20row, time_range=(0, 0.20))
    MidTieErr20[3,Index], MidTieErr20[3,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Element10,Tie_W20_Mid10row, time_range=(0, 0.20))
    
Dt02Err_L2 = np.zeros((4,3))
Dt04Err_L2 = np.zeros((4,3))
Dt06Err_L2 = np.zeros((4,3))
Dt08Err_L2 = np.zeros((4,3))
Dt10Err_L2 = np.zeros((4,3))
Dt12Err_L2 = np.zeros((4,3))
Dt14Err_L2 = np.zeros((4,3))
Dt16Err_L2 = np.zeros((4,3))
Dt18Err_L2 = np.zeros((4,3))

# -----------------L2- Norm Error Calculate-------------------------------------    
Add_Err(1,Dt02Err_L2, Dt02_error, Dt02_ele80, Dt02_80row, Dt02_ele40,Dt02_40row, Dt02_ele20,Dt02_20row, Dt02_ele10,Dt02_10row)
Add_Err(1,Dt04Err_L2, Dt04_error, Dt04_ele80, Dt04_80row, Dt04_ele40,Dt04_40row, Dt04_ele20,Dt04_20row, Dt04_ele10,Dt04_10row)
Add_Err(1,Dt06Err_L2, Dt06_error, Dt06_ele80, Dt06_80row, Dt06_ele40,Dt06_40row, Dt06_ele20,Dt06_20row, Dt06_ele10,Dt06_10row)
Add_Err(1,Dt08Err_L2, Dt08_error, Dt08_ele80, Dt08_80row, Dt08_ele40,Dt08_40row, Dt08_ele20,Dt08_20row, Dt08_ele10,Dt08_10row)
Add_Err(1,Dt10Err_L2, Dt10_error, Dt10_ele80, Dt10_80row, Dt10_ele40,Dt10_40row, Dt10_ele20,Dt10_20row, Dt10_ele10,Dt10_10row)

Add_Err(1,Dt12Err_L2, Dt12_error, Dt12_ele80, Dt12_80row, Dt12_ele40,Dt12_40row, Dt12_ele20,Dt12_20row, Dt12_ele10,Dt12_10row)
Add_Err(1,Dt14Err_L2, Dt14_error, Dt14_ele80, Dt14_80row, Dt14_ele40,Dt14_40row, Dt14_ele20,Dt14_20row, Dt14_ele10,Dt14_10row)
Add_Err(1,Dt16Err_L2, Dt16_error, Dt16_ele80, Dt16_80row, Dt16_ele40,Dt16_40row, Dt16_ele20,Dt16_20row, Dt16_ele10,Dt16_10row)
Add_Err(1,Dt18Err_L2, Dt18_error, Dt18_ele80, Dt18_80row, Dt18_ele40,Dt18_40row, Dt18_ele20,Dt18_20row, Dt18_ele10,Dt18_10row)

# ==================Draw L2 Norm error : Middele point =============================
def DifferTime_L2NormError(Peak, Dt02_err, Dt04_err, Dt06_err, Dt08_err, Dt10_err, Dt12_err, Dt14_err, Dt16_err, Dt18_err): # , Dt12_err, Dt14_err, Dt16_err, Dt18_err
    plt.figure(figsize=(10,8))
    # plt.title(f'{Integrator} L2-Norm Error', fontsize = 25) # Compare / Integrator
    plt.text(0.01, 0.94, f'{Integrator}', fontsize = 28, color= 'black', transform=plt.gca().transAxes)
    
    font_props = {'family': 'Arial', 'size': 20}
    plt.plot(Dt02_err[:,0], Dt02_err[:,Peak],marker = '^',markersize=12,markerfacecolor = 'none',label = r'$C = 0.2$', linewidth = 3.0 ,color = 'dimgray')
    plt.plot(Dt04_err[:,0], Dt04_err[:,Peak],marker = 'o',markersize=12,markerfacecolor = 'none',label = r'$C = 0.4$', linewidth = 3.0 ,color = 'darkorange')
    plt.plot(Dt06_err[:,0], Dt06_err[:,Peak],marker = '<',markersize=12,markerfacecolor = 'none',label = r'$C = 0.6$', linewidth = 3.0 ,color = 'limegreen')
    plt.plot(Dt08_err[:,0], Dt08_err[:,Peak],marker = 's',markersize=12,markerfacecolor = 'none',label = r'$C = 0.8$', linewidth = 3.0 ,color = 'mediumblue')
    plt.plot(Dt10_err[:,0], Dt10_err[:,Peak],marker = 'p',markersize=12,markerfacecolor = 'none',label = r'$C = 1.0$', linewidth = 3.0 ,color = 'crimson')
    plt.plot(Dt12_err[:,0], Dt12_err[:,Peak],marker = '*',markersize=12,markerfacecolor = 'none',label = r'$C = 1.2$', linewidth = 3.0, color = 'tab:brown')
    plt.plot(Dt14_err[:,0], Dt14_err[:,Peak],marker = '+',markersize=12,markerfacecolor = 'none',label = r'$C = 1.4$', linewidth = 3.0, color = 'darkviolet')
    plt.plot(Dt16_err[:,0], Dt16_err[:,Peak],marker = 'x',markersize=12,markerfacecolor = 'none',label = r'$C = 1.6$', linewidth = 3.0,color = 'goldenrod')
    plt.plot(Dt18_err[:,0], Dt18_err[:,Peak],marker = 'D',markersize=12,markerfacecolor = 'none',label = r'$C = 1.8$', linewidth = 3.0,color = 'magenta')
    
    legend1 = plt.legend(ncol=2,prop=font_props, loc=(0.43, 0.01)) #ncol=2,fontsize=16 frameon=False , loc='upper left'
    legend1.get_frame().set_edgecolor('grey')
    legend1.get_frame().set_linewidth(2)  # 設置外框寬度
    
    plt.xticks(fontsize = 20, fontweight='bold', color='black')
    plt.yticks(fontsize = 20, fontweight='bold', color='black')
    
    plt.xlabel(f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', fontsize = 26)
    plt.ylabel('Normalized L2 Norm Error '+ r"$\ E_{L2}$" , fontsize = 28) # 'L2 Norm Error: '+ r"$\ E_{L2}$"  / 'L2 normalization: '+ r"$\ E_{L2N}$" 

    # plt.xlim(0.0, 0.20)
    # plt.ylim(-15.0, 15.0)
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
    x_ticks_Num = np.array([0.125, 0.25, 0.50, 1.0])  # 设置线性刻度间距为0.125
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.3f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='major', labelsize= 25, length=8, width=2)
    # -------------- Consider Y-axis  -----------------------
    ax.set_yscale('log', base=10)
    ax.set_yticks([], minor=False)
    ax.set_yticks([], minor=True)
    y_ticks_Num = np.array([0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4])  # 0.1, 0.2, 0.3, 0.4, 0.5, 0.6
    ax.set_yticks(y_ticks_Num)
    ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks_Num], rotation=0, fontsize=12)
    ax.tick_params(axis='y', which='major', labelsize= 25, length=8, width=2)
    # ------- Miner ticks -----------------
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='y', which='minor', length=4, width=2, color='gray')   

    ax.set_ylim(0.0, 0.5)  # 例如从0.1到10

# DifferTime_L2NormError(1, Dt02Err_L2, Dt04Err_L2, Dt06Err_L2, Dt08Err_L2, Dt10Err_L2, Dt12Err_L2, Dt14Err_L2, Dt16Err_L2, Dt18Err_L2)

# ================= Consider C data as X-axis ==============================
C_Data = np.arange(0.2, 1.8, 0.2)# np.arange(0.2, 2.0, 0.2) / Central (0.2, 1.2, 0.2) / Linear (0.2, 1.8, 0.2)
Dy80row_err = np.zeros((len(C_Data),2))
Dy40row_err = np.zeros((len(C_Data),2))
Dy20row_err = np.zeros((len(C_Data),2))
Dy10row_err = np.zeros((len(C_Data),2))

# ------------- For Relative Error -------------------
def C_Relative(C_Data, Dy80row_err, Mesh_Num):
    Dy80row_err[:,0] = C_Data[:]
    Dy80row_err[0,1] = Dt02_err[Mesh_Num, 1]
    Dy80row_err[1,1] = Dt04_err[Mesh_Num, 1]
    Dy80row_err[2,1] = Dt06_err[Mesh_Num, 1]
    Dy80row_err[3,1] = Dt08_err[Mesh_Num, 1]
    Dy80row_err[4,1] = Dt10_err[Mesh_Num, 1]
    Dy80row_err[5,1] = Dt12_err[Mesh_Num, 1]
    Dy80row_err[6,1] = Dt14_err[Mesh_Num, 1]
    Dy80row_err[7,1] = Dt16_err[Mesh_Num, 1]
    # Dy80row_err[8,1] = Dt18_err[Mesh_Num, 1]#  ; 2.62104e+10
    return Dy80row_err
# ---------- Mesh Size = 80, 40, 20, 10 row -------------
C_Relative(C_Data, Dy80row_err, 0)
C_Relative(C_Data, Dy40row_err, 1)
C_Relative(C_Data, Dy20row_err, 2)
C_Relative(C_Data, Dy10row_err, 3)

# ==================Draw Relative error : X-axis = C data =============================
def DifferTime_elemetError2(Dy80row_err, Dy40row_err, Dy20row_err, Dy10row_err): 
    plt.figure(figsize=(10,8))
    # plt.title(f'{Integrator} Relative Error', fontsize = 25) # Compare / Integrator
    plt.text(0.01, 0.95, f'{Integrator}', fontsize = 28, color= 'black', transform=plt.gca().transAxes)
    
    # plt.text(0.04, 0.86, r'$C_{cr}=$ $\mathrm{infinite}$', fontsize=28, transform=plt.gca().transAxes)
    plt.text(0.92, 0.15, r'$C_{cr} = 1.73$', fontsize= 28, transform=plt.gca().transAxes, rotation=270) # 0.75, 0.25, r'$C_{cr} = 1.0$' / 0.92, 0.15, r'$C_{cr} = 1.73$'
    
    font_props = {'family': 'Arial', 'size': 20}
    plt.plot(Dy80row_err[:,0], Dy80row_err[:,1],marker = '^',markersize=12,markerfacecolor = 'none',label = r'$\Delta_c =  $ $\mathrm {0.125m}$', linewidth = 3.0, color = 'limegreen')
    plt.plot(Dy40row_err[:,0], Dy40row_err[:,1],marker = 'o',markersize=12,markerfacecolor = 'none',label =  r'$\Delta_c = $ $\mathrm {0.250m}$', linewidth = 3.0, color = 'darkorange') # , ls = ':'
    plt.plot(Dy20row_err[:,0], Dy20row_err[:,1],marker = '<',markersize=12,markerfacecolor = 'none',label = r'$\Delta_c = $ $\mathrm {0.500m}$', linewidth = 3.0, color = 'mediumblue') # , ls= '-.'
    plt.plot(Dy10row_err[:,0], Dy10row_err[:,1],marker = 's',markersize=12,markerfacecolor = 'none',label = r'$\Delta_c = $ $\mathrm {1.000m}$', linewidth = 3.0, color = 'crimson')# , ls = '--'
    
    legend1 = plt.legend(ncol= 1,prop=font_props, loc='lower left') #ncol=2,fontsize=16 frameon=False , loc='upper left'
    legend1.get_frame().set_edgecolor('grey')
    legend1.get_frame().set_linewidth(2)  # 設置外框寬度
    
    plt.xticks(fontsize = 20, fontweight='bold', color='black')
    plt.yticks(fontsize = 22, fontweight='bold', color='black')
    
    plt.xlabel(f'Time Increment Ratio ' +r'$C$', fontsize = 28)
    plt.ylabel('Peak Velocity Error '+ r"$\ E_{Max}$" + r" (%)", fontsize = 28)

    plt.xlim(0.2, 1.8)
    plt.ylim(-15.0, 15.0)
    # plt.grid(True)
    # ========== set up figure thick ============================
    bwidth = 2
    TK = plt.gca()
    TK.spines['bottom'].set_linewidth(bwidth)
    TK.spines['left'].set_linewidth(bwidth)
    TK.spines['top'].set_linewidth(bwidth)
    TK.spines['right'].set_linewidth(bwidth)
    
    # -------------- Draw to show critical Dt ------------------------------------
    plt.axvline(x= 1.73, color='black', linestyle='--', linewidth= 3) # Linear = 1.73 ; Central = 1.0
   
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.2))
    # -------------- Consider X-axis  -----------------------
    ax.set_xscale('log', base=10)
    ax.set_xticks([], minor=False)
    ax.set_xticks([], minor=True)
    x_ticks_Num = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8])  # 设置线性刻度间距为0.125
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.1f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='major', labelsize= 24, length=8, width=2)
    
    # ax.set_yscale('log', base=10)
    ax.tick_params(axis = 'y', which='major', labelsize= 25, length=8, width=2)
    
# DifferTime_elemetError2(Dy80row_err, Dy40row_err, Dy20row_err, Dy10row_err)

# ------------- For L2-Norm Error -------------------
Dy80row_errL2 = np.zeros((len(C_Data),2))
Dy40row_errL2 = np.zeros((len(C_Data),2))
Dy20row_errL2 = np.zeros((len(C_Data),2))
Dy10row_errL2 = np.zeros((len(C_Data),2))

def C_L2Norm(C_Data, Dy80row_errL2, Mesh_Num):
    Dy80row_errL2[:,0] = C_Data[:]
    Dy80row_errL2[0,1] = Dt02Err_L2[Mesh_Num, 1]
    Dy80row_errL2[1,1] = Dt04Err_L2[Mesh_Num, 1]
    Dy80row_errL2[2,1] = Dt06Err_L2[Mesh_Num, 1]
    Dy80row_errL2[3,1] = Dt08Err_L2[Mesh_Num, 1]
    Dy80row_errL2[4,1] = Dt10Err_L2[Mesh_Num, 1]
    Dy80row_errL2[5,1] = Dt12Err_L2[Mesh_Num, 1]
    Dy80row_errL2[6,1] = Dt14Err_L2[Mesh_Num, 1]
    Dy80row_errL2[7,1] = Dt16Err_L2[Mesh_Num, 1]
    Dy80row_errL2[8,1] = Dt18Err_L2[Mesh_Num, 1] 
    return Dy80row_err

C_L2Norm(C_Data, Dy80row_errL2, 0)
C_L2Norm(C_Data, Dy40row_errL2, 1)
C_L2Norm(C_Data, Dy20row_errL2, 2)
C_L2Norm(C_Data, Dy10row_errL2, 3)

# ==================Draw L2 Norm error : C data =============================
Mesh80_Dt = (0.125/cp)*C_Data
Mesh40_Dt = (0.25/cp)*C_Data
Mesh20_Dt = (0.50/cp)*C_Data
Mesh10_Dt = (1.0/cp)*C_Data

def DifferTime_L2NormError2(Dy80row_errL2, Dy40row_errL2, Dy20row_errL2, Dy10row_errL2): 
    plt.figure(figsize=(10,8))
    # plt.title(f'{Integrator} L2-Norm Error', fontsize = 25) # Compare / Integrator
    plt.text(0.01, 0.15, f'{Integrator}', fontsize = 28, color= 'black', transform=plt.gca().transAxes)
    
    plt.text(0.04, 0.07, r'$C_{cr}=$ $\mathrm{infinite}$', fontsize=28, transform=plt.gca().transAxes)
    # plt.text(0.04, 0.06, r'$C_{cr} = 1.73$', fontsize= 28, transform=plt.gca().transAxes) # 0.06 / 0.6
    
    font_props = {'family': 'Arial', 'size': 18}
    plt.plot(Dy80row_errL2[:,0], Dy80row_errL2[:,1],marker = '^',markersize=12,markerfacecolor = 'none',label = r'$\Delta_c =  $ $\mathrm {0.125m}$', linewidth = 3.0, color = 'limegreen')
    plt.plot(Dy40row_errL2[:,0], Dy40row_errL2[:,1],marker = 'o',markersize=12,markerfacecolor = 'none',label =  r'$\Delta_c =  $ $\mathrm {0.250m}$', linewidth = 3.0, color = 'darkorange')
    plt.plot(Dy20row_errL2[:,0], Dy20row_errL2[:,1],marker = '<',markersize=12,markerfacecolor = 'none',label = r'$\Delta_c =  $ $\mathrm {0.500m}$', linewidth = 3.0, color = 'mediumblue')
    plt.plot(Dy10row_errL2[:,0], Dy10row_errL2[:,1],marker = 's',markersize=12,markerfacecolor = 'none',label = r'$\Delta_c =  $ $\mathrm {1.000m}$', linewidth = 3.0, color = 'crimson')
        
    legend1 = plt.legend(ncol=1,prop=font_props, loc= (0.03, 0.72)) #ncol=2,fontsize=16 frameon=False , loc='upper left'
    legend1.get_frame().set_edgecolor('grey')
    legend1.get_frame().set_linewidth(2)  # 設置外框寬度
    
    plt.xticks(fontsize = 20, fontweight='bold', color='black')
    plt.yticks(fontsize = 20, fontweight='bold', color='black')
    
    plt.xlabel(f'Time Increment Ratio ' +r'$C$', fontsize = 28)
    plt.ylabel('Normalized L2 Norm Error '+ r"$\ E_{L2}$" , fontsize = 28) # 'L2 Norm Error: '+ r"$\ E_{L2}$" / 'L2 normalization'+ r"$\ E_{L2N}$"

    plt.xlim(0.2, 1.8)
    plt.ylim(0, 0.6)
    # plt.grid(True)
    # ========== set up figure thick ============================
    bwidth = 2
    TK = plt.gca()
    TK.spines['bottom'].set_linewidth(bwidth)
    TK.spines['left'].set_linewidth(bwidth)
    TK.spines['top'].set_linewidth(bwidth)
    TK.spines['right'].set_linewidth(bwidth)
    
    # # -------------- Draw to show critical Dt ------------------------------------
    # plt.axvline(x= 1.73, color='black', linestyle='--', linewidth= 3)  # Linear = 1.73 ; Central = 1.0
    
    ax = plt.gca()
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.2))
    # -------------- Consider X-axis  -----------------------
    ax.set_xscale('log', base=10)
    ax.set_xticks([], minor=False)
    ax.set_xticks([], minor=True)
    x_ticks_Num = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8])  # 设置线性刻度间距为0.125
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.1f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='major', labelsize= 24, length=8, width=2)
    
    # -------------- Consider Y-axis  -----------------------
    ax.set_yscale('log', base=10)
    ax.set_yticks([], minor=False)
    ax.set_yticks([], minor=True)
    y_ticks_Num = np.array([0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4, 0.6])  # 设置线性刻度间距为0.1  np.arange(0.1, 10.1, 0.1)
    ax.set_yticks(y_ticks_Num)
    ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks_Num], rotation=0, fontsize=12)
    ax.tick_params(axis='y', which='major', labelsize= 25, length=8, width=2)
    # ------- Miner ticks -----------------
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='y', which='minor', length=4, width=2, color='gray') # , width=2
      
    ax.set_ylim(0.0, 0.6)  # 例如从0.1到10

# DifferTime_L2NormError2(Dy80row_errL2, Dy40row_errL2, Dy20row_errL2, Dy10row_errL2)
