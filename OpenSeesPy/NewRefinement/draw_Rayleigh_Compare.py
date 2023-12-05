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

# # =================== Middle Node ============================ 
# # ------------ 10,1 m Tie Boundary------------------
# file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopTie_Rayleigh_80row/node6521.out"
# file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopForce_80row/node6521.out"
# file3 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopTie_Rayleigh_80row/node725.out"
# file4 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopForce_80row/node725.out"

# # ---------10,1 m LK Dashpot ---------------
# file5 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopLK_Rayleigh_80row/node6521.out"
# file6 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideDash_80row/node6521.out"
# file7 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopLK_Rayleigh_80row/node725.out"
# file8 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideDash_80row/node725.out"

# # =================== Quarter Node ============================ 
# # ------------ 10,1 m Tie Boundary------------------
# file9 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopTie_Rayleigh_80row/node6541.out"
# file10 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopForce_80row/node6541.out"
# file11 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopTie_Rayleigh_80row/node727.out"
# file12 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopForce_80row/node727.out"

# # # ---------10, 1 m LK Dashpot ---------------
# file13 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopLK_Rayleigh_80row/node6541.out"
# file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideDash_80row/node6541.out"
# file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopLK_Rayleigh_80row/node727.out"
# file16 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideDash_80row/node727.out"

# # ============== Middle Node ==================
# # ------------ 10,1 m Tie Boundary------------------
# W10Tie_Ray80row = rdnumpy(file1)
# W10Tie_80row = rdnumpy(file2)
# W1Tie_Ray80row = rdnumpy(file3)
# W1Tie_80row = rdnumpy(file4)

# # ------------ 10,1 m LK Dashpot------------------
# W10LK_Ray80row = rdnumpy(file5)
# W10LK_80row = rdnumpy(file6)
# W1LK_Ray80row = rdnumpy(file7)
# W1LK_80row = rdnumpy(file8)

# # ============== Quarter Node ==================
# # ------------ 10,1 m Tie Boundary------------------
# W10Tie_Ray80row_QUA = rdnumpy(file9)
# W10Tie_80row_QUA = rdnumpy(file10)
# W1Tie_Ray80row_QUA = rdnumpy(file11)
# W1Tie_80row_QUA = rdnumpy(file12)

# # ------------ 10,1 m LK Dashpot------------------
# W10LK_Ray80row_QUA = rdnumpy(file13)
# W10LK_80row_QUA = rdnumpy(file14)
# W1LK_Ray80row_QUA = rdnumpy(file15)
# W1LK_80row_QUA = rdnumpy(file16)

def timesTime(Width20_Mid80row,Width20_Mid40row,Width20_Mid20row,Width20_Mid10row):
    column_to_multiply = 0
    Width20_Mid80row[:, column_to_multiply] *= 10
    Width20_Mid40row[:, column_to_multiply] *= 10
    Width20_Mid20row[:, column_to_multiply] *= 10
    Width20_Mid10row[:, column_to_multiply] *= 10

# timesTime(W10Tie_Ray80row,W10Tie_80row,W1Tie_Ray80row,W1Tie_80row)
# timesTime(W10LK_Ray80row,W10LK_80row,W1LK_Ray80row,W1LK_80row)
# timesTime(W10Tie_Ray80row_QUA,W10Tie_80row_QUA,W1Tie_Ray80row_QUA,W1Tie_80row_QUA)
# timesTime(W10LK_Ray80row_QUA,W10LK_80row_QUA,W1LK_Ray80row_QUA,W1LK_80row_QUA)

# plt_axis2 = 2
# def Differ_SoilWidthVel(titlelabel, W10Tie_Ray80row, W10Tie_80row, label1, label2):
#     font_props = {'family': 'Arial', 'size': 20}
#     plt.figure(figsize=(8,6))
#     plt.title(titlelabel,fontsize = 20)
#     plt.plot(W10Tie_80row[:,0],W10Tie_80row[:,plt_axis2],label = label2,color= 'limegreen', ls = '-.',linewidth=3.0)
#     plt.plot(W10Tie_Ray80row[:,0],W10Tie_Ray80row[:,plt_axis2],label = label1,color= 'darkorange', ls = '--',linewidth=5.0)
    
   
#     plt.ylabel(r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$",fontsize=18)
#     plt.xlabel(r"$\mathrm {time}$ ${t}$  $(10^{-1}\,s)$",fontsize=18)
    
