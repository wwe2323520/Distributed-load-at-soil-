# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 22:21:09 2023

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
pi = np.pi
plt.rc('font', family= 'Times New Roman')

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

# file1 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\TopForce_80row\node12961.out"
# file2 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\TopForce_80row\node6521.out"
# file3 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\TopForce_80row\node725.out"

# file1 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\TopForce_40row\node6521.out"
# file2 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\TopForce_40row\node3281.out"
# file3 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\TopForce_40row\node365.out"

# file1 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\TopForce_20row\node3301.out"
# file2 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\TopForce_20row\node1661.out"
# file3 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\TopForce_20row\node185.out"

file1 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\TopSideMidBeamDash_10row\node1691.out"
file2 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\TopSideMidBeamDash_10row\node851.out"
file3 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\TopSideMidBeamDash_10row\node95.out"

Mid20m = rdnumpy(file1)
Mid10m = rdnumpy(file2)
Mid1m = rdnumpy(file3)


# file6 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\TopForce_80row\node13001.out"
# file7 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\TopSideDash_80row\node6541.out"
# file8 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\TopSideDash_80row\node727.out"

# file6 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\TopForce_40row\node6561.out"
# file7 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\TopForce_40row\node3301.out"
# file8 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\TopForce_40row\node367.out"

# file6 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\TopForce_20row\node3341.out"
# file7 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\TopForce_20row\node1681.out"
# file8 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\TopForce_20row\node187.out"

file6 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\20mRefinement\TopSideMidBeamDash_10row\node1731.out"
file7 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\10mRefinement\TopSideMidBeamDash_10row\node871.out"
file8 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\1mRefinement\TopSideMidBeamDash_10row\node97.out"


Quarter20m = rdnumpy(file6)
Quarter10m = rdnumpy(file7)
Quarter1m = rdnumpy(file8)

plt_axis2 = 2
# # ------- wave put into the timeSeries ---------------   
plt.figure(figsize=(8,6))
  
plt.xlabel("time (s)",fontsize=18)
plt.ylabel(r"$V_y$  $(m/s)$",fontsize=18)

# # plt.title('Mid Point',fontsize = 18) 

# plt.plot(Mid20m[:,0],Mid20m[:,plt_axis2],label =r'${\rm 20msoil}$ ($\Delta C=0.25 $ ${\rm m}$)', ls = '--',linewidth=6.0)
# plt.plot(Mid10m[:,0],Mid10m[:,plt_axis2],label =r'${\rm 10msoil}$ ($\Delta C=0.25 $ ${\rm m}$)', ls = '-.',linewidth=4.0)
# plt.plot(Mid1m[:,0],Mid1m[:,plt_axis2],label =r'${\rm 1msoil}$ ($\Delta C=0.25 $ ${\rm m}$)', ls = ':',linewidth=2.0)

# # # # # plt.title('Quarter Point',fontsize = 18) 

plt.plot(Quarter20m[:,0],Quarter20m[:,plt_axis2],label =r'${\rm 20msoil}$ ($\Delta C=1.0$ ${\rm m}$)', ls = '--',linewidth=6.0)
plt.plot(Quarter10m[:,0],Quarter10m[:,plt_axis2],label =r'${\rm 10msoil}$ ($\Delta C=1.0$ ${\rm m}$)', ls = '-.',linewidth=4.0)
plt.plot(Quarter1m[:,0],Quarter1m[:,plt_axis2],label =r'${\rm 1msoil}$ ($\Delta C=1.0$ ${\rm m}$)', ls = ':',linewidth=2.0)

plt.legend(loc='upper right',fontsize=16) #ncol=2
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlim(0.0, 0.20)
plt.grid(True)

# x_axis = 0.025 # 0.1 0.05
ax4 = plt.gca()
# ax4.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax4.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax4.yaxis.get_offset_text().set(size=18)

# =========== Build Different element size dt ================================
def ele_dt(element):
    tns = L/cs # wave transport time
    dcell = tns/element #each cell time
    dt = dcell/10 #eace cell have 10 steps
    return(dt)

