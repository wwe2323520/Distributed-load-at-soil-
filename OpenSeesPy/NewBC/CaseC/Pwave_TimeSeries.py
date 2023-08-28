# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 16:38:29 2023

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

pi = np.pi

cp = 100.0 # m/s
L = 10 # m(Soil_Depth)
fp = cp/L 
Tp = 1/fp
w =  pi/5 # 0 to 10 = 0 to 2*pi => x = pi/5

time = np.arange(0.0,0.1001,1e-4)

# ---------- Soil Coordinate --------------
x = cp*time #m

yOut =  np.zeros(len(x))
def Incoming_wave(x,t):
    return np.sin(w*(x-cp*t))

def Outcoming_wave(x,t):
    return +np.sin(w*(x+cp*t))

total_Transport = np.arange(0.0,20.1, 0.01)
XIn = np.zeros((len(total_Transport),100))
XNodeIn = np.zeros((len(total_Transport),101))

Nele = 100
dy = L/Nele # 0.1
dx= 10/1000 # 0.01 each element have 10 step dx

Nnode = 101
# ---------- Incoming wave (Beam distributed load)-------------------
input_disp = 5 # 5
# X = 0~10 m 
for j in range(Nele):
    tin = time[input_disp+10*j] 
    x0 = dy*j + 0.05
    
    for i in range(1001):      
        xii = x0 + dx*i 
        XIn[5+10*j+i,j] = Incoming_wave(xii,tin)  #from 0.05m to 9.95m

# # ---------- Outcoming wave (Beam distributed load)-------------------
XOut = np.zeros((len(total_Transport),100))
Output_disp = 5 # 9.95
# X = 10m ~ 20m
for j in range(100):# Nele
    tout = time[Output_disp+10*j] 
    x0 = 9.95-dy*j 
    # x0 = dy*j + 0.05
    for i in range(1001):      
        xoo = x0 + dx*i 
        XOut[995-10*j+i,99-j] = Outcoming_wave(xoo,tout)  #from 9.95m to 0.05m
        
# ---------- Incoming wave (Nodal Load)-------------------       
NodeIn_id = 0
for k in range(Nnode):#Nnode
# ----- Node load ----------
    tNodeIn = time[NodeIn_id+10*k]
    x0_1 = dy*k + 0.0
    
    for i in range(1001):      
        xii_1 = x0_1 + dx*i 
        XNodeIn[0+10*k+i,k] = Incoming_wave(xii_1,tNodeIn)  #from 0.0m to 10.0m
        
# ---------- Incoming wave (Nodal Load)-------------------  
XNodeOut = np.zeros((len(total_Transport),101))
NodeOut_id = 0
for k in range(Nnode):#Nnode
# ----- Node load ----------
    tNodeOut = time[NodeOut_id+10*k]
    x0_1 = 10.0-dy*k 
    # print()
    for i in range(1001):
        xoo_1 = x0_1 + dx*i 
        XNodeOut[1000-10*k+i,100-k] = Outcoming_wave(xoo_1,tNodeOut)  #from 10.0m to 0.0m


total_time = np.arange(0.0,0.4001,1e-4)
wave1 = np.zeros((len(total_time),Nele))

# ===== New BC Sideforce on Left and Right ==============
PSideforce_xx = np.zeros((len(total_time),Nele))
PNodeforce_y = np.zeros((len(total_time),Nnode))

# ===== Input Incoming Wave and Outcoming Wave to wave1 =======================
nu = 0.3  #  0.3 -> (epsilon_z /=0)
rho = 2020 #1600 kg/m3  ; =1.6 ton/m3  
cp = 100 #m/s
E = (cp*cp)*rho*(1+nu)*(1-2*nu)/(1-nu)
G = E/(2*(1+nu))

cs = (G/rho)**(0.5) #m/s

ForceX_Cofficient = (nu/(1-nu))
for g in [i for i in range(100)]: #Nele
    to = int(10*g+5)
    for t in range(len(total_time)):
        if t < 1000:
            # wave1[to+t,g] += XIn[to+t,g]
            # wave1[to+t,g] = (wave1[to+t,g] + XIn[to+t,g])  # original wave transport
# ----- Pwave sigma xx --------------------------
            PSideforce_xx[to+t,g] = PSideforce_xx[to+t,g] + (ForceX_Cofficient *XIn[to+t,g])
# ----- Pwave eta_S*(Vy) --------------------------            
            # PSideforce_y[to+t,g] = PSideforce_y[to+t,g] + (ForceY_Cofficient *XIn[to+t,g])
    
        if t >= 1000 and t < 2000:
            # wave1[to+t,99-g] += XOut[t-to,99-g]
            # wave1[to+t,99-g] = wave1[to+t,99-g] + XOut[t-to,99-g]   # original wave transport
# ----- Pwave sigma xx --------------------------
            PSideforce_xx[to+t,99-g] = PSideforce_xx[to+t,99-g] + (-ForceX_Cofficient *XOut[t-to,99-g])
# ----- Pwave eta_S*(Vy) --------------------------            
            # PSideforce_y[to+t,99-g] = PSideforce_y[to+t,99-g] + (ForceY_Cofficient *XOut[t-to,99-g])

