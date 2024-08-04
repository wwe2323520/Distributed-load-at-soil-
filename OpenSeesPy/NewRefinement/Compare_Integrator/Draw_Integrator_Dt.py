# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 11:11:10 2024

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
            
        if total_time[t] >= 0.025 and total_time[t] < 0.050:
            Pwave[to+t,End_Ele-g] = Pwave[to+t,End_Ele-g] + Cp_vel_Coefficient*XIn[t-to,End_Ele-g]   # XOut[t-to,End_Ele-g]

row80 = f'node161'
row40 = f'node81'
row20 = f'node41'
row10 = f'node21'

Integrator = f'Central Differential' # Central Differential / HHT_Alpha / NewMark_Linear / NewMark_Constant

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

Condition4 =  f"Test_Integrator/{Integrator}/Dt_0.8"# 
file13 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/row80/Velocity/{row80}.out"
file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/row40/Velocity/{row40}.out"
file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/row20/Velocity/{row20}.out"
file16 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/row10/Velocity/{row10}.out"

Dt08_80row = rdnumpy(file13)
Dt08_40row = rdnumpy(file14)
Dt08_20row = rdnumpy(file14)
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

# Condition7 =  f"Test_Integrator/{Integrator}/Dt_1.4"# 
# file25 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/row80/Velocity/{row80}.out"
# file26 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/row40/Velocity/{row40}.out"
# file27 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/row20/Velocity/{row20}.out"
# file28 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/row10/Velocity/{row10}.out"

# Dt14_80row = rdnumpy(file25)
# Dt14_40row = rdnumpy(file26)
# Dt14_20row = rdnumpy(file27)
# Dt14_10row = rdnumpy(file28)

# Condition8 =  f"Test_Integrator/{Integrator}/Dt_1.6"# 
# file29 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/row80/Velocity/{row80}.out"
# file30 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/row40/Velocity/{row40}.out"
# file31 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/row20/Velocity/{row20}.out"
# file32 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/row10/Velocity/{row10}.out"

# Dt16_80row = rdnumpy(file29)
# Dt16_40row = rdnumpy(file30)
# Dt16_20row = rdnumpy(file31)
# Dt16_10row = rdnumpy(file32)

# Condition9 =  f"Test_Integrator/{Integrator}/Dt_1.8"# 
# file33 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/row80/Velocity/{row80}.out"
# file34 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/row40/Velocity/{row40}.out"
# file35 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/row20/Velocity/{row20}.out"
# file36 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/row10/Velocity/{row10}.out"

# Dt18_80row = rdnumpy(file33)
# Dt18_40row = rdnumpy(file34)
# Dt18_20row = rdnumpy(file35)
# Dt18_10row = rdnumpy(file36)

def CompareDt_DiffVel(titleName, D80_Dt10, D80_Dt11, D80_Dt12, D80_Dt14):
    plt.figure(figsize=(10,8))
    plt.title(titleName, fontsize = 20)
# ------------------- Theory ------------------------------
    plt.plot(total_time, Pwave[:,79],label =r'$\mathrm{Analytical}$',color= 'black',linewidth=7.0)
    
