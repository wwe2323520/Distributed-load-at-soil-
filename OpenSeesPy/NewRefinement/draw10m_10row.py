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
file2 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele401.out"
file3 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele721.out"

file4 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1.out"
file5 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node406.out"
file6 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node811.out"

#----------------------------- Center column file -----------------------------------
file7 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele41.out"
file8 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele441.out"
file9 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele761.out"

file10 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node41.out"
file11 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node446.out"
file12 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node851.out"

#----------------------------- Right column file -----------------------------------
file13 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele80.out"
file14 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele480.out"
file15 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele800.out"

file16 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node81.out"
file17 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node486.out"
file18 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node891.out"

# # ------------Side Velocity -------------------
# file19 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1649.out"
# file20 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1749.out"
# file21 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1849.out"

# file22 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1650.out"
# file23 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1750.out"
# file24 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1848.out"

# file25 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1850.out"
# file26 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1950.out"
# file27 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node2050.out"

# file28 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1851.out"
# file29 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1951.out"
# file30 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node2049.out"


#----------------------------- Structure file -----------------------------------
# file19 = r"D:\shiang\opensees\20220330\extend_soil\stress\Column1_stress.out"
# file20 = r"D:\shiang\opensees\20220330\extend_soil\stress\Column2_stress.out"
# file21 = r"D:\shiang\opensees\20220330\extend_soil\stress\Beam_stress.out"

# file22 = r"D:\shiang\opensees\20220330\extend_soil\velocity\node1030_vel.out"
# file23 = r"D:\shiang\opensees\20220330\extend_soil\velocity\node1031_vel.out"
# file24 = r"D:\shiang\opensees\20220330\extend_soil\velocity\node1032_vel.out"
# file25 = r"D:\shiang\opensees\20220330\extend_soil\velocity\node1033_vel.out"
#----------------------------- Left column file -----------------------------------
ele1 = rdnumpy(file1)
ele401 = rdnumpy(file2)
ele721 = rdnumpy(file3)

vel1 = rdnumpy(file4)
vel406 = rdnumpy(file5)
vel811 = rdnumpy(file6)
#----------------------------- Center column file -----------------------------------
ele41 = rdnumpy(file7)
ele441 = rdnumpy(file8)
ele761 = rdnumpy(file9)

vel41 = rdnumpy(file10)
vel446 = rdnumpy(file11)
vel851 = rdnumpy(file12)
#----------------------------- Right column file -----------------------------------
ele80 = rdnumpy(file13)
ele480 = rdnumpy(file14)
ele800 = rdnumpy(file15)

vel81 = rdnumpy(file16)
vel486 = rdnumpy(file17)
vel891 = rdnumpy(file18)

# # -------------------- Side dash Velocity ----------------
# dash1650 = rdnumpy(file22)
# dash1750 = rdnumpy(file23)
# dash1848 = rdnumpy(file24)

# dash1851 = rdnumpy(file28)
# dash1951 = rdnumpy(file29)
# dash2049 = rdnumpy(file30)
# # -------------------- Side Node Velocity ----------------
# Side1649 = rdnumpy(file19)
# Side1749 = rdnumpy(file20)
# Side1849 = rdnumpy(file21)

# Side1850 = rdnumpy(file25)
# Side1950 = rdnumpy(file26)
# Side2050 = rdnumpy(file27)
# #----------------------------- Structure file -----------------------------------
# col1 = rdnumpy(file19)
# col2 = rdnumpy(file20)
# Beam = rdnumpy(file21)

# vel1030 = rdnumpy(file22)
# vel1031 = rdnumpy(file23)
# vel1032 = rdnumpy(file24)
# vel1033 = rdnumpy(file25)

