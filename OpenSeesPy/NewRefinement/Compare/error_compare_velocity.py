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
Soil_100row= 100 # dt= 5e-05   #cpdt = 

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
dcell = tns/Soil_100row #each cell time
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

Nele = 100
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

    for i in range(1001): #1001      
        xii = x0 + dx*i 
        XIn[5+10*j+i,j] = Incoming_wave(xii,tin)  #from 0.05m to 9.95m

# ---------- Outcoming wave -------------------
XOut = np.zeros((len(total_Transport),Nele))
Output_disp = 5 # 9.95
# X = 10m ~ 20m
for j in range(Nele):# Nele
    tout = time[Output_disp+10*j] 
    x0 = 9.95-dy*j   #9.95-dy*j 

    for i in range(1001):      
        xoo = x0 + dx*i 
        XOut[995-10*j+i,99-j] = Outcoming_wave(xoo,tout)  #from 9.95m to 0.05m

total_time = np.arange(0.0,0.4001,dt) #5e-5 in 100row
wave1 = np.zeros((len(total_time),Nele))

# ===== New BC Sideforce on Left and Right ==============
SSideforce_10rowx = np.zeros((len(total_time),Nele))
SSideforce_10rowy = np.zeros((len(total_time),Nele))

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
# # ----- Swave eta_p*(Vx) --------------------------
            SSideforce_10rowx[to+t,g] = SSideforce_10rowx[to+t,g] + (ForceX_Cofficient *XIn[to+t,g])
# # ----- Swave sigma xy --------------------------            
            SSideforce_10rowy[to+t,g] = SSideforce_10rowy[to+t,g] + (XIn[to+t,g])
    
        if total_time[t] >= 0.05 and total_time[t] < 0.1:  #t >= 1000 and t < 2000:
            # wave1[to+t,99-g] += XOut[t-to,99-g]
            wave1[to+t,99-g] = wave1[to+t,99-g] + (vely_Coefficient* XOut[t-to,99-g])  # original wave transport
# # ----- Swave eta_p*(Vx) --------------------------
            SSideforce_10rowx[to+t,99-g] = SSideforce_10rowx[to+t,99-g] + (ForceX_Cofficient *XOut[t-to,99-g])
# # ----- Swave sigma xy --------------------------            
            SSideforce_10rowy[to+t,99-g] = SSideforce_10rowy[to+t,99-g] + (-XOut[t-to,99-g])
            
Analysis = np.zeros((len(total_time),2))
Analysis[:,0] = total_time[:]
Analysis[:,1] = wave1[:,99]

# plt.plot(Analysis[:,0], Analysis[:,1])
# plt.grid(True)
# # ---- Output matrix eace column to txt file --------------
# num_rows, num_cols = SSideforce_10rowy.shape# 8001,100
# # 建立資料夾
# # ---------- Pwave ---------------
# P_folder_name_x = "SSideforce_10rowx"
# P_folder_name_y = "SSideforce_10rowy"

# os.makedirs(P_folder_name_x, exist_ok=True)
# for col in range(num_cols):
#     column_values = SSideforce_10rowx[:, col]
#     output_file = f"ele{col + 1}.txt"
#     with open(os.path.join(P_folder_name_x, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")

# os.makedirs(P_folder_name_y, exist_ok=True)
# # 逐一建立txt檔案並放入資料夾
# for col in range(num_cols):
#     column_values = SSideforce_10rowy[:, col]
#     output_file = f"ele{col + 1}.txt"
#     with open(os.path.join(P_folder_name_y, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")
         
# # #----------------------------- Left column file -----------------------------------
#　 ====== Mid Point File  ====================
file1 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\SideBeam_80row\node12961.out"
file2 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\SideBeam_40row\node6521.out"
file3 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\SideBeam_20row\node3301.out"
file4 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\SideBeam_10row\node1691.out"

# file1 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\SideBeam_80row\node6521.out"
# file2 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\SideBeam_40row\node3281.out"
# file3 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\SideBeam_20row\node1661.out"
# file4 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\SideBeam_10row\node851.out"

# file1 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\SideBeam_80row\node725.out"
# file2 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\SideBeam_40row\node365.out"
# file3 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\SideBeam_20row\node185.out"
# file4 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\SideBeam_10row\node95.out"

# file5 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\0.7mRefinement\10Row(Pwave)\node84.out"