# -----------------Test Integrator Differ Mesh -------------------------   
    plt.plot(D80_Dt10[:,0], D80_Dt10[:, 2], label = r'$\Delta_{y} = 0.0125H$', color= 'limegreen', linewidth = 6.0) # , ls = '--' 
    plt.plot(D80_Dt11[:,0], D80_Dt11[:, 2], label = r'$\Delta_{y} = 0.025H$', color= 'orange', ls = '-.',  linewidth = 5.0) # , ls = '-.'
    plt.plot(D80_Dt12[:,0], D80_Dt12[:, 2], label = r'$\Delta_{y} = 0.05H$', color= 'purple', ls = '-', linewidth = 4.0) # , ls = ':'
    plt.plot(D80_Dt14[:,0], D80_Dt14[:, 2], label = r'$\Delta_{y} = 0.1H$', color= 'red', linewidth = 3.0) # , ls = ':'
    
    plt.grid(True)
    plt.legend(fontsize=18) # loc='lower left',
    
    plt.xlim(0, 0.2)
    # plt.ylim(-0.9, 0.9)
    
    plt.xlabel(r"$\mathrm {time}$ ${t}$ $\mathrm {(s)}$", fontsize = 20) # r"$G^{'}/G$"
    plt.ylabel(r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", fontsize = 20)  # r"$m_{x'}/m_{x}$"
    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 18)
    
    ax = plt.gca()
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
    ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    ax.yaxis.get_offset_text().set(size=18)

Compare = f'HHT-'+r'$\alpha$'

CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 0.2$ $(\Delta_{tp})$', Dt02_80row, Dt02_40row, Dt02_20row, Dt02_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 0.4$ $(\Delta_{tp})$', Dt04_80row, Dt04_40row, Dt04_20row, Dt04_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 0.6$ $(\Delta_{tp})$', Dt06_80row, Dt06_40row, Dt06_20row, Dt06_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 0.8$ $(\Delta_{tp})$', Dt08_80row, Dt08_40row, Dt08_20row, Dt08_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 1.0$ $(\Delta_{tp})$', Dt10_80row, Dt10_40row, Dt10_20row, Dt10_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 1.2$ $(\Delta_{tp})$', Dt12_80row, Dt12_40row, Dt12_20row, Dt12_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 1.4$ $(\Delta_{tp})$', Dt14_80row, Dt14_40row, Dt14_20row, Dt14_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 1.6$ $(\Delta_{tp})$', Dt16_80row, Dt16_40row, Dt16_20row, Dt16_10row)
# CompareDt_DiffVel(f'{Integrator} ' + r'$\Delta_{t} = 1.8$ $(\Delta_{tp})$', Dt18_80row, Dt18_40row, Dt18_20row, Dt18_10row)

# ================================== Prepare Relative Error and Absolute Error ============================
def Find_ColMaxValue(column_index,ele80_Mid):
    column = ele80_Mid[:, column_index]
    max_value = np.max(column)
    max_index = np.argmax(column)
    
    min_value = np.min(column)
    min_index = np.argmin(column)

    print(f'max_value= {max_value}; max_index= {max_index}; min_value= {min_value}; min_index= {min_index}')
    return(max_value,min_value)
# =========== Find Grounf Surface Max/ Min Peak Value ==========================
column_index = 2 # Pwave = 2 (yaxis)
Analysis_column = 79

# =========== Find Grounf Surface Max/ Min Peak Value ==========================
column_index = 2 # Pwave = 2 (yaxis)
Analysis_column = 79

# =================================== Middle Node ===================================
# ------------ Dt = 0.2-----------------------
maxDt02_80row, minDt02_80row = Find_ColMaxValue(column_index, Dt02_80row)
maxDt02_40row, minDt02_40row = Find_ColMaxValue(column_index, Dt02_40row)
maxDt02_20row, minDt02_20row = Find_ColMaxValue(column_index, Dt02_20row)
maxDt02_10row, minDt02_10row = Find_ColMaxValue(column_index, Dt02_10row)
# ------------ Dt = 0.4-----------------------
maxDt04_80row, minDt04_80row = Find_ColMaxValue(column_index, Dt04_80row)
maxDt04_40row, minDt04_40row = Find_ColMaxValue(column_index, Dt04_40row)
maxDt04_20row, minDt04_20row = Find_ColMaxValue(column_index, Dt04_20row)
maxDt04_10row, minDt04_10row = Find_ColMaxValue(column_index, Dt04_10row)
# ------------ Dt = 0.6-----------------------
maxDt06_80row, minDt06_80row = Find_ColMaxValue(column_index, Dt06_80row)
maxDt06_40row, minDt06_40row = Find_ColMaxValue(column_index, Dt06_40row)
maxDt06_20row, minDt06_20row = Find_ColMaxValue(column_index, Dt06_20row)
maxDt06_10row, minDt06_10row = Find_ColMaxValue(column_index, Dt06_10row)
# ------------ Dt = 0.8-----------------------
maxDt08_80row, minDt08_80row = Find_ColMaxValue(column_index, Dt08_80row)
maxDt08_40row, minDt08_40row = Find_ColMaxValue(column_index, Dt08_40row)
maxDt08_20row, minDt08_20row = Find_ColMaxValue(column_index, Dt08_20row)
maxDt08_10row, minDt08_10row = Find_ColMaxValue(column_index, Dt08_10row)
# ------------ Dt = 1.0-----------------------
maxDt10_80row, minDt10_80row = Find_ColMaxValue(column_index, Dt10_80row)
maxDt10_40row, minDt10_40row = Find_ColMaxValue(column_index, Dt10_40row)
maxDt10_20row, minDt10_20row = Find_ColMaxValue(column_index, Dt10_20row)
maxDt10_10row, minDt10_10row = Find_ColMaxValue(column_index, Dt10_10row)
# ------------ Dt = 1.2-----------------------
maxDt12_80row, minDt12_80row = Find_ColMaxValue(column_index, Dt12_80row)
maxDt12_40row, minDt12_40row = Find_ColMaxValue(column_index, Dt12_40row)
maxDt12_20row, minDt12_20row = Find_ColMaxValue(column_index, Dt12_20row)
maxDt12_10row, minDt12_10row = Find_ColMaxValue(column_index, Dt12_10row)