# plt_axis1 = 2
# x_axis = 0.5
def draw_stress(title_name,ele1,ele2,ele3,label1,label2,label3):
    plt.figure(figsize=(10,8))
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 18)
    plt.xlabel("time(s)",fontsize=18)
    plt.ylabel(r'Stress $(N/m^2)$', fontsize = 18)
    
    plt.plot(ele1[:,0], ele1[:,plt_axis1], label= label1,marker='o', markevery=100)
    plt.plot(ele2[:,0], ele2[:,plt_axis1], label= label2,marker='x', markevery=100)
    plt.plot(ele3[:,0], ele3[:,plt_axis1], label= label3)
    
    
    plt.legend(loc='upper right',fontsize=18)
    plt.xlim(0,0.4)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)   
    
# plt_axis2 = 2
def draw_Vel(title_name,vel1,vel2,vel3,label1,label2,label3):
    plt.figure(figsize=(10,8))
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 18)
    plt.xlabel("time(s)",fontsize=18)
    plt.ylabel(r'Stress $(N/m^2)$', fontsize = 18)
    
    plt.plot(vel1[:,0], vel1[:,plt_axis2], label= label1,marker='o', markevery=100)
    plt.plot(vel2[:,0], vel2[:,plt_axis2], label= label2,marker='x', markevery=100)
    plt.plot(vel3[:,0], vel3[:,plt_axis2], label= label3)
    
    
    plt.legend(loc='upper right',fontsize=18)
    plt.xlim(0,0.4)
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

plt_axis1 = 3  # Stress yaxis   
plt_axis2 = 1  # Velocity yaxis

# plt_axis3 = 1  # Structure Stress
# plt_axis4 = 1  # Structure Vel
# ============== Left/Right/Center Stress =======================
x_axis = 0.05
draw_stress("Left side stress",ele1,ele401,ele721,"ele1","ele401","ele721")
ax1 = plt.gca()
ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax1.yaxis.get_offset_text().set(size=18)

draw_stress("Center side stress",ele41,ele441,ele761,"ele41","ele441","ele761")
ax3 = plt.gca()
ax3.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax3.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax3.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax3.yaxis.get_offset_text().set(size=18)


draw_stress("Right side stress",ele80,ele480,ele800,"ele80","ele480","ele800")
ax2 = plt.gca()
ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax2.yaxis.get_offset_text().set(size=18)



# ============== Left/Right/Center Velocity =======================
draw_Vel("Left side Velocity",vel1,vel406,vel811,"vel1","vel406","vel811")
ax4 = plt.gca()
ax4.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax4.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax4.yaxis.get_offset_text().set(size=18)

draw_Vel("Center side Velocity",vel41,vel446,vel851,"vel41","vel446","vel851")
ax6 = plt.gca()
ax6.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax6.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax6.yaxis.get_offset_text().set(size=18)

draw_Vel("Right side Velocity",vel81,vel486,vel891,"vel81","vel486","vel891")
ax5 = plt.gca()
ax5.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax5.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax5.yaxis.get_offset_text().set(size=18)

# # -------------Dashpot Velocity -----------------
# draw_Vel("Left Dashpot Velocity",dash1650,dash1750,dash1848,"dash1650","dash1750","dash1848")
# ax7 = plt.gca()
# ax7.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax7.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax7.yaxis.get_offset_text().set(size=18)

# draw_Vel("Right Dashpot Velocity",dash1851,dash1951,dash2049,"dash1851","dash1951","dash2049")
# ax8 = plt.gca()
# ax8.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax8.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax8.yaxis.get_offset_text().set(size=18)

# # -------------Side Velocity -----------------
# draw_Vel("Left Beam Velocity",Side1649,Side1749,Side1849,"Side1649","Side1749","Side1849")
# ax9 = plt.gca()
# ax9.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax9.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax9.yaxis.get_offset_text().set(size=18)

# draw_Vel("Right Beam Velocity",Side1850,Side1950,Side2050,"Side1850","Side1950","Side2050")
# ax10 = plt.gca()
# ax10.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax10.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax10.yaxis.get_offset_text().set(size=18)

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
# ax8.yaxis.get_offset_text().set(size=18)# -*- coding: utf-8 -*-