# Mid20 = rdnumpy(file1)  # 1/2 Node Velocity
# Mid10 = rdnumpy(file2)  # 1/2 Node Velocity
# Mid1  = rdnumpy(file3)  # 1/2 Node Velocity

Mid80row = rdnumpy(file1)
Mid40row = rdnumpy(file2)
Mid20row = rdnumpy(file3)
Mid10row = rdnumpy(file4)

# #　 ====== Quarter Point File  ====================
file6 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\SideBeam_80row\node13001.out"
file7 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\SideBeam_40row\node6561.out"
file8 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\SideBeam_20row\node3341.out"
file9 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\SideBeam_10row\node1731.out"

# file6 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\SideBeam_80row\node6541.out"
# file7 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\SideBeam_40row\node3301.out"
# file8 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\SideBeam_20row\node1681.out"
# file9 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\SideBeam_10row\node871.out"

# file6 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\SideBeam_80row\node727.out"
# file7 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\SideBeam_40row\node367.out"
# file8 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\SideBeam_20row\node187.out"
# file9 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\SideBeam_10row\node97.out"

# # file10 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\0.7mRefinement\10Row(Pwave)\node86.out"

# Quarter20 = rdnumpy(file6)  # 1/4 Node Velocity
# Quarter10 = rdnumpy(file7)  # 1/4 Node Velocity
# Quarter1 = rdnumpy(file8)  # 1/4 Node Velocity

Quarter80row = rdnumpy(file6)
Quarter40row = rdnumpy(file7)
Quarter20row = rdnumpy(file8)
Quarter10row = rdnumpy(file9)



plt_axis2 = 1
# # ------- wave put into the timeSeries ---------------   
plt.figure(figsize=(8,6))
  
# plt.title(r'SideForce $\eta_{p}v_x$',fontsize = 18)  
# plt.ylabel(r"$\eta_{p}v_x$  $(N/m^2)$",fontsize=18) 

# plt.title(r'SideForce  $\sigma_{xy}$',fontsize = 18) 
# plt.ylabel(r"$\sigma_{xy}$  $(N/m^2)$",fontsize=18)  

plt.xlabel("time (s)",fontsize=18)


plt.ylabel(r"$V_x$  $(m/s)$",fontsize=18)
# # ------ wave Transport -----------------
# plt.plot(total_time,wave1[:,0],label ='Ele 1', marker='o', markevery=100)
# plt.plot(total_time,wave1[:,50],label ='Ele 5', marker='x', markevery=100)
# plt.plot(total_time,wave1[:,99],label ='Ele 10', marker='x', markevery=100)

# # plt.title('Mid Point',fontsize = 18) 
# plt.plot(total_time,wave1[:,99],label ='Analytical',color= 'black',linewidth=2.0)
# plt.plot(Mid20[:,0],Mid20[:,plt_axis2],label ='20m Soil(0.125m)', ls = '--',linewidth=6.0)
# plt.plot(Mid10[:,0],Mid10[:,plt_axis2],label ='10m Soil(0.125m)', ls = '-.',linewidth=4.0)
# plt.plot(Mid1[:,0],Mid1[:,plt_axis2],label ='1m Soil(0.125m)', ls = ':',linewidth=2.0)

# # # # # plt.title('Quarter Point',fontsize = 18) 
# plt.plot(total_time,wave1[:,99],label ='Analytical',color= 'black',linewidth=2.0)
# plt.plot(Quarter20[:,0],Quarter20[:,plt_axis2],label ='20m Soil(0.125m)', ls = '--',linewidth=6.0)
# plt.plot(Quarter10[:,0],Quarter10[:,plt_axis2],label ='10m Soil(0.125m)', ls = '-.',linewidth=4.0)
# plt.plot(Quarter1[:,0],Quarter1[:,plt_axis2],label ='1m Soil(0.125m)', ls = ':',linewidth=2.0)

# Refinement  Mid node:
# plt.plot(total_time,wave1[:,99],label ='Analytical',color= 'black',linewidth=4.0)
# plt.plot(Mid80row[:,0],Mid80row[:,plt_axis2],label =r'${\rm 20msoil}$ ($\Delta C=0.125$ ${\rm m}$)', ls = '--',linewidth=6.0)
# plt.plot(Mid40row[:,0],Mid40row[:,plt_axis2],label =r'${\rm 20msoil}$ ($\Delta C=0.25$ ${\rm m}$)', ls = '-.',linewidth=4.0)
# plt.plot(Mid20row[:,0],Mid20row[:,plt_axis2],label =r'${\rm 20msoil}$ ($\Delta C=0.50$ ${\rm m}$)', ls = ':',linewidth=3.0)
# plt.plot(Mid10row[:,0],Mid10row[:,plt_axis2],label =r'${\rm 20msoil}$ ($\Delta C=1$ ${\rm m}$)', ls = '-',linewidth=2.0)