ForceY_Cofficient = (cs/cp)
for m in range(101): #Nnode 101
    t1 = int(10*m+0)
    # print(t1)
    for n in range(len(total_time)):
        if n < 1000:
# ----- Pwave eta_S*(Vy) --------------------------  
            PNodeforce_y[t1+n,m] = PNodeforce_y[t1+n,m] + (ForceY_Cofficient *XNodeIn[t1+n,m])
        if n >= 1000 and n < 2000:
# ----- Pwave eta_S*(Vy) --------------------------            
            PNodeforce_y[t1+n,100-m] = PNodeforce_y[t1+n,100-m] + (ForceY_Cofficient *XNodeOut[n-t1,100-m])

# ---- Output matrix eace column to txt file --------------
num_rows, num_cols = PSideforce_xx.shape# 8001,100
# 建立資料夾
# ---------- Pwave ---------------
P_folder_name_x = "P_Sideforce_x"

# os.makedirs(P_folder_name_x, exist_ok=True)
# for col in range(num_cols):
#     column_values = PSideforce_xx[:, col]
#     output_file = f"ele{col + 1}.txt"
#     with open(os.path.join(P_folder_name_x, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")

P_folder_name_y = "P_Nodeforce_y"
# ---- Output matrix eace column to txt file --------------
num_rows, num_cols = PNodeforce_y.shape# 8001,100
os.makedirs(P_folder_name_y, exist_ok=True)
# 逐一建立txt檔案並放入資料夾
for col in range(num_cols):
    column_values = PNodeforce_y[:, col]
    output_file = f"Node{col + 1}.txt"
    with open(os.path.join(P_folder_name_y, output_file), 'w') as f:
        for value in column_values:
            f.write(f"{value}\n")
            
# ------- wave put into the timeSeries ---------------   
plt.figure()
# plt.title('Wave Transport',fontsize = 18)   
# plt.title(r'SideForce $\sigma_{xx}$',fontsize = 18)         
plt.title(r'NodeForce $\eta_{s}v_y$',fontsize = 18)   
plt.xlabel("tns(s)",fontsize=18)
# # ----- Pwave sigma xx --------------------------
# plt.plot(total_time,PSideforce_xx[:,0],label ='Ele 1', marker='o', markevery=100)
# plt.plot(total_time,PSideforce_xx[:,50],label ='Ele 51', marker='x', markevery=100)
# plt.plot(total_time,PSideforce_xx[:,99],label ='Ele 100', marker='d', markevery=100)

# ----- Pwave eta_S*(Vy) -------------
plt.plot(total_time,PNodeforce_y[:,0],label ='Node 1', marker='o', markevery=100)
plt.plot(total_time,PNodeforce_y[:,50],label ='Node 51', marker='x', markevery=100)
plt.plot(total_time,PNodeforce_y[:,100],label ='Node 101', marker='d', markevery=100)

plt.legend(loc='upper right',fontsize=18)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlim(0.0, 0.40)
plt.grid(True)

# # ========== Incoming Wave ==========================================
# plt.figure()
# plt.title('Incoming Wave',fontsize = 18)
# plt.xlabel("x(m)",fontsize=18)
# plt.ylabel(r"$y=sin(x-c_{p}t)$",fontsize=18)
# # ---- Beam Incoming wave ----------------------
# # plt.plot(total_Transport,XIn[:,0],label ='Element 1',marker='o', markevery=100)
# # plt.plot(total_Transport,XIn[:,50],label ='Element 50',marker='d', markevery=100)
# # plt.plot(total_Transport,XIn[:,99],label ='Element 100',marker='x', markevery=100)

# # ---- Node Incoming wave ----------------------
# plt.plot(total_Transport,XNodeIn[:,0],label ='Node 1',marker='o', markevery=100)
# plt.plot(total_Transport,XNodeIn[:,50],label ='Node 50',marker='d', markevery=100)
# plt.plot(total_Transport,XNodeIn[:,100],label ='Node 101',marker='x', markevery=100)
# plt.legend(loc='upper right',fontsize=18)
# plt.xlim(0,20.0)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid(True)

# # ========== Outcoming Wave ==========================================
# plt.figure()
# plt.title('Outcoming Wave',fontsize = 18)
# plt.xlabel("x(m)",fontsize=18)
# plt.ylabel(r"$y=sin(x+c_{p}t)$",fontsize=18)
# # # ---- Beam Incoming wave ----------------------
# # plt.plot(total_Transport,XOut[:,0],label ='Element 1',marker='o', markevery=100)
# # plt.plot(total_Transport,XOut[:,50],label ='Element 50',marker='d', markevery=100)
# # plt.plot(total_Transport,XOut[:,99],label ='Element 100',marker='x', markevery=100)

# # # ---- Node Incoming wave ----------------------
# plt.plot(total_Transport,XNodeOut[:,0],label ='Node 1',marker='o', markevery=100)
# plt.plot(total_Transport,XNodeOut[:,50],label ='Node 50',marker='d', markevery=100)
# plt.plot(total_Transport,XNodeOut[:,100],label ='Node 101',marker='x', markevery=100)
# plt.xlim(0,20.0)

# plt.legend(loc='upper right',fontsize=18)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid(True)
    
