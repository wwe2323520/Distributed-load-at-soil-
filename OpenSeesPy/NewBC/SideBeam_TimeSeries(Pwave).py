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
A = 0.1*1
time = np.arange(0.0,0.1001,1e-4)

#----------- Soil Coordinate --------------
x = cp*time #m

yOut =  np.zeros(len(x))
def Incoming_wave(x,t):
    yIn = np.sin(w*(x-cp*t))
    return yIn

def Outcoming_wave(x,t):
    yOut = +np.sin(w*(x+cp*t))
    return yOut

total_Transport = np.arange(0.0,20.1, 0.01)
XIn = np.zeros((len(total_Transport),100))

Nele = 100
dy = L/Nele # 0.1
dx= 10/1000 # 0.01 each element have 10 step dx

# ---------- Incoming wave -------------------
input_disp = 5 # 5
# X = 0~10 m 
for j in range(Nele):
    tin = time[input_disp+10*j] 
    x0 = dy*j + 0.05
    # print(x0,cp*tin)
    for i in range(1001):      
        x = x0 + dx*i 
        XIn[5+10*j+i,j] = Incoming_wave(x,tin)  #from 0.05m to 9.95m

# ---------- Outcoming wave -------------------
XOut = np.zeros((len(total_Transport),100))
Output_disp = 5 # 9.95
# X = 10m ~ 20m
for j in range(100):# Nele
    tout = time[Output_disp+10*j] 
    x0 = 9.95-dy*j 
    # x0 = dy*j + 0.05
    for i in range(1001):      
        x = x0 + dx*i 
        XOut[995-10*j+i,99-j] = Outcoming_wave(x,tout)  #from 9.95m to 0.05m

total_time = np.arange(0.0,0.8001,1e-4)
wave1 = np.zeros((len(total_time),Nele))

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


vely_Coefficient =  2/(A*rho*cp)
for g in [i for i in range(100)]: #Nele
    to = int(10*g+5)
    for t in range(len(total_time)):
        if t < 1000:
            # wave1[to+t,g] += XIn[to+t,g]
            wave1[to+t,g] = wave1[to+t,g] + (vely_Coefficient* XIn[to+t,g])  # original wave transport
# ----- Pwave sigma xx --------------------------
            PSideforce_x[to+t,g] = PSideforce_x[to+t,g] + (ForceX_Cofficient *XIn[to+t,g])
# ----- Pwave eta_S*(Vy) --------------------------            
            PSideforce_y[to+t,g] = PSideforce_y[to+t,g] + (ForceY_Cofficient *XIn[to+t,g])
    
        if t >= 1000 and t < 2000:
            # wave1[to+t,99-g] += XOut[t-to,99-g]
            wave1[to+t,99-g] = wave1[to+t,99-g] + (vely_Coefficient* XOut[t-to,99-g])  # original wave transport
# ----- Pwave sigma xx --------------------------
            PSideforce_x[to+t,99-g] = PSideforce_x[to+t,99-g] + (-ForceX_Cofficient *XOut[t-to,99-g])
# ----- Pwave eta_S*(Vy) --------------------------            
            PSideforce_y[to+t,99-g] = PSideforce_y[to+t,99-g] + (ForceY_Cofficient *XOut[t-to,99-g])
            
            
            
# # ---- Output matrix eace column to txt file --------------
# num_rows, num_cols = PSideforce_y.shape# 8001,100
# # 建立資料夾
# # ---------- Pwave ---------------
# P_folder_name_x = "P_Sideforce_x"
# P_folder_name_y = "P_Sideforce_y"

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
         
#----------------------------- Left column file -----------------------------------
#　 ====== Mid Point File  ====================
file1 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\0.7mRefinement\160Row(Pwave)\node1284.out"
file2 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\0.7mRefinement\80Row(Pwave)\node644.out"
file3 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\0.7mRefinement\40Row(Pwave)\node324.out"
file4 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\0.7mRefinement\20Row(Pwave)\node164.out"
file5 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\0.7mRefinement\10Row(Pwave)\node84.out"

# Mid20 = rdnumpy(file1)  # 1/2 Node Velocity
# Mid10 = rdnumpy(file2)  # 1/2 Node Velocity
# Mid7  = rdnumpy(file3)  # 1/2 Node Velocity

Mid160row = rdnumpy(file1)
Mid80row = rdnumpy(file2)
Mid40row = rdnumpy(file3)
Mid20row = rdnumpy(file4)
Mid10row = rdnumpy(file5)
# #　 ====== Quarter Point File  ====================
file6 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\0.7mRefinement\160Row(Pwave)\node1286.out"
file7 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\0.7mRefinement\80Row(Pwave)\node646.out"
file8 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\0.7mRefinement\40Row(Pwave)\node326.out"
file9 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\0.7mRefinement\20Row(Pwave)\node166.out"
file10 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\0.7mRefinement\10Row(Pwave)\node86.out"

# Quarter20 = rdnumpy(file4)  # 1/4 Node Velocity
# Quarter10m = rdnumpy(file5)  # 1/4 Node Velocity
# Quarter7m = rdnumpy(file6)  # 1/4 Node Velocity

Quarter160row = rdnumpy(file6)
Quarter80row = rdnumpy(file7)
Quarter40row = rdnumpy(file8)
Quarter20row = rdnumpy(file9)
Quarter10row = rdnumpy(file10)


plt_axis2 = 2
# ------- wave put into the timeSeries ---------------   
plt.figure(figsize=(8,6))
  