#     plt.legend(loc='upper right',prop=font_props) #ncol=2,fontsize=16
#     plt.xticks(fontsize = 16)
#     plt.yticks(fontsize = 16)
    
#     # plt.xlim(0.0, 0.20)  # original x axis (totalTime = 0~0.4 s)
#     plt.xlim(0.0, 2.0) # **** 10 Times the x axis ******   (totalTime = 0~ 4 s)
#     plt.grid(True) 

# # ================== Middle Node ============================
# x_axis = 0.267 # 0.1 0.05 **** 10 Times the x axis ******
# # ================== Tie Boundary ===============================
# Differ_SoilWidthVel('W= 10m Rayleigh Dashpot(Tie Boundary)\n (Middle Node)', W10Tie_Ray80row, W10Tie_80row,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
# ax1 = plt.gca()
# ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax1.yaxis.get_offset_text().set(size=18)

# Differ_SoilWidthVel('W= 1m Rayleigh Dashpot(Tie Boundary)', W1Tie_Ray80row, W1Tie_80row,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
# ax2 = plt.gca()
# ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax2.yaxis.get_offset_text().set(size=18)

# # ================== LK Dashpot Boundary ===============================
# Differ_SoilWidthVel('W= 10m Rayleigh Dashpot(LK Dashpot)\n (Middle Node)', W10LK_Ray80row, W10LK_80row,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
# ax1 = plt.gca()
# ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax1.yaxis.get_offset_text().set(size=18)

# Differ_SoilWidthVel('W= 1m Rayleigh Dashpot(LK Dashpot)', W1LK_Ray80row, W1LK_80row,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
# ax2 = plt.gca()
# ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax2.yaxis.get_offset_text().set(size=18)

# # ================== Quarter Node ============================
# # ================== Tie Boundary ===============================
# Differ_SoilWidthVel('W= 10m Rayleigh Dashpot(Tie Boundary)\n (Quarter Node)', W10Tie_Ray80row_QUA, W10Tie_80row_QUA,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
# ax1 = plt.gca()
# ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax1.yaxis.get_offset_text().set(size=18)

# Differ_SoilWidthVel('W= 1m Rayleigh Dashpot(Tie Boundary)\n (Quarter Node)', W1Tie_Ray80row_QUA, W1Tie_80row_QUA,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
# ax2 = plt.gca()
# ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax2.yaxis.get_offset_text().set(size=18)

# # ================== LK Dashpot Boundary ===============================
# Differ_SoilWidthVel('W= 10m Rayleigh Dashpot(LK Dashpot)\n (Quarter Node)', W10LK_Ray80row_QUA, W10LK_80row_QUA,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
# ax1 = plt.gca()
# ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax1.yaxis.get_offset_text().set(size=18)

# Differ_SoilWidthVel('W= 1m Rayleigh Dashpot(LK Dashpot)\n (Quarter Node)', W1LK_Ray80row_QUA, W1LK_80row_QUA,'with Rayleigh Dashpot', 'No Rayleigh Dashpot')
# ax2 = plt.gca()
# ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax2.yaxis.get_offset_text().set(size=18)

# ========================== Compare Diggerent Rayleigh Dashpot (Middle / Quarter Node)=======================================#
file1 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{0.2}_Cb{0.2}/SurfaceVelocity/W5.0node6521.out'
file2 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{0.2}_Cb{0.2}/SurfaceVelocity/W7.5node6541.out'

file3 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{0.4}_Cb{0.4}/SurfaceVelocity/W5.0node6521.out'
file4 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{0.4}_Cb{0.4}/SurfaceVelocity/W7.5node6541.out'

