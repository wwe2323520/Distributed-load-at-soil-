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

file1 = r"D:\shiang\opensees\Different\Stress\10msoil\ele1_stress_P.out"
file2 = r"D:\shiang\opensees\Different\Stress\10msoil\ele5001_stress_P.out"
file3 = r"D:\shiang\opensees\Different\Stress\10msoil\ele9901_stress_P.out"

file4 = r"D:\shiang\opensees\Different\Velocity\10msoil\node1_vel_P.out"
file5 = r"D:\shiang\opensees\Different\Velocity\10msoil\node5051_vel_P.out"
file6 = r"D:\shiang\opensees\Different\Velocity\10msoil\node10101_vel_P.out"

#----------------------------- Right column file -----------------------------------
file7 = r"D:\shiang\opensees\Different\Stress\10msoil\ele100_stress_P.out"
file8 = r"D:\shiang\opensees\Different\Stress\10msoil\ele5100_stress_P.out"
file9 = r"D:\shiang\opensees\Different\Stress\10msoil\ele10000_stress_P.out"

file10 = r"D:\shiang\opensees\Different\Velocity\10msoil\node101_vel_P.out"
file11 = r"D:\shiang\opensees\Different\Velocity\10msoil\node5151_vel_P.out"
file12 = r"D:\shiang\opensees\Different\Velocity\10msoil\node10201_vel_P.out"

#----------------------------- Center column file -----------------------------------
file13 = r"D:\shiang\opensees\Different\Stress\10msoil\ele51_stress_P.out"
file14 = r"D:\shiang\opensees\Different\Stress\10msoil\ele5051_stress_P.out"
file15 = r"D:\shiang\opensees\Different\Stress\10msoil\ele9951_stress_P.out"

file16 = r"D:\shiang\opensees\Different\Velocity\10msoil\node51_vel_P.out"
file17 = r"D:\shiang\opensees\Different\Velocity\10msoil\node5101_vel_P.out"
file18 = r"D:\shiang\opensees\Different\Velocity\10msoil\node10151_vel_P.out"

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
ele5001 = rdnumpy(file2)
ele9901 = rdnumpy(file3)

vel1 = rdnumpy(file4)
vel5051 = rdnumpy(file5)
vel10101 = rdnumpy(file6)
#----------------------------- Right column file -----------------------------------
ele100 = rdnumpy(file7)
ele5100 = rdnumpy(file8)
ele10000 = rdnumpy(file9)

vel101 = rdnumpy(file10)
vel5151 = rdnumpy(file11)
vel10201 = rdnumpy(file12)
#----------------------------- Center column file -----------------------------------
ele51 = rdnumpy(file13)
ele5051 = rdnumpy(file14)
ele9951 = rdnumpy(file15)

vel51 = rdnumpy(file16)
vel5101 = rdnumpy(file17)
vel10151 = rdnumpy(file18)
#----------------------------- Structure file -----------------------------------
# col1 = rdnumpy(file19)
# col2 = rdnumpy(file20)
# Beam = rdnumpy(file21)

# vel1030 = rdnumpy(file22)
# vel1031 = rdnumpy(file23)
# vel1032 = rdnumpy(file24)
# vel1033 = rdnumpy(file25)

# plt_axis1 = 2
x_axis = 0.5
def draw_stress(title_name,ele1,ele2,ele3,label1,label2,label3):
    plt.figure()
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 18)
    plt.xlabel("tns",fontsize=18)
    
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
    plt.figure()
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 18)
    plt.xlabel("tns",fontsize=18)
    
    plt.plot(vel1[:,0], vel1[:,plt_axis2], label= label1,marker='o', markevery=100)
    plt.plot(vel2[:,0], vel2[:,plt_axis2], label= label2,marker='x', markevery=100)
    plt.plot(vel3[:,0], vel3[:,plt_axis2], label= label3)
    
    
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
draw_stress("Left side stress",ele1,ele5001,ele9901,"ele1","ele5001","ele5001")
ax1 = plt.gca()
ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax1.yaxis.get_offset_text().set(size=18)

draw_stress("Right side stress",ele100,ele5100,ele10000,"ele100","ele5100","ele10000")
ax2 = plt.gca()
ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax2.yaxis.get_offset_text().set(size=18)

draw_stress("Center side stress",ele51,ele5051,ele9951,"ele51","ele5051","ele9951")
ax3 = plt.gca()
ax3.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax3.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax3.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax3.yaxis.get_offset_text().set(size=18)


# ============== Left/Right/Center Velocity =======================
draw_Vel("Left side Velocity",vel1,vel5051,vel10101,"vel1","vel5051","vel10101")
ax4 = plt.gca()
ax4.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax4.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax4.yaxis.get_offset_text().set(size=18)

draw_Vel("Right side Velocity",vel101,vel5151,vel10201,"vel101","vel5151","vel10201")
ax5 = plt.gca()
ax5.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax5.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax5.yaxis.get_offset_text().set(size=18)

