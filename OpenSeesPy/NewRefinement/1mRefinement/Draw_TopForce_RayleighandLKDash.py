# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 17:16:40 2023

@author: User
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

# #----------------------------- One column file (Global Coordinate)-----------------------------------
Condition = f'Column_Quad/Pwave/1mWidth/TopForce_SideRayleigh' # 0.0001Scale
# ========== Left Column ===================
# ======= Stress =================
file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Stress/ele1.out"  #{Condition}/
file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Stress/ele321.out"
file3 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Stress/ele633.out"
# ---------- Velocity --------
file4 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Velocity/node1.out"
file5 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Velocity/node361.out"
file6 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Velocity/node721.out"

# ========== Center Column ===================
file7 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Stress/ele5.out"
file8 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Stress/ele325.out"
file9 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Stress/ele637.out"
# ---------- Velocity --------
file10 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Velocity/node5.out"
file11 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Velocity/node365.out"
file12 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Velocity/node725.out"

# ========== Right Column ===================
file13 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Stress/ele8.out"
file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Stress/ele328.out"
file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Stress/ele640.out"
# ---------- Velocity --------
file16 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Velocity/node9.out"
file17 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Velocity/node369.out"
file18 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Velocity/node729.out"

file37 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition}/Velocity/node727.out"
#----------------------------- 1m Width column file ((Global Coordinate)) ----------------------------------
# ========== Left Column ===================-
ele1 = rdnumpy(file1)
ele321 = rdnumpy(file2)
ele633 = rdnumpy(file3)

vel1 = rdnumpy(file4)
vel361 = rdnumpy(file5)
vel721 = rdnumpy(file6)

# ========== Center Column ===================-
ele5 = rdnumpy(file7)
ele325 = rdnumpy(file8)
ele637 = rdnumpy(file9)

vel5 = rdnumpy(file10)
vel365 = rdnumpy(file11)
vel725 = rdnumpy(file12)

# ========== Right Column ===================-
ele8 = rdnumpy(file13)
ele328 = rdnumpy(file14)
ele640 = rdnumpy(file15)

vel9 = rdnumpy(file16)
vel369 = rdnumpy(file17)
vel729 = rdnumpy(file18)

# ========== Left Column ===================
Condition2 = f'Column_Quad/Pwave/1mWidth/TopForce_LKDash' 
# ======= Stress =================
file19 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Stress/ele1.out"  #{Condition}/
file20 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Stress/ele321.out"
file21 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Stress/ele633.out"
# ---------- Velocity --------
file22 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Velocity/node1.out"
file23 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Velocity/node361.out"
file24 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Velocity/node721.out"

# ========== Center Column ===================
file25 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Stress/ele5.out"
file26 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Stress/ele325.out"
file27 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Stress/ele637.out"
# ---------- Velocity --------
file28 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Velocity/node5.out"
file29 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Velocity/node365.out"
file30 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Velocity/node725.out"

# ========== Right Column ===================
file31 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Stress/ele8.out"
file32 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Stress/ele328.out"
file33 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Stress/ele640.out"
# ---------- Velocity --------
file34 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Velocity/node9.out"
file35 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Velocity/node369.out"
file36 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Velocity/node729.out"

file38 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/Velocity/node727.out"
#----------------------------- 1m Width column file (LK_Dashpot) ----------------------------------
# ========== Left Column ===================-
LK_ele1 = rdnumpy(file19)
LK_ele321 = rdnumpy(file20)
LK_ele633 = rdnumpy(file21)

LK_vel1 = rdnumpy(file22)
LK_vel361 = rdnumpy(file23)
LK_vel721 = rdnumpy(file24)

# ========== Center Column ===================-
LK_ele5 = rdnumpy(file25)
LK_ele325 = rdnumpy(file26)
LK_ele637 = rdnumpy(file27)

LK_vel5 = rdnumpy(file28)
LK_vel365 = rdnumpy(file29)
LK_vel725 = rdnumpy(file30)

# ========== Right Column ===================-
LK_ele8 = rdnumpy(file31)
LK_ele328 = rdnumpy(file32)
LK_ele640 = rdnumpy(file33)

LK_vel9 = rdnumpy(file34)
LK_vel369 = rdnumpy(file35)
LK_vel729 = rdnumpy(file36)

# -------------Quater Node ---------------
vel727 = rdnumpy(file37)
LK_vel727 = rdnumpy(file38)