# plt.title(r'SideForce  $\sigma_{xx}$',fontsize = 18) 
# plt.ylabel(r"$\sigma_{xx}$  $(N/m^2)$",fontsize=18)  
      
# plt.title(r'NodeForce $\eta_{s}v_y$',fontsize = 18)  
# plt.ylabel(r"$\eta_{s}v_y$  $(N/m^2)$",fontsize=18) 

plt.xlabel("time (s)",fontsize=18)


plt.ylabel(r"$V_y$  $(m/s)$",fontsize=18)
# ------ wave Transport -----------------
# plt.plot(total_time,wave1[:,0],label ='Ele 1', marker='o', markevery=100)
# plt.plot(total_time,wave1[:,50],label ='Ele 51', marker='x', markevery=100)

# plt.title('Mid Point',fontsize = 18) 
# plt.plot(total_time,wave1[:,99],label ='Analytical',color= 'black',linewidth=2.0)
# plt.plot(Mid20[:,0],Mid20[:,plt_axis2],label ='20m Soil', ls = '--',linewidth=4.0)
# plt.plot(Mid10[:,0],Mid10[:,plt_axis2],label ='10m Soil', ls = '-.',linewidth=4.0)
# plt.plot(Mid7[:,0],Mid7[:,plt_axis2],label ='0.7m Soil', ls = ':',linewidth=4.0)

# # # # plt.title('Quarter Point',fontsize = 18) 
# plt.plot(total_time,wave1[:,99],label ='Analytical',color= 'black',linewidth=2.0)
# plt.plot(Quarter20[:,0],Quarter20[:,plt_axis2],label ='20m Soil', ls = '--',linewidth=4.0)
# plt.plot(Quarter10m[:,0],Quarter10m[:,plt_axis2],label ='10m Soil', ls = '-.')
# plt.plot(Quarter7m[:,0],Quarter7m[:,plt_axis2],label ='0.7m Soil', ls = ':',linewidth=4.0)

# # Refinement  Mid node:
# plt.plot(total_time,wave1[:,99],label ='Analytical',color= 'black',linewidth=2.0)
# plt.plot(Mid160row[:,0],Mid160row[:,plt_axis2],label ='160row', ls = '--',linewidth=4.0)
# plt.plot(Mid80row[:,0],Mid80row[:,plt_axis2],label ='80row', ls = '-.',linewidth=4.0)
# plt.plot(Mid40row[:,0],Mid40row[:,plt_axis2],label ='40row', ls = ':',linewidth=4.0)
# plt.plot(Mid20row[:,0],Mid20row[:,plt_axis2],label ='20row', ls = '-',linewidth=4.0)
# plt.plot(Mid10row[:,0],Mid10row[:,plt_axis2],label ='10row', ls = 'dotted',linewidth=4.0)

# Refinement  Quarter node:
plt.plot(total_time,wave1[:,99],label ='Analytical',color= 'black',linewidth=2.0)
plt.plot(Quarter160row[:,0],Quarter160row[:,plt_axis2],label ='160row', ls = '--',linewidth=4.0)
plt.plot(Quarter80row[:,0],Quarter80row[:,plt_axis2],label ='80row', ls = '-.',linewidth=4.0)
plt.plot(Quarter40row[:,0],Quarter40row[:,plt_axis2],label ='40row', ls = ':',linewidth=4.0)
plt.plot(Quarter20row[:,0],Quarter20row[:,plt_axis2],label ='20row', ls = '-',linewidth=4.0)
plt.plot(Quarter10row[:,0],Quarter10row[:,plt_axis2],label ='10row', ls = 'dotted',linewidth=4.0)




# # ----- Pwave sigma xx --------------------------
# plt.plot(total_time,PSideforce_x[:,0],label ='Ele 1', marker='o', markevery=100)
# plt.plot(total_time,PSideforce_x[:,50],label ='Ele 51', marker='x', markevery=100)
# plt.plot(total_time,PSideforce_x[:,99],label ='Ele 100', marker='d', markevery=100)

# # ----- Pwave eta_S*(Vy) -------------
# plt.plot(total_time,PSideforce_y[:,0],label ='Ele 1', marker='o', markevery=100)
# plt.plot(total_time,PSideforce_y[:,50],label ='Ele 51', marker='x', markevery=100)
# plt.plot(total_time,PSideforce_y[:,99],label ='Ele 100', marker='d', markevery=100)

plt.legend(loc='upper right',fontsize=16)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlim(0.0, 0.80)
plt.grid(True)

x_axis = 0.1 # 0.1 0.05
ax4 = plt.gca()
ax4.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax4.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax4.yaxis.get_offset_text().set(size=18)

# # # ========== Incoming Wave ==========================================
# plt.figure()
# plt.title('Incoming Wave',fontsize = 18)
# plt.xlabel("x(m)",fontsize=18)
# plt.ylabel(r"$y=sin(x-c_{p}t)$",fontsize=18)
# plt.plot(total_Transport,XIn[:,0],label ='Element 1',marker='o', markevery=100)
# plt.plot(total_Transport,XIn[:,50],label ='Element 50',marker='d', markevery=100)
# plt.plot(total_Transport,XIn[:,99],label ='Element 100',marker='x', markevery=100)
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
# plt.plot(total_Transport,XOut[:,50],label ='Element 50',marker='d', markevery=100)
# plt.plot(total_Transport,XOut[:,99],label ='Element 100',marker='x', markevery=100)
# plt.xlim(0,20.0)

# plt.legend(loc='upper right',fontsize=18)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid(True)
    