# # ------------ Dt = 1.4-----------------------
# maxDt14_80row, minDt14_80row = Find_ColMaxValue(column_index, Dt14_80row)
# maxDt14_40row, minDt14_40row = Find_ColMaxValue(column_index, Dt14_40row)
# maxDt14_20row, minDt14_20row = Find_ColMaxValue(column_index, Dt14_20row)
# maxDt14_10row, minDt14_10row = Find_ColMaxValue(column_index, Dt14_10row)
# # ------------ Dt = 1.6-----------------------
# maxDt16_80row, minDt16_80row = Find_ColMaxValue(column_index, Dt16_80row)
# maxDt16_40row, minDt16_40row = Find_ColMaxValue(column_index, Dt16_40row)
# maxDt16_20row, minDt16_20row = Find_ColMaxValue(column_index, Dt16_20row)
# maxDt16_10row, minDt16_10row = Find_ColMaxValue(column_index, Dt16_10row)
# # ------------ Dt = 1.8-----------------------
# maxDt18_80row, minDt18_80row = Find_ColMaxValue(column_index, Dt18_80row)
# maxDt18_40row, minDt18_40row = Find_ColMaxValue(column_index, Dt18_40row)
# maxDt18_20row, minDt18_20row = Find_ColMaxValue(column_index, Dt18_20row)
# maxDt18_10row, minDt18_10row = Find_ColMaxValue(column_index, Dt18_10row)

maxAnaly, minAnaly = Find_ColMaxValue(Analysis_column,Pwave)
Mesh_Size = np.zeros(4)
ele = 80 
for m in range(len(Mesh_Size)):
    if m == 0 :    
        Mesh_Size[m] = L/ (ele)
    if m > 0:    
        Mesh_Size[m] = Mesh_Size[m-1]*2

def errMatrix(error_dc,maxDt02_80row,minDt02_80row,maxDt02_40row,minDt02_40row,maxDt02_20row,minDt02_20row,maxDt02_10row,minDt02_10row):
    error_dc[:,0] = Mesh_Size[:]
    error_dc[0,1] = maxDt02_80row
    error_dc[0,2] = minDt02_80row
    error_dc[1,1] = maxDt02_40row
    error_dc[1,2] = minDt02_40row
    error_dc[2,1] = maxDt02_20row
    error_dc[2,2] = minDt02_20row
    error_dc[3,1] = maxDt02_10row
    error_dc[3,2] = minDt02_10row
    return error_dc

