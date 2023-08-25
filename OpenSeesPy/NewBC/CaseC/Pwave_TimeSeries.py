# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 10:07:52 2023

@author: User
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
plt.rc('font', family= 'Times New Roman')
pi = np.pi

num_f = 100
eleforce_id = np.empty(num_f, dtype=object)
for a in range(num_f):
    eleforce_id[a] = f"ele{a+1}"    #r"$f_{%dx}$"%(2*b+1) # f"u{b+1}x"
    
num_N = 101
Nodeid = np.empty(num_N, dtype=object)
for b in range(num_N):
    Nodeid[b] = f"Node{8*b+1}"    #r"$f_{%dx}$"%(2*b+1) # f"u{b+1}x"
#----- SurfeceLoad wave propogate -----------
#Give p-wave vel 
cp = 100  # m/s 

nu = 0.3
rho = 2020 #1600 kg/m3  ; =1.6 ton/m3 
E = (cp*cp)*rho*(1+nu)*(1-2*nu)/(1-nu)
G = E/(2*(1+nu))

cs = (G/rho)**(0.5) #m/s
Lp  = 10  # 10 m  2

fp = cp/Lp
Tp = 1/fp
wp = (2*pi)/Tp
# print(f"lamb_cp= {Lp} ;fcp= {fp} ;Tp= {Tp} ;wp= {wp}")
A = 0.1*1

#calaulate wave length
fcs = cs / Lp
Ts = 1/ fcs
ws = 2*pi/ Ts


time = np.arange(0,0.8001,1e-4)
PVel_FF = np.zeros(len(time))

# -------- P WAVE ----------------
Nodeforce_y = np.zeros((len(time),101)) # Side Node Force: Dashpot
Sideforce_x = np.zeros((len(time),100)) # Side Beam Force: Distributed Load


for k in range(len(time)):
    if k < 1001:
# ------- For P wave Velocity------------------------------------
        PVel_FF[k] = np.sin(wp*time[k])/(-rho*cp*A)
step = 1000#1000
Tstep = 2*step

Cp_id = np.zeros(100)
eleSize = np.arange(0.0, 10, 0.1)

for i in range(100):
    Cp_id[i] = round((eleSize[i]/cp)*10000,0)

# =============== Side Beam Force: Distributed Load ========================
for i in range(100):#100
    cpid = int(Cp_id[i])
    for j in range(len(time)): #len(time)
# ------- For P wave ------------------------------------
        if j <= 1000:
            Sideforce_x[cpid+j,i] = (nu/(1-nu))*np.sin(wp*time[j])
            
        elif (j > 1000 and j <= 2000):
            Sideforce_x[cpid+j,99-i] = -(nu/(1-nu))*np.sin(wp*time[j-step]) #-

# =============== Side Node Force: Dashpot ===================================
eta_s = rho*cs
eta_p = rho*cp
for k in range(101):
    for g in range(len(time)):
        if g <= 1000:
            Nodeforce_y[g+10*k,k] = -eta_s*PVel_FF[g]*A

        if (g >= 1000 and g <= 2000):
            Nodeforce_y[g+10*k,100-k] = -eta_s*PVel_FF[g-1000]*A         


            
# # # ---- Velocity Freefield Plot ----------------
# # # plt.figure()
# # # plt.plot(time,SVel_FF)
# # # plt.grid(True)

# eleForce $\eta_{s}v_y$
plt.figure()
plt.rcParams["figure.figsize"] = (12, 8)
plt.title(r'NodeForce $\eta_{s}v_y$', fontsize = 18)
plt.xlabel("tns(s)",fontsize=18)
# =========== Nodal Force =====================
plt.plot(time,Nodeforce_y[:,0],label = Nodeid[0],marker='o', markevery=100)
plt.plot(time,Nodeforce_y[:,50],label = Nodeid[50],marker='x', markevery=100)
plt.plot(time,Nodeforce_y[:,100],label = Nodeid[100],marker='d', markevery=100)

# =========== Element Force =====================
# plt.plot(time,Sideforce_x[:,0],label = eleforce_id[0],marker='o', markevery=100)
# plt.plot(time,Sideforce_x[:,50],label = eleforce_id[50],marker='x', markevery=100)
# plt.plot(time,Sideforce_x[:,99],label = eleforce_id[99],marker='d', markevery=100)

# for h in range(100):    #101
# # -------- P wave -----------------
#     plt.plot(time,Nodeforce_y[:,h],label = Nodeid[h])#force[4*i,:]
#     plt.plot(time,Sideforce_x[:,h],label = force_id[h])#force[4*i,:]

plt.grid(True)   
plt.legend(loc='upper right',fontsize=10, ncol=5)
plt.xlim(0,0.3)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)

# ---- Output matrix eace column to txt file --------------
# ---------- NodeForce ---------------
num_rows, num_cols = Nodeforce_y.shape# 8001,100
# 建立資料夾

P_folder_name_y = "P_Nodeforce_y"
os.makedirs(P_folder_name_y, exist_ok=True)
# 逐一建立txt檔案並放入資料夾
for col in range(num_cols):
    column_values = Nodeforce_y[:, col]
    output_file = f"Node{col + 1}.txt"
    with open(os.path.join(P_folder_name_y, output_file), 'w') as f:
        for value in column_values:
            f.write(f"{value}\n")
            
# ---------- Element Force ---------------
Elenum_rows, Elenum_cols = Sideforce_x.shape# 8001,100

P_folder_name_x = "P_Sideforce_x"
os.makedirs(P_folder_name_x, exist_ok=True)
os.makedirs(P_folder_name_x, exist_ok=True)
for col in range(Elenum_cols):
    column_values = Sideforce_x[:, col]
    output_file = f"ele{col + 1}.txt"
    with open(os.path.join(P_folder_name_x, output_file), 'w') as f:
        for value in column_values:
            f.write(f"{value}\n")
