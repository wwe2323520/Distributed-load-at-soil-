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
PVel_FF = np.zeros(len(time))

# -------- P WAVE -----------------
Sideforce_y = np.zeros((len(time),100))
Sideforce_x = np.zeros((len(time),100))

    
for k in range(len(time)):
    if k < 1001:
# ------- For P wave ------------------------------------
        PVel_FF[k] = np.sin(wp*time[k])/(-rho*cp*A)
step = 1000#1000
Tstep = 2*step
        
eta_s = rho*cs
eta_p = rho*cp
for i in range(100):#100
    for j in range(len(time)): #len(time)
# ------- For P wave ------------------------------------
        if j <= 1000:
            Sideforce_y[10*i+j,i] = -eta_s*PVel_FF[j]*A
            Sideforce_x[10*i+j,i] = (nu/(1-nu))*np.sin(wp*time[j])
            
        if j >= 1000 and j <= 2000:
            Sideforce_y[10*i+j,99-i] = -eta_s*PVel_FF[j-step]*A #-
            Sideforce_x[10*i+j,99-i] = -(nu/(1-nu))*np.sin(wp*time[j-step]) #+
        
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
for h in range(100):    #101
# -------- P wave -----------------
    plt.plot(time,Sideforce_y[:,h],label = force_id[h])#force[4*i,:]
    plt.plot(time,Sideforce_x[:,h],label = force_id[h])#force[4*i,:]


plt.grid(True)   
plt.legend(loc='upper right',fontsize=10, ncol=5)
plt.xlim(0,0.3)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)

# ---- Output matrix eace column to txt file --------------
num_rows, num_cols = Sideforce_y.shape# 8001,100
# 建立資料夾
# ---------- Pwave ---------------
P_folder_name_y = "P_Sideforce_y"
P_folder_name_x = "P_Sideforce_x"

os.makedirs(P_folder_name_y, exist_ok=True)
# 逐一建立txt檔案並放入資料夾
for col in range(num_cols):
    column_values = Sideforce_y[:, col]
    output_file = f"ele{col + 1}.txt"
    with open(os.path.join(P_folder_name_y, output_file), 'w') as f:
        for value in column_values:
            f.write(f"{value}\n")

os.makedirs(P_folder_name_x, exist_ok=True)
for col in range(num_cols):
    column_values = Sideforce_x[:, col]
    output_file = f"ele{col + 1}.txt"
    with open(os.path.join(P_folder_name_x, output_file), 'w') as f:
        for value in column_values:
            f.write(f"{value}\n")
