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

#----------------------------- Left column file -----------------------------------
file1 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele1.out"
file2 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele141.out"
file3 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele274.out"

file4 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1.out"
file5 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node161.out"
file6 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node321.out"

#----------------------------- Center column file -----------------------------------
file7 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele4.out"
file8 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele144.out"
file9 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele277.out"

file10 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node4.out"
file11 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node164.out"
file12 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node324.out"

#----------------------------- Right column file -----------------------------------
file13 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele7.out"
file14 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele147.out"
file15 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele280.out"

file16 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node8.out"
file17 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node168.out"
file18 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node328.out"


# # ------------node Displacement -------------------
# file19 = r"D:\shiang\opensees\20220330\OpenSeesPy\Disp\node1.out"
# file20 = r"D:\shiang\opensees\20220330\OpenSeesPy\Disp\node8.out"
# file21 = r"D:\shiang\opensees\20220330\OpenSeesPy\Disp\node9.out"
# file22 = r"D:\shiang\opensees\20220330\OpenSeesPy\Disp\node16.out"
#----------------------------- Structure file -----------------------------------
# file19 = r"D:\shiang\opensees\20220330\extend_soil\stress\Column1_stress.out"
# file20 = r"D:\shiang\opensees\20220330\extend_soil\stress\Column2_stress.out"
# file21 = r"D:\shiang\opensees\20220330\extend_soil\stress\Beam_stress.out"

# file22 = r"D:\shiang\opensees\20220330\extend_soil\velocity\node1030_vel.out"
# file23 = r"D:\shiang\opensees\20220330\extend_soil\velocity\node1031_vel.out"
# file24 = r"D:\shiang\opensees\20220330\extend_soil\velocity\node1032_vel.out"
# file25 = r"D:\shiang\opensees\20220330\extend_soil\velocity\node1033_vel.out"

# # ============ Dashpot Node Velocity =====================
# file23 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node951.out"
# file24 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1049.out"
# file25 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1250.out"
#----------------------------- Left column file -----------------------------------
ele1 = rdnumpy(file1)
ele141 = rdnumpy(file2)
ele274 = rdnumpy(file3)

vel1 = rdnumpy(file4)
vel161 = rdnumpy(file5)
vel321 = rdnumpy(file6)

#----------------------------- Center column file -----------------------------------
ele4 = rdnumpy(file7)
ele144 = rdnumpy(file8)
ele277 = rdnumpy(file9)

vel4 = rdnumpy(file10)
vel164 = rdnumpy(file11)
vel324 = rdnumpy(file12)

#----------------------------- Right column file -----------------------------------
ele7 = rdnumpy(file13)
ele147 = rdnumpy(file14)
ele280 = rdnumpy(file15)

vel8 = rdnumpy(file16)
vel168 = rdnumpy(file17)
vel328 = rdnumpy(file18)

# # -------------------- Node Disp ----------------
# disp1 = rdnumpy(file19)
# disp8 = rdnumpy(file20)
# disp9 = rdnumpy(file21)
# disp16 = rdnumpy(file22)
#----------------------------- Structure file -----------------------------------
# col1 = rdnumpy(file19)
# col2 = rdnumpy(file20)
# Beam = rdnumpy(file21)

# vel1030 = rdnumpy(file22)
# vel1031 = rdnumpy(file23)
# vel1032 = rdnumpy(file24)
# vel1033 = rdnumpy(file25)
# Dash951 = rdnumpy(file23)
# Dash1049 = rdnumpy(file24)
# Dash1250 = rdnumpy(file25)

# plt_axis1 = 2
x_axis = 0.5
def draw_stress(title_name,ele1,ele2,ele3,label1,label2,label3):
    plt.figure(figsize=(10,8))
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 18)
    plt.xlabel("time (s)",fontsize=18)
    plt.ylabel(r'Stress $(N/m^2)$', fontsize = 18)
    
    plt.plot(ele1[:,0], ele1[:,plt_axis1], label= label1,marker='o', markevery=100)
    plt.plot(ele2[:,0], ele2[:,plt_axis1], label= label2,marker='x', markevery=100)
    plt.plot(ele3[:,0], ele3[:,plt_axis1], label= label3)
    
    
    plt.legend(loc='upper right',fontsize=18)
    plt.xlim(0,0.8)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)   
    
# plt_axis2 = 2
def draw_Vel(title_name,vel1,vel2,vel3,label1,label2,label3):
    plt.figure(figsize=(10,8))
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 18)
    plt.xlabel("time (s)",fontsize=18)
    plt.ylabel('Velocity (m/s)', fontsize = 18)
    
    plt.plot(vel1[:,0], vel1[:,plt_axis2], label= label1,marker='o', markevery=100)
    plt.plot(vel2[:,0], vel2[:,plt_axis2], label= label2,marker='x', markevery=100)
    plt.plot(vel3[:,0], vel3[:,plt_axis2], label= label3)
    
    
    plt.legend(loc='upper right',fontsize=18)
    plt.xlim(0,0.8)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)   
    
