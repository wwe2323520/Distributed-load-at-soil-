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
file2 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele41.out"
file3 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele73.out"

file4 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1.out"
file5 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node46.out"
file6 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node91.out"

#----------------------------- Center column file -----------------------------------
file7 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele5.out"
file8 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele45.out"
file9 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele77.out"

file10 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node5.out"
file11 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node50.out"
file12 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node95.out"

#----------------------------- Right column file -----------------------------------
file13 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele8.out"
file14 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele48.out"
file15 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele80.out"

file16 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node9.out"
file17 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node54.out"
file18 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node99.out"

# ---------- Left Beam Node Velocity / Stress -----------------
file19 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node145.out"
file20 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node155.0.out"
file21 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node165.out"

file22 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele107.out"
file23 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele117.0.out"
file24 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele125.out"

#---- Left Beam Center Node Velocity ------
file25 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node187.out"
file26 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node197.0.out"
file27 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node205.out"
# ----- Left Dashpot fix y node ------------- 
file28 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node188.out"
file29 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node198.0.out"
file30 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node206.out"


#--------------- Right Beam Node Velocity / Stress------
file31 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node166.out"
file32 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node176.0.out"
file33 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node186.out"

file34 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele127.out"
file35 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele137.0.out"
file36 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele145.out"

#---- Right Beam Center Node 20220330 ------
file37 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node228.out"
file38 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node238.0.out"
file39 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node246.out"

# ----- Right Dashpot fix y node ------------- 
file40 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node229.out"
file41 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node239.0.out"
file42 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node247.out"

#----------------------------- Left column file -----------------------------------
ele1 = rdnumpy(file1)
ele41 = rdnumpy(file2)
ele73 = rdnumpy(file3)

vel1 = rdnumpy(file4)
vel46 = rdnumpy(file5)
vel91 = rdnumpy(file6)
#----------------------------- Center column file -----------------------------------
ele5 = rdnumpy(file7)
ele45 = rdnumpy(file8)
ele77 = rdnumpy(file9)

vel5 = rdnumpy(file10)
vel50 = rdnumpy(file11)
vel95 = rdnumpy(file12)
#----------------------------- Right column file -----------------------------------
ele8 = rdnumpy(file13)
ele48 = rdnumpy(file14)
ele80 = rdnumpy(file15)

vel9 = rdnumpy(file16)
vel54 = rdnumpy(file17)
vel99 = rdnumpy(file18)

# -------------------- Left Beam Node Velocity / Stress----------------
vel145 = rdnumpy(file19)
vel155 = rdnumpy(file20)
vel165 = rdnumpy(file21)

Beam107 = rdnumpy(file22)
Beam117 = rdnumpy(file23)
Beam125 = rdnumpy(file24)

# -------------------- Left Beam Center free velocity----------------
dash187 = rdnumpy(file25)
dash197 = rdnumpy(file26)
dash205 = rdnumpy(file27)
# -------------------- Side dash fix Velocity ----------------
dash188 = rdnumpy(file28)
dash198 = rdnumpy(file29)
dash206 = rdnumpy(file30)

# -------------------- Right Beam Node Velocity / Stress----------------
vel166 = rdnumpy(file31)
vel176 = rdnumpy(file32)
vel186 = rdnumpy(file33)

Beam127 = rdnumpy(file34)
Beam137 = rdnumpy(file35)
Beam145 = rdnumpy(file36)

# -------------------- Right Beam Center free velocity----------------
dash228 = rdnumpy(file37)
dash238 = rdnumpy(file38)
dash246 = rdnumpy(file39)
# -------------------- Right Side dash fix Velocity ----------------
dash229 = rdnumpy(file40)
dash239 = rdnumpy(file41)
dash247 = rdnumpy(file42)


# plt_axis1 = 2
# x_axis = 0.5
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
    plt.xlim(0,0.4)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)   
    
# plt_axis2 = 2
def draw_Vel(title_name,vel1,vel2,vel3,label1,label2,label3):
    plt.figure(figsize=(10,8))
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 18)
    plt.xlabel("time (s)",fontsize=18)
    plt.ylabel(r'Velocity $(m/s)$', fontsize = 18)
    
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
draw_stress("Left side stress",ele1,ele41,ele73,"ele1","ele41","ele73")
ax1 = plt.gca()
ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax1.yaxis.get_offset_text().set(size=18)

draw_stress("Center side stress",ele5,ele45,ele77,"ele5","ele45","ele77")
ax3 = plt.gca()
ax3.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax3.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax3.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax3.yaxis.get_offset_text().set(size=18)


draw_stress("Right side stress",ele8,ele48,ele80,"ele8","ele48","ele80")
ax2 = plt.gca()
ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax2.yaxis.get_offset_text().set(size=18)



# ============== Left/Right/Center Velocity =======================
draw_Vel("Left side Velocity",vel1,vel46,vel91,"vel1","vel46","vel91")
ax4 = plt.gca()
ax4.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax4.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax4.yaxis.get_offset_text().set(size=18)

draw_Vel("Center side Velocity",vel5,vel50,vel95,"vel5","vel50","vel95")
ax6 = plt.gca()
ax6.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax6.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax6.yaxis.get_offset_text().set(size=18)

draw_Vel("Right side Velocity",vel9,vel54,vel99,"vel9","vel54","vel99")
ax5 = plt.gca()
ax5.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax5.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax5.yaxis.get_offset_text().set(size=18)


# -------------Side Velocity -----------------
draw_Vel("Left Beam Velocity",vel145,vel155,vel165,"vel145","vel155","vel165")
ax9 = plt.gca()
ax9.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax9.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax9.yaxis.get_offset_text().set(size=18)

draw_Vel("Left Side Free Dash Velocity",dash187,dash197,dash205,"dash187","dash197","dash205")
ax10 = plt.gca()
ax10.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax10.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax10.yaxis.get_offset_text().set(size=18)

draw_Vel("Left Side Fix Dash Velocity",dash188,dash198,dash206,"dash188","dash198","dash206")
ax11 = plt.gca()
ax11.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax11.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax11.yaxis.get_offset_text().set(size=18)

draw_stress("Left Beam Force",Beam107,Beam117,Beam125,"Beam107","Beam117","Beam125")
ax12 = plt.gca()
ax12.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax12.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax12.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax12.yaxis.get_offset_text().set(size=18)

# -------------Side Velocity -----------------
draw_Vel("Right Beam Velocity",vel166,vel176,vel186,"vel166","vel176","vel186")
ax13 = plt.gca()
ax13.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax13.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax13.yaxis.get_offset_text().set(size=18)

draw_Vel("Right Side Free Dash Velocity",dash228,dash238,dash246,"dash228","dash238","dash246")
ax14 = plt.gca()
ax14.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax14.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax14.yaxis.get_offset_text().set(size=18)

draw_Vel("Right Side Fix Dash Velocity",dash229,dash239,dash247,"dash229","dash239","dash247")
ax15 = plt.gca()
ax15.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax15.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax15.yaxis.get_offset_text().set(size=18)

draw_stress("Right Beam Force",Beam127,Beam137,Beam145,"Beam127","Beam137","Beam145")
ax16 = plt.gca()
ax16.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax16.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax16.yaxis.get_offset_text().set(size=18)



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
