# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 15:30:47 2025

@author: User
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
from matplotlib.ticker import LogLocator, NullFormatter, LogFormatter
plt.rcParams['savefig.dpi'] = 300

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

file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/1D_Transport/Newmark_Linear_Test/simple/W_2m/HZ_40/BeamType1_40row\Velocity/node689.out"
file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/1D_Transport/Newmark_Linear_Test/simple/W_2m/HZ_40/BeamType3_40row\Velocity/node689.out"
Beam_based = rdnumpy(file1)
Node_based = rdnumpy(file2)

def CompareDt_DiffBC(Beam, Node):
    plt.figure(figsize=(10,8))
    # plt.title(titleName, fontsize = 28)
# ------------------- Theory ------------------------------
    plt.plot(total_time, Pwave[:,79],label =r'$\mathrm{Analytical}$',color= 'dimgray',linewidth=3.5)
    
# -----------------Test Integrator Differ Mesh -------------------------   
    plt.plot(Beam[:,0], Beam[:, 2], label = 'Beam-based', color= 'mediumblue',marker = '^',markersize=12, markerfacecolor = 'none' , markevery=5, mew=2.0, linewidth=2.0) # , ls = '--' 
    plt.plot(Node[:,0], Node[:, 2], label = 'Node-based', color= 'crimson',marker = '<',markersize=12,markerfacecolor = 'none' , markevery=5, mew=2.0, linewidth=2.0) # , ls = '-.', mediumorchid
  
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
    plt.ylim(-1.0, 1.0)
    
    plt.xlabel(r"$\mathrm {time}$ ${t}$ $\mathrm {(s)}$", fontsize = 28) # r"$G^{'}/G$"
    plt.ylabel(r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", fontsize = 28)  # r"$m_{x'}/m_{x}$"
    plt.xticks(fontsize = 18, fontweight='bold', color='black')
    plt.yticks(fontsize = 18, fontweight='bold', color='black')
    
    ax = plt.gca()
    ax.tick_params(axis='x', which='major', labelsize= 23, length=8, width=2)
    
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1.0)) # 0.50
    ax.tick_params(axis='y', which='major', labelsize= 23, length=8, width=2)
    # ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    # ax.yaxis.get_offset_text().set(size=18)
    plt.savefig("D:/shiang/opensees/20220330/extend_soil/Paper_Image_300DPI/1D_Transport/Newmark Linear/Simple/Beam_Node_Test.png")
CompareDt_DiffBC(Beam_based, Node_based)
