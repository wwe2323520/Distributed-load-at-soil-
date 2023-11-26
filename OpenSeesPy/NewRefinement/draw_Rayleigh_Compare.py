# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 17:51:30 2023

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

# =================== Middle Node ============================ 
# ------------ 10,1 m Tie Boundary------------------
file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopTie_Rayleigh_80row/node6521.out"
file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopForce_80row/node6521.out"
file3 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopTie_Rayleigh_80row/node725.out"
file4 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopForce_80row/node725.out"

# ---------10,1 m LK Dashpot ---------------
file5 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopLK_Rayleigh_80row/node6521.out"
file6 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideDash_80row/node6521.out"
file7 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopLK_Rayleigh_80row/node725.out"
file8 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideDash_80row/node725.out"

# =================== Quarter Node ============================ 
# ------------ 10,1 m Tie Boundary------------------
file9 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopTie_Rayleigh_80row/node6541.out"
file10 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopForce_80row/node6541.out"
file11 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopTie_Rayleigh_80row/node727.out"
file12 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopForce_80row/node727.out"

# # ---------10, 1 m LK Dashpot ---------------
file13 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopLK_Rayleigh_80row/node6541.out"
file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideDash_80row/node6541.out"
file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopLK_Rayleigh_80row/node727.out"
file16 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideDash_80row/node727.out"

# ============== Middle Node ==================
# ------------ 10,1 m Tie Boundary------------------
W10Tie_Ray80row = rdnumpy(file1)
W10Tie_80row = rdnumpy(file2)
W1Tie_Ray80row = rdnumpy(file3)
W1Tie_80row = rdnumpy(file4)

# ------------ 10,1 m LK Dashpot------------------
W10LK_Ray80row = rdnumpy(file5)
W10LK_80row = rdnumpy(file6)
W1LK_Ray80row = rdnumpy(file7)
W1LK_80row = rdnumpy(file8)

# ============== Quarter Node ==================
# ------------ 10,1 m Tie Boundary------------------
W10Tie_Ray80row_QUA = rdnumpy(file9)
W10Tie_80row_QUA = rdnumpy(file10)
W1Tie_Ray80row_QUA = rdnumpy(file11)
W1Tie_80row_QUA = rdnumpy(file12)

# ------------ 10,1 m LK Dashpot------------------
W10LK_Ray80row_QUA = rdnumpy(file13)
W10LK_80row_QUA = rdnumpy(file14)
W1LK_Ray80row_QUA = rdnumpy(file15)
W1LK_80row_QUA = rdnumpy(file16)

def timesTime(Width20_Mid80row,Width20_Mid40row,Width20_Mid20row,Width20_Mid10row):
    column_to_multiply = 0
    Width20_Mid80row[:, column_to_multiply] *= 10
    Width20_Mid40row[:, column_to_multiply] *= 10
    Width20_Mid20row[:, column_to_multiply] *= 10
    Width20_Mid10row[:, column_to_multiply] *= 10

timesTime(W10Tie_Ray80row,W10Tie_80row,W1Tie_Ray80row,W1Tie_80row)
timesTime(W10LK_Ray80row,W10LK_80row,W1LK_Ray80row,W1LK_80row)
timesTime(W10Tie_Ray80row_QUA,W10Tie_80row_QUA,W1Tie_Ray80row_QUA,W1Tie_80row_QUA)
timesTime(W10LK_Ray80row_QUA,W10LK_80row_QUA,W1LK_Ray80row_QUA,W1LK_80row_QUA)

plt_axis2 = 2
def Differ_SoilWidthVel(titlelabel, W10Tie_Ray80row, W10Tie_80row, label1, label2):
    font_props = {'family': 'Arial', 'size': 20}
    plt.figure(figsize=(8,6))
    plt.title(titlelabel,fontsize = 20)
    plt.plot(W10Tie_80row[:,0],W10Tie_80row[:,plt_axis2],label = label2,color= 'limegreen', ls = '-.',linewidth=3.0)
    plt.plot(W10Tie_Ray80row[:,0],W10Tie_Ray80row[:,plt_axis2],label = label1,color= 'darkorange', ls = '--',linewidth=5.0)
    
   
    plt.ylabel(r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$",fontsize=18)
    plt.xlabel(r"$\mathrm {time}$ ${t}$  $(10^{-1}\,s)$",fontsize=18)
    
    plt.legend(loc='upper right',prop=font_props) #ncol=2,fontsize=16
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    
    # plt.xlim(0.0, 0.20)  # original x axis (totalTime = 0~0.4 s)
    plt.xlim(0.0, 2.0) # **** 10 Times the x axis ******   (totalTime = 0~ 4 s)
    plt.grid(True) 

# ================== Middle Node ============================
x_axis = 0.267 # 0.1 0.05 **** 10 Times the x axis ******
# ================== Tie Boundary ===============================
Differ_SoilWidthVel('W= 10m Rayleigh Dashpot(Tie Boundary)\n (Middle Node)', W10Tie_Ray80row, W10Tie_80row,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
ax1 = plt.gca()
ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax1.yaxis.get_offset_text().set(size=18)

Differ_SoilWidthVel('W= 1m Rayleigh Dashpot(Tie Boundary)', W1Tie_Ray80row, W1Tie_80row,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
ax2 = plt.gca()
ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax2.yaxis.get_offset_text().set(size=18)

# ================== LK Dashpot Boundary ===============================
Differ_SoilWidthVel('W= 10m Rayleigh Dashpot(LK Dashpot)\n (Middle Node)', W10LK_Ray80row, W10LK_80row,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
ax1 = plt.gca()
ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax1.yaxis.get_offset_text().set(size=18)

Differ_SoilWidthVel('W= 1m Rayleigh Dashpot(LK Dashpot)', W1LK_Ray80row, W1LK_80row,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
ax2 = plt.gca()
ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax2.yaxis.get_offset_text().set(size=18)

# ================== Quarter Node ============================
# ================== Tie Boundary ===============================
Differ_SoilWidthVel('W= 10m Rayleigh Dashpot(Tie Boundary)\n (Quarter Node)', W10Tie_Ray80row_QUA, W10Tie_80row_QUA,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
ax1 = plt.gca()
ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax1.yaxis.get_offset_text().set(size=18)

Differ_SoilWidthVel('W= 1m Rayleigh Dashpot(Tie Boundary)\n (Quarter Node)', W1Tie_Ray80row_QUA, W1Tie_80row_QUA,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
ax2 = plt.gca()
ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax2.yaxis.get_offset_text().set(size=18)

# ================== LK Dashpot Boundary ===============================
Differ_SoilWidthVel('W= 10m Rayleigh Dashpot(LK Dashpot)\n (Quarter Node)', W10LK_Ray80row_QUA, W10LK_80row_QUA,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
ax1 = plt.gca()
ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax1.yaxis.get_offset_text().set(size=18)

Differ_SoilWidthVel('W= 1m Rayleigh Dashpot(LK Dashpot)\n (Quarter Node)', W1LK_Ray80row_QUA, W1LK_80row_QUA,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
ax2 = plt.gca()
ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax2.yaxis.get_offset_text().set(size=18)
