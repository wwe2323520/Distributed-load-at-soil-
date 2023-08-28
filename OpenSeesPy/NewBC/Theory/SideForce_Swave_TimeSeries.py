# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 22:41:51 2023

@author: User
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

pi = np.pi

cp = 100.0 # m/s
L = 10 # m(Soil_Depth)
# fp = cp/L 
# Tp = 1/fp
nu = 0.3  #  0.3 -> (epsilon_z /=0)
rho = 2020 #1600 kg/m3  ; =1.6 ton/m3  
E = (cp*cp)*rho*(1+nu)*(1-2*nu)/(1-nu)
G = E/(2*(1+nu))
cs = (G/rho)**(0.5) #m/s

w =  pi/5 # 0 to 10 = 0 to 2*pi => x = pi/5

tns = L/cs # Swave transport to surface time

time = np.arange(0.0,0.1871,1e-4)
Nt = len(time)
#----------- Soil Coordinate --------------
x = cs*time #m
def Incoming_wave(x,t):
    return np.sin(w*(x-cs*t))

def Outcoming_wave(x,t):
    return np.sin(w*(x+cs*t))

#---------------- To decide beam Center node id ----------------------
def diff_val(xvalue: float, absvalue: float) -> float:
    return abs(xvalue-absvalue)

cs_id = []
count = 0
for j in [float(0.05 + 0.1*i) for i in range(100)]: #Nele
    for i in range(Nt-1):
        lv = x[i]
        rv = x[i+1]
        judge_value = j
        if (lv <= judge_value and judge_value <= rv):
            rdval = diff_val(rv, judge_value)
            ldval = diff_val(lv, judge_value)
            if (rdval < ldval):
                cs_id.append(i+1)
                # print(f"judge value = {judge_value}, rval = {rv}, i = {i+1}")
            else:
                cs_id.append(i)
                # print(f"judge value = {judge_value}, lval = {lv}, i = {i}")
            count += 1
            break
cs_id = np.array(cs_id, dtype = int)
# print(count)

total_Transport = np.arange(0.0,30.1, (10/1870))

Nele = 100

dx= 10/1870 # total soil have 1870 step in Cs from 0-10m
# ---------- Incoming wave ------------------
XIn = np.zeros((len(total_Transport),100))
# X = 0~10 m 
for j in range(Nele): #100
    # tin = time[input_disp+10*j]
    csid = cs_id[j]
    tin = time[cs_id[j]]
    x0 = x[csid]  # 0.05,0.15,0.25....,9.95
    # print(x0,cs*tin)
    for i in range(1870):      
        xii = x0 + dx*i 
        XIn[cs_id[j]+i,j] = Incoming_wave(xii,tin)  #from 0.05m to 9.95m
        
# ---------- Outcoming wave -------------------
XOut = np.zeros((len(total_Transport),100))
# Output_disp = 5 # 9.95
# X = 10m ~ 20m
for j in range(Nele):# 100
    # tout = time[Output_disp+10*j] 
    csid = cs_id[99-j]
    tout = time[cs_id[j]]
    x0 = x[csid] 
    # print(cs*tout,x0)
    for i in range(1870):      
        xoo = x0 + dx*i 
        XOut[csid+i,99-j] = Outcoming_wave(xoo,tout)  #from 9.95m to 0.05m       
        
total_time = np.arange(0.0,0.6001,1e-4)
Swave = np.zeros((len(total_time),Nele))

# ===== New BC Sideforce on Left and Right ==============
SSideforce_x = np.zeros((len(total_time),Nele))
SSideforce_y = np.zeros((len(total_time),Nele))

ForceX_Cofficient = (cp/cs)
# ===== Input Incoming Wave and Outcoming Wave to wave1 =======================
for g in range(100): #Nele
    to = cs_id[g]
    for t in range(len(total_time)):
        if t < 1870:
            # Swave[to+t,g] = (Swave[to+t,g] + XIn[to+t,g])  # original wave transport
# ----- Swave eta_p*(Vx) --------------------------
            SSideforce_x[to+t,g] = SSideforce_x[to+t,g] + (ForceX_Cofficient *XIn[to+t,g])