# ============================= Middle Node ========================================
# ------------Dt = 0.2 Error Peak Value-----------------------
Dt02_error = np.zeros((4,3))
errMatrix(Dt02_error, maxDt02_80row,minDt02_80row, maxDt02_40row,minDt02_40row, maxDt02_20row,minDt02_20row, maxDt02_10row,minDt02_10row)
# ------------Dt = 0.4 Error Peak Value-----------------------
Dt04_error = np.zeros((4,3))
errMatrix(Dt04_error, maxDt04_80row,minDt04_80row, maxDt04_40row,minDt04_40row, maxDt04_20row,minDt04_20row, maxDt04_10row,minDt04_10row)
# ------------Dt = 0.6 Error Peak Value-----------------------
Dt06_error = np.zeros((4,3))
errMatrix(Dt06_error, maxDt06_80row,minDt06_80row, maxDt06_40row,minDt06_40row, maxDt06_20row,minDt06_20row, maxDt06_10row,minDt06_10row)
# ------------Dt = 0.8 Error Peak Value-----------------------
Dt08_error = np.zeros((4,3))
errMatrix(Dt08_error, maxDt08_80row,minDt08_80row, maxDt08_40row,minDt08_40row, maxDt08_20row,minDt08_20row, maxDt08_10row,minDt08_10row)
# ------------Dt = 1.0 Error Peak Value-----------------------
Dt10_error = np.zeros((4,3))
errMatrix(Dt10_error, maxDt10_80row,minDt10_80row, maxDt10_40row,minDt10_40row, maxDt10_20row,minDt10_20row, maxDt10_10row,minDt10_10row)
# ------------Dt = 1.2 Error Peak Value-----------------------
Dt12_error = np.zeros((4,3))
errMatrix(Dt12_error, maxDt12_80row,minDt12_80row, maxDt12_40row,minDt12_40row, maxDt12_20row,minDt12_20row, maxDt12_10row,minDt12_10row)

# calculate_Error()
Dt02_err = np.zeros((4,3))
Dt04_err = np.zeros((4,3))
Dt06_err = np.zeros((4,3))
Dt08_err = np.zeros((4,3))
Dt10_err = np.zeros((4,3))
Dt12_err = np.zeros((4,3))

# # ------------Dt = 1.4 Error Peak Value-----------------------
# Dt14_error = np.zeros((4,3))
# errMatrix(Dt14_error, maxDt14_80row,minDt14_80row, maxDt14_40row,minDt14_40row, maxDt14_20row,minDt14_20row, maxDt14_10row,minDt14_10row)
# # ------------Dt = 1.6 Error Peak Value-----------------------
# Dt16_error = np.zeros((4,3))
# errMatrix(Dt16_error, maxDt16_80row,minDt16_80row, maxDt16_40row,minDt16_40row, maxDt16_20row,minDt16_20row, maxDt16_10row,minDt16_10row)
# # ------------Dt = 1.8 Error Peak Value-----------------------
# Dt18_error = np.zeros((4,3))
# errMatrix(Dt18_error, maxDt18_80row,minDt18_80row, maxDt18_40row,minDt18_40row, maxDt18_20row,minDt18_20row, maxDt18_10row,minDt18_10row)

# Dt14_err = np.zeros((4,3))
# Dt16_err = np.zeros((4,3))
# Dt18_err = np.zeros((4,3))

def Calculate_Error(TieErr, Tie_error):
    for i in range(len(Mesh_Size)):
        TieErr[:,0] = Tie_error[:,0]
# ------------------------- Absolute Relative Error ------------------        
        TieErr[i,1] = (abs(Tie_error[i,1] - maxAnaly)/maxAnaly)*100
        TieErr[i,2] = (abs(Tie_error[i,2] - minAnaly)/minAnaly)*100
        
Calculate_Error(Dt02_err, Dt02_error)
Calculate_Error(Dt04_err, Dt04_error)
Calculate_Error(Dt06_err, Dt06_error)
Calculate_Error(Dt08_err, Dt08_error)
Calculate_Error(Dt10_err, Dt10_error)
Calculate_Error(Dt12_err, Dt12_error)

# Calculate_Error(Dt14_err, Dt14_error)
# Calculate_Error(Dt16_err, Dt16_error)
# Calculate_Error(Dt18_err, Dt18_error)

