# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 22:21:09 2023

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
from matplotlib.ticker import ScalarFormatter
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
# ----------- Element on vertical direction ------------------ 
Soil_10row= 10 # dt= 5e-4       #cpdt = 2.67e-4
Soil_20row= 20 # dt= 2.5e-4     #cpdt = 1.33e-4
Soil_40row= 40 # dt= 1.25e-4    #cpdt = 6.68e-05
Soil_80row= 80 # dt= 6.25e-05   #cpdt = 3.34e-05
Soil_100row= 100 # dt= 5e-05   #cpdt = 
# ----------- Soil/Wave parameters -------------------
cs = 200 # m/s
L = 10 # m(Soil_Depth)

nu = 0.3  #  0.3 -> (epsilon_z /=0)
rho = 2000 #1600 kg/m3  ; =1.6 ton/m3  
G = (cs*cs)*rho  # N/m^2 = Kg/(m*s^2)
E =  G*2*(1+nu)  # N/m^2 = Kg/(m*s^2)
cp = (E*(1-nu)/((1+nu)*(1-2*nu)*rho))**(0.5)

A = 0.1# 0.1
w =  pi/5 # 0 to 10 = 0 to 2*pi => x = pi/5

# ------------------- calculate eace step time -------------------
tns = L/cs # wave transport time
dcell = tns/Soil_100row #each cell time
dt = dcell/10 #eace cell have 10 steps
print(f"wave travel = {tns} ;dcell = {dcell} ;dt = {dt}")

time = np.arange(0.0,0.050005,dt)
Nt = len(time)
#　 =================== Middle Point File (1/2) ====================
# ------------------- File Path Name --------------------
Boundary = 'TopForce'
Boundary1 = 'Tie Boundary Condition (TopForce)' # for plot title
ele80 = f"{Boundary}_80row"
ele40 = f"{Boundary}_40row"
ele20 = f"{Boundary}_20row"
ele10 = f"{Boundary}_10row"

file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/{ele80}/node12961.out"
file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/{ele40}/node6521.out"
file3 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/{ele20}/node3301.out"
file4 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/{ele10}/node1691.out"

file5 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/{ele80}/node6521.out"
file6 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/{ele40}/node3281.out"
file7 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/{ele20}/node1661.out"
file8 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/{ele10}/node851.out"

file9 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/{ele80}/node725.out"
file10 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/{ele40}/node365.out"
file11 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/{ele20}/node185.out"
file12 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/{ele10}/node95.out"

Width20_Mid80row = rdnumpy(file1)
Width20_Mid40row = rdnumpy(file2)
Width20_Mid20row = rdnumpy(file3)
Width20_Mid10row = rdnumpy(file4)

Width10_Mid80row = rdnumpy(file5)
Width10_Mid40row = rdnumpy(file6)
Width10_Mid20row = rdnumpy(file7)
Width10_Mid10row = rdnumpy(file8)

Width1_Mid80row = rdnumpy(file9)
Width1_Mid40row = rdnumpy(file10)
Width1_Mid20row = rdnumpy(file11)
Width1_Mid10row = rdnumpy(file12)

# ================ Three-Quarter Point File (3/4) ====================
file13 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/{ele80}/node13001.out"
file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/{ele40}/node6561.out"
file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/{ele20}/node3341.out"
file16 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/{ele10}/node1731.out"

file17 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/{ele80}/node6541.out"
file18 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/{ele40}/node3301.out"
file19 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/{ele20}/node1681.out"
file20 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/{ele10}/node871.out"

file21 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/{ele80}/node727.out"
file22 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/{ele40}/node367.out"
file23 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/{ele20}/node187.out"
file24 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/{ele10}/node97.out"

Width20_Quarter80row = rdnumpy(file13)
Width20_Quarter40row = rdnumpy(file14)
Width20_Quarter20row = rdnumpy(file15)
Width20_Quarter10row = rdnumpy(file16)

Width10_Quarter80row = rdnumpy(file17)
Width10_Quarter40row = rdnumpy(file18)
Width10_Quarter20row = rdnumpy(file19)
Width10_Quarter10row = rdnumpy(file20)

Width1_Quarter80row = rdnumpy(file21)
Width1_Quarter40row = rdnumpy(file22)
Width1_Quarter20row = rdnumpy(file23)
Width1_Quarter10row = rdnumpy(file24)


plt_axis2 = 2
# # ------- wave put into the timeSeries ---------------
def Differ_elemetVel(Mid80row,Mid40row,Mid20row,Mid10row):
    # plt.figure(figsize=(8,6))
    font_props = {'family': 'Arial', 'size': 10}
    # plt.xlabel("time (s)",fontsize=18)
    # plt.ylabel(r"$V_x$  $(m/s)$",fontsize=18)
    # plt.title(titleName,x=0.75,y=0.25, fontsize = 20)
    
    # plt.plot(total_time,wave1[:,99],label =r'$\mathrm{Analytical}$',color= 'black',linewidth=2.0)
    plt.plot(Mid80row[:,0],Mid80row[:,plt_axis2],label =r'$\Delta_C=0.125\, \mathrm{m}$', ls = '--',color= 'darkorange',linewidth=6.0)
    plt.plot(Mid40row[:,0],Mid40row[:,plt_axis2],label =r'$\Delta_C=0.25\, \mathrm{m}$', ls = '-.',color= 'limegreen',linewidth=4.0)
    plt.plot(Mid20row[:,0],Mid20row[:,plt_axis2],label =r'$\Delta_C=0.50\, \mathrm{m}$', ls = ':',color= 'blue',linewidth=3.0)
    plt.plot(Mid10row[:,0],Mid10row[:,plt_axis2],label =r'$\Delta_C=1\, \mathrm{m}$', ls = '-',color= 'red',linewidth=2.0)
    
    plt.legend(loc='upper right',prop=font_props) #ncol=2,fontsize=16
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xlim(0.0, 0.20)
    plt.grid(True)

def Differ_SoilWidthVel(Width20_Mid80row,Width10_Mid80row,Width1_Mid80row):
    # plt.figure(figsize=(8,6))
    font_props = {'family': 'Arial', 'size': 10}
    # plt.xlabel("time (s)",fontsize=18)
    # plt.ylabel(r"$V_x$  $(m/s)$",fontsize=18)
    # plt.title(titleName,x=0.75,y=0.25, fontsize = 18)

    
    # plt.plot(total_time,wave1[:,99],label = r'$\mathrm{Analytical}$',color= 'black',linewidth=2.0)
    plt.plot(Width20_Mid80row[:,0],Width20_Mid80row[:,plt_axis2],label ='20m Soil',color= 'darkorange', ls = '--',linewidth=6.0)
    plt.plot(Width10_Mid80row[:,0],Width10_Mid80row[:,plt_axis2],label ='10m Soil',color= 'limegreen', ls = '-.',linewidth=4.0)
    plt.plot(Width1_Mid80row[:,0],Width1_Mid80row[:,plt_axis2],label ='1m Soil',color= 'red', ls = '-',linewidth=2.0)
    
    plt.legend(loc='upper right',prop=font_props) #ncol=2,fontsize=16
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xlim(0.0, 0.20)
    plt.grid(True)
    
# # ------------ Draw Same SoilWidth with Different row element: Middle Point -----------------------
x_axis = 0.0267 # 0.1 0.05
# fig1, (ax1,ax2,ax3) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8,8))
# fig1.suptitle(f'{Boundary1} \n(Middle node)',x=0.50,y =0.95,fontsize = 20)
# fig1.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
# fig1.text(0.44,0.04, 'time t (s)', va= 'center', fontsize=20)