# plt_axis1 = 2
# x_axis = 0.5
Extend_scale = 1 #100
def draw_stress(title_name,ele1,ele2,ele3, label1,label2,label3, LK1, LK2, LK3): #, LK1, LK2, LK3
    plt.figure(figsize=(10,8))
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 20)
    plt.xlabel(r"$\mathrm {time}$ ${t}$ $\mathrm {(s)}$",fontsize=18)
    plt.ylabel(r'Stress $(N/m^2)$', fontsize = 18)

    plt.plot(LK1[:,0], LK1[:,plt_axis1], label=  r"Bot LK Dashpot", color= 'aqua',linewidth=6.0) #"Bot LK Dashpot" / r"$\mathrm {Bot}$ $(1/10000)$G"
    plt.plot(LK2[:,0], LK2[:,plt_axis1], label=  r"Cen LK Dashpot", color= 'lime',linewidth=5.0) #'Cen LK Dashpot'/ r"$\mathrm {Cen}$ $(1/10000)$G"
    plt.plot(LK3[:,0], LK3[:,plt_axis1], label=  r"Top LK Dashpot", color= 'bisque',linewidth=4.0) # 'Top LK Dashpot' / r"$\mathrm {Top}$ $(1/10000)$G"
    
    plt.plot(ele1[:,0], ele1[:,plt_axis1], label= label1, ls= "--" , color= 'darkorange',linewidth=4.0) # , ls= "--"
    plt.plot(ele2[:,0], ele2[:,plt_axis1], label= label2, ls = '-.' , color= 'red',linewidth=3.0)
    plt.plot(ele3[:,0], ele3[:,plt_axis1], label= label3, ls= ":" , color= 'blue',linewidth=2.0)
    
    plt.legend(loc='upper right',fontsize=18)
    plt.xlim(0,0.2*Extend_scale)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)   

# plt_axis2 = 2
def draw_Vel(title_name,vel1,vel2,vel3, label1,label2,label3, LK1, LK2, LK3): #, LK1, LK2, LK3
    plt.figure(figsize=(10,8))
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 20)
    plt.xlabel(r"$\mathrm {time}$ ${t}$ $\mathrm {(s)}$ ",fontsize=18)
    plt.ylabel(r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$", fontsize = 18)
    
    plt.plot(LK1[:,0], LK1[:,plt_axis2], label= r"Bot LK Dashpot", color= 'aqua',linewidth=6.0) #Bot LK Dashpot / r"$\mathrm {Bot}$ $(1/10000)$G"
    plt.plot(LK2[:,0], LK2[:,plt_axis2], label= r"Cen LK Dashpot", color= 'lime',linewidth=5.0) #Cen LK Dashpot / r"$\mathrm {Cen}$ $(1/10000)$G"
    plt.plot(LK3[:,0], LK3[:,plt_axis2], label= r"Top LK Dashpot", color= 'bisque',linewidth=4.0) #Top LK Dashpot / r"$\mathrm {Top}$ $(1/10000)$G"
    
    plt.plot(vel1[:,0], vel1[:,plt_axis2], label= label1, ls= "--" , color= 'darkorange',linewidth=4.0) #, ls= "--"
    plt.plot(vel2[:,0], vel2[:,plt_axis2], label= label2, ls = '-.' , color= 'red',linewidth=3.0)
    plt.plot(vel3[:,0], vel3[:,plt_axis2], label= label3, ls= ":"  , color= 'blue',linewidth=2.0)
       
    plt.legend(loc='upper right',fontsize=18)
    plt.xlim(0,0.2*Extend_scale) #0.4
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)   

plt_axis1 = 2  # Stress yaxis   3(Global) / 3 (Local)
plt_axis2 = 2  # Velocity yaxis 1(Global) / 2 (Local)

plt_axis3 = 1  # Structure Stress
plt_axis4 = 1  # Structure Vel
# # # # ============== Left/Right/Center Stress ======================= # r"$\mathrm {Bot}$ $(1/100)$G", r"$\mathrm {Cen}$ $(1/100)$G",r"$\mathrm {Top}$ $(1/100)$G" 
x_axis = 0.0267*Extend_scale #0.0267 / 0.025
# draw_stress("Left Element Stress",ele1,ele321,ele633,"Bot Element","Center Element","Top Element", LK_ele1, LK_ele321, LK_ele633) #"Bot Element","Center Element","Top Element"
# ax1 = plt.gca()
# ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# # ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
# ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax1.yaxis.get_offset_text().set(size=18)

# draw_stress("Center Element Stress",ele5,ele325,ele637,"Bot Element","Center Element","Top Element", LK_ele5, LK_ele325, LK_ele637) #"Bot Element","Center Element","Top Element"
# ax2 = plt.gca()
# ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# # ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))
# ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax2.yaxis.get_offset_text().set(size=18)

# draw_stress("Right Element Stress",ele8,ele328,ele640,"Bot Element","Center Element","Top Element", LK_ele8, LK_ele328, LK_ele640) #"Bot Element","Center Element","Top Element"
# ax3 = plt.gca()
# ax3.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# # ax3.yaxis.set_major_locator(ticker.MultipleLocator(1))
# ax3.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax3.yaxis.get_offset_text().set(size=18)

