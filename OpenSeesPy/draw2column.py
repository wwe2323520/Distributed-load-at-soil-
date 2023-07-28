# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 14:51:10 2023

@author: User
"""

import matplotlib.pyplot as plt
import numpy as np
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
# ------ Stress File -------------
# ---------- 1 column ----------------
# file1 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele1.out"
# file2 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele51.out"
# file3 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele100.out"

# file4 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1.out"
# file5 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node101.out"
# file6 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node201.out"

# ---------- 2 column ----------------
file1 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele1.out"
file2 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele101.out"
file3 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele199.out"

file4 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele2.out"
file5 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele102.out"
file6 = r"D:\shiang\opensees\20220330\OpenSeesPy\Stress\ele200.out"

file7 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node1.out"
file8 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node151.out"
file9 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node301.out"

file10 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node3.out"
file11 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node153.out"
file12 = r"D:\shiang\opensees\20220330\OpenSeesPy\Velocity\node303.out"
# --------------- Stress ---------------
# ----- 1 column -----------------
# ele1 =  rdnumpy(file1)
# ele51 =  rdnumpy(file2)
# ele100 =  rdnumpy(file3)

# vel1 =  rdnumpy(file4)
# vel101 =  rdnumpy(file5)
# vel201 =  rdnumpy(file6)

# ----- 2 column ---------------------
ele1 =  rdnumpy(file1)
ele101 =  rdnumpy(file2)
ele199 = rdnumpy(file3)

ele2 =  rdnumpy(file4)
ele102 =  rdnumpy(file5)
ele200 = rdnumpy(file6)

vel1 = rdnumpy(file7)
vel151 = rdnumpy(file8)
vel301 = rdnumpy(file9)

vel3 = rdnumpy(file10)
vel153 = rdnumpy(file11)
vel303 = rdnumpy(file12)

plt_axis1 = 2 # Stress
plt_axis2 = 2 # Vel / Disp

x_axis = 0.5
def draw_stress(title_name,ele1,ele2,label1,label2):
    plt.figure()
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.title(title_name, fontsize = 18)
    plt.xlabel("tns",fontsize=18)
    
    plt.plot(ele1[:,0], ele1[:,plt_axis1], label= label1,marker='o', markevery=100)
    plt.plot(ele2[:,0], ele2[:,plt_axis1], label= label2,marker='x', markevery=100)
    # plt.plot(ele3[:,0], ele3[:,plt_axis1], label= label3)
       
    plt.legend(loc='upper right',fontsize=18)
    plt.xlim(0,0.8)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)   
    
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

def quad_stress(title_name,ele1,ele2,ele3,label1,label2,label3):
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
#---------------- Beam Stress -------------------
# draw_stress("Beam Stress",ele500,ele501,"ele500","ele501")

#---------------- Left Stress -------------------
x_axis = 0.05
# ------- 1 column ------------
# quad_stress("quad element Stress(P wave)", ele1, ele51, ele100, "ele1", "ele51", "ele100")

# draw_Vel("Node Velocity(P wave)",vel1,vel101,vel201,"vel1","vel101","vel201")
# ax2 = plt.gca()
# ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
# # ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
# ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
# ax2.yaxis.get_offset_text().set(size=18)

# ------- 2 column -------------
quad_stress("left column Stress", ele1, ele101, ele199, "ele1", "ele101", "ele199")
quad_stress("Right column Stress", ele2, ele102, ele200, "ele2", "ele102", "ele200")

draw_Vel("Left Velocity(P wave)",vel1,vel151,vel301,"vel1","vel151","vel301")
draw_Vel("Right Velocity(P wave)",vel3,vel153,vel303,"vel3","vel153","vel303")
#---------------- Right Stress -------------------
# quad_stress("Right column Stress", ele2, ele102, ele200, "ele2", "ele102", "ele200")






















