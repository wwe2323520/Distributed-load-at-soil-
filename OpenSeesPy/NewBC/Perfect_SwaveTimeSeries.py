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
Sideforce_InX = np.zeros((len(time),100))
Sideforce_InY = np.zeros((len(time),100))

Sideforce_OutX = np.zeros((len(time),100))
Sideforce_OutY = np.zeros((len(time),100))

Cs_id = np.zeros(100)
eleSize = np.arange(0.0, 10, 0.1)

for i in range(100):
    Cs_id[i] = round((eleSize[i]/cs)*10000,0)

Tstep = 1870
for k in range(len(time)):
# ------- For S wave ------------------------------------
    if k <= 1870:
        SVel_FF[k] = np.sin(ws*time[k])/(-rho*cs*A)
eta_s = rho*cs
eta_p = rho*cp
for i in range(100):
    csid = int(Cs_id[i])
    for j in range(len(time)): #len(time)
# ------- For S wave ------------------------------------
        if j <= 1870:
            Sideforce_InX[csid+j,i] = -eta_p*SVel_FF[j]*A ;#-
            Sideforce_InY[csid+j,i] = +np.sin(ws*time[j])  ;#+

for i in range(100):
    csid = int(Cs_id[i])
    for j in range(len(time)): #len(time)
# ------- For S wave ------------------------------------
        if j >=Tstep and j < 2*Tstep:
            Sideforce_OutX[csid+j,99-i] = -eta_p*SVel_FF[j-Tstep]*A ;#-
            Sideforce_OutY[csid+j,99-i] = -np.sin(ws*time[j-Tstep])  ;#+
            
num_f = 100
force_id = np.empty(num_f, dtype=object)
for b in range(num_f):
    force_id[b] = f"ele{b+1}"    #r"$f_{%dx}$"%(2*b+1) # f"u{b+1}x"
            
# ---- Velocity Freefield Plot ----------------
# plt.figure()
# plt.plot(time,SVel_FF)
# plt.grid(True)


plt.figure()
plt.rcParams["figure.figsize"] = (12, 8)
plt.title("eleForce", fontsize = 18)
plt.xlabel("tns(s)",fontsize=18)

plt.plot(time,Sideforce_InX[:,0],label = force_id[0],marker='o', markevery=100)
plt.plot(time,Sideforce_InX[:,50],label = force_id[50],marker='x', markevery=100)
plt.plot(time,Sideforce_InX[:,99],label = force_id[99],marker='d', markevery=100)

# plt.plot(time,Sideforce_OutX[:,0],label = force_id[0],marker='o', markevery=100)
# plt.plot(time,Sideforce_OutX[:,50],label = force_id[50],marker='x', markevery=100)
# plt.plot(time,Sideforce_OutX[:,99],label = force_id[99],marker='d', markevery=100)
# for h in range(100):    #101
# # -------- S wave -----------------
#     # plt.plot(time,Sideforce_X[:,h],label = force_id[h])#force[4*i,:]
#     plt.plot(time,Sideforce_Y[:,h],label = force_id[h])#force[4*i,:]

plt.grid(True)   
plt.legend(loc='upper right',fontsize=10, ncol=5)
plt.xlim(0,0.7)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)


# ---- Output matrix eace column to txt file --------------
num_rows, num_cols = Sideforce_InY.shape# 8001,100
# 建立資料夾
# ---------- Pwave ---------------
P_folder_name_y = "S_Sideforce_Iny"
P_folder_name_x = "S_Sideforce_Inx"

os.makedirs(P_folder_name_y, exist_ok=True)
# 逐一建立txt檔案並放入資料夾
for col in range(num_cols):
    column_values = Sideforce_InY[:, col]
    output_file = f"ele{col + 1}.txt"
    with open(os.path.join(P_folder_name_y, output_file), 'w') as f:
        for value in column_values:
            f.write(f"{value}\n")

os.makedirs(P_folder_name_x, exist_ok=True)
for col in range(num_cols):
    column_values = Sideforce_InX[:, col]
    output_file = f"ele{col + 1}.txt"
    with open(os.path.join(P_folder_name_x, output_file), 'w') as f:
        for value in column_values:
            f.write(f"{value}\n")
            
num_rows, num_cols = Sideforce_OutY.shape# 8001,100
# 建立資料夾
# ---------- Pwave ---------------
P_folder_name_y = "S_Sideforce_Outy"
P_folder_name_x = "S_Sideforce_Outx"

os.makedirs(P_folder_name_y, exist_ok=True)
# 逐一建立txt檔案並放入資料夾
for col in range(num_cols):
    column_values = Sideforce_OutY[:, col]
    output_file = f"ele{col + 1}.txt"
    with open(os.path.join(P_folder_name_y, output_file), 'w') as f:
        for value in column_values:
            f.write(f"{value}\n")

os.makedirs(P_folder_name_x, exist_ok=True)
for col in range(num_cols):
    column_values = Sideforce_OutX[:, col]
    output_file = f"ele{col + 1}.txt"
    with open(os.path.join(P_folder_name_x, output_file), 'w') as f:
        for value in column_values:
            f.write(f"{value}\n")
            
# print(f"Txt files have been saved in the folder '{S_folder_name_y,S_folder_name_x}'.")