# # plt.plot(Mid10row[:,0],Mid10row[:,plt_axis2],label ='10row', ls = 'dotted',linewidth=4.0)
soilWidth = 20
# # # # Refinement  Quarter node:
plt.plot(total_time,wave1[:,99],label ='Analytical',color= 'black',linewidth=4.0)
plt.plot(Quarter80row[:,0],Quarter80row[:,plt_axis2],label =r'${\rm 20msoil}$ ($\Delta C=0.125$ ${\rm m}$)', ls = '--',linewidth=6.0)
plt.plot(Quarter40row[:,0],Quarter40row[:,plt_axis2],label =r'${\rm 20msoil}$ ($\Delta C=0.25$ ${\rm m}$)', ls = '-.',linewidth=4.0)
plt.plot(Quarter20row[:,0],Quarter20row[:,plt_axis2],label =r'${\rm 20msoil}$ ($\Delta C=0.50$ ${\rm m}$)', ls = ':',linewidth=3.0)
plt.plot(Quarter10row[:,0],Quarter10row[:,plt_axis2],label =r'${\rm 20msoil}$ ($\Delta C=1.0$ ${\rm m}$)', ls = '-',linewidth=2.0)

# # plt.plot(Quarter10row[:,0],Quarter10row[:,plt_axis2],label ='10row', ls = 'dotted',linewidth=4.0)




# # ----- Swave  eta_p*(Vx) --------------------------
# plt.plot(total_time,SSideforce_10rowx[:,0],label ='Ele 1', marker='o', markevery=100)
# plt.plot(total_time,SSideforce_10rowx[:,5],label ='Ele 51', marker='x', markevery=100)
# plt.plot(total_time,SSideforce_10rowx[:,9],label ='Ele 100', marker='d', markevery=100)

# # ----- Swave sigma_Xy -------------
# plt.plot(total_time,SSideforce_10rowy[:,0],label ='Ele 1', marker='o', markevery=100)
# plt.plot(total_time,SSideforce_10rowy[:,5],label ='Ele 5', marker='x', markevery=100)
# plt.plot(total_time,SSideforce_10rowy[:,9],label ='Ele 10', marker='d', markevery=100)

plt.legend(loc='upper right',fontsize=16) #ncol=2
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlim(0.0, 0.20)
plt.grid(True)

x_axis = 0.025 # 0.1 0.05
ax4 = plt.gca()
ax4.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax4.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax4.yaxis.get_offset_text().set(size=18)

# # ========== Incoming Wave ==========================================
# plt.figure()
# plt.title('Incoming Wave',fontsize = 18)
# plt.xlabel("x(m)",fontsize=18)
# plt.ylabel(r"$y=sin(x-c_{s}t)$",fontsize=18)
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

# =========== Build Different element size dt ================================
def ele_dt(element):
    tns = L/cs # wave transport time
    dcell = tns/element #each cell time
    dt = dcell/10 #eace cell have 10 steps
    return(dt)

def ele_compare(ele80,Mid80row):
    for j in range(16):
        dt = round(0.0125*j +0.0125,4)
        # print(dt)
        for i in range(len(Mid80row)):
            if Mid80row[i, 0] == dt:
                ele80[1+j,0] = Mid80row[i,0]
                ele80[1+j,1] = Mid80row[i,1]
                # print(i,Mid20[i,0],Mid20[i,1])
ele10_time = np.arange(0.0,0.4001,ele_dt(10)) #5e-5 in 100row
ele20_time = np.arange(0.0,0.4001,ele_dt(20))
ele40_time = np.arange(0.0,0.4001,ele_dt(40))
ele80_time = np.arange(0.0,0.4000,ele_dt(80))


ele80_Mid = np.zeros((17,2))
ele40_Mid = np.zeros((17,2))
ele20_Mid = np.zeros((17,2))
ele10_Mid = np.zeros((17,2))

ele80_Quarter = np.zeros((17,2))
ele40_Quarter = np.zeros((17,2))
ele20_Quarter = np.zeros((17,2))
ele10_Quarter = np.zeros((17,2))