draw_Vel("Center side Velocity",vel51,vel5101,vel10151,"vel51","vel5101","vel10151")
ax6 = plt.gca()
ax6.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax6.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax6.yaxis.get_offset_text().set(size=18)


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
file1 = r"D:\shiang\opensees\20220330\extend_soil\stress\10m_soil\ele1_stress.out"
file2 = r"D:\shiang\opensees\20220330\extend_soil\stress\10m_soil\ele5001_stress.out"
file3 = r"D:\shiang\opensees\20220330\extend_soil\stress\10m_soil\ele9901_stress.out"

file4 = r"D:\shiang\opensees\20220330\extend_soil\velocity\10m_soil\node1_vel.out"
file5 = r"D:\shiang\opensees\20220330\extend_soil\velocity\10m_soil\node5051_vel.out"
file6 = r"D:\shiang\opensees\20220330\extend_soil\velocity\10m_soil\node10101_vel.out"

#----------------------------- Right column file -----------------------------------
file7 = r"D:\shiang\opensees\20220330\extend_soil\stress\10m_soil\ele100_stress.out"
file8 = r"D:\shiang\opensees\20220330\extend_soil\stress\10m_soil\ele5100_stress.out"
file9 = r"D:\shiang\opensees\20220330\extend_soil\stress\10m_soil\ele10000_stress.out"

file10 = r"D:\shiang\opensees\20220330\extend_soil\velocity\10m_soil\node101_vel.out"
file11 = r"D:\shiang\opensees\20220330\extend_soil\velocity\10m_soil\node5151_vel.out"
file12 = r"D:\shiang\opensees\20220330\extend_soil\velocity\10m_soil\node10201_vel.out"

#----------------------------- Center column file -----------------------------------
file13 = r"D:\shiang\opensees\20220330\extend_soil\stress\10m_soil\ele51_stress.out"
file14 = r"D:\shiang\opensees\20220330\extend_soil\stress\10m_soil\ele5051_stress.out"
file15 = r"D:\shiang\opensees\20220330\extend_soil\stress\10m_soil\ele9951_stress.out"

file16 = r"D:\shiang\opensees\20220330\extend_soil\velocity\node51_vel.out"
file17 = r"D:\shiang\opensees\20220330\extend_soil\velocity\node5101_vel.out"
file18 = r"D:\shiang\opensees\20220330\extend_soil\velocity\node10151_vel.out"

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
ele5001 = rdnumpy(file2)
ele9901 = rdnumpy(file3)

vel1 = rdnumpy(file4)
vel5051 = rdnumpy(file5)
vel10101 = rdnumpy(file6)
#----------------------------- Right column file -----------------------------------
ele100 = rdnumpy(file7)
ele5100 = rdnumpy(file8)
ele10000 = rdnumpy(file9)

vel101 = rdnumpy(file10)
vel5151 = rdnumpy(file11)
vel10201 = rdnumpy(file12)
#----------------------------- Center column file -----------------------------------
ele51 = rdnumpy(file13)
ele5051 = rdnumpy(file14)
ele9951 = rdnumpy(file15)

vel51 = rdnumpy(file16)
vel5101 = rdnumpy(file17)
vel10151 = rdnumpy(file18)
#----------------------------- Structure file -----------------------------------
# col1 = rdnumpy(file19)
# col2 = rdnumpy(file20)
# Beam = rdnumpy(file21)

# vel1030 = rdnumpy(file22)
# vel1031 = rdnumpy(file23)
# vel1032 = rdnumpy(file24)
# vel1033 = rdnumpy(file25)

# plt_axis1 = 2
x_axis = 0.5
def draw_stress(title_name,ele1,ele2,ele3,label1,label2,label3):
    plt.figure()
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 18)
    plt.xlabel("tns",fontsize=18)
    
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
    plt.figure()
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 18)
    plt.xlabel("tns",fontsize=18)
    
    plt.plot(vel1[:,0], vel1[:,plt_axis2], label= label1,marker='o', markevery=100)
    plt.plot(vel2[:,0], vel2[:,plt_axis2], label= label2,marker='x', markevery=100)
    plt.plot(vel3[:,0], vel3[:,plt_axis2], label= label3)
    
    
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
draw_stress("Left side stress",ele1,ele5001,ele9901,"ele1","ele5001","ele5001")
ax1 = plt.gca()
ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax1.yaxis.get_offset_text().set(size=18)

draw_stress("Right side stress",ele100,ele5100,ele10000,"ele100","ele5100","ele10000")
ax2 = plt.gca()
ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax2.yaxis.get_offset_text().set(size=18)

draw_stress("Center side stress",ele51,ele5051,ele9951,"ele51","ele5051","ele9951")
ax3 = plt.gca()
ax3.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax3.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax3.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax3.yaxis.get_offset_text().set(size=18)


# ============== Left/Right/Center Velocity =======================
draw_Vel("Left side Velocity",vel1,vel5051,vel10101,"vel1","vel5051","vel10101")
ax4 = plt.gca()
ax4.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax4.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax4.yaxis.get_offset_text().set(size=18)

draw_Vel("Right side Velocity",vel101,vel5151,vel10201,"vel101","vel5151","vel10201")
ax5 = plt.gca()
ax5.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax5.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax5.yaxis.get_offset_text().set(size=18)

draw_Vel("Center side Velocity",vel51,vel5101,vel10151,"vel51","vel5101","vel10151")
ax6 = plt.gca()
ax6.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax6.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax6.yaxis.get_offset_text().set(size=18)


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