# x_axis =  0.05#0.0267
# # ============== Left/Right/Center Velocity ======================= r"$\mathrm {Bot}$ $(1/100)$G", r"$\mathrm {Cen}$ $(1/100)$G",r"$\mathrm {Top}$ $(1/100)$G"
# draw_Vel("Left side Velocity",vel1,vel361,vel721,"Bot velocity","Center velocity","Top velocity", LK_vel1, LK_vel361, LK_vel721) #"Bot velocity","Center velocity","Top velocity"
# ax4 = plt.gca()
# ax4.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax4.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax4.yaxis.get_offset_text().set(size=18)

# draw_Vel("Center side Velocity",vel5,vel365,vel725,"Bot velocity","Center velocity","Top velocity", LK_vel5, LK_vel365, LK_vel725) #"Bot velocity","Center velocity","Top velocity"
# ax5 = plt.gca()
# ax5.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax5.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax5.yaxis.get_offset_text().set(size=18)

# draw_Vel("Right side Velocity",vel9,vel369,vel729,"Bot velocity","Center velocity","Top velocity", LK_vel9, LK_vel369, LK_vel729) #"Bot velocity","Center velocity","Top velocity"
# ax6 = plt.gca()
# ax6.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax6.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax6.yaxis.get_offset_text().set(size=18)

# ------------- Draw Compare Quarter node -------------------
# plt.figure(figsize=(10,8))
# plt.rcParams["figure.figsize"] = (12, 8)
# plt.title("Compare Quarter Node with LK Dashpot", fontsize = 20)
# plt.xlabel(r"$\mathrm {time}$ ${t}$ $\mathrm {(s)}$ ",fontsize=18)
# plt.ylabel(r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", fontsize = 18)

# plt.plot(LK_vel727[:,0], LK_vel727[:,plt_axis2], label= r"LK Dashpot", color= 'bisque',linewidth=5.0) #Top LK Dashpot / r"$\mathrm {Top}$ $(1/10000)$G"

# plt.plot(vel727[:,0], vel727[:,plt_axis2], label= r"Rayleigh Damping", ls= ":"  , color= 'blue',linewidth=3.0)
   
# plt.legend(loc='upper right',fontsize=18)
# plt.xlim(0,0.2*Extend_scale) #0.4
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid(True)   

# ax7 = plt.gca()
# ax7.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax7.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax7.yaxis.get_offset_text().set(size=18)

def Combine_stress(ele1,ele2,ele3, LK1, LK2, LK3): #, LK1, LK2, LK3
    plt.rcParams["figure.figsize"] = (12, 8)

    plt.plot(LK1[:,0], LK1[:,plt_axis1], label=  r"Bot LK Dashpot", color= 'aqua',linewidth=6.0) #"Bot LK Dashpot" / r"$\mathrm {Bot}$ $(1/10000)$G"
    plt.plot(LK2[:,0], LK2[:,plt_axis1], label=  r"Cen LK Dashpot", color= 'lime',linewidth=5.0) #'Cen LK Dashpot'/ r"$\mathrm {Cen}$ $(1/10000)$G"
    plt.plot(LK3[:,0], LK3[:,plt_axis1], label=  r"Top LK Dashpot", color= 'bisque',linewidth=4.0) # 'Top LK Dashpot' / r"$\mathrm {Top}$ $(1/10000)$G"
    
    plt.plot(ele1[:,0], ele1[:,plt_axis1], label= f"Bot Element", ls= "--" , color= 'darkorange',linewidth=4.0) # , ls= "--"
    plt.plot(ele2[:,0], ele2[:,plt_axis1], label= f"Center Element", ls = '-.' , color= 'red',linewidth=3.0)
    plt.plot(ele3[:,0], ele3[:,plt_axis1], label= f"Top Element", ls= ":" , color= 'blue',linewidth=2.0)
    
    plt.xlim(0,0.2*Extend_scale)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)   