# ================= Save differ element size velocity ===========================
ele_compare(ele80_Mid,Mid80row)
ele_compare(ele40_Mid,Mid40row)
ele_compare(ele20_Mid,Mid20row)
ele_compare(ele10_Mid,Mid10row)

ele_compare(ele80_Quarter,Quarter80row)
ele_compare(ele40_Quarter,Quarter40row)
ele_compare(ele20_Quarter,Quarter20row)
ele_compare(ele10_Quarter,Quarter10row)
# ----------- Analysis Theory velocity ----------------       
Analy_compare = np.zeros((17,2))
for j in range(16):
    # print(dt)
    Analy_compare[1+j,0] = Analysis[250+250*j,0]
    Analy_compare[1+j,1] = Analysis[250+250*j,1]
    # print(250+250*j,Analysis[250+250*j,0], Analysis[250+250*j,1])

# ----------- Put all differ element inside matrics --------------- 
total_MidCompare = np.zeros((len(Analy_compare),6))
total_MidCompare[:,0] = Analy_compare[:,0]
total_MidCompare[:,1] = Analy_compare[:,1]
total_MidCompare[:,2] = ele80_Mid[:,1]
total_MidCompare[:,3] = ele40_Mid[:,1]
total_MidCompare[:,4] = ele20_Mid[:,1]
total_MidCompare[:,5] = ele10_Mid[:,1]
total_MidCompare[6,1] = 0

total_QuarterCompare = np.zeros((len(Analy_compare),6))
total_QuarterCompare[:,0] = Analy_compare[:,0]
total_QuarterCompare[:,1] = Analy_compare[:,1]
total_QuarterCompare[:,2] = ele80_Quarter[:,1]
total_QuarterCompare[:,3] = ele40_Quarter[:,1]
total_QuarterCompare[:,4] = ele20_Quarter[:,1]
total_QuarterCompare[:,5] = ele10_Quarter[:,1]
total_QuarterCompare[6,1] = 0

error_Midcompare = np.zeros((len(Analy_compare),5))
error_Midcompare[:,0] =  total_MidCompare[:,0]

error_Quartercompare = np.zeros((len(Analy_compare),5))
error_Quartercompare[:,0] =  total_QuarterCompare[:,0]
for i in range(4):#4
    for j in range(len(error_Midcompare)):
        error_Midcompare[j,1+i] = ((total_MidCompare[j,2+i] - total_MidCompare[j,1])/ total_MidCompare[j,1])*100
        error_Quartercompare[j,1+i] = ((total_QuarterCompare[j,2+i] - total_QuarterCompare[j,1])/ total_QuarterCompare[j,1])*100
        
        # print(j,i)
#----------------- Make the nan,inf to be 0 -----------------
where_are_nan1 = np.isnan(error_Midcompare) 
where_are_inf1 = np.isinf(error_Midcompare)
error_Midcompare[where_are_nan1] = 0
error_Midcompare[where_are_inf1] = 0

where_are_nan2 = np.isnan(error_Quartercompare) 
where_are_inf2 = np.isinf(error_Quartercompare)
error_Quartercompare[where_are_nan2] = 0
error_Quartercompare[where_are_inf2] = 0

# ------- relative error figure -------------
plt.figure(figsize=(10,8))
# plt.title(r'Ground Surface relative error: Middle point',fontsize = 18) 
plt.ylabel(r'Relative error (%)',fontsize=18)  
plt.xlabel("Time increment $\Delta t$",fontsize=18)

plt.plot(error_Midcompare[:,0],error_Midcompare[:,1],label = r"$\Delta c = 0.125$ ${\rm m}$ ${\rm (80 element)}$", marker = '^',markersize=16,markerfacecolor = 'white')
plt.plot(error_Midcompare[:,0],error_Midcompare[:,2],label = r"$\Delta c = 0.25$ ${\rm m}$ ${\rm (40 element)}$", marker = 's',markersize=14,markerfacecolor = 'white')
plt.plot(error_Midcompare[:,0],error_Midcompare[:,3],label = r"$\Delta c = 0.50$ ${\rm m}$ ${\rm (20 element)}$", marker = 'o',markersize=12,markerfacecolor = 'white')
plt.plot(error_Midcompare[:,0],error_Midcompare[:,4],label = r"$\Delta c = 1.0$ ${\rm m}$ ${\rm (10 element)}$", marker = '>',markersize=10,markerfacecolor = 'white')