# ----- Swave sigma_yy --------------------------   
            SSideforce_y[to+t,g] = SSideforce_y[to+t,g] + (XIn[to+t,g])
        if t >= 1870 and t < (1870*2):
            # Swave[to+t,99-g] = Swave[to+t,99-g] + XOut[t-to,99-g]   # original wave transport
# ----- Swave sigma xx --------------------------
            SSideforce_x[to+t,99-g] = SSideforce_x[to+t,99-g] + (ForceX_Cofficient *XOut[t-to,99-g])
# ----- Swave sigma_yy --------------------------
            SSideforce_y[to+t,99-g] = SSideforce_y[to+t,99-g] + (-XOut[t-to,99-g])

# # ---- Output matrix eace column to txt file --------------
# num_rows, num_cols = SSideforce_y.shape# 8001,100
# # 建立資料夾
# # ---------- Pwave ---------------
# S_folder_name_x = "S_Sideforce_x"
# S_folder_name_y = "S_Sideforce_y"

# os.makedirs(S_folder_name_x, exist_ok=True)
# for col in range(num_cols):
#     column_values = SSideforce_x[:, col]
#     output_file = f"ele{col + 1}.txt"
#     with open(os.path.join(S_folder_name_x, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")

# os.makedirs(S_folder_name_y, exist_ok=True)
# # 逐一建立txt檔案並放入資料夾
# for col in range(num_cols):
#     column_values = SSideforce_y[:, col]
#     output_file = f"ele{col + 1}.txt"
#     with open(os.path.join(S_folder_name_y, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")
            
# ------- wave put into the timeSeries ---------------   
plt.figure()
# plt.title('Wave Transport',fontsize = 18)   
 
# plt.title(r'SideForce $\sigma_{xy}$',fontsize = 18)         
plt.title(r'SideForce $\eta_{p}v_x$',fontsize = 18)   
plt.xlabel("tns(s)",fontsize=18)
# # ----- Swave eta_p*(Vx) -------------
plt.plot(total_time,SSideforce_x[:,0],label ='Element 1', marker='o', markevery=100)
plt.plot(total_time,SSideforce_x[:,50],label ='Element 51', marker='x', markevery=100)
plt.plot(total_time,SSideforce_x[:,99],label ='Element 100', marker='d', markevery=100)

# ----- Swave sigma_xy -------------
# plt.plot(total_time,SSideforce_y[:,0],label ='Element 1', marker='o', markevery=100)
# plt.plot(total_time,SSideforce_y[:,50],label ='Element 51', marker='x', markevery=100)
# plt.plot(total_time,SSideforce_y[:,99],label ='Element 100', marker='d', markevery=100)

plt.legend(loc='upper right',fontsize=18)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlim(0.0, 0.60)
plt.grid(True)
# ========== Incoming Wave ==========================================
plt.figure()
plt.title('Incoming Wave',fontsize = 18)
plt.xlabel("x(m)",fontsize=18)
plt.ylabel(r"$y=sin\omega(x-c_{s}t)$",fontsize=18)
plt.plot(total_Transport,XIn[:,0],label ='Element 1',marker='o', markevery=100)
plt.plot(total_Transport,XIn[:,50],label ='Element 50',marker='d', markevery=100)
plt.plot(total_Transport,XIn[:,99],label ='Element 100',marker='x', markevery=100)
plt.legend(loc='upper right',fontsize=18)
plt.xlim(0,20.0)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid(True)

# ========== Outcoming Wave ==========================================
plt.figure()
plt.title('Outcoming Wave',fontsize = 18)
plt.xlabel("x(m)",fontsize=18)
plt.ylabel(r"$y=sin\omega(x+c_{s}t)$",fontsize=18)
plt.plot(total_Transport,XOut[:,0],label ='Element 1',marker='o', markevery=100)
plt.plot(total_Transport,XOut[:,50],label ='Element 50',marker='d', markevery=100)
plt.plot(total_Transport,XOut[:,99],label ='Element 100',marker='x', markevery=100)
plt.xlim(0,20.0)

plt.legend(loc='upper right',fontsize=18)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid(True)

        
