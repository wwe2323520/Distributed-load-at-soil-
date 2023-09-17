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
pi = np.pi
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

# lamb_cs = 0.1 #total length cs
Soil_10row= 10 # dt= 5e-4       #cpdt = 2.67e-4
Soil_20row= 20 # dt= 2.5e-4     #cpdt = 1.33e-4
Soil_40row= 40 # dt= 1.25e-4    #cpdt = 6.68e-05
Soil_80row= 80 # dt= 6.25e-05   #cpdt = 3.34e-05
Soil_100row= 100 # dt= 6.25e-05   #cpdt = 3.34e-05

cs = 200 # m/s
L = 10 # m(Soil_Depth)
# fp = cp/L 
# Tp = 1/fp
nu = 0.3  #  0.3 -> (epsilon_z /=0)
rho = 2000 #1600 kg/m3  ; =1.6 ton/m3  
G = (cs*cs)*rho  # N/m^2 = Kg/(m*s^2)
E =  G*2*(1+nu)  # N/m^2 = Kg/(m*s^2)
cp = (E*(1-nu)/((1+nu)*(1-2*nu)*rho))**(0.5)

A = 0.1# 0.1
w =  pi/5 # 0 to 10 = 0 to 2*pi => x = pi/5

# calculate eace step time
tns = L/cs # wave transport time
dcell = tns/Soil_80row #each cell time
dt = dcell/10 #eace cell have 10 steps
print(f"wave travel = {tns} ;dcell = {dcell} ;dt = {dt}")

time = np.arange(0.0,0.050005,dt)
Nt = len(time)
#----------- Soil Coordinate --------------
x = cs*time #m

yOut =  np.zeros(len(x))
def Incoming_wave(x,t):
    yIn = np.sin(w*(x-cs*t))
    return yIn

def Outcoming_wave(x,t):
    yOut = +np.sin(w*(x+cs*t))
    return yOut

Nele = 80
dy = L/Nele # 1, 0.1
dx= dy/10 # 0.1, 0.01 each element have 10 step dx

total_Transport = np.arange(0.0,20.1, dx)
XIn = np.zeros((len(total_Transport),Nele))


# ---------- Incoming wave -------------------
input_disp = 5 # 5
# X = 0~10 m 
for j in range(Nele):#Nele
    tin = time[input_disp+10*j] 
    x0 = dy*j + (dy/2)
    # print(x0,cs*tin)
    for i in range(801): #101/201/401/801/1001      
        xii = x0 + dx*i 
        XIn[5+10*j+i,j] = Incoming_wave(xii,tin)  #from 0.05m to 9.95m

# ---------- Outcoming wave -------------------
XOut = np.zeros((len(total_Transport),Nele))
Output_disp = 5 # 9.95
# X = 10m ~ 20m
for j in range(Nele):# Nele
    tout = time[Output_disp+10*j] 
    x0 = 9.9375-dy*j   #9.5/9.75/9.875/9.9375/9.95-dy*j 
    # print(x0,cs*tout)
    for i in range(801):   #101/201/401/801/1001    
        xoo = x0 + dx*i 
        XOut[795-10*j+i,79-j] = Outcoming_wave(xoo,tout)  #from 9.75m to 0.25m

total_time = np.arange(0.0,0.4001,dt) #5e-5 in 100row
wave1 = np.zeros((len(total_time),Nele))

# ===== New BC Sideforce on Left and Right ==============
# SSideforce_10rowx = np.zeros((len(total_time),Nele))
# SSideforce_10rowy = np.zeros((len(total_time),Nele))
# SSideforce_20rowx = np.zeros((len(total_time),Nele))
# SSideforce_20rowy = np.zeros((len(total_time),Nele))
# SSideforce_40rowx = np.zeros((len(total_time),Nele))
# SSideforce_40rowy = np.zeros((len(total_time),Nele))
SSideforce_80rowx = np.zeros((len(total_time),Nele))
SSideforce_80rowy = np.zeros((len(total_time),Nele))


# ===== Input Incoming Wave and Outcoming Wave to wave1 =======================
ForceX_Cofficient = (cp/cs)
# ForceY_Cofficient = 


vely_Coefficient =  2/(A*rho*cs)
for g in [i for i in range(Nele)]: #Nele
    to = int(10*g+5)
    for t in range(len(total_time)):
        if total_time[t] < 0.05:   #t < 1000:
            # wave1[to+t,g] += XIn[to+t,g]
            wave1[to+t,g] = wave1[to+t,g] + (vely_Coefficient* XIn[to+t,g])  # original wave transport
# ----- Swave eta_p*(Vx) --------------------------
            SSideforce_80rowx[to+t,g] = SSideforce_80rowx[to+t,g] + (ForceX_Cofficient *XIn[to+t,g])
