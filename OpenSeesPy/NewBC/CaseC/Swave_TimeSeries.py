# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 14:31:26 2023

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

SVel_FF = np.zeros(len(time))
# -------- S WAVE -----------------
Nodeforce_X = np.zeros((len(time),101))
Sideforce_Y = np.zeros((len(time),100))

Cs_id = np.zeros(100)
eleSize = np.arange(0.0, 10, 0.1)

for i in range(100):
    Cs_id[i] = round((eleSize[i]/cs)*10000,0)

Tstep = 1870
for k in range(len(time)):
# ------- For S wave ------------------------------------
    if k <= 1870:
        SVel_FF[k] = np.sin(ws*time[k])/(-rho*cs*A)
        
# =============== Side Beam Force: Distributed Load ========================
for i in range(100):
    csid = int(Cs_id[i])
    for j in range(len(time)): #len(time)
# ------- For S wave ------------------------------------
        if j <= 1870:
            # Sideforce_X[csid+j,i] = -eta_p*SVel_FF[j]*A ;#-
            Sideforce_Y[csid+j,i] = +np.sin(ws*time[j])  ;#+
        if j >=Tstep and j < 2*Tstep:
            # Sideforce_X[csid+j,99-i] = -eta_p*SVel_FF[j-Tstep]*A ;#-
            Sideforce_Y[csid+j,99-i] = -np.sin(ws*time[j])  ;#+
            
# =============== Side Node Force: Dashpot =================================== 
CsNode_id = np.zeros(101)
NodeSize = np.arange(0.0, 10.1, 0.1)

for i in range(101):
    CsNode_id[i] = round((NodeSize[i]/cs)*10000,0)
    
eta_s = rho*cs
eta_p = rho*cp
for i in range(101):
    CsNodeid = int(CsNode_id[i])
    for k in range(len(time)):
        if k < 1870:    
            Nodeforce_X[CsNodeid+k,i] =  -eta_p*SVel_FF[k]*A
        if k >=Tstep and k < 2*Tstep:
            Nodeforce_X[CsNodeid+k,100-i] =  -eta_p*SVel_FF[k-Tstep]*A
# ---- Velocity Freefield Plot ----------------
# plt.figure()
# plt.plot(time,SVel_FF)
# plt.grid(True)


plt.figure()
plt.rcParams["figure.figsize"] = (12, 8)
plt.title("eleForce", fontsize = 18)
plt.xlabel("tns(s)",fontsize=18)
# # =========== Nodal Force =====================
# plt.plot(time,Nodeforce_X[:,0],label = Nodeid[0],marker='o', markevery=100)
# plt.plot(time,Nodeforce_X[:,50],label = Nodeid[50],marker='x', markevery=100)
# plt.plot(time,Nodeforce_X[:,100],label = Nodeid[100],marker='d', markevery=100)

# =========== Element Force =====================
plt.plot(time,Sideforce_Y[:,0],label = Nodeid[0],marker='o', markevery=100)
plt.plot(time,Sideforce_Y[:,50],label = Nodeid[50],marker='x', markevery=100)
plt.plot(time,Sideforce_Y[:,99],label = Nodeid[99],marker='d', markevery=100)
# for h in range(100):    #101
# -------- S wave -----------------
    # plt.plot(time,Sideforce_X[:,h],label = force_id[h])#force[4*i,:]
    # plt.plot(time,Sideforce_Y[:,h],label = force_id[h])#force[4*i,:]

plt.grid(True)   
plt.legend(loc='upper right',fontsize=10, ncol=5)
plt.xlim(0,0.7)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)

# ---------- Element Force ---------------
num_rows, num_cols = Sideforce_Y.shape# 8001,100
S_folder_name_y = "S_Sideforce_y"

os.makedirs(S_folder_name_y, exist_ok=True)
for col in range(num_cols):
    column_values = Sideforce_Y[:, col]
    output_file = f"ele{col + 1}.txt"
    with open(os.path.join(S_folder_name_y, output_file), 'w') as f:
        for value in column_values:
            f.write(f"{value}\n")


# ---------- NodeForce ---------------
num_rows, num_cols = Nodeforce_X.shape# 8001,100
S_folder_name_x = "S_Nodeforce_X"
os.makedirs(S_folder_name_x, exist_ok=True)
for col in range(num_cols):
    column_values = Nodeforce_X[:, col]
    output_file = f"Node{col + 1}.txt"
    with open(os.path.join(S_folder_name_x, output_file), 'w') as f:
        for value in column_values:
            f.write(f"{value}\n")    
            
print(f"Txt files have been saved in the folder '{S_folder_name_y,S_folder_name_x}'.")