file5 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{0.4}_Cb{0.6}/SurfaceVelocity/W5.0node6521.out'
file6 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{0.4}_Cb{0.6}/SurfaceVelocity/W7.5node6541.out'

file7 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{0.6}_Cb{0.4}/SurfaceVelocity/W5.0node6521.out'
file8 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{0.6}_Cb{0.4}/SurfaceVelocity/W7.5node6541.out'

file9 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{0.8}_Cb{0.2}/SurfaceVelocity/W5.0node6521.out'
file10 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{0.8}_Cb{0.2}/SurfaceVelocity/W7.5node6541.out'

file11 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{0.8}_Cb{0.4}/SurfaceVelocity/W5.0node6521.out'
file12 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{0.8}_Cb{0.4}/SurfaceVelocity/W7.5node6541.out'

file13 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{0.8}_Cb{1.2}/SurfaceVelocity/W5.0node6521.out'
file14 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{0.8}_Cb{1.2}/SurfaceVelocity/W7.5node6541.out'

file15 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{1.0}_Cb{0.4}/SurfaceVelocity/W5.0node6521.out'
file16 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{1.0}_Cb{0.4}/SurfaceVelocity/W7.5node6541.out'

file17 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{1.2}_Cb{0.4}/SurfaceVelocity/W5.0node6521.out'
file18 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{1.2}_Cb{0.4}/SurfaceVelocity/W7.5node6541.out'

file19 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{1.6}_Cb{0.4}/SurfaceVelocity/W5.0node6521.out'
file20 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{1.6}_Cb{0.4}/SurfaceVelocity/W7.5node6541.out'

file21 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{2.0}_Cb{0.2}/SurfaceVelocity/W5.0node6521.out'
file22 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{2.0}_Cb{0.2}/SurfaceVelocity/W7.5node6541.out'

file23 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{2.0}_Cb{0.4}/SurfaceVelocity/W5.0node6521.out'
file24 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{2.0}_Cb{0.4}/SurfaceVelocity/W7.5node6541.out'

file25 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{2.0}_Cb{1.2}/SurfaceVelocity/W5.0node6521.out'
file26 = f'E:/unAnalysisFile/RayleighDashpot/Tie/Ca{2.0}_Cb{1.2}/SurfaceVelocity/W7.5node6541.out'

# ------------- Original Tie Boundary without Rayleigh Dashpot ------------------
file27 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopForce_80row/node6521.out"
file28 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopForce_80row/node6541.out"
# ================= Middle Node ==============================
Ca2Cb2Mid = rdnumpy(file1)
Ca4Cb4Mid = rdnumpy(file3)
Ca4Cb6Mid = rdnumpy(file5)
Ca6Cb4Mid = rdnumpy(file7)

Ca8Cb2Mid = rdnumpy(file9)
Ca8Cb4Mid = rdnumpy(file11)
Ca8Cb12Mid = rdnumpy(file13)
Ca10Cb4Mid = rdnumpy(file15)

Ca12Cb4Mid = rdnumpy(file17)
Ca16Cb4Mid = rdnumpy(file19)
Ca20Cb2Mid = rdnumpy(file21)
Ca20Cb4Mid = rdnumpy(file23)

Ca20Cb12Mid = rdnumpy(file25)

timesTime(Ca2Cb2Mid,Ca4Cb4Mid,Ca4Cb6Mid,Ca6Cb4Mid)
timesTime(Ca8Cb2Mid,Ca8Cb4Mid,Ca8Cb12Mid,Ca10Cb4Mid)
timesTime(Ca12Cb4Mid,Ca16Cb4Mid,Ca20Cb2Mid,Ca20Cb4Mid)
Ca20Cb12Mid[:, 0] *= 10
# ================= Quarter Node ==============================
Ca2Cb2Qua = rdnumpy(file2)
Ca4Cb4Qua = rdnumpy(file4)
Ca4Cb6Qua = rdnumpy(file6)
Ca6Cb4Qua = rdnumpy(file8)