# ax1 = plt.subplot(311)
# Differ_elemetVel(Width20_Mid80row,Width20_Mid40row,Width20_Mid20row,Width20_Mid10row)
# ax1.set_title(f"SW 20m",fontsize =18, x=0.10, y=0.78)

# ax2 = plt.subplot(312)
# Differ_elemetVel(Width10_Mid80row,Width10_Mid40row,Width10_Mid20row,Width10_Mid10row)
# ax2.set_title(f"SW 10m",fontsize =18, x=0.10, y=0.78)

# ax3 = plt.subplot(313)
# Differ_elemetVel(Width1_Mid80row,Width1_Mid40row,Width1_Mid20row,Width1_Mid10row)
# ax3.set_title(f"SW 1m",fontsize =18, x=0.10, y=0.80)

# for ax in [ax1,ax2,ax3]:
#     formatter = ticker.ScalarFormatter(useMathText =True)
#     formatter.set_scientific(True)
#     formatter.set_powerlimits((0,0))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
#     ax.yaxis.set_major_formatter(formatter)
#     ax.xaxis.set_major_formatter(formatter)
#     ax.yaxis.get_offset_text().set(size=18)
#     ax.xaxis.get_offset_text().set(size=18)
    
# ------------ Draw Same SoilWidth with Different row element: Quarter Point -----------------------
fig2, (ax4,ax5,ax6) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8,8))
fig2.suptitle(f'{Boundary1} \n(Three Quarter node)',x=0.50,y =0.95,fontsize = 20)
fig2.text(0.026,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig2.text(0.44,0.04, 'time t (s)', va= 'center', fontsize=20)

ax4 = plt.subplot(311)
Differ_elemetVel(Width20_Quarter80row,Width20_Quarter40row,Width20_Quarter20row,Width20_Quarter10row)
ax4.set_title(f"SW 20m",fontsize =18, x=0.10, y=0.76)

ax5 = plt.subplot(312)
Differ_elemetVel(Width10_Quarter80row,Width10_Quarter40row,Width10_Quarter20row,Width10_Quarter10row)
ax5.set_title(f"SW 10m",fontsize =18, x=0.10, y=0.76)

ax6 = plt.subplot(313)
Differ_elemetVel(Width1_Quarter80row,Width1_Quarter40row,Width1_Quarter20row,Width1_Quarter10row)
ax6.set_title(f"SW 1m",fontsize =18, x=0.10, y=0.76)

for ax in [ax4,ax5,ax6]:
    formatter = ticker.ScalarFormatter(useMathText =True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set(size=18)
    ax.xaxis.get_offset_text().set(size=18)

# ------------ Draw Different SoilWidth with Same row element: Middle Point -----------------------
fig3, (ax7,ax8,ax9,ax10) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8,8))
fig3.suptitle(f'{Boundary1} \n(Middle node)',x=0.50,y =0.95,fontsize = 20)
fig3.text(0.030,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig3.text(0.45,0.04, 'time t (s)', va= 'center', fontsize=20)

ax7 = plt.subplot(411)
Differ_SoilWidthVel(Width20_Mid80row,Width10_Mid80row,Width1_Mid80row)
ax7.set_title(r'$\Delta_C='+ '0.125' + r'\mathrm{m}$',fontsize =16, x=0.50, y=0.76)

ax8 = plt.subplot(412)
Differ_SoilWidthVel(Width20_Mid40row,Width10_Mid40row,Width1_Mid40row)
ax8.set_title(r'$\Delta_C='+ '0.25' + r'\mathrm{m}$',fontsize =16, x=0.50, y=0.76)


ax9 = plt.subplot(413)
Differ_SoilWidthVel(Width20_Quarter20row,Width10_Quarter20row,Width1_Mid20row)
ax9.set_title(r'$\Delta_C='+ '0.50' + r'\mathrm{m}$',fontsize =16, x=0.50, y=0.76)

ax10 = plt.subplot(414)
Differ_SoilWidthVel(Width20_Mid10row,Width10_Mid10row,Width1_Mid10row)
ax10.set_title(r'$\Delta_C='+ '1.0' + r'\mathrm{m}$',fontsize =16, x=0.50, y=0.76)

for ax in [ax7,ax8,ax9,ax10]:
    formatter = ticker.ScalarFormatter(useMathText =True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set(size=18)
    ax.xaxis.get_offset_text().set(size=18)

plt.subplots_adjust(left=0.125,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.88, 
                    wspace=0.2, 
                    hspace=0.35)
# # fig3.tight_layout()
# ------------ Draw Different SoilWidth with Same row element: Middle Point -----------------------
fig4, (ax11,ax12,ax13,ax14) = plt.subplots(nrows= 4, ncols=1, sharex=True, figsize=(8,8))
fig4.suptitle(f'{Boundary1} \n(Three Quarter node)',x=0.50,y =0.95,fontsize = 20)
fig4.text(0.046,0.5,r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig4.text(0.45,0.04, 'time t (s)', va= 'center', fontsize=20)

ax11 = plt.subplot(411)
Differ_SoilWidthVel(Width20_Quarter80row,Width10_Quarter80row,Width1_Quarter80row)
ax11.set_title(r'$\Delta_C='+ '0.125' + r'\mathrm{m}$',fontsize =16, x=0.50, y=0.76)

ax12 = plt.subplot(412)
Differ_SoilWidthVel(Width20_Quarter40row,Width10_Quarter40row,Width1_Quarter40row)
ax12.set_title(r'$\Delta_C='+ '0.25' + r'\mathrm{m}$',fontsize =16, x=0.50, y=0.76)

ax13 = plt.subplot(413)
Differ_SoilWidthVel(Width20_Quarter20row,Width10_Quarter20row,Width1_Quarter20row)
ax13.set_title(r'$\Delta_C='+ '0.50' + r'\mathrm{m}$',fontsize =16, x=0.50, y=0.76)

ax14 = plt.subplot(414)
Differ_SoilWidthVel(Width20_Quarter10row,Width10_Quarter10row,Width1_Quarter10row)
ax14.set_title(r'$\Delta_C='+ '1.0' + r'\mathrm{m}$',fontsize =16, x=0.50, y=0.76)

for ax in [ax11,ax12,ax13,ax14]:
    formatter = ticker.ScalarFormatter(useMathText =True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set(size=18)
    ax.xaxis.get_offset_text().set(size=18)

plt.subplots_adjust(left=0.125,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.88, 
                    wspace=0.2, 
                    hspace=0.35)
# # =========== Build Different element size dt ================================
# def ele_dt(element):
#     tns = L/cp # wave transport time
#     dcell = tns/element #each cell time
#     dt = dcell/10 #eace cell have 10 steps
#     return(dt)

# # ele10_time = np.arange(0.0,0.4001,ele_dt(10)) #5e-5 in 100row
# # ele20_time = np.arange(0.0,0.4001,ele_dt(20))
# # ele40_time = np.arange(0.0,0.4001,ele_dt(40))
# # ele80_time = np.arange(0.0,0.4000,ele_dt(80))

# # ========== Check range time increment about relative error ====================
# top_time = 0.0424514
# Min_timeIncrement = (L/Soil_80row)/ cp
# Max_timeIncrement = (L/Soil_10row)/ cp
# error_dt = np.arange(top_time, top_time+(Max_timeIncrement+Min_timeIncrement), 2*Min_timeIncrement)
# print(Max_timeIncrement,Min_timeIncrement)
# # ------------ Build Middle different SoilWidth error time Step ---------------- 
# Width20_ele80_Mid = np.zeros((len(error_dt),2))
# Width20_ele40_Mid = np.zeros((len(error_dt),2))
# Width20_ele20_Mid = np.zeros((len(error_dt),2))
# Width20_ele10_Mid = np.zeros((len(error_dt),2))

# Width10_ele80_Mid = np.zeros((len(error_dt),2))
# Width10_ele40_Mid = np.zeros((len(error_dt),2))
# Width10_ele20_Mid = np.zeros((len(error_dt),2))
# Width10_ele10_Mid = np.zeros((len(error_dt),2))

# Width1_ele80_Mid = np.zeros((len(error_dt),2))
# Width1_ele40_Mid = np.zeros((len(error_dt),2))
# Width1_ele20_Mid = np.zeros((len(error_dt),2))
# Width1_ele10_Mid = np.zeros((len(error_dt),2))

# # # ------------ Build three quarter different SoilWidth error time Step ---------------- 
# Width20_ele80_Quarter = np.zeros((len(error_dt),2))
# Width20_ele40_Quarter = np.zeros((len(error_dt),2))
# Width20_ele20_Quarter = np.zeros((len(error_dt),2))
# Width20_ele10_Quarter = np.zeros((len(error_dt),2))

# Width10_ele80_Quarter = np.zeros((len(error_dt),2))
# Width10_ele40_Quarter = np.zeros((len(error_dt),2))
# Width10_ele20_Quarter = np.zeros((len(error_dt),2))
# Width10_ele10_Quarter = np.zeros((len(error_dt),2))

# Width1_ele80_Quarter = np.zeros((len(error_dt),2))
# Width1_ele40_Quarter = np.zeros((len(error_dt),2))
# Width1_ele20_Quarter = np.zeros((len(error_dt),2))
# Width1_ele10_Quarter = np.zeros((len(error_dt),2))

# # # ================= Save differ element size velocity ===========================
# def ele_compare(Width20_ele80_Mid, Width20_Mid80row):
#     Width20_ele80_Mid[:,0] = error_dt[:]
#     for j in range(len(error_dt)):
#         dt = round(error_dt[j],6)
#         for i in range(len(Width20_Mid80row)): 
#             if Width20_Mid80row[i,0] == dt:
#                 # print(Mid80row[i,0])      
#                 Width20_ele80_Mid[j,1] = Width20_Mid80row[i,1]

# # # ======= Ground surface Middle node Velocity compare (20m、10m、1m) : Middle===========================
# Width20_ele80_Mid[:,0] = error_dt[:]
# Width20_ele80_Mid[0,1] = Width20_Mid80row[1270,2]
# Width20_ele80_Mid[1,1] = Width20_Mid80row[1290,2]
# Width20_ele80_Mid[2,1] = Width20_Mid80row[1310,2]
# Width20_ele80_Mid[3,1] = Width20_Mid80row[1330,2]
# Width20_ele80_Mid[4,1] = Width20_Mid80row[1350,2]    

# Width20_ele40_Mid[:,0] = error_dt[:]
# Width20_ele40_Mid[0,1] = Width20_Mid40row[634,2]
# Width20_ele40_Mid[1,1] = Width20_Mid40row[644,2]
# Width20_ele40_Mid[2,1] = Width20_Mid40row[654,2]
# Width20_ele40_Mid[3,1] = Width20_Mid40row[664,2]
# Width20_ele40_Mid[4,1] = Width20_Mid40row[674,2] 

# Width20_ele20_Mid[:,0] = error_dt[:]
# Width20_ele20_Mid[0,1] = Width20_Mid20row[318,2]
# Width20_ele20_Mid[1,1] = Width20_Mid20row[323,2]
# Width20_ele20_Mid[2,1] = Width20_Mid20row[328,2]
# Width20_ele20_Mid[3,1] = Width20_Mid20row[333,2]
# Width20_ele20_Mid[4,1] = Width20_Mid20row[338,2] 

# Width20_ele10_Mid[:,0] = error_dt[:]
# Width20_ele10_Mid[0,1] = Width20_Mid10row[157,2]
# Width20_ele10_Mid[1,1] = Width20_Mid10row[160,2]
# Width20_ele10_Mid[2,1] = Width20_Mid10row[163,2]
# Width20_ele10_Mid[3,1] = Width20_Mid10row[166,2]
# Width20_ele10_Mid[4,1] = Width20_Mid10row[169,2] 

# Width10_ele80_Mid[:,0] = error_dt[:]
# Width10_ele80_Mid[0,1] = Width10_Mid80row[1270,2]
# Width10_ele80_Mid[1,1] = Width10_Mid80row[1290,2]
# Width10_ele80_Mid[2,1] = Width10_Mid80row[1310,2]
# Width10_ele80_Mid[3,1] = Width10_Mid80row[1330,2]
# Width10_ele80_Mid[4,1] = Width10_Mid80row[1350,2]    

# Width10_ele40_Mid[:,0] = error_dt[:]
# Width10_ele40_Mid[0,1] = Width10_Mid40row[634,2]
# Width10_ele40_Mid[1,1] = Width10_Mid40row[644,2]
# Width10_ele40_Mid[2,1] = Width10_Mid40row[654,2]
# Width10_ele40_Mid[3,1] = Width10_Mid40row[664,2]
# Width10_ele40_Mid[4,1] = Width10_Mid40row[674,2] 

# Width10_ele20_Mid[:,0] = error_dt[:]
# Width10_ele20_Mid[0,1] = Width10_Mid20row[318,2]
# Width10_ele20_Mid[1,1] = Width10_Mid20row[323,2]
# Width10_ele20_Mid[2,1] = Width10_Mid20row[328,2]
# Width10_ele20_Mid[3,1] = Width10_Mid20row[333,2]
# Width10_ele20_Mid[4,1] = Width10_Mid20row[338,2] 

# Width10_ele10_Mid[:,0] = error_dt[:]
# Width10_ele10_Mid[0,1] = Width10_Mid10row[157,2]
# Width10_ele10_Mid[1,1] = Width10_Mid10row[160,2]
# Width10_ele10_Mid[2,1] = Width10_Mid10row[163,2]
# Width10_ele10_Mid[3,1] = Width10_Mid10row[166,2]
# Width10_ele10_Mid[4,1] = Width10_Mid10row[169,2] 

# Width1_ele80_Mid[:,0] = error_dt[:]
# Width1_ele80_Mid[0,1] = Width1_Mid80row[1270,2]
# Width1_ele80_Mid[1,1] = Width1_Mid80row[1290,2]
# Width1_ele80_Mid[2,1] = Width1_Mid80row[1310,2]
# Width1_ele80_Mid[3,1] = Width1_Mid80row[1330,2]
# Width1_ele80_Mid[4,1] = Width1_Mid80row[1350,2]    

# Width1_ele40_Mid[:,0] = error_dt[:]
# Width1_ele40_Mid[0,1] = Width1_Mid40row[634,2]
# Width1_ele40_Mid[1,1] = Width1_Mid40row[644,2]
# Width1_ele40_Mid[2,1] = Width1_Mid40row[654,2]
# Width1_ele40_Mid[3,1] = Width1_Mid40row[664,2]
# Width1_ele40_Mid[4,1] = Width1_Mid40row[674,2] 

# Width1_ele20_Mid[:,0] = error_dt[:]
# Width1_ele20_Mid[0,1] = Width1_Mid20row[318,2]
# Width1_ele20_Mid[1,1] = Width1_Mid20row[323,2]
# Width1_ele20_Mid[2,1] = Width1_Mid20row[328,2]
# Width1_ele20_Mid[3,1] = Width1_Mid20row[333,2]
# Width1_ele20_Mid[4,1] = Width1_Mid20row[338,2] 

# Width1_ele10_Mid[:,0] = error_dt[:]
# Width1_ele10_Mid[0,1] = Width1_Mid10row[157,2]
# Width1_ele10_Mid[1,1] = Width1_Mid10row[160,2]
# Width1_ele10_Mid[2,1] = Width1_Mid10row[163,2]
# Width1_ele10_Mid[3,1] = Width1_Mid10row[166,2]
# Width1_ele10_Mid[4,1] = Width1_Mid10row[169,2]   
     
# # # ======= Ground surface Middle node Velocity compare (20m、10m、1m) : three Quarter===========================
# Width20_ele80_Quarter[:,0] = error_dt[:]
# Width20_ele80_Quarter[0,1] = Width20_Quarter80row[1270,2]
# Width20_ele80_Quarter[1,1] = Width20_Quarter80row[1290,2]
# Width20_ele80_Quarter[2,1] = Width20_Quarter80row[1310,2]
# Width20_ele80_Quarter[3,1] = Width20_Quarter80row[1330,2]
# Width20_ele80_Quarter[4,1] = Width20_Quarter80row[1350,2]    

# Width20_ele40_Quarter[:,0] = error_dt[:]
# Width20_ele40_Quarter[0,1] = Width20_Quarter40row[634,2]
# Width20_ele40_Quarter[1,1] = Width20_Quarter40row[644,2]
# Width20_ele40_Quarter[2,1] = Width20_Quarter40row[654,2]
# Width20_ele40_Quarter[3,1] = Width20_Quarter40row[664,2]
# Width20_ele40_Quarter[4,1] = Width20_Quarter40row[674,2] 

# Width20_ele20_Quarter[:,0] = error_dt[:]
# Width20_ele20_Quarter[0,1] = Width20_Quarter20row[318,2]
# Width20_ele20_Quarter[1,1] = Width20_Quarter20row[323,2]
# Width20_ele20_Quarter[2,1] = Width20_Quarter20row[328,2]
# Width20_ele20_Quarter[3,1] = Width20_Quarter20row[333,2]
# Width20_ele20_Quarter[4,1] = Width20_Quarter20row[338,2] 

# Width20_ele10_Quarter[:,0] = error_dt[:]
# Width20_ele10_Quarter[0,1] = Width20_Quarter10row[157,2]
# Width20_ele10_Quarter[1,1] = Width20_Quarter10row[160,2]
# Width20_ele10_Quarter[2,1] = Width20_Quarter10row[163,2]
# Width20_ele10_Quarter[3,1] = Width20_Quarter10row[166,2]
# Width20_ele10_Quarter[4,1] = Width20_Quarter10row[169,2] 

# Width10_ele80_Quarter[:,0] = error_dt[:]
# Width10_ele80_Quarter[0,1] = Width10_Quarter80row[1270,2]
# Width10_ele80_Quarter[1,1] = Width10_Quarter80row[1290,2]
# Width10_ele80_Quarter[2,1] = Width10_Quarter80row[1310,2]
# Width10_ele80_Quarter[3,1] = Width10_Quarter80row[1330,2]
# Width10_ele80_Quarter[4,1] = Width10_Quarter80row[1350,2]    

# Width10_ele40_Quarter[:,0] = error_dt[:]
# Width10_ele40_Quarter[0,1] = Width10_Quarter40row[634,2]
# Width10_ele40_Quarter[1,1] = Width10_Quarter40row[644,2]
# Width10_ele40_Quarter[2,1] = Width10_Quarter40row[654,2]
# Width10_ele40_Quarter[3,1] = Width10_Quarter40row[664,2]
# Width10_ele40_Quarter[4,1] = Width10_Quarter40row[674,2] 

# Width10_ele20_Quarter[:,0] = error_dt[:]
# Width10_ele20_Quarter[0,1] = Width10_Quarter20row[318,2]
# Width10_ele20_Quarter[1,1] = Width10_Quarter20row[323,2]
# Width10_ele20_Quarter[2,1] = Width10_Quarter20row[328,2]
# Width10_ele20_Quarter[3,1] = Width10_Quarter20row[333,2]
# Width10_ele20_Quarter[4,1] = Width10_Quarter20row[338,2] 

# Width10_ele10_Quarter[:,0] = error_dt[:]
# Width10_ele10_Quarter[0,1] = Width10_Quarter10row[157,2]
# Width10_ele10_Quarter[1,1] = Width10_Quarter10row[160,2]
# Width10_ele10_Quarter[2,1] = Width10_Quarter10row[163,2]
# Width10_ele10_Quarter[3,1] = Width10_Quarter10row[166,2]
# Width10_ele10_Quarter[4,1] = Width10_Quarter10row[169,2] 

# Width1_ele80_Quarter[:,0] = error_dt[:]
# Width1_ele80_Quarter[0,1] = Width1_Quarter80row[1270,2]
# Width1_ele80_Quarter[1,1] = Width1_Quarter80row[1290,2]
# Width1_ele80_Quarter[2,1] = Width1_Quarter80row[1310,2]
# Width1_ele80_Quarter[3,1] = Width1_Quarter80row[1330,2]
# Width1_ele80_Quarter[4,1] = Width1_Quarter80row[1350,2]    

# Width1_ele40_Quarter[:,0] = error_dt[:]
# Width1_ele40_Quarter[0,1] = Width1_Quarter40row[634,2]
# Width1_ele40_Quarter[1,1] = Width1_Quarter40row[644,2]
# Width1_ele40_Quarter[2,1] = Width1_Quarter40row[654,2]
# Width1_ele40_Quarter[3,1] = Width1_Quarter40row[664,2]
# Width1_ele40_Quarter[4,1] = Width1_Quarter40row[674,2] 

# Width1_ele20_Quarter[:,0] = error_dt[:]
# Width1_ele20_Quarter[0,1] = Width1_Quarter20row[318,2]
# Width1_ele20_Quarter[1,1] = Width1_Quarter20row[323,2]
# Width1_ele20_Quarter[2,1] = Width1_Quarter20row[328,2]
# Width1_ele20_Quarter[3,1] = Width1_Quarter20row[333,2]
# Width1_ele20_Quarter[4,1] = Width1_Quarter20row[338,2] 

# Width1_ele10_Quarter[:,0] = error_dt[:]
# Width1_ele10_Quarter[0,1] = Width1_Quarter10row[157,2]
# Width1_ele10_Quarter[1,1] = Width1_Quarter10row[160,2]
# Width1_ele10_Quarter[2,1] = Width1_Quarter10row[163,2]
# Width1_ele10_Quarter[3,1] = Width1_Quarter10row[166,2]
# Width1_ele10_Quarter[4,1] = Width1_Quarter10row[169,2] 

# def Find_ColMaxValue(ele80_Mid):
#     column_index = 2
#     column = ele80_Mid[:, column_index]
#     max_value = np.max(column)
#     max_index = np.argmax(column)
#     # print(f'max_value= {max_value}; max_index= {max_index}')
#     return(max_value)
# # # =========== Middle point(Ground surface) Find Max Velocity Value ===================
# Width20_ele80_max = Find_ColMaxValue(Width20_Mid80row)
# Width20_ele40_max = Find_ColMaxValue(Width20_Mid40row)
# Width20_ele20_max = Find_ColMaxValue(Width20_Mid20row)
# Width20_ele10_max = Find_ColMaxValue(Width20_Mid10row)

# Width10_ele80_max = Find_ColMaxValue(Width10_Mid80row)
# Width10_ele40_max = Find_ColMaxValue(Width10_Mid40row)
# Width10_ele20_max = Find_ColMaxValue(Width10_Mid20row)
# Width10_ele10_max = Find_ColMaxValue(Width10_Mid10row)

# Width1_ele80_max = Find_ColMaxValue(Width1_Mid80row)
# Width1_ele40_max = Find_ColMaxValue(Width1_Mid40row)
# Width1_ele20_max = Find_ColMaxValue(Width1_Mid20row)
# Width1_ele10_max = Find_ColMaxValue(Width1_Mid10row)

# # =========== Three-Quarter point(Ground surface) Find Max Velocity Value ===================
# Width20_ele80_Quartermax = Find_ColMaxValue(Width20_Quarter80row)
# Width20_ele40_Quartermax = Find_ColMaxValue(Width20_Quarter40row)
# Width20_ele20_Quartermax = Find_ColMaxValue(Width20_Quarter20row)
# Width20_ele10_Quartermax = Find_ColMaxValue(Width20_Quarter10row)

# Width10_ele80_Quartermax = Find_ColMaxValue(Width10_Quarter80row)
# Width10_ele40_Quartermax = Find_ColMaxValue(Width10_Quarter40row)
# Width10_ele20_Quartermax = Find_ColMaxValue(Width10_Quarter20row)
# Width10_ele10_Quartermax = Find_ColMaxValue(Width10_Quarter10row)

# Width1_ele80_Quartermax = Find_ColMaxValue(Width1_Quarter80row)
# Width1_ele40_Quartermax = Find_ColMaxValue(Width1_Quarter40row)
# Width1_ele20_Quartermax = Find_ColMaxValue(Width1_Quarter20row)
# Width1_ele10_Quartermax = Find_ColMaxValue(Width1_Quarter10row)

# # ----------- Middle point relative error ---------------------
# RE_Width20_80Mid = np.zeros((len(Width20_ele80_Mid),2))
# RE_Width20_40Mid = np.zeros((len(Width20_ele40_Mid),2))
# RE_Width20_20Mid = np.zeros((len(Width20_ele20_Mid),2))
# RE_Width20_10Mid = np.zeros((len(Width20_ele10_Mid),2))

# RE_Width10_80Mid = np.zeros((len(Width10_ele80_Mid),2))
# RE_Width10_40Mid = np.zeros((len(Width10_ele40_Mid),2))
# RE_Width10_20Mid = np.zeros((len(Width10_ele20_Mid),2))
# RE_Width10_10Mid = np.zeros((len(Width10_ele10_Mid),2))

# RE_Width1_80Mid = np.zeros((len(Width1_ele80_Mid),2))
# RE_Width1_40Mid = np.zeros((len(Width1_ele40_Mid),2))
# RE_Width1_20Mid = np.zeros((len(Width1_ele20_Mid),2))
# RE_Width1_10Mid = np.zeros((len(Width1_ele10_Mid),2))

# # ----------- three quarter point relative error ---------------------
# RE_Width20_80Quarter = np.zeros((len(Width20_ele80_Quarter),2))
# RE_Width20_40Quarter = np.zeros((len(Width20_ele40_Quarter),2))
# RE_Width20_20Quarter = np.zeros((len(Width20_ele20_Quarter),2))
# RE_Width20_10Quarter = np.zeros((len(Width20_ele10_Quarter),2))

# RE_Width10_80Quarter = np.zeros((len(Width10_ele80_Quarter),2))
# RE_Width10_40Quarter = np.zeros((len(Width10_ele40_Quarter),2))
# RE_Width10_20Quarter = np.zeros((len(Width10_ele20_Quarter),2))
# RE_Width10_10Quarter = np.zeros((len(Width10_ele10_Quarter),2))

# RE_Width1_80Quarter = np.zeros((len(Width1_ele80_Quarter),2))
# RE_Width1_40Quarter = np.zeros((len(Width1_ele40_Quarter),2))
# RE_Width1_20Quarter = np.zeros((len(Width1_ele20_Quarter),2))
# RE_Width1_10Quarter = np.zeros((len(Width1_ele10_Quarter),2))


# def calculate_error(relative_Error80,ele80_Mid,ele80_max):
# # # ---------- calculate relative error -----------------
#     for n in range(len(ele80_Mid)):
#         relative_Error80[n,0] = ele80_Mid[n,0]
#         relative_Error80[n,1] = ((ele80_Mid[n,1]- ele80_max)/ele80_max)*100
#         # relative_Error80[n,1] = ((ele80_Mid[n,1]- 0.0001)/ele80_max)*100
# # ----------- Middle point Calculate relative error ---------------------
# calculate_error(RE_Width20_80Mid, Width20_ele80_Mid, Width20_ele80_max)
# calculate_error(RE_Width20_40Mid, Width20_ele40_Mid, Width20_ele40_max)
# calculate_error(RE_Width20_20Mid, Width20_ele20_Mid, Width20_ele20_max)
# calculate_error(RE_Width20_10Mid, Width20_ele10_Mid, Width20_ele10_max)

# calculate_error(RE_Width10_80Mid, Width10_ele80_Mid, Width10_ele80_max)
# calculate_error(RE_Width10_40Mid, Width10_ele40_Mid, Width10_ele40_max)
# calculate_error(RE_Width10_20Mid, Width10_ele20_Mid, Width10_ele20_max)
# calculate_error(RE_Width10_10Mid, Width10_ele10_Mid, Width10_ele10_max)

# calculate_error(RE_Width1_80Mid, Width1_ele80_Mid, Width1_ele80_max)
# calculate_error(RE_Width1_40Mid, Width1_ele40_Mid, Width1_ele40_max)
# calculate_error(RE_Width1_20Mid, Width1_ele20_Mid, Width1_ele20_max)
# calculate_error(RE_Width1_10Mid, Width1_ele10_Mid, Width1_ele10_max)

# # ----------- Three Quarter point Calculate relative error ---------------------
# calculate_error(RE_Width20_80Quarter, Width20_ele80_Quarter, Width20_ele80_Quartermax)
# calculate_error(RE_Width20_40Quarter, Width20_ele40_Quarter, Width20_ele40_Quartermax)
# calculate_error(RE_Width20_20Quarter, Width20_ele20_Quarter, Width20_ele20_Quartermax)
# calculate_error(RE_Width20_10Quarter, Width20_ele10_Quarter, Width20_ele10_Quartermax)

# calculate_error(RE_Width10_80Quarter, Width10_ele80_Quarter, Width10_ele80_Quartermax)
# calculate_error(RE_Width10_40Quarter, Width10_ele40_Quarter, Width10_ele40_Quartermax)
# calculate_error(RE_Width10_20Quarter, Width10_ele20_Quarter, Width10_ele20_Quartermax)
# calculate_error(RE_Width10_10Quarter, Width10_ele10_Quarter, Width10_ele10_Quartermax)

# calculate_error(RE_Width1_80Quarter, Width1_ele80_Quarter, Width1_ele80_Quartermax)
# calculate_error(RE_Width1_40Quarter, Width1_ele40_Quarter, Width1_ele40_Quartermax)
# calculate_error(RE_Width1_20Quarter, Width1_ele20_Quarter, Width1_ele20_Quartermax)
# calculate_error(RE_Width1_10Quarter, Width1_ele10_Quarter, Width1_ele10_Quartermax)

# TimeIncrement = np.zeros(5)
# for k in range(len(error_dt)):    
#     TimeIncrement[k] = error_dt[k] - 0.0424514
#     # print(TimeIncrement[k])
# # ==================Draw Relative error : Middele point =============================
# def Differ_elemetError(RE_Width20_80Mid,RE_Width20_40Mid,RE_Width20_20Mid,RE_Width20_10Mid):
#     # plt.figure(figsize=(8,6))
#     font_props = {'family': 'Arial', 'size': 10}
#     # plt.xlabel("time (s)",fontsize= 20)
#     # plt.ylabel(r"relative error (%)",fontsize=20)
#     # plt.title("Ground Surface relative error: Middle node(TieBC)", fontsize = 18)
#     # plt.title(titleName,x=0.25,y=0.35, fontsize = 18)
    
#     plt.plot(TimeIncrement[:],RE_Width20_80Mid[:,1],marker = '^',markersize=12,markerfacecolor = 'white',label = r"$\Delta c = 0.125$ ${\rm m}$")
#     plt.plot(TimeIncrement[:],RE_Width20_40Mid[:,1],marker = 'o',markersize=12,markerfacecolor = 'white',label = r"$\Delta c = 0.25$ ${\rm m}$")
#     plt.plot(TimeIncrement[:],RE_Width20_20Mid[:,1],marker = '<',markersize=12,markerfacecolor = 'white',label = r"$\Delta c = 0.50$ ${\rm m}$")
#     plt.plot(TimeIncrement[:],RE_Width20_10Mid[:,1],marker = 's',markersize=12,markerfacecolor = 'white',label = r"$\Delta c = 1.0$ ${\rm m}$")
    
#     plt.legend(loc='upper left',prop=font_props,frameon=False) #ncol=2,fontsize=16
#     plt.xticks(fontsize = 15)
#     plt.yticks(fontsize = 15)
#     # plt.xlim(0.0, 0.20)
#     plt.grid(True)
    
# # ------------ Relative error : Middele point ---------------------------------
# x_axis1 = Min_timeIncrement # 0.1 0.05

# fig5, (ax15,ax16,ax17) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8,8))
# fig5.suptitle(f'{Boundary1} \n(Middle node)',x=0.5,y =0.99,fontsize = 20)
# fig5.text(0.03,0.5, 'Relative error (%)', va= 'center', rotation= 'vertical', fontsize=20)
# fig5.text(0.35,0.05, f'Time Increment '+ r'$\Delta t$ $\mathrm {(s)}$', va= 'center', fontsize=18)

# ax15 = plt.subplot(311)
# Differ_elemetError(RE_Width20_80Mid,RE_Width20_40Mid,RE_Width20_20Mid,RE_Width20_10Mid)
# ax15.set_title(f"Soil Width 20m",fontsize =16)

# ax16 = plt.subplot(312)
# Differ_elemetError(RE_Width10_80Mid,RE_Width10_40Mid,RE_Width10_20Mid,RE_Width10_10Mid)
# ax16.set_title(f"Soil Width 10m",fontsize =16)

# ax17 = plt.subplot(313)
# Differ_elemetError(RE_Width1_80Mid,RE_Width1_40Mid,RE_Width1_20Mid,RE_Width1_10Mid)
# ax17.set_title(f"Soil Width 1m",fontsize =16)
# # ax17.xaxis.set_major_locator(ticker.MultipleLocator(x_axis1))
# # ax17.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# for ax in [ax15,ax16,ax17]:
#     ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
#     # ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis1))
#     ax.ticklabel_format(axis='x', style='sci', scilimits=(-1,2))
#     ax.yaxis.get_offset_text().set(size=18)
#     ax.xaxis.get_offset_text().set(size=16)

# # ------------ Relative error : three quarter point ---------------------------------
# fig6, (ax18,ax19,ax20) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8,8))
# fig6.suptitle(f'{Boundary1} \n(Three Quarter node)',x=0.5,y =0.99,fontsize = 20)
# fig6.text(0.03,0.5, 'Relative error (%)', va= 'center', rotation= 'vertical', fontsize=20)
# fig6.text(0.35,0.05, f'Time Increment '+ r'$\Delta t$ $\mathrm {(s)}$', va= 'center', fontsize=18)

# ax18 = plt.subplot(311)
# Differ_elemetError(RE_Width20_80Quarter,RE_Width20_40Quarter,RE_Width20_20Quarter,RE_Width20_10Quarter)
# ax18.set_title(f"Soil Width 20m",fontsize =16)

# ax19 = plt.subplot(312)
# Differ_elemetError(RE_Width10_80Quarter,RE_Width10_40Quarter,RE_Width10_20Quarter,RE_Width10_10Quarter)
# ax19.set_title(f"Soil Width 10m",fontsize =16)

# ax20 = plt.subplot(313)
# Differ_elemetError(RE_Width1_80Quarter,RE_Width1_40Quarter,RE_Width1_20Quarter,RE_Width1_10Quarter)
# ax20.set_title(f"Soil Width 1m",fontsize =16)

# for ax in [ax18,ax19,ax20]:
#     ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis1))
#     ax.ticklabel_format(axis='x', style='sci', scilimits=(-1,2))
#     ax.yaxis.get_offset_text().set(size=18)
#     ax.xaxis.get_offset_text().set(size=16)
# # ========== Relative error fot different "Time Increment"(for x in differernt Vertical element) ================================
# # ----------- Mideele Point -----------------
# W20_dt80Mid = np.zeros((4,2))
# W20_dt40Mid = np.zeros((4,2))
# W20_dt20Mid = np.zeros((4,2))
# W20_dt10Mid = np.zeros((4,2))

# W10_dt80Mid = np.zeros((4,2))
# W10_dt40Mid = np.zeros((4,2))
# W10_dt20Mid = np.zeros((4,2))
# W10_dt10Mid = np.zeros((4,2))

# W1_dt80Mid = np.zeros((4,2))
# W1_dt40Mid = np.zeros((4,2))
# W1_dt20Mid = np.zeros((4,2))
# W1_dt10Mid = np.zeros((4,2))

# # -----------Three Quarter Point -----------------
# W20_dt80Qua = np.zeros((4,2))
# W20_dt40Qua = np.zeros((4,2))
# W20_dt20Qua = np.zeros((4,2))
# W20_dt10Qua = np.zeros((4,2))

# W10_dt80Qua = np.zeros((4,2))
# W10_dt40Qua = np.zeros((4,2))
# W10_dt20Qua = np.zeros((4,2))
# W10_dt10Qua = np.zeros((4,2))

# W1_dt80Qua = np.zeros((4,2))
# W1_dt40Qua = np.zeros((4,2))
# W1_dt20Qua = np.zeros((4,2))
# W1_dt10Qua = np.zeros((4,2))


# matrix_values = np.array((80.0, 40.0, 20.0, 10.0))
# dc = L/matrix_values
# dc_dt = top_time+ dc/cp
# def Time_RE(W20_dt80Mid,W20_dt40Mid, W20_dt20Mid, W20_dt10Mid, Width20_Mid80row, Width20_Mid40row, Width20_Mid20row, Width20_Mid10row):
#     # ---- ele 80 dt = 0.0427855 --------------
#     W20_dt80Mid[:,0] = dc[:]
#     W20_dt80Mid[0,1] = Width20_Mid80row[1280,2]
#     W20_dt80Mid[1,1] = Width20_Mid40row[639,2] #-4.83304e-06
#     W20_dt80Mid[2,1] = Width20_Mid20row[320,2] #4.543-e06
#     W20_dt80Mid[3,1] = Width20_Mid10row[159,2] # 3.9174e-06
#     # ---- ele 40 dt = 0.0431196 --------------
#     W20_dt40Mid[:,0] = dc[:]
#     W20_dt40Mid[0,1] = Width20_Mid80row[1290,2]
#     W20_dt40Mid[1,1] = Width20_Mid40row[644,2] #-4.83304e-06
#     W20_dt40Mid[2,1] = Width20_Mid20row[323,2] #4.543-e06
#     W20_dt40Mid[3,1] = Width20_Mid10row[161,2] # 3.9174e-06
#     # ---- ele 20 dt = 0.0437877 --------------
#     W20_dt20Mid[:,0] = dc[:]
#     W20_dt20Mid[0,1] = Width20_Mid80row[1310,2]
#     W20_dt20Mid[1,1] = Width20_Mid40row[654,2] #-4.83304e-06
#     W20_dt20Mid[2,1] = Width20_Mid20row[328,2] #4.543-e06
#     W20_dt20Mid[3,1] = Width20_Mid10row[163,2] # 3.9174e-06
#     # ---- ele 10 dt = 0.045124 --------------
#     W20_dt10Mid[:,0] = dc[:]
#     W20_dt10Mid[0,1] = Width20_Mid80row[1350,2]
#     W20_dt10Mid[1,1] = Width20_Mid40row[674,2] #-4.83304e-06
#     W20_dt10Mid[2,1] = Width20_Mid20row[338,2] #4.543-e06
#     W20_dt10Mid[3,1] = Width20_Mid10row[168,2] # 3.9174e-06
#             # print(u)
# # ------------------------------- SoilWidth 20、10、1m:Middle point-------------------------------
# Time_RE(W20_dt80Mid,W20_dt40Mid, W20_dt20Mid, W20_dt10Mid, Width20_Mid80row, Width20_Mid40row, Width20_Mid20row, Width20_Mid10row)
# Time_RE(W10_dt80Mid,W10_dt40Mid, W10_dt20Mid, W10_dt10Mid, Width10_Mid80row, Width10_Mid40row, Width10_Mid20row, Width10_Mid10row)
# Time_RE(W1_dt80Mid,W1_dt40Mid, W1_dt20Mid, W1_dt10Mid, Width1_Mid80row, Width1_Mid40row, Width1_Mid20row, Width1_Mid10row)

# # ------------------------------- SoilWidth 20、10、1m:Three Quarter point-------------------------------
# Time_RE(W20_dt80Qua,W20_dt40Qua, W20_dt20Qua, W20_dt10Qua, Width20_Quarter80row, Width20_Quarter40row, Width20_Quarter20row, Width20_Quarter10row)
# Time_RE(W10_dt80Qua,W10_dt40Qua, W10_dt20Qua, W10_dt10Qua, Width10_Quarter80row, Width10_Quarter40row, Width10_Quarter20row, Width10_Quarter10row)
# Time_RE(W1_dt80Qua,W1_dt40Qua, W1_dt20Qua, W1_dt10Qua, Width1_Quarter80row, Width1_Quarter40row, Width1_Quarter20row, Width1_Quarter10row)

# def calculate_Dc_error(RE_DC_W20_80Mid, W20_dt80, Width20_ele80_max,Width20_ele40_max, Width20_ele20_max, Width20_ele10_max):
#     RE_DC_W20_80Mid[:,0] =  W20_dt80[:,0]
#     RE_DC_W20_80Mid[0,1] =  ((W20_dt80[0,1]- Width20_ele80_max)/Width20_ele80_max)*100
#     RE_DC_W20_80Mid[1,1] =  ((W20_dt80[1,1]- Width20_ele40_max)/Width20_ele40_max)*100
#     RE_DC_W20_80Mid[2,1] =  ((W20_dt80[2,1]- Width20_ele20_max)/Width20_ele20_max)*100
#     RE_DC_W20_80Mid[3,1] =  ((W20_dt80[3,1]- Width20_ele10_max)/Width20_ele10_max)*100

# # ------------------------------- Time Increment Relative Error: 20、10、1m (Middle point)-------------------- 
# RE_DC_W20_80Mid = np.zeros((len(W20_dt80Mid),2))
# RE_DC_W20_40Mid = np.zeros((len(W20_dt40Mid),2))
# RE_DC_W20_20Mid = np.zeros((len(W20_dt20Mid),2))
# RE_DC_W20_10Mid = np.zeros((len(W20_dt10Mid),2))

# RE_DC_W10_80Mid = np.zeros((len(W10_dt80Mid),2))
# RE_DC_W10_40Mid = np.zeros((len(W10_dt40Mid),2))
# RE_DC_W10_20Mid = np.zeros((len(W10_dt20Mid),2))
# RE_DC_W10_10Mid = np.zeros((len(W10_dt10Mid),2))

# RE_DC_W1_80Mid = np.zeros((len(W1_dt80Mid),2))
# RE_DC_W1_40Mid = np.zeros((len(W1_dt40Mid),2))
# RE_DC_W1_20Mid = np.zeros((len(W1_dt20Mid),2))
# RE_DC_W1_10Mid = np.zeros((len(W1_dt10Mid),2))

# calculate_Dc_error(RE_DC_W20_80Mid, W20_dt80Mid, Width20_ele80_max,Width20_ele40_max, Width20_ele20_max, Width20_ele10_max)
# calculate_Dc_error(RE_DC_W20_40Mid, W20_dt40Mid, Width20_ele80_max,Width20_ele40_max, Width20_ele20_max, Width20_ele10_max)
# calculate_Dc_error(RE_DC_W20_20Mid, W20_dt20Mid, Width20_ele80_max,Width20_ele40_max, Width20_ele20_max, Width20_ele10_max)
# calculate_Dc_error(RE_DC_W20_10Mid, W20_dt10Mid, Width20_ele80_max,Width20_ele40_max, Width20_ele20_max, Width20_ele10_max)

# calculate_Dc_error(RE_DC_W10_80Mid, W10_dt80Mid, Width10_ele80_max,Width10_ele40_max, Width10_ele20_max, Width10_ele10_max)
# calculate_Dc_error(RE_DC_W10_40Mid, W10_dt40Mid, Width10_ele80_max,Width10_ele40_max, Width10_ele20_max, Width10_ele10_max)
# calculate_Dc_error(RE_DC_W10_20Mid, W10_dt20Mid, Width10_ele80_max,Width10_ele40_max, Width10_ele20_max, Width10_ele10_max)
# calculate_Dc_error(RE_DC_W10_10Mid, W10_dt10Mid, Width10_ele80_max,Width10_ele40_max, Width10_ele20_max, Width10_ele10_max)

# calculate_Dc_error(RE_DC_W1_80Mid, W1_dt80Mid, Width1_ele80_max,Width1_ele40_max, Width1_ele20_max, Width1_ele10_max)
# calculate_Dc_error(RE_DC_W1_40Mid, W1_dt40Mid, Width1_ele80_max,Width1_ele40_max, Width1_ele20_max, Width1_ele10_max)
# calculate_Dc_error(RE_DC_W1_20Mid, W1_dt20Mid, Width1_ele80_max,Width1_ele40_max, Width1_ele20_max, Width1_ele10_max)
# calculate_Dc_error(RE_DC_W1_10Mid, W1_dt10Mid, Width1_ele80_max,Width1_ele40_max, Width1_ele20_max, Width1_ele10_max)

# # ------------------------------- Time Increment Relative Error: 20、10、1m (Three Quarter point)-------------------- 
# RE_DC_W20_80Qua = np.zeros((len(W20_dt80Qua),2))
# RE_DC_W20_40Qua = np.zeros((len(W20_dt40Qua),2))
# RE_DC_W20_20Qua = np.zeros((len(W20_dt20Qua),2))
# RE_DC_W20_10Qua = np.zeros((len(W20_dt10Qua),2))

# RE_DC_W10_80Qua = np.zeros((len(W10_dt80Qua),2))
# RE_DC_W10_40Qua = np.zeros((len(W10_dt40Qua),2))
# RE_DC_W10_20Qua = np.zeros((len(W10_dt20Qua),2))
# RE_DC_W10_10Qua = np.zeros((len(W10_dt10Qua),2))

# RE_DC_W1_80Qua = np.zeros((len(W1_dt80Qua),2))
# RE_DC_W1_40Qua = np.zeros((len(W1_dt40Qua),2))
# RE_DC_W1_20Qua = np.zeros((len(W1_dt20Qua),2))
# RE_DC_W1_10Qua = np.zeros((len(W1_dt10Qua),2))

# calculate_Dc_error(RE_DC_W20_80Qua, W20_dt80Qua, Width20_ele80_Quartermax,Width20_ele40_Quartermax, Width20_ele20_Quartermax, Width20_ele10_Quartermax)
# calculate_Dc_error(RE_DC_W20_40Qua, W20_dt40Qua, Width20_ele80_Quartermax,Width20_ele40_Quartermax, Width20_ele20_Quartermax, Width20_ele10_Quartermax)
# calculate_Dc_error(RE_DC_W20_20Qua, W20_dt20Qua, Width20_ele80_Quartermax,Width20_ele40_Quartermax, Width20_ele20_Quartermax, Width20_ele10_Quartermax)
# calculate_Dc_error(RE_DC_W20_10Qua, W20_dt10Qua, Width20_ele80_Quartermax,Width20_ele40_Quartermax, Width20_ele20_Quartermax, Width20_ele10_Quartermax)

# calculate_Dc_error(RE_DC_W10_80Qua, W10_dt80Qua, Width10_ele80_Quartermax,Width10_ele40_Quartermax, Width10_ele20_Quartermax, Width10_ele10_Quartermax)
# calculate_Dc_error(RE_DC_W10_40Qua, W10_dt40Qua, Width10_ele80_Quartermax,Width10_ele40_Quartermax, Width10_ele20_Quartermax, Width10_ele10_Quartermax)
# calculate_Dc_error(RE_DC_W10_20Qua, W10_dt20Qua, Width10_ele80_Quartermax,Width10_ele40_Quartermax, Width10_ele20_Quartermax, Width10_ele10_Quartermax)
# calculate_Dc_error(RE_DC_W10_10Qua, W10_dt10Qua, Width10_ele80_Quartermax,Width10_ele40_Quartermax, Width10_ele20_Quartermax, Width10_ele10_Quartermax)

# calculate_Dc_error(RE_DC_W1_80Qua, W1_dt80Qua, Width1_ele80_Quartermax,Width1_ele40_Quartermax, Width1_ele20_Quartermax, Width1_ele10_Quartermax)
# calculate_Dc_error(RE_DC_W1_40Qua, W1_dt40Qua, Width1_ele80_Quartermax,Width1_ele40_Quartermax, Width1_ele20_Quartermax, Width1_ele10_Quartermax)
# calculate_Dc_error(RE_DC_W1_20Qua, W1_dt20Qua, Width1_ele80_Quartermax,Width1_ele40_Quartermax, Width1_ele20_Quartermax, Width1_ele10_Quartermax)
# calculate_Dc_error(RE_DC_W1_10Qua, W1_dt10Qua, Width1_ele80_Quartermax,Width1_ele40_Quartermax, Width1_ele20_Quartermax, Width1_ele10_Quartermax)

# # ------------------------------- Time Increment Relative Error: 20、10、1m (Middle point)-------------------- 
# # ==================Draw Relative error : Middele point =============================
# def DifferTime_elemetError(RE_DC_W20_80Mid, RE_DC_W20_40Mid, RE_DC_W20_20Mid, RE_DC_W20_10Mid):
#     # plt.figure(figsize=(8,6))
#     font_props = {'family': 'Arial', 'size': 10}
#     # plt.xlabel("time (s)",fontsize= 20)
#     # plt.ylabel(r"relative error (%)",fontsize=20)
#     # plt.title("Ground Surface relative error: Middle node(TieBC)", fontsize = 18)
#     # plt.title(titleName,x=0.25,y=0.35, fontsize = 18)
    
#     plt.plot(RE_DC_W20_80Mid[:,0],RE_DC_W20_80Mid[:,1],marker = '^',markersize=12,markerfacecolor = 'white',label = r"$\Delta t = 0.000625$ ${\rm s}$")
#     plt.plot(RE_DC_W20_40Mid[:,0],RE_DC_W20_40Mid[:,1],marker = 'o',markersize=12,markerfacecolor = 'white',label = r"$\Delta t = 0.00125$ ${\rm s}$")
#     plt.plot(RE_DC_W20_20Mid[:,0],RE_DC_W20_20Mid[:,1],marker = '<',markersize=12,markerfacecolor = 'white',label = r"$\Delta t = 0.0025$ ${\rm s}$")
#     plt.plot(RE_DC_W20_10Mid[:,0],RE_DC_W20_10Mid[:,1],marker = 's',markersize=12,markerfacecolor = 'white',label = r"$\Delta t = 0.005$ ${\rm s}$")
    
#     plt.legend(loc='lower right',prop=font_props) #ncol=2,fontsize=16 frameon=False
#     plt.xticks(fontsize = 15)
#     plt.yticks(fontsize = 15)
#     # plt.xlim(0.0, 0.20)
#     plt.grid(True)
    
# x_axis2 = 0.125 # 0.1 0.05    

# # ==================Draw Relative error : Middele point =============================
# # (ax11,ax12,ax13)
# fig7, (ax21,ax22,ax23) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8,8))
# fig7.suptitle(f'{Boundary1} \n(Middle node)',x=0.5,y =0.99,fontsize = 20)
# fig7.text(0.03,0.5, 'Relative error (%)', va= 'center', rotation= 'vertical', fontsize=20)
# fig7.text(0.40,0.05, f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# # fig1.text(0.25,0.05, 'Middle Node', va= 'center', fontsize=16)
# # fig1.text(0.65,0.05, 'Three_Quarter Node', va= 'center', fontsize=16)

# ax21 = plt.subplot(311)
# DifferTime_elemetError(RE_DC_W20_80Mid,RE_DC_W20_40Mid,RE_DC_W20_20Mid,RE_DC_W20_10Mid)
# ax21.set_title(f"Soil Width 20m",fontsize =16)


# ax22 = plt.subplot(312)
# DifferTime_elemetError(RE_DC_W10_80Mid,RE_DC_W10_40Mid,RE_DC_W10_20Mid,RE_DC_W10_10Mid)
# ax22.set_title(f"Soil Width 10m",fontsize =16)


# ax23 = plt.subplot(313)
# DifferTime_elemetError(RE_DC_W1_80Mid,RE_DC_W1_40Mid,RE_DC_W1_20Mid,RE_DC_W1_10Mid)
# ax23.set_title(f"Soil Width 1m",fontsize =16)
# ax23.xaxis.set_major_locator(ticker.MultipleLocator(x_axis2))
# ax23.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# for ax in [ax21,ax22,ax23]:
#     ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis2))
#     ax.ticklabel_format(axis='x', style='sci', scilimits=(-1,2))
    
# # ==================Draw Relative error(20,10,1 m) : Three Quarter point =============================
# fig8, (ax24,ax25,ax26) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8,8))
# fig8.suptitle(f'{Boundary1} \n(Three Quarter node)',x=0.5,y =0.99,fontsize = 20)
# fig8.text(0.03,0.5, 'Relative error (%)', va= 'center', rotation= 'vertical', fontsize=20)
# fig8.text(0.40,0.05, f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax24 = plt.subplot(311)
# DifferTime_elemetError(RE_DC_W20_80Qua,RE_DC_W20_40Qua,RE_DC_W20_20Qua,RE_DC_W20_10Qua)
# ax24.set_title(f"Soil Width 20m",fontsize =16)

# ax25 = plt.subplot(312)
# DifferTime_elemetError(RE_DC_W10_80Qua,RE_DC_W10_40Qua,RE_DC_W10_20Qua,RE_DC_W10_10Qua)
# ax25.set_title(f"Soil Width 10m",fontsize =16)

# ax26 = plt.subplot(313)
# DifferTime_elemetError(RE_DC_W1_80Qua,RE_DC_W1_40Qua,RE_DC_W1_20Qua,RE_DC_W1_10Qua)
# ax26.set_title(f"Soil Width 1m",fontsize =16)

# for ax in [ax24,ax25,ax26]:
#     ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis2))
#     ax.ticklabel_format(axis='x', style='sci', scilimits=(-1,2))