# ==================Draw Relative error : Middele point =============================
def DifferTime_elemetError(Peak, Dt02_err, Dt04_err, Dt06_err, Dt08_err, Dt10_err): # , Dt12_err, Dt14_err, Dt16_err, Dt18_err
    plt.figure(figsize=(10,8))
    plt.title(f'{Integrator} Relative Error', fontsize = 20) # Compare / Integrator
    
    font_props = {'family': 'Arial', 'size': 14}
    plt.plot(Dt02_err[:,0], Dt02_err[:,Peak],marker = '^',markersize=12,markerfacecolor = 'white',label = r'$C = 0.2$')
    plt.plot(Dt04_err[:,0], Dt04_err[:,Peak],marker = 'o',markersize=11,markerfacecolor = 'white',label =  r'$C = 0.4$')
    plt.plot(Dt06_err[:,0], Dt06_err[:,Peak],marker = '<',markersize=10,markerfacecolor = 'white',label = r'$C = 0.6$')
    plt.plot(Dt08_err[:,0], Dt08_err[:,Peak],marker = 's',markersize=9,markerfacecolor = 'white',label = r'$C = 0.8$')
    plt.plot(Dt10_err[:,0], Dt10_err[:,Peak],marker = 'p',markersize=8,markerfacecolor = 'white',label = r'$C = 1.0$')
    # plt.plot(Dt12_err[:,0], Dt12_err[:,Peak],marker = '*',markersize=7,markerfacecolor = 'white',label = r'$C = 1.2$')
    # plt.plot(Dt14_err[:,0], Dt14_err[:,Peak],marker = '+',markersize=6,markerfacecolor = 'white',label = r'$C = 1.4$')
    # plt.plot(Dt16_err[:,0], Dt16_err[:,Peak],marker = 'x',markersize=5,markerfacecolor = 'white',label = r'$C = 1.6$')
    # plt.plot(Dt18_err[:,0], Dt18_err[:,Peak],marker = 'D',markersize=4,markerfacecolor = 'white',label = r'$C = 1.8$')
    
    plt.legend(ncol=3, loc='upper left',prop=font_props) #ncol=2,fontsize=16 frameon=False
    # plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    
    plt.xlabel(f'Mesh size ' + r'$\Delta_y$ $\,(log_{10})\,$  $\mathrm {(m)}$', fontsize = 20)
    plt.ylabel('Peak Velocity Error: '+ r"$\ E_{Max}$" + r" (%)", fontsize = 20)

    # plt.xlim(0.0, 0.20)
    plt.grid(True)
    
    ax = plt.gca()
    ax.set_xscale('log', base=10)
    ax.tick_params(axis = 'x', which = 'both', labelsize = 17)
    
    ax.set_yscale('log', base=10)
    ax.tick_params(axis = 'y', which = 'both', labelsize = 17)
    
    # # ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
    # ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    # ax.yaxis.get_offset_text().set(size=18)

DifferTime_elemetError(1, Dt02_err, Dt04_err, Dt06_err, Dt08_err, Dt10_err) # , Dt12_err, Dt14_err, Dt16_err, Dt18_err
# # ==================Draw Relative error : Middele point =============================
# def DifferTime_elemetError2(Peak, Dt12_err, Dt14_err, Dt16_err, Dt18_err):
#     plt.figure(figsize=(10,8))
#     plt.title(f'{Compare} Relative Error', fontsize = 20) # Compare / Integrator
    
#     font_props = {'family': 'Arial', 'size': 18}
#     plt.plot(Dt12_err[:,0], Dt12_err[:,Peak],marker = '^',markersize=12,markerfacecolor = 'white',label = r'$C = 1.2$')
#     plt.plot(Dt14_err[:,0], Dt14_err[:,Peak],marker = 'o',markersize=10,markerfacecolor = 'white',label =  r'$C = 1.4$')
#     plt.plot(Dt16_err[:,0], Dt16_err[:,Peak],marker = '<',markersize=8,markerfacecolor = 'white',label = r'$C = 1.6$')
#     plt.plot(Dt18_err[:,0], Dt18_err[:,Peak],marker = 's',markersize=6,markerfacecolor = 'white',label = r'$C = 1.8$')
    
#     plt.legend(loc='upper left',prop=font_props) #ncol=2,fontsize=16 frameon=False
    
#     plt.xlabel(f'Mesh size ' + r'$\Delta_y$ $\,(log_{10})\,$  $\mathrm {(m)}$', fontsize = 20)
#     plt.ylabel('Peak Velocity Error: '+ r"$\ E_{Max}$" + r" (%)", fontsize = 20)

#     # plt.xlim(0.0, 0.20)
#     plt.grid(True)
    
#     ax = plt.gca()
#     ax.set_xscale('log', base=10)
#     ax.tick_params(axis = 'x', which = 'both', labelsize = 17)
    
#     ax.set_yscale('log', base=10)
#     ax.tick_params(axis = 'y', which = 'both', labelsize = 17)
    
#     # # ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
#     # ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
#     # ax.yaxis.get_offset_text().set(size=18)


# DifferTime_elemetError2(1, Dt12_err, Dt14_err, Dt16_err, Dt18_err)