# ----- Swave sigma xy --------------------------            
            SSideforce_80rowy[to+t,g] = SSideforce_80rowy[to+t,g] + (XIn[to+t,g])
    
        if total_time[t] >= 0.05 and total_time[t] < 0.1:  #t >= 1000 and t < 2000:
            # wave1[to+t,99-g] += XOut[t-to,99-g]
            wave1[to+t,79-g] = wave1[to+t,79-g] + (vely_Coefficient* XOut[t-to,79-g])  # original wave transport
# # ----- Swave eta_p*(Vx) --------------------------
            SSideforce_80rowx[to+t,79-g] = SSideforce_80rowx[to+t,79-g] + (ForceX_Cofficient *XOut[t-to,79-g])
# # ----- Swave sigma xy --------------------------            
            SSideforce_80rowy[to+t,79-g] = SSideforce_80rowy[to+t,79-g] + (-XOut[t-to,79-g])
            
            
            
# # ---- Output matrix eace column to txt file --------------
# num_rows, num_cols = SSideforce_80rowy.shape# 8001,100
# # 建立資料夾
# # ---------- Pwave ---------------
# P_folder_name_x = "SSideforce_80rowx"
# P_folder_name_y = "SSideforce_80rowy"

# os.makedirs(P_folder_name_x, exist_ok=True)
# for col in range(num_cols):
#     column_values = SSideforce_80rowx[:, col]
#     output_file = f"ele{col + 1}.txt"
#     with open(os.path.join(P_folder_name_x, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")

# os.makedirs(P_folder_name_y, exist_ok=True)
# # 逐一建立txt檔案並放入資料夾
# for col in range(num_cols):
#     column_values = SSideforce_80rowy[:, col]
#     output_file = f"ele{col + 1}.txt"
#     with open(os.path.join(P_folder_name_y, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")
         
# # #----------------------------- Left column file -----------------------------------
# # #　 ====== Mid Point File  ====================
# file1 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\SideDash_80row\node12961.out"
# file2 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\SideDash_80row\node6521.out"
# file3 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\SideDash_80row\node725.out"
# # file4 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\SideDash_10row\node1691.out"
# # file5 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\0.7mRefinement\10Row(Pwave)\node84.out"

# Mid20 = rdnumpy(file1)  # 1/2 Node Velocity
# Mid10 = rdnumpy(file2)  # 1/2 Node Velocity
# Mid1  = rdnumpy(file3)  # 1/2 Node Velocity

# # Mid80row = rdnumpy(file1)
# # Mid40row = rdnumpy(file2)
# # Mid20row = rdnumpy(file3)
# # Mid10row = rdnumpy(file4)

# # # #　 ====== Quarter Point File  ====================
# file6 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\SideDash_80row\node13001.out"
# file7 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\SideDash_80row\node6541.out"
# file8 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\SideDash_80row\node727.out"
# # file9 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\SideDash_10row\node1731.out"
# # file10 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\0.7mRefinement\10Row(Pwave)\node86.out"

# Quarter20 = rdnumpy(file6)  # 1/4 Node Velocity
# Quarter10 = rdnumpy(file7)  # 1/4 Node Velocity
# Quarter1 = rdnumpy(file8)  # 1/4 Node Velocity

# # Quarter80row = rdnumpy(file6)
# # Quarter40row = rdnumpy(file7)
# # Quarter20row = rdnumpy(file8)
# # Quarter10row = rdnumpy(file9)



# plt_axis2 = 1
# # ------- wave put into the timeSeries ---------------   
plt.figure(figsize=(8,6))
  
# plt.title(r'SideForce $\eta_{p}v_x$',fontsize = 18)  
# plt.ylabel(r"$\eta_{p}v_x$  $(N/m^2)$",fontsize=18) 

plt.title(r'SideForce  $\sigma_{xy}$',fontsize = 18) 
plt.ylabel(r"$\sigma_{xy}$  $(N/m^2)$",fontsize=18)  

plt.xlabel("time (s)",fontsize=18)

# plt.ylabel(r"$V_x$  $(m/s)$",fontsize=18)
# # ------ wave Transport -----------------
# plt.plot(total_time,wave1[:,0],label ='Ele 1', marker='o', markevery=100)
# plt.plot(total_time,wave1[:,40],label ='Ele 40', marker='x', markevery=100)
# plt.plot(total_time,wave1[:,79],label ='Ele 80', marker='x', markevery=100)
# # plt.title('Mid Point',fontsize = 18) 
# plt.plot(total_time,wave1[:,99],label ='Analytical',color= 'black',linewidth=2.0)
# plt.plot(Mid20[:,0],Mid20[:,plt_axis2],label ='20m Soil(0.125m)', ls = '--',linewidth=6.0)
# plt.plot(Mid10[:,0],Mid10[:,plt_axis2],label ='10m Soil(0.125m)', ls = '-.',linewidth=4.0)
# plt.plot(Mid1[:,0],Mid1[:,plt_axis2],label ='1m Soil(0.125m)', ls = ':',linewidth=2.0)