plt.legend(loc='upper right',fontsize=15) #ncol=2
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlim(0.0, 0.20)
plt.grid(True)

# x_axis = 0.0125 # 0.1 0.05
ax4 = plt.gca()
# plt.rcParams['ax4.formatter.limits'] = [-3, 3]
# ax4.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax4.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax4.ticklabel_format(style='sci', scilimits=(-1,2), axis='x')
ax4.yaxis.get_offset_text().set(size=18)
ax4.xaxis.get_offset_text().set(size=18)


plt.figure(figsize=(10,8))
# plt.title(r'Ground Surface relative error: Quarter point',fontsize = 18) 
plt.ylabel(r'Relative error (%)',fontsize=18)  
plt.xlabel("Time increment $\Delta t$",fontsize=18)

plt.plot(error_Quartercompare[:,0],error_Quartercompare[:,1],label = r"$\Delta c = 0.125$ ${\rm m}$ ${\rm (80 element)}$", marker = '^',markersize=16,markerfacecolor = 'white')
plt.plot(error_Quartercompare[:,0],error_Quartercompare[:,2],label = r"$\Delta c = 0.25$ ${\rm m}$ ${\rm (40 element)}$", marker = 's',markersize=14,markerfacecolor = 'white')
plt.plot(error_Quartercompare[:,0],error_Quartercompare[:,3],label = r"$\Delta c = 0.50$ ${\rm m}$ ${\rm (20 element)}$", marker = 'o',markersize=12,markerfacecolor = 'white')
plt.plot(error_Quartercompare[:,0],error_Quartercompare[:,4],label = r"$\Delta c = 1.0$ ${\rm m}$ ${\rm (10 element)}$", marker = '>',markersize=10,markerfacecolor = 'white')

plt.legend(loc='upper right',fontsize=15) #ncol=2
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlim(0.0, 0.20)
plt.grid(True)

# x_axis = 0.0125 # 0.1 0.05
ax5 = plt.gca()
# plt.rcParams['ax4.formatter.limits'] = [-3, 3]
# ax4.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax5.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax5.ticklabel_format(style='sci', scilimits=(-1,2), axis='x')
ax5.yaxis.get_offset_text().set(size=18)
ax5.xaxis.get_offset_text().set(size=18)






# for i in range(5):
#     for j in range(len(Analy_compare)):
#         total_Compare[j,i] = A

# plt.plot(Analy_compare[:,0],Analy_compare[:,1])
# plt.grid(True)
    # if Mid20[i,0] == 0.025:
    #     ele80_20Ref[1,0] = Mid20[i,0]
    #     ele80_20Ref[1,1] = Mid20[i,1] 
    #     print(i,Mid20[i,1])
    # if Mid20[i,0] == 0.050:
    #     ele80_20Ref[2,0] = Mid20[i,0]
    #     ele80_20Ref[2,1] = Mid20[i,1] 
    #     print(i,Mid20[i,1])
    # if Mid20[i,0] == 0.075:
    #     ele80_20Ref[3,0] = Mid20[i,0]
    #     ele80_20Ref[3,1] = Mid20[i,1] 
    #     print(i,Mid20[i,1])
    # if Mid20[i,0] == 0.10:
    #     ele80_20Ref[4,0] = Mid20[i,0]
    #     ele80_20Ref[4,1] = Mid20[i,1] 
    #     print(i,Mid20[i,1])
    # if Mid20[i,0] == 0.125:
    #     ele80_20Ref[5,0] = Mid20[i,0]
    #     ele80_20Ref[5,1] = Mid20[i,1] 
    #     print(i,Mid20[i,1])
    # if Mid20[i,0] == 0.150:
    #     ele80_20Ref[6,0] = Mid20[i,0]
    #     ele80_20Ref[6,1] = Mid20[i,1] 
    #     print(i,Mid20[i,1])
    # if Mid20[i,0] == 0.175:
    #     ele80_20Ref[7,0] = Mid20[i,0]
    #     ele80_20Ref[7,1] = Mid20[i,1] 
    #     print(i,Mid20[i,1])
    # if Mid20[i,0] == 0.20:
    #     ele80_20Ref[8,0] = Mid20[i,0]
    #     ele80_20Ref[8,1] = Mid20[i,1] 
    #     print(i,Mid20[i,1])
