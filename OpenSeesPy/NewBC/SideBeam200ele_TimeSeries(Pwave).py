# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 16:01:18 2023

@author: User
"""
# vel[i] = -P*np.sin(ws*time[i])/(-rho*cs*A)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

plt.rc('font', family= 'Times New Roman')
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

pi = np.pi

cp = 100.0 # m/s
L = 10 # m(Soil_Depth)
fp = cp/L 
Tp = 1/fp
w =  pi/5 # 0 to 10 = 0 to 2*pi => x = pi/5
A = 0.05#0.1*1

dt = 5e-5
time = np.arange(0.0,0.1001,dt) #5e-5

#----------- Soil Coordinate --------------
x = cp*time #m

yOut =  np.zeros(len(x))
def Incoming_wave(x,t):
    yIn = np.sin(w*(x-cp*t))
    return yIn

def Outcoming_wave(x,t):
    yOut = +np.sin(w*(x+cp*t))
    return yOut

dtotal = dt*cp
total_Transport = np.arange(0.0,20.1, dtotal) # dtotal= 100*5e-5=5e-3
XIn = np.zeros((len(total_Transport),200))

Nele = 200
dy = L/Nele # 0.1
dx= 10/2000 #  each element size 0.05 have 10 step dx -> 0.05m*200 ele => 200*10step = 2000

# ---------- Incoming wave -------------------
input_disp = 5 # 5
# X = 0~10 m 
for j in range(Nele): #Nele
    tin = time[input_disp+10*j] 
    x0 = dy*j + 0.025  # x from the initial coordinate
    # print(j,x0,cp*tin)
    for i in range(len(time)-1):      
        xii = x0 + dx*i 
        XIn[5+10*j+i,j] = Incoming_wave(xii,tin)  #from 0.025m to 9.975m

# ---------- Outcoming wave -------------------
XOut = np.zeros((len(total_Transport),200))
Output_disp = 5 # 9.95
# X = 10m ~ 20m
for j in range(Nele):# Nele
    tout = time[Output_disp+10*j] 
    x0 = 9.975-dy*j 

    for i in range(len(time)-1):      
        xoo = x0 + dx*i 
        XOut[1995-10*j+i,199-j] = Outcoming_wave(xoo,tout)  #from 9.95m to 0.05m

total_time = np.arange(0.0,0.80005,5e-5)
wave1 = np.zeros((len(total_time),Nele))

# plt.plot(total_Transport,XIn[:,0])
# plt.plot(total_Transport,XIn[:,100])
# plt.plot(total_Transport,XIn[:,199])
# plt.grid(True)
# ===== New BC Sideforce on Left and Right ==============
PSideforce_x = np.zeros((len(total_time),Nele))
PSideforce_y = np.zeros((len(total_time),Nele))

# ===== Input Incoming Wave and Outcoming Wave to wave1 =======================
nu = 0.3  #  0.3 -> (epsilon_z /=0)
rho = 2020 #1600 kg/m3  ; =1.6 ton/m3  
cp = 100 #m/s
E = (cp*cp)*rho*(1+nu)*(1-2*nu)/(1-nu)
G = E/(2*(1+nu))

cs = (G/rho)**(0.5) #m/s

ForceX_Cofficient = (nu/(1-nu))
ForceY_Cofficient = (cs/cp)


vely_Coefficient =  1/(A*rho*cp)
for g in [i for i in range(Nele)]: #Nele=200
    to = int(10*g+5)
    for t in range(len(total_time)):
        if total_time[t] < 0.1:         # if t < 2000:
            # wave1[to+t,g] += XIn[to+t,g]
            wave1[to+t,g] = wave1[to+t,g] + (vely_Coefficient* XIn[to+t,g])  # original wave Velocity transport
# ----- Pwave sigma xx --------------------------
            PSideforce_x[to+t,g] = PSideforce_x[to+t,g] + (ForceX_Cofficient *XIn[to+t,g])
# ----- Pwave eta_S*(Vy) --------------------------            
            PSideforce_y[to+t,g] = PSideforce_y[to+t,g] + (ForceY_Cofficient *XIn[to+t,g])
    
        if total_time[t] >= 0.1 and total_time[t] < 0.2: # if t > 2000 and t <4000:
            # wave1[to+t,199-g] += XOut[t-to,199-g]
            wave1[to+t,199-g] = wave1[to+t,199-g] + (vely_Coefficient* XOut[t-to,199-g])  # original wave Velocity transport
# ----- Pwave sigma xx --------------------------
            PSideforce_x[to+t,199-g] = PSideforce_x[to+t,199-g] + (-ForceX_Cofficient *XOut[t-to,199-g])
# ----- Pwave eta_S*(Vy) --------------------------            
            PSideforce_y[to+t,199-g] = PSideforce_y[to+t,199-g] + (ForceY_Cofficient *XOut[t-to,199-g])
            
            
            
# # ---- Output matrix eace column to txt file --------------
# num_rows, num_cols = PSideforce_y.shape# 16002,200
# # 建立資料夾
# # ---------- Pwave ---------------
# P_folder_name_x = "P_Sideforce200ele_x"
# P_folder_name_y = "P_Sideforce200ele_y"

# os.makedirs(P_folder_name_x, exist_ok=True)
# for col in range(num_cols):
#     column_values = PSideforce_x[:, col]
#     output_file = f"ele{col + 1}.txt"
#     with open(os.path.join(P_folder_name_x, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")

# os.makedirs(P_folder_name_y, exist_ok=True)
# # 逐一建立txt檔案並放入資料夾
# for col in range(num_cols):
#     column_values = PSideforce_y[:, col]
#     output_file = f"ele{col + 1}.txt"
#     with open(os.path.join(P_folder_name_y, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")
        

plt_axis2 = 2
# ------- wave put into the timeSeries ---------------   
plt.figure(figsize=(8,6))
  
# plt.title(r'SideForce  $\sigma_{xx}$',fontsize = 18) 
# plt.ylabel(r"$\sigma_{xx}$  $(N/m^2)$",fontsize=18)  
      
plt.title(r'SideForce $\eta_{s}v_y$',fontsize = 18)  
plt.ylabel(r"$\eta_{s}v_y$  $(N/m^2)$",fontsize=18) 

# plt.title(r'$v_y$ $m/s$',fontsize = 18) 
plt.xlabel("time (s)",fontsize=18)


# plt.ylabel(r"$V_y$  $(m/s)$",fontsize=18)
# # ------ wave Transport -----------------
# plt.plot(total_time,wave1[:,0],label ='Ele 1', marker='o', markevery=100)
# plt.plot(total_time,wave1[:,100],label ='Ele 51', marker='x', markevery=100)
# plt.plot(total_time,wave1[:,199],label ='Ele 199', marker='x', markevery=100)


# # ----- Pwave sigma xx --------------------------
# plt.plot(total_time,PSideforce_x[:,0],label ='Ele 1', marker='o', markevery=100)
# plt.plot(total_time,PSideforce_x[:,100],label ='Ele 100', marker='x', markevery=100)
# plt.plot(total_time,PSideforce_x[:,199],label ='Ele 199', marker='d', markevery=100)

# plt.plot(total_time,PSideforce_x[:,50],label ='Ele 50', marker='x', markevery=100)
# ----- Pwave eta_S*(Vy) -------------
plt.plot(total_time,PSideforce_y[:,0],label ='Ele 1', marker='o', markevery=100)
plt.plot(total_time,PSideforce_y[:,100],label ='Ele 100', marker='x', markevery=100)
plt.plot(total_time,PSideforce_y[:,199],label ='Ele 199', marker='d', markevery=100)

plt.legend(loc='upper right',fontsize=18)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlim(0.0, 0.80)
plt.grid(True)

# x_axis = 0.05 # 0.1 0.05
ax4 = plt.gca()
# ax4.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax4.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax4.yaxis.get_offset_text().set(size=18)

# ========== Incoming Wave ==========================================
# plt.figure()
# plt.title('Incoming Wave',fontsize = 18)
# plt.xlabel("x(m)",fontsize=18)
# plt.ylabel(r"$y=sin(x-c_{p}t)$",fontsize=18)
# plt.plot(total_Transport,XIn[:,0],label ='Element 1',marker='o', markevery=100)
# plt.plot(total_Transport,XIn[:,100],label ='Element 50',marker='d', markevery=100)
# plt.plot(total_Transport,XIn[:,199],label ='Element 100',marker='x', markevery=100)
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
# plt.plot(total_Transport,XOut[:,0],label ='Element 1',marker='o', markevery=100)
# plt.plot(total_Transport,XOut[:,100],label ='Element 50',marker='d', markevery=100)
# plt.plot(total_Transport,XOut[:,199],label ='Element 100',marker='x', markevery=100)
# plt.xlim(0,20.0)

# plt.legend(loc='upper right',fontsize=18)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid(True)
    