# # # # # plt.title('Quarter Point',fontsize = 18) 
# # plt.plot(total_time,wave1[:,99],label ='Analytical',color= 'black',linewidth=2.0)
# # plt.plot(Quarter20[:,0],Quarter20[:,plt_axis2],label ='20m Soil(0.125m)', ls = '--',linewidth=6.0)
# # plt.plot(Quarter10[:,0],Quarter10[:,plt_axis2],label ='10m Soil(0.125m)', ls = '-.',linewidth=4.0)
# # plt.plot(Quarter1[:,0],Quarter1[:,plt_axis2],label ='1m Soil(0.125m)', ls = ':',linewidth=2.0)

# # # Refinement  Mid node:
# # plt.plot(total_time,wave1[:,99],label ='Analytical',color= 'black',linewidth=2.0)
# # plt.plot(Mid80row[:,0],Mid80row[:,plt_axis2],label ='20msoil(0.125m)', ls = '--',linewidth=6.0)
# # plt.plot(Mid40row[:,0],Mid40row[:,plt_axis2],label ='20msoil(0.25m)', ls = '-.',linewidth=4.0)
# # plt.plot(Mid20row[:,0],Mid20row[:,plt_axis2],label ='20msoil(0.50m)', ls = ':',linewidth=3.0)
# # plt.plot(Mid10row[:,0],Mid10row[:,plt_axis2],label ='20msoil(1m)', ls = '-',linewidth=2.0)

# # plt.plot(Mid10row[:,0],Mid10row[:,plt_axis2],label ='10row', ls = 'dotted',linewidth=4.0)

# # # Refinement  Quarter node:
# # plt.plot(total_time,wave1[:,99],label ='Analytical',color= 'black',linewidth=2.0)
# # plt.plot(Quarter80row[:,0],Quarter80row[:,plt_axis2],label ='20msoil(0.125m)', ls = '--',linewidth=6.0)
# # plt.plot(Quarter40row[:,0],Quarter40row[:,plt_axis2],label ='20msoil(0.25m)', ls = '-.',linewidth=4.0)
# # plt.plot(Quarter20row[:,0],Quarter20row[:,plt_axis2],label ='20msoil(0.50m)', ls = ':',linewidth=3.0)
# # plt.plot(Quarter10row[:,0],Quarter10row[:,plt_axis2],label ='20msoil(1m)', ls = '-',linewidth=2.0)

# # plt.plot(Quarter10row[:,0],Quarter10row[:,plt_axis2],label ='10row', ls = 'dotted',linewidth=4.0)




# # ----- Swave  eta_p*(Vx) --------------------------
# plt.plot(total_time,SSideforce_80rowx[:,0],label ='Ele 1', marker='o', markevery=100)
# plt.plot(total_time,SSideforce_80rowx[:,40],label ='Ele 40', marker='x', markevery=100)
# plt.plot(total_time,SSideforce_80rowx[:,79],label ='Ele 80', marker='d', markevery=100)

# ----- Swave sigma_Xy -------------
plt.plot(total_time,SSideforce_80rowy[:,0],label ='Ele 1', marker='o', markevery=100)
plt.plot(total_time,SSideforce_80rowy[:,40],label ='Ele 40', marker='x', markevery=100)
plt.plot(total_time,SSideforce_80rowy[:,79],label ='Ele 80', marker='d', markevery=100)

plt.legend(loc='upper right',fontsize=18) #ncol=2
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlim(0.0, 0.40)
plt.grid(True)

# x_axis = 0.05 # 0.1 0.05
ax4 = plt.gca()
# ax4.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax4.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax4.yaxis.get_offset_text().set(size=18)

# # ========== Incoming Wave ==========================================
# plt.figure()
# plt.title('Incoming Wave',fontsize = 18)
# plt.xlabel("x(m)",fontsize=18)
# plt.ylabel(r"$y=sin(x-c_{s}t)$",fontsize=18)
# plt.plot(total_Transport,XIn[:,0],label ='Element 1',marker='o', markevery=100)
# plt.plot(total_Transport,XIn[:,40],label ='Element 40',marker='d', markevery=100)
# plt.plot(total_Transport,XIn[:,79],label ='Element 80',marker='x', markevery=100)
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
# plt.plot(total_Transport,XOut[:,40],label ='Element 40',marker='d', markevery=100)
# plt.plot(total_Transport,XOut[:,79],label ='Element 80',marker='x', markevery=100)
# plt.xlim(0,20.0)

# plt.legend(loc='upper right',fontsize=18)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid(True)
    