def draw_Disp(title_name,disp1,disp2,disp3,disp4,label1,label2,label3,label4):
    plt.figure()
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 18)
    plt.xlabel("tns",fontsize=18)
    
    plt.plot(disp1[:,0], disp1[:,plt_axis2], label= label1,marker='o', markevery=100)
    plt.plot(disp2[:,0], disp2[:,plt_axis2], label= label2,marker='x', markevery=100)
    plt.plot(disp3[:,0], disp3[:,plt_axis2], label= label3,marker='d', markevery=100)
    plt.plot(disp4[:,0], disp4[:,plt_axis2], label= label4,marker='v', markevery=100)
    
    plt.legend(loc='upper right',fontsize=18)
    plt.xlim(0,0.8)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)   
    
    

def draw_structure_stress(title_name,col1,col2,Beam,label1,label2,label3):
    plt.figure()
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 18)
    plt.xlabel("tns",fontsize=18)
    
    plt.plot(col1[:,0], col1[:,plt_axis3], label= label1,marker='o', markevery=100)
    plt.plot(col2[:,0], col2[:,plt_axis3], label= label2,marker='x', markevery=100)
    plt.plot(Beam[:,0], Beam[:,plt_axis3], label= label3)
    
    plt.legend(loc='upper right',fontsize=18)
    plt.xlim(0,0.8)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)   
    
def draw_structure_vel(title_name,vel1,vel2,vel3,vel4,label1,label2,label3,label4):
    plt.figure()
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 18)
    plt.xlabel("tns",fontsize=18)
    
    plt.plot(vel1[:,0], vel1[:,plt_axis4], label= label1,marker='o', markevery=100)
    plt.plot(vel2[:,0], vel2[:,plt_axis4], label= label2,marker='x', markevery=100)
    plt.plot(vel3[:,0], vel3[:,plt_axis4], label= label3,marker='d', markevery=100)
    plt.plot(vel4[:,0], vel4[:,plt_axis4], label= label4)
    
    plt.legend(loc='upper right',fontsize=18)
    plt.xlim(0,0.8)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)   

plt_axis1 = 2  # Stress yaxis   
plt_axis2 = 2  # Velocity yaxis

# plt_axis3 = 1  # Structure Stress
# plt_axis4 = 1  # Structure Vel
# ============== Left/Right/Center Stress =======================
x_axis = 0.05
draw_stress("Left side stress",ele1,ele141,ele274,"ele1","ele141","ele274")
ax1 = plt.gca()
ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax1.yaxis.get_offset_text().set(size=18)

draw_stress("Center side stress",ele4,ele144,ele277,"ele4","ele144","ele277")
ax3 = plt.gca()
ax3.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax3.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax3.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax3.yaxis.get_offset_text().set(size=18)

draw_stress("Right side stress",ele7,ele147,ele280,"ele7","ele147","ele280")
ax2 = plt.gca()
ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax2.yaxis.get_offset_text().set(size=18)

# ============== Left/Right/Center Velocity =======================
draw_Vel("Left side Velocity",vel1,vel161,vel321,"vel1","vel161","vel321")
ax4 = plt.gca()
ax4.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax4.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax4.yaxis.get_offset_text().set(size=18)

draw_Vel("Center side Velocity",vel4,vel164,vel324,"vel4","vel164","vel324")
ax6 = plt.gca()
ax6.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax6.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax6.yaxis.get_offset_text().set(size=18)

draw_Vel("Right side Velocity",vel8,vel168,vel328,"vel8","vel168","vel328")
ax5 = plt.gca()
ax5.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax5.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax5.yaxis.get_offset_text().set(size=18)

# -------------Dashpot Velocity -----------------
# draw_Vel("Side Dashpot Velocity",Dash951,Dash1049,Dash1250,"Dash951","Dash1049","Dash1250")
# ax7 = plt.gca()
# ax7.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax7.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax7.yaxis.get_offset_text().set(size=18)

# ================X Disp ===========================
# draw_Disp("node Displacement",disp1,disp8, disp9, disp16,"disp1","disp8","disp9","disp16")
# ax7 = plt.gca()
# ax7.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax7.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax7.yaxis.get_offset_text().set(size=18)

# # ============== Structure Stress =======================
# draw_structure_stress("Structure Sterss",col1,col2,Beam,"Coluumn1","Coluumn2","Beam")
# ax7 = plt.gca()
# ax7.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax7.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax7.yaxis.get_offset_text().set(size=18)
# # ============== Structure Velocity =======================
# draw_structure_vel("Structure Velocity",vel1030,vel1031,vel1032,vel1033,"vel1030","vel1031","vel1032","vel1033")
# ax8 = plt.gca()
# ax8.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax8.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax8.yaxis.get_offset_text().set(size=18)