def ele_compare(ele80,Mid20m):
    for j in range(16): #16
        dt = round(0.0125*j +0.0125,4)
        # dt = round(0.012549*j +0.012549,6)
        # dt = round(0.012502*j +0.012502,6)
        # dt = round(0.0126252*j +0.0126252,6)
        # dt = round(0.012358*j +0.012358,6)
        # print(dt)
        for i in range(len(Mid20m)):
            if round(Mid20m[i, 0],6) == dt:
                ele80[1+j,0] = Mid20m[i,0]
                ele80[1+j,1] = Mid20m[i,2]
                # print(i,Mid20m[i,0],Mid20m[i,1])
                
ele10_time = np.arange(0.0,0.4001,ele_dt(10)) #5e-5 in 100row
ele20_time = np.arange(0.0,0.4001,ele_dt(20))
ele40_time = np.arange(0.0,0.4001,ele_dt(40))
ele80_time = np.arange(0.0,0.4000,ele_dt(80))


Mid20 = np.zeros((17,2))
Mid10 = np.zeros((17,2))
Mid1 = np.zeros((17,2))

Quarter20 = np.zeros((17,2))
Quarter10 = np.zeros((17,2))
Quarter1 = np.zeros((17,2))


# ================= Save differ element size velocity ===========================
ele_compare(Mid20,Mid20m)
ele_compare(Mid10,Mid10m)
ele_compare(Mid1,Mid1m)

ele_compare(Quarter20,Quarter20m)
ele_compare(Quarter10,Quarter10m)
ele_compare(Quarter1,Quarter1m)

total_MidCompare = np.zeros((len(Mid20),4))
total_MidCompare[:,0] = Mid20[:,0]
total_MidCompare[:,1] = Mid20[:,1]
total_MidCompare[:,2] = Mid10[:,1]
total_MidCompare[:,3] = Mid1[:,1]
total_MidCompare[1,1] = 0
total_MidCompare[2,1] = 0

total_QuarterCompare = np.zeros((len(Quarter20),4))
total_QuarterCompare[:,0] = Quarter20[:,0]
total_QuarterCompare[:,1] = Quarter20[:,1]
total_QuarterCompare[:,2] = Quarter10[:,1]
total_QuarterCompare[:,3] = Quarter1[:,1]
total_QuarterCompare[1,1] = 0
total_QuarterCompare[2,1] = 0

error_Midcompare = np.zeros((len(total_MidCompare),3))
error_Midcompare[:,0] =  total_MidCompare[:,0]

error_Quartercompare = np.zeros((len(total_QuarterCompare),3))
error_Quartercompare[:,0] =  total_QuarterCompare[:,0]
for i in range(2):#4
    for j in range(len(error_Midcompare)):
        error_Midcompare[j,1+i] = ((total_MidCompare[j,2+i] - total_MidCompare[j,1])/ total_MidCompare[j,1])*100
        error_Quartercompare[j,1+i] = ((total_QuarterCompare[j,2+i] - total_QuarterCompare[j,1])/ total_QuarterCompare[j,1])*100
    
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

plt.plot(error_Midcompare[:,0],error_Midcompare[:,1],label = r"$\Delta c = 0.25$ ${\rm m}$ ${\rm (soilwidth = 10m)}$", marker = '^',markersize=16,markerfacecolor = 'white')
plt.plot(error_Midcompare[:,0],error_Midcompare[:,2],label = r"$\Delta c = 0.25$ ${\rm m}$ ${\rm (soilwidth = 1m)}$", marker = 's',markersize=14,markerfacecolor = 'white')

plt.legend(loc='upper left',fontsize=15) #ncol=2
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

plt.plot(error_Quartercompare[:,0],error_Quartercompare[:,1],label = r"$\Delta c = 0.25$ ${\rm m}$ ${\rm (soilwidth = 10m)}$", marker = '^',markersize=16,markerfacecolor = 'white')
plt.plot(error_Quartercompare[:,0],error_Quartercompare[:,2],label = r"$\Delta c = 0.25$ ${\rm m}$ ${\rm (soilwidth = 1m)}$", marker = 's',markersize=14,markerfacecolor = 'white')

plt.legend(loc='lower right',fontsize=15) #ncol=2
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