Ca8Cb2Qua = rdnumpy(file10)
Ca8Cb4Qua = rdnumpy(file12)
Ca8Cb12Qua = rdnumpy(file14)
Ca10Cb4Qua = rdnumpy(file16)

Ca12Cb4Qua = rdnumpy(file18)
Ca16Cb4Qua = rdnumpy(file20)
Ca20Cb2Qua = rdnumpy(file22)
Ca20Cb4Qua = rdnumpy(file24)

Ca20Cb12Qua = rdnumpy(file26)

timesTime(Ca2Cb2Qua,Ca4Cb4Qua,Ca4Cb6Qua,Ca6Cb4Qua)
timesTime(Ca8Cb2Qua,Ca8Cb4Qua,Ca8Cb12Qua,Ca10Cb4Qua)
timesTime(Ca12Cb4Qua,Ca16Cb4Qua,Ca20Cb2Qua,Ca20Cb4Qua)
Ca20Cb12Qua[:, 0] *= 10
# ------------- Original Tie Boundary without Rayleigh Dashpot ------------------
W10Tie_80row = rdnumpy(file27)
W10Tie_80rowQua = rdnumpy(file28)

W10Tie_80row[:, 0] *= 10
W10Tie_80rowQua[:, 0] *= 10

plt_axis2 = 2
def Differ_Dashpot(titlelabel,W10Tie_80row, Ca2Cb2Mid, Ca4Cb4Mid, Ca4Cb6Mid, Ca6Cb4Mid, label1, label2, label3, label4):
    font_props = {'family': 'Arial', 'size': 18}
    plt.figure(figsize=(8,6))
    plt.title(titlelabel,fontsize = 20)
    plt.plot(W10Tie_80row[:,0],W10Tie_80row[:,plt_axis2],label = 'No Rayleigh',color= 'black',linewidth=6.0)
    plt.plot(Ca2Cb2Mid[:,0],Ca2Cb2Mid[:,plt_axis2],label = label1,color= 'limegreen', ls = '--',linewidth=6.0)
    plt.plot(Ca4Cb4Mid[:,0],Ca4Cb4Mid[:,plt_axis2],label = label2,color= 'darkorange', ls = '-.',linewidth=5.0)
    plt.plot(Ca4Cb6Mid[:,0],Ca4Cb6Mid[:,plt_axis2],label = label3,color= 'blue', ls = ':',linewidth=4.0)
    plt.plot(Ca6Cb4Mid[:,0],Ca6Cb4Mid[:,plt_axis2],label = label4,color= 'red', ls = '-',linewidth=2.0)
   
    plt.ylabel(r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$",fontsize=18)
    plt.xlabel(r"$\mathrm {time}$ ${t}$  $(10^{-1}\,s)$",fontsize=18)
    
    plt.legend(loc='upper right',prop=font_props) #ncol=2,fontsize=16
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    
    # plt.xlim(0.0, 0.20)  # original x axis (totalTime = 0~0.4 s)
    plt.xlim(0.0, 2.0) # **** 10 Times the x axis ******   (totalTime = 0~ 4 s)
    plt.grid(True) 
    
def Compare_Dashpot(titlelabel,W10Tie_80row, Ca20Cb12Mid, label1):
    font_props = {'family': 'Arial', 'size': 18}
    plt.figure(figsize=(8,6))
    plt.title(titlelabel,fontsize = 20)
    plt.plot(W10Tie_80row[:,0],W10Tie_80row[:,plt_axis2],label = 'No Rayleigh',color= 'black',linewidth=4.0)
    plt.plot(Ca20Cb12Mid[:,0],Ca20Cb12Mid[:,plt_axis2],label = label1,color= 'darkorange', ls = '-.',linewidth=2.0)

    plt.ylabel(r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$",fontsize=18)
    plt.xlabel(r"$\mathrm {time}$ ${t}$  $(10^{-1}\,s)$",fontsize=18)
    
    plt.legend(loc='upper right',prop=font_props) #ncol=2,fontsize=16
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    
    # plt.xlim(0.0, 0.20)  # original x axis (totalTime = 0~0.4 s)
    plt.xlim(0.0, 2.0) # **** 10 Times the x axis ******   (totalTime = 0~ 4 s)
    plt.grid(True) 
        
x_axis = 0.267
# ================== Middle Node Compare Tie Boundary  =====================================
Differ_Dashpot("Compare Rayleigh Dashpot Cofficient \n (Middle Node)",W10Tie_80row, Ca2Cb2Mid, Ca4Cb4Mid, Ca4Cb6Mid, Ca6Cb4Mid,
               'Ca0.2_Cb0.2','Ca0.4_Cb0.4','Ca0.4_Cb0.6','Ca0.6_Cb0.4')
ax1 = plt.gca()
ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax1.yaxis.get_offset_text().set(size=18)

Differ_Dashpot("Compare Rayleigh Dashpot Cofficient \n (Middle Node)",W10Tie_80row, Ca8Cb2Mid, Ca8Cb4Mid, Ca8Cb12Mid, Ca10Cb4Mid,
               'Ca0.8_Cb0.2','Ca0.8_Cb0.4','Ca0.8_Cb1.2','Ca1.0_Cb0.4')
ax2 = plt.gca()
ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax2.yaxis.get_offset_text().set(size=18)

Differ_Dashpot("Compare Rayleigh Dashpot Cofficient \n (Middle Node)",W10Tie_80row, Ca12Cb4Mid, Ca16Cb4Mid, Ca20Cb2Mid, Ca20Cb4Mid,
               'Ca1.2_Cb0.4','Ca1.6_Cb0.4','Ca2.0_Cb0.2','Ca2.0_Cb0.4')
ax3 = plt.gca()
ax3.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax3.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax3.yaxis.get_offset_text().set(size=18)

Compare_Dashpot("Compare Rayleigh Dashpot Cofficient \n (Middle Node)",W10Tie_80row, Ca20Cb12Mid, 'Ca2.0_Cb1.2')
ax1 = plt.gca()
ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax1.yaxis.get_offset_text().set(size=18)

# ================== Quarter Node Compare Tie Boundary  =====================================
Differ_Dashpot("Compare Rayleigh Dashpot Cofficient \n (Quarter Node)",W10Tie_80rowQua, Ca2Cb2Qua, Ca4Cb4Qua, Ca4Cb6Qua, Ca6Cb4Qua,
               'Ca0.2_Cb0.2','Ca0.4_Cb0.4','Ca0.4_Cb0.6','Ca0.6_Cb0.4')
ax4 = plt.gca()
ax4.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax4.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax4.yaxis.get_offset_text().set(size=18)

Differ_Dashpot("Compare Rayleigh Dashpot Cofficient \n (Quarter Node)",W10Tie_80rowQua, Ca8Cb2Qua, Ca8Cb4Qua, Ca8Cb12Qua, Ca10Cb4Qua,
                'Ca0.8_Cb0.2','Ca0.8_Cb0.4','Ca0.8_Cb1.2','Ca1.0_Cb0.4')
ax5 = plt.gca()
ax5.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax5.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax5.yaxis.get_offset_text().set(size=18)

Differ_Dashpot("Compare Rayleigh Dashpot Cofficient \n (Quarter Node)",W10Tie_80rowQua, Ca12Cb4Qua, Ca16Cb4Qua, Ca20Cb2Qua, Ca20Cb4Qua,
                'Ca1.2_Cb0.4','Ca1.6_Cb0.4','Ca2.0_Cb0.2','Ca2.0_Cb0.4')
ax6 = plt.gca()
ax6.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax6.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax6.yaxis.get_offset_text().set(size=18)

Compare_Dashpot("Differ Rayleigh Dashpot Cofficient \n (Quarter Node)",W10Tie_80rowQua, Ca20Cb12Qua, 'Ca2.0_Cb1.2')
ax6 = plt.gca()
ax6.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax6.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax6.yaxis.get_offset_text().set(size=18)