# plt_axis2 = 2
def Combine_Vel(vel1,vel2,vel3, LK1, LK2, LK3): #, LK1, LK2, LK3
    plt.rcParams["figure.figsize"] = (12, 8)
    
    plt.plot(LK1[:,0], LK1[:,plt_axis2], label= r"Bot LK Dashpot", color= 'aqua',linewidth=6.0) #Bot LK Dashpot / r"$\mathrm {Bot}$ $(1/10000)$G"
    plt.plot(LK2[:,0], LK2[:,plt_axis2], label= r"Cen LK Dashpot", color= 'lime',linewidth=5.0) #Cen LK Dashpot / r"$\mathrm {Cen}$ $(1/10000)$G"
    plt.plot(LK3[:,0], LK3[:,plt_axis2], label= r"Top LK Dashpot", color= 'bisque',linewidth=4.0) #Top LK Dashpot / r"$\mathrm {Top}$ $(1/10000)$G"
    
    plt.plot(vel1[:,0], vel1[:,plt_axis2], label= f"Bot Node", ls= "--" , color= 'darkorange',linewidth=4.0) #, ls= "--"
    plt.plot(vel2[:,0], vel2[:,plt_axis2], label= f"Center Node", ls = '-.' , color= 'red',linewidth=3.0)
    plt.plot(vel3[:,0], vel3[:,plt_axis2], label= f"Top Node", ls= ":"  , color= 'blue',linewidth=2.0)
       
    plt.xlim(0,0.2*Extend_scale) #0.4
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)   


# # ---------- Combine 3 figure into a column ---------------------
# row_heights = [3,3,3]
# fig1, (ax1,ax2,ax3) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# fig1.suptitle(f'Rayleigh Damping Compare with LK Dashpot',x=0.50,y =0.95,fontsize = 20)
# fig1.text(0.22,0.89, f"Constant TimeSeries in P Wave Direction", color = "red", fontsize=20) 
# fig1.text(0.015,0.5, r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=22)
# fig1.text(0.45,0.05, r"$\mathrm {time}$ ${t}$ $\mathrm {(s)}$ ", va= 'center', fontsize=20)

# ax1 = plt.subplot(311)
# Combine_Vel(vel1,vel361,vel721, LK_vel1, LK_vel361, LK_vel721)
# ax1.set_title("Left Column" ,fontsize =23, x=0.70, y=0.75)
 
# ax2 = plt.subplot(312)
# Combine_Vel(vel5,vel365,vel725, LK_vel5, LK_vel365, LK_vel725)
# ax2.set_title("Center Column",fontsize =23, x=0.58, y=0.80)

# ax3 = plt.subplot(313)
# Combine_Vel(vel9,vel369,vel729, LK_vel9, LK_vel369, LK_vel729)
# ax3.set_title("Right Column",fontsize =23, x=0.70, y=0.75)

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig1.axes[-1].get_legend_handles_labels()
# fig1.legend(lines, labels, loc = (0.7, 0.53),prop=font_props) # 'center right'

# for ax in [ax1,ax2,ax3]:
#     formatter = ticker.ScalarFormatter(useMathText =True)
#     formatter.set_scientific(True)
#     formatter.set_powerlimits((0,0))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
#     ax.yaxis.set_major_formatter(formatter)
#     # ax.xaxis.set_major_formatter(formatter)
#     ax.yaxis.get_offset_text().set(size=18)
#     # ax.xaxis.get_offset_text().set(size=18)
    
# row_heights = [3,3,3]
# fig2, (ax4,ax5,ax6) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# fig2.suptitle(f'Rayleigh Damping Compare with LK Dashpot',x=0.50,y =0.95,fontsize = 20)
# fig2.text(0.22,0.89, f"Constant TimeSeries in P Wave Direction", color = "red", fontsize=20) 
# fig2.text(0.015,0.5, r'Stress $(N/m^2)$', va= 'center', rotation= 'vertical', fontsize=22)
# fig2.text(0.45,0.05, r"$\mathrm {time}$ ${t}$ $\mathrm {(s)}$ ", va= 'center', fontsize=20)

# ax4 = plt.subplot(311)
# Combine_stress(ele1,ele321,ele633, LK_ele1, LK_ele321, LK_ele633)
# ax4.set_title("Left Column" ,fontsize =23, x=0.56, y=0.15)
 
# ax5 = plt.subplot(312)
# Combine_stress(ele5,ele325,ele637, LK_ele5, LK_ele325, LK_ele637)
# ax5.set_title("Center Column",fontsize =23, x=0.58, y=0.15)

# ax6 = plt.subplot(313)
# Combine_stress(ele8,ele328,ele640, LK_ele8, LK_ele328, LK_ele640)
# ax6.set_title("Right Column",fontsize =23, x=0.56, y=0.15)

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig2.axes[-1].get_legend_handles_labels()
# fig2.legend(lines, labels, loc = (0.7, 0.53),prop=font_props) # 'center right'

# for ax in [ax4,ax5,ax6]:
#     formatter = ticker.ScalarFormatter(useMathText =True)
#     formatter.set_scientific(True)
#     formatter.set_powerlimits((0,0))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
#     ax.yaxis.set_major_formatter(formatter)
#     # ax.xaxis.set_major_formatter(formatter)
#     ax.yaxis.get_offset_text().set(size=18)
#     # ax.xaxis.get_offset_text().set(size=18)
