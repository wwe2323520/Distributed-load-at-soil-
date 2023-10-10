# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 16:33:00 2023

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
from matplotlib.ticker import ScalarFormatter
import scipy.signal
from scipy.signal import find_peaks

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
tns = L/cp # wave transport time
dcell = tns/Soil_100row #each cell time
dt = dcell/10 #eace cell have 10 steps
print(f"wave travel = {tns} ;dcell = {dcell} ;dt = {dt}")

time = np.arange(0.0,0.050005,dt)
Nt = len(time)

# Analysis = np.zeros((len(total_time),2))
# Analysis[:,0] = total_time[:]
# Analysis[:,1] = wave1[:,99]
#　 =================== Middle Point File (1/2) ====================
# ------------------- File Path Name --------------------
# Boundary = 'TieBC'
# Boundary1 = 'Tie Boundary Condition'

# ele80 = f"{Boundary}_80row"
# ele40 = f"{Boundary}_40row"
# ele20 = f"{Boundary}_20row"
# ele10 = f"{Boundary}_10row"
soilWidth = 20
# --------- Tie Boundary Condition ----------------
file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopForce_80row/node12961.out"
file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopForce_40row/node6521.out"
file3 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopForce_20row/node3301.out"
file4 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopForce_10row/node1691.out"
# --------- LK Dashpot Boundary Condition ----------------
file5 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideDash_80row/node12961.out"
file6 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideDash_40row/node6521.out"
file7 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideDash_20row/node3301.out"
file8 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideDash_10row/node1691.out"
# --------- Distributed Beam Boundary Condition ----------------
file9 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideBeam_80row/node12961.out"
file10 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideBeam_40row/node6521.out"
file11 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideBeam_20row/node3301.out"
file12 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideBeam_10row/node1691.out"
# --------- Distributed Beam and Node Boundary Condition ----------------
file13 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideNodeDash_80row/node12961.out"
file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideNodeDash_40row/node6521.out"
file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideNodeDash_20row/node3301.out"
file16 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideNodeDash_10row/node1691.out"

Tie_W20_Mid80row = rdnumpy(file1)
Tie_W20_Mid40row = rdnumpy(file2)
Tie_W20_Mid20row = rdnumpy(file3)
Tie_W20_Mid10row = rdnumpy(file4)

LK_W20_Mid80row = rdnumpy(file5)
LK_W20_Mid40row = rdnumpy(file6)
LK_W20_Mid20row = rdnumpy(file7)
LK_W20_Mid10row = rdnumpy(file8)

Beam_W20_Mid80row = rdnumpy(file9)
Beam_W20_Mid40row = rdnumpy(file10)
Beam_W20_Mid20row = rdnumpy(file11)
Beam_W20_Mid10row = rdnumpy(file12)

BeamNode_W20_Mid80row = rdnumpy(file13)
BeamNode_W20_Mid40row = rdnumpy(file14)
BeamNode_W20_Mid20row = rdnumpy(file15)
BeamNode_W20_Mid10row = rdnumpy(file16)

# --------- Tie Boundary Condition ----------------
file17 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopForce_80row/node6521.out"
file18 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopForce_40row/node3281.out"
file19 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopForce_20row/node1661.out"
file20 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopForce_10row/node851.out"
# --------- LK Dashpot Boundary Condition ----------------
file21 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideDash_80row/node6521.out"
file22 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideDash_40row/node3281.out"
file23 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideDash_20row/node1661.out"
file24 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideDash_10row/node851.out"
# --------- Distributed Beam Boundary Condition ----------------
file25 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideBeam_80row/node6521.out"
file26 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideBeam_40row/node3281.out"
file27 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideBeam_20row/node1661.out"
file28 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideBeam_10row/node851.out"
# --------- Distributed Beam and Node Boundary Condition ----------------
file29 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideNodeDash_80row/node6521.out"
file30 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideNodeDash_40row/node3281.out"
file31 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideNodeDash_20row/node1661.out"
file32 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideNodeDash_10row/node851.out"

Tie_W10_Mid80row = rdnumpy(file17)
Tie_W10_Mid40row = rdnumpy(file18)
Tie_W10_Mid20row = rdnumpy(file19)
Tie_W10_Mid10row = rdnumpy(file20)

LK_W10_Mid80row = rdnumpy(file21)
LK_W10_Mid40row = rdnumpy(file22)
LK_W10_Mid20row = rdnumpy(file23)
LK_W10_Mid10row = rdnumpy(file24)

Beam_W10_Mid80row = rdnumpy(file25)
Beam_W10_Mid40row = rdnumpy(file26)
Beam_W10_Mid20row = rdnumpy(file27)
Beam_W10_Mid10row = rdnumpy(file28)

BeamNode_W10_Mid80row = rdnumpy(file29)
BeamNode_W10_Mid40row = rdnumpy(file30)
BeamNode_W10_Mid20row = rdnumpy(file31)
BeamNode_W10_Mid10row = rdnumpy(file32)

# --------- Tie Boundary Condition ----------------
file33 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopForce_80row/node725.out"
file34 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopForce_40row/node365.out"
file35 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopForce_20row/node185.out"
file36 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopForce_10row/node95.out"
# --------- LK Dashpot Boundary Condition ----------------
file37 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideDash_80row/node725.out"
file38 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideDash_40row/node365.out"
file39 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideDash_20row/node185.out"
file40 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideDash_10row/node95.out"
# --------- Distributed Beam Boundary Condition ----------------
file41 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideBeam_80row/node725.out"
file42 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideBeam_40row/node365.out"
file43 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideBeam_20row/node185.out"
file44 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideBeam_10row/node95.out"
# --------- Distributed Beam and Node Boundary Condition ----------------
file45 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideNodeDash_80row/node725.out"
file46 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideNodeDash_40row/node365.out"
file47 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideNodeDash_20row/node185.out"
file48 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideNodeDash_10row/node95.out"

Tie_W1_Mid80row = rdnumpy(file33)
Tie_W1_Mid40row = rdnumpy(file34)
Tie_W1_Mid20row = rdnumpy(file35)
Tie_W1_Mid10row = rdnumpy(file36)

LK_W1_Mid80row = rdnumpy(file37)
LK_W1_Mid40row = rdnumpy(file38)
LK_W1_Mid20row = rdnumpy(file39)
LK_W1_Mid10row = rdnumpy(file40)

Beam_W1_Mid80row = rdnumpy(file41)
Beam_W1_Mid40row = rdnumpy(file42)
Beam_W1_Mid20row = rdnumpy(file43)
Beam_W1_Mid10row = rdnumpy(file44)

BeamNode_W1_Mid80row = rdnumpy(file45)
BeamNode_W1_Mid40row = rdnumpy(file46)
BeamNode_W1_Mid20row = rdnumpy(file47)
BeamNode_W1_Mid10row = rdnumpy(file48)


# # ================ Three-Quarter Point File (3/4) ====================
# --------- Tie Boundary Condition ----------------
file49 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopForce_80row/node13001.out"
file50 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopForce_40row/node6561.out"
file51 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopForce_20row/node3341.out"
file52 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopForce_10row/node1731.out"
# --------- LK Dashpot Boundary Condition ----------------
file53 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideDash_80row/node13001.out"
file54 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideDash_40row/node6561.out"
file55 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideDash_20row/node3341.out"
file56 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideDash_10row/node1731.out"
# --------- Distributed Beam Boundary Condition ----------------
file57 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideBeam_80row/node13001.out"
file58 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideBeam_40row/node6561.out"
file59 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideBeam_20row/node3341.out"
file60 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideBeam_10row/node1731.out"
# --------- Distributed Beam and Node Boundary Condition ----------------
file61 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideNodeDash_80row/node13001.out"
file62 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideNodeDash_40row/node6561.out"
file63 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideNodeDash_20row/node3341.out"
file64 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TopSideNodeDash_10row/node1731.out"

Tie_W20_Qua80row = rdnumpy(file49)
Tie_W20_Qua40row = rdnumpy(file50)
Tie_W20_Qua20row = rdnumpy(file51)
Tie_W20_Qua10row = rdnumpy(file52)

LK_W20_Qua80row = rdnumpy(file53)
LK_W20_Qua40row = rdnumpy(file54)
LK_W20_Qua20row = rdnumpy(file55)
LK_W20_Qua10row = rdnumpy(file56)

Beam_W20_Qua80row = rdnumpy(file57)
Beam_W20_Qua40row = rdnumpy(file58)
Beam_W20_Qua20row = rdnumpy(file59)
Beam_W20_Qua10row = rdnumpy(file60)

BeamNode_W20_Qua80row = rdnumpy(file61)
BeamNode_W20_Qua40row = rdnumpy(file62)
BeamNode_W20_Qua20row = rdnumpy(file63)
BeamNode_W20_Qua10row = rdnumpy(file64)

# --------- Tie Boundary Condition ----------------
file65 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopForce_80row/node6541.out"
file66 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopForce_40row/node3301.out"
file67 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopForce_20row/node1681.out"
file68 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopForce_10row/node871.out"
# --------- LK Dashpot Boundary Condition ----------------
file69 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideDash_80row/node6541.out"
file70 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideDash_40row/node3301.out"
file71 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideDash_20row/node1681.out"
file72 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideDash_10row/node871.out"
# --------- Distributed Beam Boundary Condition ----------------
file73 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideBeam_80row/node6541.out"
file74 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideBeam_40row/node3301.out"
file75 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideBeam_20row/node1681.out"
file76 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideBeam_10row/node871.out"
# --------- Distributed Beam and Node Boundary Condition ----------------
file77 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideNodeDash_80row/node6541.out"
file78 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideNodeDash_40row/node3301.out"
file79 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideNodeDash_20row/node1681.out"
file80 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TopSideNodeDash_10row/node871.out"

Tie_W10_Qua80row = rdnumpy(file65)
Tie_W10_Qua40row = rdnumpy(file66)
Tie_W10_Qua20row = rdnumpy(file67)
Tie_W10_Qua10row = rdnumpy(file68)

LK_W10_Qua80row = rdnumpy(file69)
LK_W10_Qua40row = rdnumpy(file70)
LK_W10_Qua20row = rdnumpy(file71)
LK_W10_Qua10row = rdnumpy(file72)

Beam_W10_Qua80row = rdnumpy(file73)
Beam_W10_Qua40row = rdnumpy(file74)
Beam_W10_Qua20row = rdnumpy(file75)
Beam_W10_Qua10row = rdnumpy(file76)

BeamNode_W10_Qua80row = rdnumpy(file77)
BeamNode_W10_Qua40row = rdnumpy(file78)
BeamNode_W10_Qua20row = rdnumpy(file79)
BeamNode_W10_Qua10row = rdnumpy(file80)
# --------- Tie Boundary Condition ----------------
file81 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopForce_80row/node727.out"
file82 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopForce_40row/node367.out"
file83 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopForce_20row/node187.out"
file84 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopForce_10row/node97.out"
# --------- LK Dashpot Boundary Condition ----------------
file85 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideDash_80row/node727.out"
file86 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideDash_40row/node367.out"
file87 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideDash_20row/node187.out"
file88 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideDash_10row/node97.out"
# --------- Distributed Beam Boundary Condition ----------------
file89 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideBeam_80row/node727.out"
file90 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideBeam_40row/node367.out"
file91 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideBeam_20row/node187.out"
file92 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideBeam_10row/node97.out"
# --------- Distributed Beam and Node Boundary Condition ----------------
file93 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideNodeDash_80row/node727.out"
file94 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideNodeDash_40row/node367.out"
file95 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideNodeDash_20row/node187.out"
file96 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TopSideNodeDash_10row/node97.out"

Tie_W1_Qua80row = rdnumpy(file81)
Tie_W1_Qua40row = rdnumpy(file82)
Tie_W1_Qua20row = rdnumpy(file83)
Tie_W1_Qua10row = rdnumpy(file84)

LK_W1_Qua80row = rdnumpy(file85)
LK_W1_Qua40row = rdnumpy(file86)
LK_W1_Qua20row = rdnumpy(file87)
LK_W1_Qua10row = rdnumpy(file88)

Beam_W1_Qua80row = rdnumpy(file89)
Beam_W1_Qua40row = rdnumpy(file90)
Beam_W1_Qua20row = rdnumpy(file91)
Beam_W1_Qua10row = rdnumpy(file92)

BeamNode_W1_Qua80row = rdnumpy(file93)
BeamNode_W1_Qua40row = rdnumpy(file94)
BeamNode_W1_Qua20row = rdnumpy(file95)
BeamNode_W1_Qua10row = rdnumpy(file96)

plt_axis2 = 2 
# # ------- wave put into the timeSeries ---------------
def Differ_BCVel(Mid80row,Mid40row,Mid20row,Mid10row):
    # plt.figure(figsize=(8,6))
    font_props = {'family': 'Arial', 'size': 9}
    # plt.xlabel("time (s)",fontsize=18)
    # plt.ylabel(r"$V_x$  $(m/s)$",fontsize=18)
    # plt.title(titleName,x=0.75,y=0.25, fontsize = 20)
    
    plt.plot(Mid80row[:,0],Mid80row[:,plt_axis2],label ='Tie BC', ls = '--',color= 'darkorange',linewidth=6.0)
    plt.plot(Mid40row[:,0],Mid40row[:,plt_axis2],label ='LK Dashpot BC', ls = '-.',color= 'limegreen',linewidth=5.0)
    plt.plot(Mid20row[:,0],Mid20row[:,plt_axis2],label ='Beam BC', ls = ':',color= 'blue',linewidth=4.0)
    plt.plot(Mid10row[:,0],Mid10row[:,plt_axis2],label ='Beam and Node Dashpot BC', ls = '-',color= 'red',linewidth=2.0)
    
    plt.legend(loc='upper right',prop=font_props,framealpha=0.0) #ncol=2,fontsize=16 loc='lower left'
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xlim(0.0, 0.20)
    # plt.xlim(0.050, 0.070)
    plt.grid(True)

# =========================== Different Boundary compare at Different Mesh Size =================================
x_axis = 0.0267# 0.1 0.05
# x_axis = 0.0025 # 0.1 0.05
row_heights = [3, 3, 3]
fig1, (ax1,ax2,ax3) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig1.suptitle(f'Different Boundary '+ r'$\Delta_C='+ '0.125' + r'\mathrm{m}$' + '\n(Middle node)',x=0.50,y =0.97,fontsize = 20)
# fig1.suptitle(f'Different Boundary '+ r'$\Delta_C='+ '0.125' + r'\mathrm{m}$' + '\n(Three Quarter node)',x=0.50,y =0.97,fontsize = 20)
fig1.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig1.text(0.45,0.04, 'time t (s)', va= 'center', fontsize=20)

ax1 = plt.subplot(311)
Differ_BCVel(Tie_W20_Mid80row, LK_W20_Mid80row, Beam_W20_Mid80row, BeamNode_W20_Mid80row)
ax1.set_title(f"SW 20m",fontsize =18, x=0.50, y=0.78)

ax2 = plt.subplot(312)
Differ_BCVel(Tie_W10_Mid80row, LK_W10_Mid80row, Beam_W10_Mid80row, BeamNode_W10_Mid80row)
ax2.set_title(f"SW 10m",fontsize =18, x=0.50, y=0.78)

ax3 = plt.subplot(313)
Differ_BCVel(Tie_W1_Mid80row, LK_W1_Mid80row, Beam_W1_Mid80row, BeamNode_W1_Mid80row)
ax3.set_title(f"SW 1m",fontsize =18, x=0.50, y=0.78)

# ax1 = plt.subplot(311)
# Differ_BCVel(Tie_W20_Qua80row, LK_W20_Qua80row, Beam_W20_Qua80row, BeamNode_W20_Qua80row)
# ax1.set_title(f"SW 20m",fontsize =18, x=0.10, y=0.78)

# ax2 = plt.subplot(312)
# Differ_BCVel(Tie_W10_Qua80row, LK_W10_Qua80row, Beam_W10_Qua80row, BeamNode_W10_Qua80row)
# ax2.set_title(f"SW 10m",fontsize =18, x=0.10, y=0.78)

# ax3 = plt.subplot(313)
# Differ_BCVel(Tie_W1_Qua80row, LK_W1_Qua80row, Beam_W1_Qua80row, BeamNode_W1_Qua80row)
# ax3.set_title(f"SW 1m",fontsize =18, x=0.10, y=0.78)

for ax in [ax1,ax2,ax3]:
    formatter = ticker.ScalarFormatter(useMathText =True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set(size=18)
    ax.xaxis.get_offset_text().set(size=18)

fig2, (ax4,ax5,ax6) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig2.suptitle(f'Different Boundary '+ r'$\Delta_C='+ '0.25' + r'\mathrm{m}$' + '\n(Middle node)',x=0.50,y =0.97,fontsize = 20)
# fig2.suptitle(f'Different Boundary '+ r'$\Delta_C='+ '0.25' + r'\mathrm{m}$' + '\n(Three Quarter node)',x=0.50,y =0.97,fontsize = 20)
fig2.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig2.text(0.45,0.04, 'time t (s)', va= 'center', fontsize=20)

ax4 = plt.subplot(311)
Differ_BCVel(Tie_W20_Mid40row, LK_W20_Mid40row, Beam_W20_Mid40row, BeamNode_W20_Mid40row)
ax4.set_title(f"SW 20m",fontsize =18, x=0.50, y=0.78)

ax5 = plt.subplot(312)
Differ_BCVel(Tie_W10_Mid40row, LK_W10_Mid40row, Beam_W10_Mid40row, BeamNode_W10_Mid40row)
ax5.set_title(f"SW 10m",fontsize =18, x=0.50, y=0.78)

ax6 = plt.subplot(313)
Differ_BCVel(Tie_W1_Mid40row, LK_W1_Mid40row, Beam_W1_Mid40row, BeamNode_W1_Mid40row)
ax6.set_title(f"SW 1m",fontsize =18, x=0.50, y=0.78)

# ax4 = plt.subplot(311)
# Differ_BCVel(Tie_W20_Qua40row, LK_W20_Qua40row, Beam_W20_Qua40row, BeamNode_W20_Qua40row)
# ax4.set_title(f"SW 20m",fontsize =18, x=0.10, y=0.78)

# ax5 = plt.subplot(312)
# Differ_BCVel(Tie_W10_Qua40row, LK_W10_Qua40row, Beam_W10_Qua40row, BeamNode_W10_Qua40row)
# ax5.set_title(f"SW 10m",fontsize =18, x=0.10, y=0.78)

# ax6 = plt.subplot(313)
# Differ_BCVel(Tie_W1_Qua40row, LK_W1_Qua40row, Beam_W1_Qua40row, BeamNode_W1_Qua40row)
# ax6.set_title(f"SW 1m",fontsize =18, x=0.10, y=0.78)

for ax in [ax4,ax5,ax6]:
    formatter = ticker.ScalarFormatter(useMathText =True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set(size=18)
    ax.xaxis.get_offset_text().set(size=18)    

fig3, (ax7,ax8,ax9) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig3.suptitle(f'Different Boundary '+ r'$\Delta_C='+ '0.50' + r'\mathrm{m}$' + '\n(Middle node)',x=0.50,y =0.97,fontsize = 20)
# fig3.suptitle(f'Different Boundary '+ r'$\Delta_C='+ '0.50' + r'\mathrm{m}$' + '\n(Three Quarter node node)',x=0.50,y =0.97,fontsize = 20)
fig3.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig3.text(0.45,0.04, 'time t (s)', va= 'center', fontsize=20)

ax7 = plt.subplot(311)
Differ_BCVel(Tie_W20_Mid20row, LK_W20_Mid20row, Beam_W20_Mid20row, BeamNode_W20_Mid20row)
ax7.set_title(f"SW 20m",fontsize =18, x=0.50, y=0.78)

ax8 = plt.subplot(312)
Differ_BCVel(Tie_W10_Mid20row, LK_W10_Mid20row, Beam_W10_Mid20row, BeamNode_W10_Mid20row)
ax8.set_title(f"SW 10m",fontsize =18, x=0.50, y=0.78)

ax9 = plt.subplot(313)
Differ_BCVel(Tie_W1_Mid20row, LK_W1_Mid20row, Beam_W1_Mid20row, BeamNode_W1_Mid20row)
ax9.set_title(f"SW 1m",fontsize =18, x=0.50, y=0.78)

# ax7 = plt.subplot(311)
# Differ_BCVel(Tie_W20_Qua20row, LK_W20_Qua20row, Beam_W20_Qua20row, BeamNode_W20_Qua20row)
# ax7.set_title(f"SW 20m",fontsize =18, x=0.10, y=0.78)

# ax8 = plt.subplot(312)
# Differ_BCVel(Tie_W10_Qua20row, LK_W10_Qua20row, Beam_W10_Qua20row, BeamNode_W10_Qua20row)
# ax8.set_title(f"SW 10m",fontsize =18, x=0.10, y=0.78)

# ax9 = plt.subplot(313)
# Differ_BCVel(Tie_W1_Qua20row, LK_W1_Qua20row, Beam_W1_Qua20row, BeamNode_W1_Qua20row)
# ax9.set_title(f"SW 1m",fontsize =18, x=0.10, y=0.78)

for ax in [ax7,ax8,ax9]:
    formatter = ticker.ScalarFormatter(useMathText =True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set(size=18)
    ax.xaxis.get_offset_text().set(size=18)

fig4, (ax10,ax11,ax12) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig4.suptitle(f'Different Boundary '+ r'$\Delta_C='+ '1.0' + r'\mathrm{m}$' + '\n(Middle node)',x=0.50,y =0.97,fontsize = 20)
# fig4.suptitle(f'Different Boundary '+ r'$\Delta_C='+ '1.0' + r'\mathrm{m}$' + '\n(Three Quarter node node)',x=0.50,y =0.97,fontsize = 20)
fig4.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig4.text(0.45,0.04, 'time t (s)', va= 'center', fontsize=20)

ax10 = plt.subplot(311)
Differ_BCVel(Tie_W20_Mid10row, LK_W20_Mid10row, Beam_W20_Mid10row, BeamNode_W20_Mid10row)
ax10.set_title(f"SW 20m",fontsize =18, x=0.50, y=0.78)

ax11 = plt.subplot(312)
Differ_BCVel(Tie_W10_Mid10row, LK_W10_Mid10row, Beam_W10_Mid10row, BeamNode_W10_Mid10row)
ax11.set_title(f"SW 10m",fontsize =18, x=0.50, y=0.78)

ax12 = plt.subplot(313)
Differ_BCVel(Tie_W1_Mid10row, LK_W1_Mid10row, Beam_W1_Mid10row, BeamNode_W1_Mid10row)
ax12.set_title(f"SW 1m",fontsize =18, x=0.50, y=0.78)

# ax10 = plt.subplot(311)
# Differ_BCVel(Tie_W20_Qua10row, LK_W20_Qua10row, Beam_W20_Qua10row, BeamNode_W20_Qua10row)
# ax10.set_title(f"SW 20m",fontsize =18, x=0.10, y=0.78)

# ax11 = plt.subplot(312)
# Differ_BCVel(Tie_W10_Qua10row, LK_W10_Qua10row, Beam_W10_Qua10row, BeamNode_W10_Qua10row)
# ax11.set_title(f"SW 10m",fontsize =18, x=0.10, y=0.78)

# ax12 = plt.subplot(313)
# Differ_BCVel(Tie_W1_Qua10row, LK_W1_Qua10row, Beam_W1_Qua10row, BeamNode_W1_Qua10row)
# ax12.set_title(f"SW 1m",fontsize =18, x=0.10, y=0.78)

for ax in [ax10,ax11,ax12]:
    formatter = ticker.ScalarFormatter(useMathText =True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set(size=18)
    ax.xaxis.get_offset_text().set(size=18)
# ============ Find Positive and Negative Peaks ================================== 
# x =  Tie_W20_Mid80row[:,2]
# positive_peaks, _ = find_peaks(x)
# x_inverted = -x
# negative_peaks, _ = find_peaks(x_inverted)
def Find_Peaks(Tie_W20_Mid80row):
    listID = []
    for i in range(1,len(Tie_W20_Mid80row)-1):
        if abs(Tie_W20_Mid80row[i,2]) > abs(Tie_W20_Mid80row[i-1,2]) and abs(Tie_W20_Mid80row[i,2]) > abs(Tie_W20_Mid80row[i+1,2]):
            listID.append(i)
    return listID

def Add_Peaks(Tie20_Mid80List,Tie_W20_Mid80row, PeakTie20_Mid80):
    for k in range(len(PeakTie20_Mid80)): 
        Id = Tie20_Mid80List[k]    
        # print(Id)
        PeakTie20_Mid80[k,0] = Tie_W20_Mid80row[Id,0]
        PeakTie20_Mid80[k,1] = Tie_W20_Mid80row[Id,2]
# ========================  Middle Node ==============================
# -------------- Tie BC -------------------
Tie20_Mid80List = Find_Peaks(Tie_W20_Mid80row)
PeakTie20_Mid80 = np.zeros((len(Tie20_Mid80List),2))
Add_Peaks(Tie20_Mid80List,Tie_W20_Mid80row, PeakTie20_Mid80)

Tie20_Mid40List = Find_Peaks(Tie_W20_Mid40row)
PeakTie20_Mid40 = np.zeros((len(Tie20_Mid40List),2))
Add_Peaks(Tie20_Mid40List,Tie_W20_Mid40row, PeakTie20_Mid40)

Tie20_Mid20List = Find_Peaks(Tie_W20_Mid20row)
PeakTie20_Mid20 = np.zeros((len(Tie20_Mid20List),2))
Add_Peaks(Tie20_Mid20List,Tie_W20_Mid20row, PeakTie20_Mid20)

Tie20_Mid10List = Find_Peaks(Tie_W20_Mid10row)
PeakTie20_Mid10 = np.zeros((len(Tie20_Mid10List),2))
Add_Peaks(Tie20_Mid10List,Tie_W20_Mid10row, PeakTie20_Mid10)

Tie10_Mid80List = Find_Peaks(Tie_W10_Mid80row)
PeakTie10_Mid80 = np.zeros((len(Tie10_Mid80List),2))
Add_Peaks(Tie10_Mid80List, Tie_W10_Mid80row, PeakTie10_Mid80)

Tie10_Mid40List = Find_Peaks(Tie_W10_Mid40row)
PeakTie10_Mid40 = np.zeros((len(Tie10_Mid40List),2))
Add_Peaks(Tie10_Mid40List, Tie_W10_Mid40row, PeakTie10_Mid40)

Tie10_Mid20List = Find_Peaks(Tie_W10_Mid20row)
PeakTie10_Mid20 = np.zeros((len(Tie10_Mid20List),2))
Add_Peaks(Tie10_Mid20List, Tie_W10_Mid20row, PeakTie10_Mid20)

Tie10_Mid10List = Find_Peaks(Tie_W10_Mid10row)
PeakTie10_Mid10 = np.zeros((len(Tie10_Mid10List),2))
Add_Peaks(Tie10_Mid10List, Tie_W10_Mid10row, PeakTie10_Mid10)

Tie1_Mid80List = Find_Peaks(Tie_W1_Mid80row)
PeakTie1_Mid80 = np.zeros((len(Tie1_Mid80List),2))
Add_Peaks(Tie1_Mid80List, Tie_W1_Mid80row, PeakTie1_Mid80)

Tie1_Mid40List = Find_Peaks(Tie_W1_Mid40row)
PeakTie1_Mid40 = np.zeros((len(Tie1_Mid40List),2))
Add_Peaks(Tie1_Mid40List, Tie_W1_Mid40row, PeakTie1_Mid40)

Tie1_Mid20List = Find_Peaks(Tie_W1_Mid20row)
PeakTie1_Mid20 = np.zeros((len(Tie1_Mid20List),2))
Add_Peaks(Tie1_Mid20List, Tie_W1_Mid20row, PeakTie1_Mid20)

Tie1_Mid10List = Find_Peaks(Tie_W1_Mid10row)
PeakTie1_Mid10 = np.zeros((len(Tie1_Mid10List),2))
Add_Peaks(Tie1_Mid10List,Tie_W1_Mid10row, PeakTie1_Mid10)

# -------------- LK Dashpot BC -------------------
LK20_Mid80List = Find_Peaks(LK_W20_Mid80row)
PeakLK20_Mid80 = np.zeros((len(LK20_Mid80List),2))
Add_Peaks(LK20_Mid80List,LK_W20_Mid80row, PeakLK20_Mid80)

LK20_Mid40List = Find_Peaks(LK_W20_Mid40row)
PeakLK20_Mid40 = np.zeros((len(LK20_Mid40List),2))
Add_Peaks(LK20_Mid40List,LK_W20_Mid40row, PeakLK20_Mid40)

LK20_Mid20List = Find_Peaks(LK_W20_Mid20row)
PeakLK20_Mid20 = np.zeros((len(LK20_Mid20List),2))
Add_Peaks(LK20_Mid20List, LK_W20_Mid20row, PeakLK20_Mid20)

LK20_Mid10List = Find_Peaks(LK_W20_Mid10row)
PeakLK20_Mid10 = np.zeros((len(LK20_Mid10List),2))
Add_Peaks(LK20_Mid10List,LK_W20_Mid10row, PeakLK20_Mid10)

LK10_Mid80List = Find_Peaks(LK_W10_Mid80row)
PeakLK10_Mid80 = np.zeros((len(LK10_Mid80List),2))
Add_Peaks(LK10_Mid80List, LK_W10_Mid80row, PeakLK10_Mid80)

LK10_Mid40List = Find_Peaks(LK_W10_Mid40row)
PeakLK10_Mid40 = np.zeros((len(LK10_Mid40List),2))
Add_Peaks(LK10_Mid40List, LK_W10_Mid40row, PeakLK10_Mid40)

LK10_Mid20List = Find_Peaks(LK_W10_Mid20row)
PeakLK10_Mid20 = np.zeros((len(LK10_Mid20List),2))
Add_Peaks(LK10_Mid20List, LK_W10_Mid20row, PeakLK10_Mid20)

LK10_Mid10List = Find_Peaks(LK_W10_Mid10row)
PeakLK10_Mid10 = np.zeros((len(LK10_Mid10List),2))
Add_Peaks(LK10_Mid10List, LK_W10_Mid10row, PeakLK10_Mid10)

LK1_Mid80List = Find_Peaks(LK_W1_Mid80row)
PeakLK1_Mid80 = np.zeros((len(LK1_Mid80List),2))
Add_Peaks(LK1_Mid80List, LK_W1_Mid80row, PeakLK1_Mid80)

LK1_Mid40List = Find_Peaks(LK_W1_Mid40row)
PeakLK1_Mid40 = np.zeros((len(LK1_Mid40List),2))
Add_Peaks(LK1_Mid40List, LK_W1_Mid40row, PeakLK1_Mid40)

LK1_Mid20List = Find_Peaks(LK_W1_Mid20row)
PeakLK1_Mid20 = np.zeros((len(LK1_Mid20List),2))
Add_Peaks(LK1_Mid20List, LK_W1_Mid20row, PeakLK1_Mid20)

LK1_Mid10List = Find_Peaks(LK_W1_Mid10row)
PeakLK1_Mid10 = np.zeros((len(LK1_Mid10List),2))
Add_Peaks(LK1_Mid10List,LK_W1_Mid10row, PeakLK1_Mid10)

# -------------- Distributed Beam Boundary Condition -------------------
Beam20_Mid80List = Find_Peaks(Beam_W20_Mid80row)
PeakBeam20_Mid80 = np.zeros((len(Beam20_Mid80List),2))
Add_Peaks(Beam20_Mid80List, Beam_W20_Mid80row, PeakBeam20_Mid80)

Beam20_Mid40List = Find_Peaks(Beam_W20_Mid40row)
PeakBeam20_Mid40 = np.zeros((len(Beam20_Mid40List),2))
Add_Peaks(Beam20_Mid40List, Beam_W20_Mid40row, PeakBeam20_Mid40)

Beam20_Mid20List = Find_Peaks(Beam_W20_Mid20row)
PeakBeam20_Mid20 = np.zeros((len(Beam20_Mid20List),2))
Add_Peaks(Beam20_Mid20List, Beam_W20_Mid20row, PeakBeam20_Mid20)

Beam20_Mid10List = Find_Peaks(Beam_W20_Mid10row)
PeakBeam20_Mid10 = np.zeros((len(Beam20_Mid10List),2))
Add_Peaks(Beam20_Mid10List,Beam_W20_Mid10row, PeakBeam20_Mid10)

Beam10_Mid80List = Find_Peaks(Beam_W10_Mid80row)
PeakBeam10_Mid80 = np.zeros((len(Beam10_Mid80List),2))
Add_Peaks(Beam10_Mid80List, Beam_W10_Mid80row, PeakBeam10_Mid80)

Beam10_Mid40List = Find_Peaks(Beam_W10_Mid40row)
PeakBeam10_Mid40 = np.zeros((len(Beam10_Mid40List),2))
Add_Peaks(Beam10_Mid40List, Beam_W10_Mid40row, PeakBeam10_Mid40)

Beam10_Mid20List = Find_Peaks(Beam_W10_Mid20row)
PeakBeam10_Mid20 = np.zeros((len(Beam10_Mid20List),2))
Add_Peaks(Beam10_Mid20List, Beam_W10_Mid20row, PeakBeam10_Mid20)

Beam10_Mid10List = Find_Peaks(Beam_W10_Mid10row)
PeakBeam10_Mid10 = np.zeros((len(Beam10_Mid10List),2))
Add_Peaks(Beam10_Mid10List, Beam_W10_Mid10row, PeakBeam10_Mid10)

Beam1_Mid80List = Find_Peaks(Beam_W1_Mid80row)
PeakBeam1_Mid80 = np.zeros((len(Beam1_Mid80List),2))
Add_Peaks(Beam1_Mid80List, Beam_W1_Mid80row, PeakBeam1_Mid80)

Beam1_Mid40List = Find_Peaks(Beam_W1_Mid40row)
PeakBeam1_Mid40 = np.zeros((len(Beam1_Mid40List),2))
Add_Peaks(Beam1_Mid40List, Beam_W1_Mid40row, PeakBeam1_Mid40)

Beam1_Mid20List = Find_Peaks(Beam_W1_Mid20row)
PeakBeam1_Mid20 = np.zeros((len(Beam1_Mid20List),2))
Add_Peaks(Beam1_Mid20List, Beam_W1_Mid20row, PeakBeam1_Mid20)

Beam1_Mid10List = Find_Peaks(Beam_W1_Mid10row)
PeakBeam1_Mid10 = np.zeros((len(Beam1_Mid10List),2))
Add_Peaks(Beam1_Mid10List,Beam_W1_Mid10row, PeakBeam1_Mid10)

# -------------- Distributed Beam and Node Boundary Condition -------------------
BeamNode20_Mid80List = Find_Peaks(BeamNode_W20_Mid80row)
PeakBeamNode20_Mid80 = np.zeros((len(BeamNode20_Mid80List),2))
Add_Peaks(BeamNode20_Mid80List, BeamNode_W20_Mid80row, PeakBeamNode20_Mid80)

BeamNode20_Mid40List = Find_Peaks(BeamNode_W20_Mid40row)
PeakBeamNode20_Mid40 = np.zeros((len(BeamNode20_Mid40List),2))
Add_Peaks(BeamNode20_Mid40List, BeamNode_W20_Mid40row, PeakBeamNode20_Mid40)

BeamNode20_Mid20List = Find_Peaks(BeamNode_W20_Mid20row)
PeakBeamNode20_Mid20 = np.zeros((len(BeamNode20_Mid20List),2))
Add_Peaks(BeamNode20_Mid20List, BeamNode_W20_Mid20row, PeakBeamNode20_Mid20)

BeamNode20_Mid10List = Find_Peaks(BeamNode_W20_Mid10row)
PeakBeamNode20_Mid10 = np.zeros((len(BeamNode20_Mid10List),2))
Add_Peaks(BeamNode20_Mid10List,BeamNode_W20_Mid10row, PeakBeamNode20_Mid10)

BeamNode10_Mid80List = Find_Peaks(BeamNode_W10_Mid80row)
PeakBeamNode10_Mid80 = np.zeros((len(BeamNode10_Mid80List),2))
Add_Peaks(BeamNode10_Mid80List, BeamNode_W10_Mid80row, PeakBeamNode10_Mid80)

BeamNode10_Mid40List = Find_Peaks(BeamNode_W10_Mid40row)
PeakBeamNode10_Mid40 = np.zeros((len(BeamNode10_Mid40List),2))
Add_Peaks(BeamNode10_Mid40List, BeamNode_W10_Mid40row, PeakBeamNode10_Mid40)

BeamNode10_Mid20List = Find_Peaks(BeamNode_W10_Mid20row)
PeakBeamNode10_Mid20 = np.zeros((len(BeamNode10_Mid20List),2))
Add_Peaks(BeamNode10_Mid20List, BeamNode_W10_Mid20row, PeakBeamNode10_Mid20)

BeamNode10_Mid10List = Find_Peaks(BeamNode_W10_Mid10row)
PeakBeamNode10_Mid10 = np.zeros((len(BeamNode10_Mid10List),2))
Add_Peaks(BeamNode10_Mid10List, BeamNode_W10_Mid10row, PeakBeamNode10_Mid10)

BeamNode1_Mid80List = Find_Peaks(BeamNode_W1_Mid80row)
PeakBeamNode1_Mid80 = np.zeros((len(BeamNode1_Mid80List),2))
Add_Peaks(BeamNode1_Mid80List, BeamNode_W1_Mid80row, PeakBeamNode1_Mid80)

BeamNode1_Mid40List = Find_Peaks(BeamNode_W1_Mid40row)
PeakBeamNode1_Mid40 = np.zeros((len(BeamNode1_Mid40List),2))
Add_Peaks(BeamNode1_Mid40List, BeamNode_W1_Mid40row, PeakBeamNode1_Mid40)

BeamNode1_Mid20List = Find_Peaks(BeamNode_W1_Mid20row)
PeakBeamNode1_Mid20 = np.zeros((len(BeamNode1_Mid20List),2))
Add_Peaks(BeamNode1_Mid20List, BeamNode_W1_Mid20row, PeakBeamNode1_Mid20)

BeamNode1_Mid10List = Find_Peaks(BeamNode_W1_Mid10row)
PeakBeamNode1_Mid10 = np.zeros((len(BeamNode1_Mid10List),2))
Add_Peaks(BeamNode1_Mid10List, BeamNode_W1_Mid10row, PeakBeamNode1_Mid10)

# ========================  Three-Quarter Node ==============================
# -------------- Tie BC -------------------
Tie20_Qua80List = Find_Peaks(Tie_W20_Qua80row)
PeakTie20_Qua80 = np.zeros((len(Tie20_Qua80List),2))
Add_Peaks(Tie20_Qua80List, Tie_W20_Qua80row, PeakTie20_Qua80)

Tie20_Qua40List = Find_Peaks(Tie_W20_Qua40row)
PeakTie20_Qua40 = np.zeros((len(Tie20_Qua40List),2))
Add_Peaks(Tie20_Qua40List, Tie_W20_Qua40row, PeakTie20_Qua40)

Tie20_Qua20List = Find_Peaks(Tie_W20_Qua20row)
PeakTie20_Qua20 = np.zeros((len(Tie20_Qua20List),2))
Add_Peaks(Tie20_Qua20List, Tie_W20_Qua20row, PeakTie20_Qua20)

Tie20_Qua10List = Find_Peaks(Tie_W20_Qua10row)
PeakTie20_Qua10 = np.zeros((len(Tie20_Qua10List),2))
Add_Peaks(Tie20_Qua10List, Tie_W20_Qua10row, PeakTie20_Qua10)

Tie10_Qua80List = Find_Peaks(Tie_W10_Qua80row)
PeakTie10_Qua80 = np.zeros((len(Tie10_Qua80List),2))
Add_Peaks(Tie10_Qua80List, Tie_W10_Qua80row, PeakTie10_Qua80)

Tie10_Qua40List = Find_Peaks(Tie_W10_Qua40row)
PeakTie10_Qua40 = np.zeros((len(Tie10_Qua40List),2))
Add_Peaks(Tie10_Qua40List, Tie_W10_Qua40row, PeakTie10_Qua40)

Tie10_Qua20List = Find_Peaks(Tie_W10_Qua20row)
PeakTie10_Qua20 = np.zeros((len(Tie10_Qua20List),2))
Add_Peaks(Tie10_Qua20List, Tie_W10_Qua20row, PeakTie10_Qua20)

Tie10_Qua10List = Find_Peaks(Tie_W10_Qua10row)
PeakTie10_Qua10 = np.zeros((len(Tie10_Qua10List),2))
Add_Peaks(Tie10_Qua10List, Tie_W10_Qua10row, PeakTie10_Qua10)

Tie1_Qua80List = Find_Peaks(Tie_W1_Qua80row)
PeakTie1_Qua80 = np.zeros((len(Tie1_Qua80List),2))
Add_Peaks(Tie1_Qua80List, Tie_W1_Qua80row, PeakTie1_Qua80)

Tie1_Qua40List = Find_Peaks(Tie_W1_Qua40row)
PeakTie1_Qua40 = np.zeros((len(Tie1_Qua40List),2))
Add_Peaks(Tie1_Qua40List, Tie_W1_Qua40row, PeakTie1_Qua40)

Tie1_Qua20List = Find_Peaks(Tie_W1_Qua20row)
PeakTie1_Qua20 = np.zeros((len(Tie1_Qua20List),2))
Add_Peaks(Tie1_Qua20List, Tie_W1_Qua20row, PeakTie1_Qua20)

Tie1_Qua10List = Find_Peaks(Tie_W1_Qua10row)
PeakTie1_Qua10 = np.zeros((len(Tie1_Qua10List),2))
Add_Peaks(Tie1_Qua10List,Tie_W1_Qua10row, PeakTie1_Qua10)

# -------------- LK Dashpot BC -------------------
LK20_Qua80List = Find_Peaks(LK_W20_Qua80row)
PeakLK20_Qua80 = np.zeros((len(LK20_Qua80List),2))
Add_Peaks(LK20_Qua80List,LK_W20_Qua80row, PeakLK20_Qua80)

LK20_Qua40List = Find_Peaks(LK_W20_Qua40row)
PeakLK20_Qua40 = np.zeros((len(LK20_Qua40List),2))
Add_Peaks(LK20_Qua40List,LK_W20_Qua40row, PeakLK20_Qua40)

LK20_Qua20List = Find_Peaks(LK_W20_Qua20row)
PeakLK20_Qua20 = np.zeros((len(LK20_Qua20List),2))
Add_Peaks(LK20_Qua20List, LK_W20_Qua20row, PeakLK20_Qua20)

LK20_Qua10List = Find_Peaks(LK_W20_Qua10row)
PeakLK20_Qua10 = np.zeros((len(LK20_Qua10List),2))
Add_Peaks(LK20_Qua10List,LK_W20_Qua10row, PeakLK20_Qua10)

LK10_Qua80List = Find_Peaks(LK_W10_Qua80row)
PeakLK10_Qua80 = np.zeros((len(LK10_Qua80List),2))
Add_Peaks(LK10_Qua80List, LK_W10_Qua80row, PeakLK10_Qua80)

LK10_Qua40List = Find_Peaks(LK_W10_Qua40row)
PeakLK10_Qua40 = np.zeros((len(LK10_Qua40List),2))
Add_Peaks(LK10_Qua40List, LK_W10_Qua40row, PeakLK10_Qua40)

LK10_Qua20List = Find_Peaks(LK_W10_Qua20row)
PeakLK10_Qua20 = np.zeros((len(LK10_Qua20List),2))
Add_Peaks(LK10_Qua20List, LK_W10_Qua20row, PeakLK10_Qua20)

LK10_Qua10List = Find_Peaks(LK_W10_Qua10row)
PeakLK10_Qua10 = np.zeros((len(LK10_Qua10List),2))
Add_Peaks(LK10_Qua10List, LK_W10_Qua10row, PeakLK10_Qua10)

LK1_Qua80List = Find_Peaks(LK_W1_Qua80row)
PeakLK1_Qua80 = np.zeros((len(LK1_Qua80List),2))
Add_Peaks(LK1_Qua80List, LK_W1_Qua80row, PeakLK1_Qua80)

LK1_Qua40List = Find_Peaks(LK_W1_Qua40row)
PeakLK1_Qua40 = np.zeros((len(LK1_Qua40List),2))
Add_Peaks(LK1_Qua40List, LK_W1_Qua40row, PeakLK1_Qua40)

LK1_Qua20List = Find_Peaks(LK_W1_Qua20row)
PeakLK1_Qua20 = np.zeros((len(LK1_Qua20List),2))
Add_Peaks(LK1_Qua20List, LK_W1_Qua20row, PeakLK1_Qua20)

LK1_Qua10List = Find_Peaks(LK_W1_Qua10row)
PeakLK1_Qua10 = np.zeros((len(LK1_Qua10List),2))
Add_Peaks(LK1_Qua10List,LK_W1_Qua10row, PeakLK1_Qua10)

# -------------- Distributed Beam Boundary Condition -------------------
Beam20_Qua80List = Find_Peaks(Beam_W20_Qua80row)
PeakBeam20_Qua80 = np.zeros((len(Beam20_Qua80List),2))
Add_Peaks(Beam20_Qua80List, Beam_W20_Qua80row, PeakBeam20_Qua80)

Beam20_Qua40List = Find_Peaks(Beam_W20_Qua40row)
PeakBeam20_Qua40 = np.zeros((len(Beam20_Qua40List),2))
Add_Peaks(Beam20_Qua40List, Beam_W20_Qua40row, PeakBeam20_Qua40)

Beam20_Qua20List = Find_Peaks(Beam_W20_Qua20row)
PeakBeam20_Qua20 = np.zeros((len(Beam20_Qua20List),2))
Add_Peaks(Beam20_Qua20List, Beam_W20_Qua20row, PeakBeam20_Qua20)

Beam20_Qua10List = Find_Peaks(Beam_W20_Qua10row)
PeakBeam20_Qua10 = np.zeros((len(Beam20_Qua10List),2))
Add_Peaks(Beam20_Qua10List,Beam_W20_Qua10row, PeakBeam20_Qua10)

Beam10_Qua80List = Find_Peaks(Beam_W10_Qua80row)
PeakBeam10_Qua80 = np.zeros((len(Beam10_Qua80List),2))
Add_Peaks(Beam10_Qua80List, Beam_W10_Qua80row, PeakBeam10_Qua80)

Beam10_Qua40List = Find_Peaks(Beam_W10_Qua40row)
PeakBeam10_Qua40 = np.zeros((len(Beam10_Qua40List),2))
Add_Peaks(Beam10_Qua40List, Beam_W10_Qua40row, PeakBeam10_Qua40)

Beam10_Qua20List = Find_Peaks(Beam_W10_Qua20row)
PeakBeam10_Qua20 = np.zeros((len(Beam10_Qua20List),2))
Add_Peaks(Beam10_Qua20List, Beam_W10_Qua20row, PeakBeam10_Qua20)

Beam10_Qua10List = Find_Peaks(Beam_W10_Qua10row)
PeakBeam10_Qua10 = np.zeros((len(Beam10_Qua10List),2))
Add_Peaks(Beam10_Qua10List, Beam_W10_Qua10row, PeakBeam10_Qua10)

Beam1_Qua80List = Find_Peaks(Beam_W1_Qua80row)
PeakBeam1_Qua80 = np.zeros((len(Beam1_Qua80List),2))
Add_Peaks(Beam1_Qua80List, Beam_W1_Qua80row, PeakBeam1_Qua80)

Beam1_Qua40List = Find_Peaks(Beam_W1_Qua40row)
PeakBeam1_Qua40 = np.zeros((len(Beam1_Qua40List),2))
Add_Peaks(Beam1_Qua40List, Beam_W1_Qua40row, PeakBeam1_Qua40)

Beam1_Qua20List = Find_Peaks(Beam_W1_Qua20row)
PeakBeam1_Qua20 = np.zeros((len(Beam1_Qua20List),2))
Add_Peaks(Beam1_Qua20List, Beam_W1_Qua20row, PeakBeam1_Qua20)

Beam1_Qua10List = Find_Peaks(Beam_W1_Qua10row)
PeakBeam1_Qua10 = np.zeros((len(Beam1_Qua10List),2))
Add_Peaks(Beam1_Qua10List,Beam_W1_Qua10row, PeakBeam1_Qua10)

# -------------- Distributed Beam and Node Boundary Condition -------------------
BeamNode20_Qua80List = Find_Peaks(BeamNode_W20_Qua80row)
PeakBeamNode20_Qua80 = np.zeros((len(BeamNode20_Qua80List),2))
Add_Peaks(BeamNode20_Qua80List, BeamNode_W20_Qua80row, PeakBeamNode20_Qua80)

BeamNode20_Qua40List = Find_Peaks(BeamNode_W20_Qua40row)
PeakBeamNode20_Qua40 = np.zeros((len(BeamNode20_Qua40List),2))
Add_Peaks(BeamNode20_Qua40List, BeamNode_W20_Qua40row, PeakBeamNode20_Qua40)

BeamNode20_Qua20List = Find_Peaks(BeamNode_W20_Qua20row)
PeakBeamNode20_Qua20 = np.zeros((len(BeamNode20_Qua20List),2))
Add_Peaks(BeamNode20_Qua20List, BeamNode_W20_Qua20row, PeakBeamNode20_Qua20)

BeamNode20_Qua10List = Find_Peaks(BeamNode_W20_Qua10row)
PeakBeamNode20_Qua10 = np.zeros((len(BeamNode20_Qua10List),2))
Add_Peaks(BeamNode20_Qua10List,BeamNode_W20_Qua10row, PeakBeamNode20_Qua10)

BeamNode10_Qua80List = Find_Peaks(BeamNode_W10_Qua80row)
PeakBeamNode10_Qua80 = np.zeros((len(BeamNode10_Qua80List),2))
Add_Peaks(BeamNode10_Qua80List, BeamNode_W10_Qua80row, PeakBeamNode10_Qua80)

BeamNode10_Qua40List = Find_Peaks(BeamNode_W10_Qua40row)
PeakBeamNode10_Qua40 = np.zeros((len(BeamNode10_Qua40List),2))
Add_Peaks(BeamNode10_Qua40List, BeamNode_W10_Qua40row, PeakBeamNode10_Qua40)

BeamNode10_Qua20List = Find_Peaks(BeamNode_W10_Qua20row)
PeakBeamNode10_Qua20 = np.zeros((len(BeamNode10_Qua20List),2))
Add_Peaks(BeamNode10_Qua20List, BeamNode_W10_Qua20row, PeakBeamNode10_Qua20)

BeamNode10_Qua10List = Find_Peaks(BeamNode_W10_Qua10row)
PeakBeamNode10_Qua10 = np.zeros((len(BeamNode10_Qua10List),2))
Add_Peaks(BeamNode10_Qua10List, BeamNode_W10_Qua10row, PeakBeamNode10_Qua10)

BeamNode1_Qua80List = Find_Peaks(BeamNode_W1_Qua80row)
PeakBeamNode1_Qua80 = np.zeros((len(BeamNode1_Qua80List),2))
Add_Peaks(BeamNode1_Qua80List, BeamNode_W1_Qua80row, PeakBeamNode1_Qua80)

BeamNode1_Qua40List = Find_Peaks(BeamNode_W1_Qua40row)
PeakBeamNode1_Qua40 = np.zeros((len(BeamNode1_Qua40List),2))
Add_Peaks(BeamNode1_Qua40List, BeamNode_W1_Qua40row, PeakBeamNode1_Qua40)

BeamNode1_Qua20List = Find_Peaks(BeamNode_W1_Qua20row)
PeakBeamNode1_Qua20 = np.zeros((len(BeamNode1_Qua20List),2))
Add_Peaks(BeamNode1_Qua20List, BeamNode_W1_Qua20row, PeakBeamNode1_Qua20)

BeamNode1_Qua10List = Find_Peaks(BeamNode_W1_Qua10row)
PeakBeamNode1_Qua10 = np.zeros((len(BeamNode1_Qua10List),2))
Add_Peaks(BeamNode1_Qua10List, BeamNode_W1_Qua10row, PeakBeamNode1_Qua10)

# =========== Find Grounf Surface Max/ Min Peak Value in 0.0267~0.0534 ==========================
Analysis_column = 99

def Find_ColMaxValue(title,start_time, end_time ,ele80_Mid):
    time_column = 0
    mask = (ele80_Mid[:, time_column] >= start_time) & (ele80_Mid[:, time_column] <= end_time)
    
    ColumnIndex = 1
    max_value = np.max(ele80_Mid[mask, ColumnIndex])
    min_value = np.min(ele80_Mid[mask, ColumnIndex])
    max_peak_index = np.argmax(ele80_Mid[mask, ColumnIndex])
    min_peak_index = np.argmin(ele80_Mid[mask, ColumnIndex])

    print(title+ f' max_value= {max_value}; max_Time= {ele80_Mid[max_peak_index,0]}; min_value= {min_value}; min_Time= {ele80_Mid[min_peak_index,0]}')
    # print(title, f'min_value= {min_value}; min_index= {ele80_Mid[min_peak_index,0]}')
    return(max_value,min_value)
# --------------20m Tie BC -------------------            
maxTie20_Mid80, minTie20_Mid80 = Find_ColMaxValue('Tie20_Mid80',0.0267, 0.06 ,PeakTie20_Mid80)
maxTie20_Mid40, minTie20_Mid40 = Find_ColMaxValue('Tie20_Mid40',0.0267, 0.06 ,PeakTie20_Mid40)
maxTie20_Mid20, minTie20_Mid20 = Find_ColMaxValue('Tie20_Mid20',0.0267, 0.06 ,PeakTie20_Mid20)
maxTie20_Mid10, minTie20_Mid10 = Find_ColMaxValue('Tie20_Mid10',0.0267, 0.06 ,PeakTie20_Mid10)
# --------------20m LK Dashpot BC -------------------
maxLK20_Mid80, minLK20_Mid80 = Find_ColMaxValue('LK20_Mid80',0.0267, 0.06 ,PeakLK20_Mid80)
maxLK20_Mid40, minLK20_Mid40 = Find_ColMaxValue('LK20_Mid40',0.0267, 0.06 ,PeakLK20_Mid40)
maxLK20_Mid20, minLK20_Mid20 = Find_ColMaxValue('LK20_Mid20',0.0267, 0.06 ,PeakLK20_Mid20)
maxLK20_Mid10, minLK20_Mid10 = Find_ColMaxValue('LK20_Mid10',0.0267, 0.06 ,PeakLK20_Mid10)
# --------------20m Distributed Beam Boundary Condition -------------------
maxBeam20_Mid80, minBeam20_Mid80 = Find_ColMaxValue('Beam20_Mid80',0.0267, 0.06 ,PeakBeam20_Mid80)
maxBeam20_Mid40, minBeam20_Mid40 = Find_ColMaxValue('Beam20_Mid40',0.0267, 0.06 ,PeakBeam20_Mid40)
maxBeam20_Mid20, minBeam20_Mid20 = Find_ColMaxValue('Beam20_Mid20',0.0267, 0.06 ,PeakBeam20_Mid20)
maxBeam20_Mid10, minBeam20_Mid10 = Find_ColMaxValue('Beam20_Mid10',0.0267, 0.06 ,PeakBeam20_Mid10)
# --------------20m Distributed Beam and Node Boundary Condition ------------------
maxBeamNode20_Mid80, minBeamNode20_Mid80 = Find_ColMaxValue('BeamNode20_Mid80',0.0267, 0.06 ,PeakBeamNode20_Mid80)
maxBeamNode20_Mid40, minBeamNode20_Mid40 = Find_ColMaxValue('BeamNode20_Mid40',0.0267, 0.06 ,PeakBeamNode20_Mid40)
maxBeamNode20_Mid20, minBeamNode20_Mid20 = Find_ColMaxValue('BeamNode20_Mid20',0.0267, 0.06 ,PeakBeamNode20_Mid20)
maxBeamNode20_Mid10, minBeamNode20_Mid10 = Find_ColMaxValue('BeamNode20_Mid10',0.0267, 0.06 ,PeakBeamNode20_Mid10)

# --------------10m Tie BC -------------------            
maxTie10_Mid80, minTie10_Mid80 = Find_ColMaxValue('Tie10_Mid80',0.0267, 0.06 ,PeakTie10_Mid80)
maxTie10_Mid40, minTie10_Mid40 = Find_ColMaxValue('Tie10_Mid40',0.0267, 0.06 ,PeakTie10_Mid40)
maxTie10_Mid20, minTie10_Mid20 = Find_ColMaxValue('Tie10_Mid20',0.0267, 0.06 ,PeakTie10_Mid20)
maxTie10_Mid10, minTie10_Mid10 = Find_ColMaxValue('Tie10_Mid10',0.0267, 0.06 ,PeakTie10_Mid10)
# --------------10m LK Dashpot BC -------------------
maxLK10_Mid80, minLK10_Mid80 = Find_ColMaxValue('LK10_Mid80',0.0267, 0.06 ,PeakLK10_Mid80)
maxLK10_Mid40, minLK10_Mid40 = Find_ColMaxValue('LK10_Mid40',0.0267, 0.06 ,PeakLK10_Mid40)
maxLK10_Mid20, minLK10_Mid20 = Find_ColMaxValue('LK10_Mid20',0.0267, 0.06 ,PeakLK10_Mid20)
maxLK10_Mid10, minLK10_Mid10 = Find_ColMaxValue('LK10_Mid10',0.0267, 0.06 ,PeakLK10_Mid10)
# --------------10m Distributed Beam Boundary Condition -------------------
maxBeam10_Mid80, minBeam10_Mid80 = Find_ColMaxValue('Beam10_Mid80',0.0267, 0.06 ,PeakBeam10_Mid80)
maxBeam10_Mid40, minBeam10_Mid40 = Find_ColMaxValue('Beam10_Mid40',0.0267, 0.06 ,PeakBeam10_Mid40)
maxBeam10_Mid20, minBeam10_Mid20 = Find_ColMaxValue('Beam10_Mid20',0.0267, 0.06 ,PeakBeam10_Mid20)
maxBeam10_Mid10, minBeam10_Mid10 = Find_ColMaxValue('Beam10_Mid10',0.0267, 0.06 ,PeakBeam10_Mid10)
# --------------10m Distributed Beam and Node Boundary Condition ------------------
maxBeamNode10_Mid80, minBeamNode10_Mid80 = Find_ColMaxValue('BeamNode10_Mid80',0.0267, 0.06 ,PeakBeamNode10_Mid80)
maxBeamNode10_Mid40, minBeamNode10_Mid40 = Find_ColMaxValue('BeamNode10_Mid40',0.0267, 0.06 ,PeakBeamNode10_Mid40)
maxBeamNode10_Mid20, minBeamNode10_Mid20 = Find_ColMaxValue('BeamNode10_Mid20',0.0267, 0.06 ,PeakBeamNode10_Mid20)
maxBeamNode10_Mid10, minBeamNode10_Mid10 = Find_ColMaxValue('BeamNode10_Mid10',0.0267, 0.06 ,PeakBeamNode10_Mid10)

# --------------1m Tie BC -------------------            
maxTie1_Mid80, minTie1_Mid80 = Find_ColMaxValue('Tie1_Mid80',0.0267, 0.06 ,PeakTie1_Mid80)
maxTie1_Mid40, minTie1_Mid40 = Find_ColMaxValue('Tie1_Mid40',0.0267, 0.06 ,PeakTie1_Mid40)
maxTie1_Mid20, minTie1_Mid20 = Find_ColMaxValue('Tie1_Mid20',0.0267, 0.06 ,PeakTie1_Mid20)
maxTie1_Mid10, minTie1_Mid10 = Find_ColMaxValue('Tie1_Mid10',0.0267, 0.06 ,PeakTie1_Mid10)
# --------------1m LK Dashpot BC -------------------
maxLK1_Mid80, minLK1_Mid80 = Find_ColMaxValue('LK1_Mid80',0.0267, 0.06 ,PeakLK1_Mid80)
maxLK1_Mid40, minLK1_Mid40 = Find_ColMaxValue('LK1_Mid40',0.0267, 0.06 ,PeakLK1_Mid40)
maxLK1_Mid20, minLK1_Mid20 = Find_ColMaxValue('LK1_Mid20',0.0267, 0.06 ,PeakLK1_Mid20)
maxLK1_Mid10, minLK1_Mid10 = Find_ColMaxValue('LK1_Mid10',0.0267, 0.06 ,PeakLK1_Mid10)
# --------------1m Distributed Beam Boundary Condition -------------------
maxBeam1_Mid80, minBeam1_Mid80 = Find_ColMaxValue('Beam1_Mid80',0.0267, 0.06 ,PeakBeam1_Mid80)
maxBeam1_Mid40, minBeam1_Mid40 = Find_ColMaxValue('Beam1_Mid40',0.0267, 0.06 ,PeakBeam1_Mid40)
maxBeam1_Mid20, minBeam1_Mid20 = Find_ColMaxValue('Beam1_Mid20',0.0267, 0.06 ,PeakBeam1_Mid20)
maxBeam1_Mid10, minBeam1_Mid10 = Find_ColMaxValue('Beam1_Mid10',0.0267, 0.06 ,PeakBeam1_Mid10)
# --------------1m Distributed Beam and Node Boundary Condition ------------------
maxBeamNode1_Mid80, minBeamNode1_Mid80 = Find_ColMaxValue('BeamNode1_Mid80',0.0267, 0.06 ,PeakBeamNode1_Mid80)
maxBeamNode1_Mid40, minBeamNode1_Mid40 = Find_ColMaxValue('BeamNode1_Mid40',0.0267, 0.06 ,PeakBeamNode1_Mid40)
maxBeamNode1_Mid20, minBeamNode1_Mid20 = Find_ColMaxValue('BeamNode1_Mid20',0.0267, 0.06 ,PeakBeamNode1_Mid20)
maxBeamNode1_Mid10, minBeamNode1_Mid10 = Find_ColMaxValue('BeamNode1_Mid10',0.0267, 0.06 ,PeakBeamNode1_Mid10)
# -------------Make Analysis Solution as Mesh size minium with Tie BC ----------------------------
MaxAnalysis = maxTie20_Mid80
MinAnalysis = minTie20_Mid80

# ========================  Three-Quarter Node ==============================
# --------------20m Tie BC -------------------            
maxTie20_Qua80, minTie20_Qua80 = Find_ColMaxValue('Tie20_Qua80',0.0267, 0.06 ,PeakTie20_Qua80)
maxTie20_Qua40, minTie20_Qua40 = Find_ColMaxValue('Tie20_Qua40',0.0267, 0.06 ,PeakTie20_Qua40)
maxTie20_Qua20, minTie20_Qua20 = Find_ColMaxValue('Tie20_Qua20',0.0267, 0.06 ,PeakTie20_Qua20)
maxTie20_Qua10, minTie20_Qua10 = Find_ColMaxValue('Tie20_Qua10',0.0267, 0.06 ,PeakTie20_Qua10)
# --------------20m LK Dashpot BC -------------------
maxLK20_Qua80, minLK20_Qua80 = Find_ColMaxValue('LK20_Qua80',0.0267, 0.06 ,PeakLK20_Qua80)
maxLK20_Qua40, minLK20_Qua40 = Find_ColMaxValue('LK20_Qua40',0.0267, 0.06 ,PeakLK20_Qua40)
maxLK20_Qua20, minLK20_Qua20 = Find_ColMaxValue('LK20_Qua20',0.0267, 0.06 ,PeakLK20_Qua20)
maxLK20_Qua10, minLK20_Qua10 = Find_ColMaxValue('LK20_Qua10',0.0267, 0.06 ,PeakLK20_Qua10)
# --------------20m Distributed Beam Boundary Condition -------------------
maxBeam20_Qua80, minBeam20_Qua80 = Find_ColMaxValue('Beam20_Qua80',0.0267, 0.06 ,PeakBeam20_Qua80)
maxBeam20_Qua40, minBeam20_Qua40 = Find_ColMaxValue('Beam20_Qua40',0.0267, 0.06 ,PeakBeam20_Qua40)
maxBeam20_Qua20, minBeam20_Qua20 = Find_ColMaxValue('Beam20_Qua20',0.0267, 0.06 ,PeakBeam20_Qua20)
maxBeam20_Qua10, minBeam20_Qua10 = Find_ColMaxValue('Beam20_Qua10',0.0267, 0.06 ,PeakBeam20_Qua10)
# --------------20m Distributed Beam and Node Boundary Condition ------------------
maxBeamNode20_Qua80, minBeamNode20_Qua80 = Find_ColMaxValue('BeamNode20_Qua80',0.0267, 0.06 ,PeakBeamNode20_Qua80)
maxBeamNode20_Qua40, minBeamNode20_Qua40 = Find_ColMaxValue('BeamNode20_Qua40',0.0267, 0.06 ,PeakBeamNode20_Qua40)
maxBeamNode20_Qua20, minBeamNode20_Qua20 = Find_ColMaxValue('BeamNode20_Qua20',0.0267, 0.06 ,PeakBeamNode20_Qua20)
maxBeamNode20_Qua10, minBeamNode20_Qua10 = Find_ColMaxValue('BeamNode20_Qua10',0.0267, 0.06 ,PeakBeamNode20_Qua10)

# --------------10m Tie BC -------------------            
maxTie10_Qua80, minTie10_Qua80 = Find_ColMaxValue('Tie10_Qua80',0.0267, 0.06 ,PeakTie10_Qua80)
maxTie10_Qua40, minTie10_Qua40 = Find_ColMaxValue('Tie10_Qua40',0.0267, 0.06 ,PeakTie10_Qua40)
maxTie10_Qua20, minTie10_Qua20 = Find_ColMaxValue('Tie10_Qua20',0.0267, 0.06 ,PeakTie10_Qua20)
maxTie10_Qua10, minTie10_Qua10 = Find_ColMaxValue('Tie10_Qua10',0.0267, 0.06 ,PeakTie10_Qua10)
# --------------10m LK Dashpot BC -------------------
maxLK10_Qua80, minLK10_Qua80 = Find_ColMaxValue('LK10_Qua80',0.0267, 0.06 ,PeakLK10_Qua80)
maxLK10_Qua40, minLK10_Qua40 = Find_ColMaxValue('LK10_Qua40',0.0267, 0.06 ,PeakLK10_Qua40)
maxLK10_Qua20, minLK10_Qua20 = Find_ColMaxValue('LK10_Qua20',0.0267, 0.06 ,PeakLK10_Qua20)
maxLK10_Qua10, minLK10_Qua10 = Find_ColMaxValue('LK10_Qua10',0.0267, 0.06 ,PeakLK10_Qua10)
# --------------10m Distributed Beam Boundary Condition -------------------
maxBeam10_Qua80, minBeam10_Qua80 = Find_ColMaxValue('Beam10_Qua80',0.0267, 0.06 ,PeakBeam10_Qua80)
maxBeam10_Qua40, minBeam10_Qua40 = Find_ColMaxValue('Beam10_Qua40',0.0267, 0.06 ,PeakBeam10_Qua40)
maxBeam10_Qua20, minBeam10_Qua20 = Find_ColMaxValue('Beam10_Qua20',0.0267, 0.06 ,PeakBeam10_Qua20)
maxBeam10_Qua10, minBeam10_Qua10 = Find_ColMaxValue('Beam10_Qua10',0.0267, 0.06 ,PeakBeam10_Qua10)
# --------------10m Distributed Beam and Node Boundary Condition ------------------
maxBeamNode10_Qua80, minBeamNode10_Qua80 = Find_ColMaxValue('BeamNode10_Qua80',0.0267, 0.06 ,PeakBeamNode10_Qua80)
maxBeamNode10_Qua40, minBeamNode10_Qua40 = Find_ColMaxValue('BeamNode10_Qua40',0.0267, 0.06 ,PeakBeamNode10_Qua40)
maxBeamNode10_Qua20, minBeamNode10_Qua20 = Find_ColMaxValue('BeamNode10_Qua20',0.0267, 0.06 ,PeakBeamNode10_Qua20)
maxBeamNode10_Qua10, minBeamNode10_Qua10 = Find_ColMaxValue('BeamNode10_Qua10',0.0267, 0.06 ,PeakBeamNode10_Qua10)

# --------------1m Tie BC -------------------            
maxTie1_Qua80, minTie1_Qua80 = Find_ColMaxValue('Tie1_Qua80',0.0267, 0.06 ,PeakTie1_Qua80)
maxTie1_Qua40, minTie1_Qua40 = Find_ColMaxValue('Tie1_Qua40',0.0267, 0.06 ,PeakTie1_Qua40)
maxTie1_Qua20, minTie1_Qua20 = Find_ColMaxValue('Tie1_Qua20',0.0267, 0.06 ,PeakTie1_Qua20)
maxTie1_Qua10, minTie1_Qua10 = Find_ColMaxValue('Tie1_Qua10',0.0267, 0.06 ,PeakTie1_Qua10)
# --------------1m LK Dashpot BC -------------------
maxLK1_Qua80, minLK1_Qua80 = Find_ColMaxValue('LK1_Qua80',0.0267, 0.06 ,PeakLK1_Qua80)
maxLK1_Qua40, minLK1_Qua40 = Find_ColMaxValue('LK1_Qua40',0.0267, 0.06 ,PeakLK1_Qua40)
maxLK1_Qua20, minLK1_Qua20 = Find_ColMaxValue('LK1_Qua20',0.0267, 0.06 ,PeakLK1_Qua20)
maxLK1_Qua10, minLK1_Qua10 = Find_ColMaxValue('LK1_Qua10',0.0267, 0.06 ,PeakLK1_Qua10)
# --------------1m Distributed Beam Boundary Condition -------------------
maxBeam1_Qua80, minBeam1_Qua80 = Find_ColMaxValue('Beam1_Qua80',0.0267, 0.06 ,PeakBeam1_Qua80)
maxBeam1_Qua40, minBeam1_Qua40 = Find_ColMaxValue('Beam1_Qua40',0.0267, 0.06 ,PeakBeam1_Qua40)
maxBeam1_Qua20, minBeam1_Qua20 = Find_ColMaxValue('Beam1_Qua20',0.0267, 0.06 ,PeakBeam1_Qua20)
maxBeam1_Qua10, minBeam1_Qua10 = Find_ColMaxValue('Beam1_Qua10',0.0267, 0.06 ,PeakBeam1_Qua10)
# --------------1m Distributed Beam and Node Boundary Condition ------------------
maxBeamNode1_Qua80, minBeamNode1_Qua80 = Find_ColMaxValue('BeamNode1_Qua80',0.0267, 0.06 ,PeakBeamNode1_Qua80)
maxBeamNode1_Qua40, minBeamNode1_Qua40 = Find_ColMaxValue('BeamNode1_Qua40',0.0267, 0.06 ,PeakBeamNode1_Qua40)
maxBeamNode1_Qua20, minBeamNode1_Qua20 = Find_ColMaxValue('BeamNode1_Qua20',0.0267, 0.06 ,PeakBeamNode1_Qua20)
maxBeamNode1_Qua10, minBeamNode1_Qua10 = Find_ColMaxValue('BeamNode1_Qua10',0.0267, 0.06 ,PeakBeamNode1_Qua10)

# maxAnaly, minAnaly = Find_ColMaxValue(Analysis_column,wave1)
Mesh_Size = np.zeros(4)
Mesh20m_Size = np.zeros(3)

ele = 80 
for m in range(len(Mesh_Size)):
    if m == 0 :    
        Mesh_Size[m] = L/ (ele)
    if m > 0:    
        Mesh_Size[m] = Mesh_Size[m-1]*2
        Mesh20m_Size[m-1] =  Mesh_Size[m]
        
def errMatrix(error_dc,maxTie20_Mid80,minTie20_Mid80,maxTie20_Mid40,minTie20_Mid40,maxTie20_Mid20,minTie20_Mid20,maxTie20_Mid10,minTie20_Mid10):
    error_dc[:,0] = Mesh_Size[:]
    error_dc[0,1] = maxTie20_Mid80
    error_dc[0,2] = minTie20_Mid80
    error_dc[1,1] = maxTie20_Mid40
    error_dc[1,2] = minTie20_Mid40
    error_dc[2,1] = maxTie20_Mid20
    error_dc[2,2] = minTie20_Mid20
    error_dc[3,1] = maxTie20_Mid10
    error_dc[3,2] = minTie20_Mid10
    return error_dc

def err20Mat(error_dc, maxTie20_Mid40,minTie20_Mid40, maxTie20_Mid20,minTie20_Mid20, maxTie20_Mid10,minTie20_Mid10):
    error_dc[:,0] = Mesh20m_Size[:]
    error_dc[0,1] = maxTie20_Mid40
    error_dc[0,2] = minTie20_Mid40
    error_dc[1,1] = maxTie20_Mid20
    error_dc[1,2] = minTie20_Mid20
    error_dc[2,1] = maxTie20_Mid10
    error_dc[2,2] = minTie20_Mid10
    return error_dc
        

# ============================= Middle Node ========================================
# ------------W20m Tie BC Error Peak Value-----------------------
MidTie20_error = np.zeros((3,3))
err20Mat(MidTie20_error,  maxTie20_Mid40,minTie20_Mid40, maxTie20_Mid20,minTie20_Mid20, maxTie20_Mid10,minTie20_Mid10)
# ------------W20m LK BC Error Peak Value-----------------------
MidLK20_error = np.zeros((4,3))
errMatrix(MidLK20_error, maxLK20_Mid80,minLK20_Mid80, maxLK20_Mid40,minLK20_Mid40, maxLK20_Mid20,minLK20_Mid20, maxLK20_Mid10,minLK20_Mid10)
# ------------W20m Distributed Beam BC Error Peak Value-----------------------
MidBeam20_error = np.zeros((4,3))
errMatrix(MidBeam20_error, maxBeam20_Mid80,minBeam20_Mid80, maxBeam20_Mid40,minBeam20_Mid40,maxBeam20_Mid20,minBeam20_Mid20,maxBeam20_Mid10,minBeam20_Mid10)
# ------------W20m Distributed Beam and Node BC Error Peak Value-----------------------
MidBN20_error = np.zeros((4,3))
errMatrix(MidBN20_error, maxBeamNode20_Mid80,minBeamNode20_Mid80, maxBeamNode20_Mid40,minBeamNode20_Mid40,maxBeamNode20_Mid20,minBeamNode20_Mid20,maxBeamNode20_Mid10,minBeamNode20_Mid10)

# ------------W10m Tie BC Error Peak Value-----------------------
MidTie10_error = np.zeros((4,3))
errMatrix(MidTie10_error, maxTie10_Mid80,minTie10_Mid80, maxTie10_Mid40,minTie10_Mid40, maxTie10_Mid20,minTie10_Mid20, maxTie10_Mid10,minTie10_Mid10)
# ------------W10m LK BC Error Peak Value-----------------------
MidLK10_error = np.zeros((4,3))
errMatrix(MidLK10_error, maxLK10_Mid80,minLK10_Mid80, maxLK10_Mid40,minLK10_Mid40, maxLK10_Mid20,minLK10_Mid20, maxLK10_Mid10,minLK10_Mid10)
# ------------W10m Distributed Beam BC Error Peak Value-----------------------
MidBeam10_error = np.zeros((4,3))
errMatrix(MidBeam10_error, maxBeam10_Mid80,minBeam10_Mid80, maxBeam10_Mid40,minBeam10_Mid40, maxBeam10_Mid20,minBeam10_Mid20, maxBeam10_Mid10,minBeam10_Mid10)
# ------------W10m Distributed Beam and Node BC Error Peak Value-----------------------
MidBN10_error = np.zeros((4,3))
errMatrix(MidBN10_error, maxBeamNode10_Mid80,minBeamNode10_Mid80, maxBeamNode10_Mid40,minBeamNode10_Mid40, maxBeamNode10_Mid20,minBeamNode10_Mid20, maxBeamNode10_Mid10,minBeamNode10_Mid10)

# ------------W1m Tie BC Error Peak Value-----------------------
MidTie1_error = np.zeros((4,3))
errMatrix(MidTie1_error, maxTie1_Mid80,minTie1_Mid80, maxTie1_Mid40,minTie1_Mid40, maxTie1_Mid20,minTie1_Mid20, maxTie1_Mid10,minTie1_Mid10)
# ------------W1m LK BC Error Peak Value-----------------------
MidLK1_error = np.zeros((4,3))
errMatrix(MidLK1_error, maxLK1_Mid80,minLK1_Mid80, maxLK1_Mid40,minLK1_Mid40, maxLK1_Mid20,minLK1_Mid20, maxLK1_Mid10,minLK1_Mid10)
# ------------W1m Distributed Beam BC Error Peak Value-----------------------
MidBeam1_error = np.zeros((4,3))
errMatrix(MidBeam1_error, maxBeam1_Mid80,minBeam1_Mid80, maxBeam1_Mid40,minBeam1_Mid40, maxBeam1_Mid20,minBeam1_Mid20, maxBeam1_Mid10,minBeam1_Mid10)
# ------------W1m Distributed Beam and Node BC Error Peak Value-----------------------
MidBN1_error = np.zeros((4,3))
errMatrix(MidBN1_error, maxBeamNode1_Mid80,minBeamNode1_Mid80, maxBeamNode1_Mid40,minBeamNode1_Mid40, maxBeamNode1_Mid20,minBeamNode1_Mid20, maxBeamNode1_Mid10,minBeamNode1_Mid10)

# ============================= Three Quarter Node ====================================================
# ------------W20m Tie BC Error Peak Value-----------------------
QuaTie20_error = np.zeros((4,3))
errMatrix(QuaTie20_error,maxTie20_Qua80,minTie20_Qua80,maxTie20_Qua40,minTie20_Qua40,maxTie20_Qua20,minTie20_Qua20,maxTie20_Qua10,minTie20_Qua10)
# ------------W20m LK BC Error Peak Value-----------------------
QuaLK20_error = np.zeros((4,3))
errMatrix(QuaLK20_error,maxLK20_Qua80,minLK20_Qua80,maxLK20_Qua40,minLK20_Qua40,maxLK20_Qua20,minLK20_Qua20,maxLK20_Qua10,minLK20_Qua10)
# ------------W20m Distributed Beam BC Error Peak Value-----------------------
QuaBeam20_error = np.zeros((4,3))
errMatrix(QuaBeam20_error,maxBeam20_Qua80,minBeam20_Qua80,maxBeam20_Qua40,minBeam20_Qua40,maxBeam20_Qua20,minBeam20_Qua20,maxBeam20_Qua10,minBeam20_Qua10)
# ------------W20m Distributed Beam and Node BC Error Peak Value-----------------------
QuaBN20_error = np.zeros((4,3))
errMatrix(QuaBN20_error,maxBeamNode20_Qua80,minBeamNode20_Qua80,maxBeamNode20_Qua40,minBeamNode20_Qua40,maxBeamNode20_Qua20,minBeamNode20_Qua20,maxBeamNode20_Qua10,minBeamNode20_Qua10)

# ------------W10m Tie BC Error Peak Value-----------------------
QuaTie10_error = np.zeros((4,3))
errMatrix(QuaTie10_error, maxTie10_Qua80,minTie10_Qua80, maxTie10_Qua40,minTie10_Qua40, maxTie10_Qua20,minTie10_Qua20, maxTie10_Qua10,minTie10_Qua10)
# ------------W10m LK BC Error Peak Value-----------------------
QuaLK10_error = np.zeros((4,3))
errMatrix(QuaLK10_error, maxLK10_Qua80,minLK10_Qua80, maxLK10_Qua40,minLK10_Qua40, maxLK10_Qua20,minLK10_Qua20, maxLK10_Qua10,minLK10_Qua10)
# ------------W10m Distributed Beam BC Error Peak Value-----------------------
QuaBeam10_error = np.zeros((4,3))
errMatrix(QuaBeam10_error, maxBeam10_Qua80,minBeam10_Qua80, maxBeam10_Qua40,minBeam10_Qua40, maxBeam10_Qua20,minBeam10_Qua20, maxBeam10_Qua10,minBeam10_Qua10)
# ------------W10m Distributed Beam and Node BC Error Peak Value-----------------------
QuaBN10_error = np.zeros((4,3))
errMatrix(QuaBN10_error, maxBeamNode10_Qua80,minBeamNode10_Qua80, maxBeamNode10_Qua40,minBeamNode10_Qua40, maxBeamNode10_Qua20,minBeamNode10_Qua20, maxBeamNode10_Qua10,minBeamNode10_Qua10)

# ------------W1m Tie BC Error Peak Value-----------------------
QuaTie1_error = np.zeros((4,3))
errMatrix(QuaTie1_error, maxTie1_Qua80,minTie1_Qua80, maxTie1_Qua40,minTie1_Qua40, maxTie1_Qua20,minTie1_Qua20, maxTie1_Qua10,minTie1_Qua10)
# ------------W1m LK BC Error Peak Value-----------------------
QuaLK1_error = np.zeros((4,3))
errMatrix(QuaLK1_error, maxLK1_Qua80,minLK1_Qua80, maxLK1_Qua40,minLK1_Qua40, maxLK1_Qua20,minLK1_Qua20, maxLK1_Qua10,minLK1_Qua10)
# ------------W1m Distributed Beam BC Error Peak Value-----------------------
QuaBeam1_error = np.zeros((4,3))
errMatrix(QuaBeam1_error, maxBeam1_Qua80,minBeam1_Qua80, maxBeam1_Qua40,minBeam1_Qua40, maxBeam1_Qua20,minBeam1_Qua20, maxBeam1_Qua10,minBeam1_Qua10)
# ------------W1m Distributed Beam and Node BC Error Peak Value-----------------------
QuaBN1_error = np.zeros((4,3))
errMatrix(QuaBN1_error, maxBeamNode1_Qua80,minBeamNode1_Qua80, maxBeamNode1_Qua40,minBeamNode1_Qua40, maxBeamNode1_Qua20,minBeamNode1_Qua20, maxBeamNode1_Qua10,minBeamNode1_Qua10)

# calculate_Error()
MidTieErr20 = np.zeros((3,3))
MidLKErr20 = np.zeros((4,3))
MidBeamErr20 = np.zeros((4,3))
MidBNErr20 = np.zeros((4,3))

MidTieErr10 = np.zeros((4,3))
MidLKErr10 = np.zeros((4,3))
MidBeamErr10 = np.zeros((4,3))
MidBNErr10 = np.zeros((4,3))

MidTieErr1 = np.zeros((4,3))
MidLKErr1 = np.zeros((4,3))
MidBeamErr1 = np.zeros((4,3))
MidBNErr1 = np.zeros((4,3))


def Calculate_Error(Mesh_Size, TieErr,Tie_error):
    for i in range(len(Mesh_Size)):
        TieErr[:,0] = Tie_error[:,0]
        TieErr[i,1] = (abs(Tie_error[i,1] - MaxAnalysis)/MaxAnalysis)*100
        TieErr[i,2] = (abs(Tie_error[i,2] - MinAnalysis)/MinAnalysis)*100

        # TieErr[i,1] = ((Tie_error[i,1] - maxAnaly)/maxAnaly)*100
        # TieErr[i,2] = ((Tie_error[i,2] - minAnaly)/minAnaly)*100
# -------- W20 Relative Error --------------   
Calculate_Error(Mesh20m_Size, MidTieErr20, MidTie20_error)
Calculate_Error(Mesh_Size, MidLKErr20, MidLK20_error)      
Calculate_Error(Mesh_Size, MidBeamErr20, MidBeam20_error)
Calculate_Error(Mesh_Size, MidBNErr20, MidBN20_error)   
# -------- W10 Relative Error --------------   
Calculate_Error(Mesh_Size, MidTieErr10, MidTie10_error)
Calculate_Error(Mesh_Size, MidLKErr10, MidLK10_error)      
Calculate_Error(Mesh_Size, MidBeamErr10, MidBeam10_error)
Calculate_Error(Mesh_Size, MidBNErr10, MidBN10_error)   
# -------- W1 Relative Error --------------   
Calculate_Error(Mesh_Size, MidTieErr1, MidTie1_error)
Calculate_Error(Mesh_Size, MidLKErr1, MidLK1_error)      
Calculate_Error(Mesh_Size, MidBeamErr1, MidBeam1_error)
Calculate_Error(Mesh_Size, MidBNErr1, MidBN1_error)   

# ------- Three Quarter Err ----------------
QuaTieErr20 = np.zeros((4,3))
QuaLKErr20 = np.zeros((4,3))
QuaBeamErr20 = np.zeros((4,3))
QuaBNErr20 = np.zeros((4,3))

QuaTieErr10 = np.zeros((4,3))
QuaLKErr10 = np.zeros((4,3))
QuaBeamErr10 = np.zeros((4,3))
QuaBNErr10 = np.zeros((4,3))

QuaTieErr1 = np.zeros((4,3))
QuaLKErr1 = np.zeros((4,3))
QuaBeamErr1 = np.zeros((4,3))
QuaBNErr1 = np.zeros((4,3))

# -------- W20 Relative Error --------------   
Calculate_Error(Mesh_Size, QuaTieErr20, QuaTie20_error)
Calculate_Error(Mesh_Size, QuaLKErr20, QuaLK20_error)      
Calculate_Error(Mesh_Size, QuaBeamErr20, QuaBeam20_error)
Calculate_Error(Mesh_Size, QuaBNErr20, QuaBN20_error)   
# -------- W10 Relative Error --------------   
Calculate_Error(Mesh_Size, QuaTieErr10, QuaTie10_error)
Calculate_Error(Mesh_Size, QuaLKErr10, QuaLK10_error)      
Calculate_Error(Mesh_Size, QuaBeamErr10, QuaBeam10_error)
Calculate_Error(Mesh_Size, QuaBNErr10, QuaBN10_error)   
# -------- W1 Relative Error --------------   
Calculate_Error(Mesh_Size, QuaTieErr1, QuaTie1_error)
Calculate_Error(Mesh_Size, QuaLKErr1, QuaLK1_error)      
Calculate_Error(Mesh_Size, QuaBeamErr1, QuaBeam1_error)
Calculate_Error(Mesh_Size, QuaBNErr1, QuaBN1_error)   


# ------------------------------- Time Increment Relative Error: 20、10、1m (Middle point)-------------------- 
# ==================Draw Relative error : Middele point =============================
def DifferTime_elemetError(Peak,TieErr, LKErr, BeamErr, BNErr):
    # plt.figure(figsize=(8,6))
    font_props = {'family': 'Arial', 'size': 12}
    # plt.xlabel("time t(s)",fontsize= 20)
    # plt.ylabel(r"relative error (%)",fontsize=20)
    # plt.title("Compare Different Boundary Condition: Middle node", fontsize = 18)
    # plt.title(titleName,x=0.25,y=0.35, fontsize = 18)
    
    plt.plot(TieErr[:,0],TieErr[:,Peak],marker = '^',markersize=12,markerfacecolor = 'white',label = 'Tie Boundary Condition')
    plt.plot(LKErr[:,0],LKErr[:,Peak],marker = 'o',markersize=10,markerfacecolor = 'white',label = 'LK Dashpot Boundary Condition')
    plt.plot(BeamErr[:,0],BeamErr[:,Peak],marker = '<',markersize=8,markerfacecolor = 'white',label = 'Distributed Beam Boundary Condition')
    plt.plot(BNErr[:,0],BNErr[:,Peak],marker = 's',markersize=6,markerfacecolor = 'white',label = 'Distributed Beam and Node Boundary Condition')
    
    plt.legend(loc='best',prop=font_props) #ncol=2,fontsize=16 frameon=False
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    # plt.xlim(0.0, 0.20)
    plt.grid(True)

# x_axis = 0.125
figsize = (10,10)
# # ----------------- Middle Node Relative Error -------------------------
# fig5, (ax13,ax14,ax15) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
# fig5.suptitle(f'Ground Surface Different Boundary Maximum Velocity Compare (TopForce) \n(Middle node)',x=0.50,y =0.95,fontsize = 20)
# fig5.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
# fig5.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax13 = plt.subplot(311)
# DifferTime_elemetError(1,MidTieErr20, MidLKErr20, MidBeamErr20, MidBNErr20)
# ax13.set_title(f"SW 20m",fontsize =18, x=0.20, y=0.45)

# ax14 = plt.subplot(312)
# DifferTime_elemetError(1,MidTieErr10, MidLKErr10, MidBeamErr10, MidBNErr10)
# ax14.set_title(f"SW 10m",fontsize =18, x=0.20, y=0.45)

# ax15 = plt.subplot(313)
# DifferTime_elemetError(1,MidTieErr1, MidLKErr1, MidBeamErr1, MidBNErr1)
# ax15.set_title(f"SW 1m",fontsize =18, x=0.20, y=0.65)


# for ax in [ax13,ax14,ax15]:
#     formatter = ticker.ScalarFormatter(useMathText =True)
#     formatter.set_scientific(True)
#     formatter.set_powerlimits((0,0))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
#     ax.yaxis.set_major_formatter(formatter)
#     ax.xaxis.set_major_formatter(formatter)
#     ax.yaxis.get_offset_text().set(size=18)
#     ax.xaxis.get_offset_text().set(size=18)

# fig6, (ax16,ax17,ax18) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
# fig6.suptitle(f'Ground Surface Different Boundary Minimum Velocity Compare (TopForce)\n(Middle node)',x=0.50,y =0.95,fontsize = 20)
# fig6.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
# fig6.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax16 = plt.subplot(311)
# DifferTime_elemetError(2,MidTieErr20, MidLKErr20, MidBeamErr20, MidBNErr20)
# ax16.set_title(f"SW 20m",fontsize =18, x=0.20, y=0.45)

# ax17 = plt.subplot(312)
# DifferTime_elemetError(2,MidTieErr10, MidLKErr10, MidBeamErr10, MidBNErr10)
# ax17.set_title(f"SW 10m",fontsize =18, x=0.20, y=0.45)

# ax18 = plt.subplot(313)
# DifferTime_elemetError(2,MidTieErr1, MidLKErr1, MidBeamErr1, MidBNErr1)
# ax18.set_title(f"SW 1m",fontsize =18, x=0.20, y=0.45)


# for ax in [ax16,ax17,ax18]:
#     formatter = ticker.ScalarFormatter(useMathText =True)
#     formatter.set_scientific(True)
#     formatter.set_powerlimits((0,0))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
#     ax.yaxis.set_major_formatter(formatter)
#     ax.xaxis.set_major_formatter(formatter)
#     ax.yaxis.get_offset_text().set(size=18)
#     ax.xaxis.get_offset_text().set(size=18)
    
# ----------------- Three Quarter Node Relative Error -------------------------
x_axis = 0.125
fig7, (ax19,ax20,ax21) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
fig7.suptitle(f'Ground Surface Different Boundary Maximum Velocity Compare (TopForce)\n(Three Quarter node)',x=0.50,y =0.95,fontsize = 20)
fig7.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
fig7.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

ax19 = plt.subplot(311)
DifferTime_elemetError(1,QuaTieErr20, QuaLKErr20, QuaBeamErr20, QuaBNErr20)
ax19.set_title(f"SW 20m",fontsize =18, x=0.90, y=0.42)

ax20 = plt.subplot(312)
DifferTime_elemetError(1,QuaTieErr10, QuaLKErr10, QuaBeamErr10, QuaBNErr10)
ax20.set_title(f"SW 10m",fontsize =18, x=0.90, y=0.45)

ax21 = plt.subplot(313)
DifferTime_elemetError(1,QuaTieErr1, QuaLKErr1, QuaBeamErr1, QuaBNErr1)
ax21.set_title(f"SW 1m",fontsize =18, x=0.20, y=0.42)

for ax in [ax19,ax20,ax21]:
    formatter = ticker.ScalarFormatter(useMathText =True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set(size=18)
    ax.xaxis.get_offset_text().set(size=18)

fig8, (ax22,ax23,ax24) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
fig8.suptitle(f'Ground Surface Different Boundary Minimum Velocity Compare (TopForce)\n(Three Quarter node)',x=0.50,y =0.95,fontsize = 20)
fig8.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
fig8.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

ax22 = plt.subplot(311)
DifferTime_elemetError(2,QuaTieErr20, QuaLKErr20, QuaBeamErr20, QuaBNErr20)
ax22.set_title(f"SW 20m",fontsize =18, x=0.10, y=0.45)

ax23 = plt.subplot(312)
DifferTime_elemetError(2,QuaTieErr10, QuaLKErr10, QuaBeamErr10, QuaBNErr10)
ax23.set_title(f"SW 10m",fontsize =18, x=0.10, y=0.45)

ax24 = plt.subplot(313)
DifferTime_elemetError(2,QuaTieErr1, QuaLKErr1, QuaBeamErr1, QuaBNErr1)
ax24.set_title(f"SW 1m",fontsize =18, x=0.10, y=0.45)


for ax in [ax22,ax23,ax24]:
    formatter = ticker.ScalarFormatter(useMathText =True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set(size=18)
    ax.xaxis.get_offset_text().set(size=18)

# =============== Time At 0.08~0.10 s Error Compare ===========================
# --------------20m Tie BC -------------------            
T8maxTie20_Mid80, T8minTie20_Mid80 = Find_ColMaxValue('Time0.8 Tie20_Mid80',0.0801, 0.10 ,PeakTie20_Mid80)
T8maxTie20_Mid40, T8minTie20_Mid40 = Find_ColMaxValue('Time0.8 Tie20_Mid40',0.0801, 0.10 ,PeakTie20_Mid40)
T8maxTie20_Mid20, T8minTie20_Mid20 = Find_ColMaxValue('Time0.8 Tie20_Mid20',0.0801, 0.10 ,PeakTie20_Mid20)
T8maxTie20_Mid10, T8minTie20_Mid10 = Find_ColMaxValue('Time0.8 Tie20_Mid10',0.0801, 0.10 ,PeakTie20_Mid10)
# --------------20m LK Dashpot BC -------------------
T8maxLK20_Mid80, T8minLK20_Mid80 = Find_ColMaxValue('Time0.8 LK20_Mid80',0.0801, 0.10 ,PeakLK20_Mid80)
T8maxLK20_Mid40, T8minLK20_Mid40 = Find_ColMaxValue('Time0.8 LK20_Mid40',0.0801, 0.10 ,PeakLK20_Mid40)
T8maxLK20_Mid20, T8minLK20_Mid20 = Find_ColMaxValue('Time0.8 LK20_Mid20',0.0801, 0.10 ,PeakLK20_Mid20)
T8maxLK20_Mid10, T8minLK20_Mid10 = Find_ColMaxValue('Time0.8 LK20_Mid10',0.0801, 0.10 ,PeakLK20_Mid10)
# --------------20m Distributed Beam Boundary Condition -------------------
T8maxBeam20_Mid80, T8minBeam20_Mid80 = Find_ColMaxValue('Time0.8 Beam20_Mid80',0.0801, 0.10 ,PeakBeam20_Mid80)
T8maxBeam20_Mid40, T8minBeam20_Mid40 = Find_ColMaxValue('Time0.8 Beam20_Mid40',0.0801, 0.10 ,PeakBeam20_Mid40)
T8maxBeam20_Mid20, T8minBeam20_Mid20 = Find_ColMaxValue('Time0.8 Beam20_Mid20',0.0801, 0.10 ,PeakBeam20_Mid20)
T8maxBeam20_Mid10, T8minBeam20_Mid10 = Find_ColMaxValue('Time0.8 Beam20_Mid10',0.0801, 0.10 ,PeakBeam20_Mid10)
# --------------20m Distributed Beam and Node Boundary Condition ------------------
T8maxBeamNode20_Mid80, T8minBeamNode20_Mid80 = Find_ColMaxValue('Time0.8 BeamNode20_Mid80',0.0801, 0.10 ,PeakBeamNode20_Mid80)
T8maxBeamNode20_Mid40, T8minBeamNode20_Mid40 = Find_ColMaxValue('Time0.8 BeamNode20_Mid40',0.0801, 0.10 ,PeakBeamNode20_Mid40)
T8maxBeamNode20_Mid20, T8minBeamNode20_Mid20 = Find_ColMaxValue('Time0.8 BeamNode20_Mid20',0.0801, 0.10 ,PeakBeamNode20_Mid20)
T8maxBeamNode20_Mid10, T8minBeamNode20_Mid10 = Find_ColMaxValue('Time0.8 BeamNode20_Mid10',0.0801, 0.10 ,PeakBeamNode20_Mid10)

# --------------10m Tie BC -------------------            
T8maxTie10_Mid80, T8minTie10_Mid80 = Find_ColMaxValue('Time0.8 Tie10_Mid80',0.0801, 0.10 ,PeakTie10_Mid80)
T8maxTie10_Mid40, T8minTie10_Mid40 = Find_ColMaxValue('Time0.8 Tie10_Mid40',0.0801, 0.10 ,PeakTie10_Mid40)
T8maxTie10_Mid20, T8minTie10_Mid20 = Find_ColMaxValue('Time0.8 Tie10_Mid20',0.0801, 0.10 ,PeakTie10_Mid20)
T8maxTie10_Mid10, T8minTie10_Mid10 = Find_ColMaxValue('Time0.8 Tie10_Mid10',0.0801, 0.10 ,PeakTie10_Mid10)
# --------------10m LK Dashpot BC -------------------
T8maxLK10_Mid80, T8minLK10_Mid80 = Find_ColMaxValue('Time0.8 LK10_Mid80',0.0801, 0.10 ,PeakLK10_Mid80)
T8maxLK10_Mid40, T8minLK10_Mid40 = Find_ColMaxValue('Time0.8 LK10_Mid40',0.0801, 0.10 ,PeakLK10_Mid40)
T8maxLK10_Mid20, T8minLK10_Mid20 = Find_ColMaxValue('Time0.8 LK10_Mid20',0.0801, 0.10 ,PeakLK10_Mid20)
T8maxLK10_Mid10, T8minLK10_Mid10 = Find_ColMaxValue('Time0.8 LK10_Mid10',0.0801, 0.10 ,PeakLK10_Mid10)
# --------------10m Distributed Beam Boundary Condition -------------------
T8maxBeam10_Mid80, T8minBeam10_Mid80 = Find_ColMaxValue('Time0.8 Beam10_Mid80',0.0801, 0.10 ,PeakBeam10_Mid80)
T8maxBeam10_Mid40, T8minBeam10_Mid40 = Find_ColMaxValue('Time0.8 Beam10_Mid40',0.0801, 0.10 ,PeakBeam10_Mid40)
T8maxBeam10_Mid20, T8minBeam10_Mid20 = Find_ColMaxValue('Time0.8 Beam10_Mid20',0.0801, 0.10 ,PeakBeam10_Mid20)
T8maxBeam10_Mid10, T8minBeam10_Mid10 = Find_ColMaxValue('Time0.8 Beam10_Mid10',0.0801, 0.10 ,PeakBeam10_Mid10)
# --------------10m Distributed Beam and Node Boundary Condition ------------------
T8maxBeamNode10_Mid80, T8minBeamNode10_Mid80 = Find_ColMaxValue('Time0.8 BeamNode10_Mid80',0.0801, 0.10 ,PeakBeamNode10_Mid80)
T8maxBeamNode10_Mid40, T8minBeamNode10_Mid40 = Find_ColMaxValue('Time0.8 BeamNode10_Mid40',0.0801, 0.10 ,PeakBeamNode10_Mid40)
T8maxBeamNode10_Mid20, T8minBeamNode10_Mid20 = Find_ColMaxValue('Time0.8 BeamNode10_Mid20',0.0801, 0.10 ,PeakBeamNode10_Mid20)
T8maxBeamNode10_Mid10, T8minBeamNode10_Mid10 = Find_ColMaxValue('Time0.8 BeamNode10_Mid10',0.0801, 0.10 ,PeakBeamNode10_Mid10)

# --------------1m Tie BC -------------------            
T8maxTie1_Mid80, T8minTie1_Mid80 = Find_ColMaxValue('Time0.8 Tie1_Mid80',0.0801, 0.10 ,PeakTie1_Mid80)
T8maxTie1_Mid40, T8minTie1_Mid40 = Find_ColMaxValue('Time0.8 Tie1_Mid40',0.0801, 0.10 ,PeakTie1_Mid40)
T8maxTie1_Mid20, T8minTie1_Mid20 = Find_ColMaxValue('Time0.8 Tie1_Mid20',0.0801, 0.10 ,PeakTie1_Mid20)
T8maxTie1_Mid10, T8minTie1_Mid10 = Find_ColMaxValue('Time0.8 Tie1_Mid10',0.0801, 0.10 ,PeakTie1_Mid10)
# --------------1m LK Dashpot BC -------------------
T8maxLK1_Mid80, T8minLK1_Mid80 = Find_ColMaxValue('Time0.8 LK1_Mid80',0.0801, 0.10 ,PeakLK1_Mid80)
T8maxLK1_Mid40, T8minLK1_Mid40 = Find_ColMaxValue('Time0.8 LK1_Mid40',0.0801, 0.10 ,PeakLK1_Mid40)
T8maxLK1_Mid20, T8minLK1_Mid20 = Find_ColMaxValue('Time0.8 LK1_Mid20',0.0801, 0.10 ,PeakLK1_Mid20)
T8maxLK1_Mid10, T8minLK1_Mid10 = Find_ColMaxValue('Time0.8 LK1_Mid10',0.0801, 0.10 ,PeakLK1_Mid10)
# --------------1m Distributed Beam Boundary Condition -------------------
T8maxBeam1_Mid80, T8minBeam1_Mid80 = Find_ColMaxValue('Time0.8 Beam1_Mid80',0.0801, 0.10 ,PeakBeam1_Mid80)
T8maxBeam1_Mid40, T8minBeam1_Mid40 = Find_ColMaxValue('Time0.8 Beam1_Mid40',0.0801, 0.10 ,PeakBeam1_Mid40)
T8maxBeam1_Mid20, T8minBeam1_Mid20 = Find_ColMaxValue('Time0.8 Beam1_Mid20',0.0801, 0.10 ,PeakBeam1_Mid20)
T8maxBeam1_Mid10, T8minBeam1_Mid10 = Find_ColMaxValue('Time0.8 Beam1_Mid10',0.0801, 0.10 ,PeakBeam1_Mid10)
# --------------1m Distributed Beam and Node Boundary Condition ------------------
T8maxBeamNode1_Mid80, T8minBeamNode1_Mid80 = Find_ColMaxValue('Time0.8 BeamNode1_Mid80',0.0801, 0.10 ,PeakBeamNode1_Mid80)
T8maxBeamNode1_Mid40, T8minBeamNode1_Mid40 = Find_ColMaxValue('Time0.8 BeamNode1_Mid40',0.0801, 0.10 ,PeakBeamNode1_Mid40)
T8maxBeamNode1_Mid20, T8minBeamNode1_Mid20 = Find_ColMaxValue('Time0.8 BeamNode1_Mid20',0.0801, 0.10 ,PeakBeamNode1_Mid20)
T8maxBeamNode1_Mid10, T8minBeamNode1_Mid10 = Find_ColMaxValue('Time0.8 BeamNode1_Mid10',0.0801, 0.10 ,PeakBeamNode1_Mid10)
# # -------------Make Analysis Solution as Mesh size minium with Tie BC ----------------------------
# MaxAnalysis = maxTie20_Mid80
# MinAnalysis = minTie20_Mid80
# ============================= Middle Node ========================================
# ------------W20m Tie BC Error Peak Value-----------------------
T8MidTie20_error = np.zeros((3,3))
err20Mat(T8MidTie20_error,  T8maxTie20_Mid40,T8minTie20_Mid40, T8maxTie20_Mid20,T8minTie20_Mid20, T8maxTie20_Mid10,T8minTie20_Mid10)
# ------------W20m LK BC Error Peak Value-----------------------
T8MidLK20_error = np.zeros((4,3))
errMatrix(T8MidLK20_error, T8maxLK20_Mid80,T8minLK20_Mid80, T8maxLK20_Mid40,T8minLK20_Mid40, T8maxLK20_Mid20,T8minLK20_Mid20, T8maxLK20_Mid10,T8minLK20_Mid10)
# ------------W20m Distributed Beam BC Error Peak Value-----------------------
T8MidBeam20_error = np.zeros((4,3))
errMatrix(T8MidBeam20_error, T8maxBeam20_Mid80,T8minBeam20_Mid80, T8maxBeam20_Mid40,T8minBeam20_Mid40,T8maxBeam20_Mid20,T8minBeam20_Mid20,T8maxBeam20_Mid10,T8minBeam20_Mid10)
# ------------W20m Distributed Beam and Node BC Error Peak Value-----------------------
T8MidBN20_error = np.zeros((4,3))
errMatrix(T8MidBN20_error, T8maxBeamNode20_Mid80,T8minBeamNode20_Mid80, T8maxBeamNode20_Mid40,T8minBeamNode20_Mid40,T8maxBeamNode20_Mid20,T8minBeamNode20_Mid20,T8maxBeamNode20_Mid10,T8minBeamNode20_Mid10)

# ------------W10m Tie BC Error Peak Value-----------------------
T8MidTie10_error = np.zeros((4,3))
errMatrix(T8MidTie10_error, T8maxTie10_Mid80,T8minTie10_Mid80, T8maxTie10_Mid40,T8minTie10_Mid40, T8maxTie10_Mid20,T8minTie10_Mid20, T8maxTie10_Mid10,T8minTie10_Mid10)
# ------------W10m LK BC Error Peak Value-----------------------
T8MidLK10_error = np.zeros((4,3))
errMatrix(T8MidLK10_error, T8maxLK10_Mid80,T8minLK10_Mid80, T8maxLK10_Mid40,T8minLK10_Mid40, T8maxLK10_Mid20,T8minLK10_Mid20, T8maxLK10_Mid10,T8minLK10_Mid10)
# ------------W10m Distributed Beam BC Error Peak Value-----------------------
T8MidBeam10_error = np.zeros((4,3))
errMatrix(T8MidBeam10_error, T8maxBeam10_Mid80,T8minBeam10_Mid80, T8maxBeam10_Mid40,T8minBeam10_Mid40, T8maxBeam10_Mid20,T8minBeam10_Mid20, T8maxBeam10_Mid10,T8minBeam10_Mid10)
# ------------W10m Distributed Beam and Node BC Error Peak Value-----------------------
T8MidBN10_error = np.zeros((4,3))
errMatrix(T8MidBN10_error, T8maxBeamNode10_Mid80,T8minBeamNode10_Mid80, T8maxBeamNode10_Mid40,T8minBeamNode10_Mid40, T8maxBeamNode10_Mid20,T8minBeamNode10_Mid20, T8maxBeamNode10_Mid10,T8minBeamNode10_Mid10)

# ------------W1m Tie BC Error Peak Value-----------------------
T8MidTie1_error = np.zeros((4,3))
errMatrix(T8MidTie1_error, T8maxTie1_Mid80,T8minTie1_Mid80, T8maxTie1_Mid40,T8minTie1_Mid40, T8maxTie1_Mid20,T8minTie1_Mid20, T8maxTie1_Mid10,T8minTie1_Mid10)
# ------------W1m LK BC Error Peak Value-----------------------
T8MidLK1_error = np.zeros((4,3))
errMatrix(T8MidLK1_error, T8maxLK1_Mid80,T8minLK1_Mid80, T8maxLK1_Mid40,T8minLK1_Mid40, T8maxLK1_Mid20,T8minLK1_Mid20, T8maxLK1_Mid10,T8minLK1_Mid10)
# ------------W1m Distributed Beam BC Error Peak Value-----------------------
T8MidBeam1_error = np.zeros((4,3))
errMatrix(T8MidBeam1_error, T8maxBeam1_Mid80,T8minBeam1_Mid80, T8maxBeam1_Mid40,T8minBeam1_Mid40, T8maxBeam1_Mid20,T8minBeam1_Mid20, T8maxBeam1_Mid10,T8minBeam1_Mid10)
# ------------W1m Distributed Beam and Node BC Error Peak Value-----------------------
T8MidBN1_error = np.zeros((4,3))
errMatrix(T8MidBN1_error, T8maxBeamNode1_Mid80,T8minBeamNode1_Mid80, T8maxBeamNode1_Mid40,T8minBeamNode1_Mid40, T8maxBeamNode1_Mid20,T8minBeamNode1_Mid20, T8maxBeamNode1_Mid10,T8minBeamNode1_Mid10)

# ========================  Three-Quarter Node ==============================
# --------------20m Tie BC -------------------            
T8maxTie20_Qua80, T8minTie20_Qua80 = Find_ColMaxValue('Time0.8 Tie20_Qua80',0.0801, 0.10 ,PeakTie20_Qua80)
T8maxTie20_Qua40, T8minTie20_Qua40 = Find_ColMaxValue('Time0.8 Tie20_Qua40',0.0801, 0.10 ,PeakTie20_Qua40)
T8maxTie20_Qua20, T8minTie20_Qua20 = Find_ColMaxValue('Time0.8 Tie20_Qua20',0.0801, 0.10 ,PeakTie20_Qua20)
T8maxTie20_Qua10, T8minTie20_Qua10 = Find_ColMaxValue('Time0.8 Tie20_Qua10',0.0801, 0.10 ,PeakTie20_Qua10)
# --------------20m LK Dashpot BC -------------------
T8maxLK20_Qua80, T8minLK20_Qua80 = Find_ColMaxValue('Time0.8 LK20_Qua80',0.0801, 0.10 ,PeakLK20_Qua80)
T8maxLK20_Qua40, T8minLK20_Qua40 = Find_ColMaxValue('Time0.8 LK20_Qua40',0.0801, 0.10 ,PeakLK20_Qua40)
T8maxLK20_Qua20, T8minLK20_Qua20 = Find_ColMaxValue('Time0.8 LK20_Qua20',0.0801, 0.10 ,PeakLK20_Qua20)
T8maxLK20_Qua10, T8minLK20_Qua10 = Find_ColMaxValue('Time0.8 LK20_Qua10',0.0801, 0.10 ,PeakLK20_Qua10)
# --------------20m Distributed Beam Boundary Condition -------------------
T8maxBeam20_Qua80, T8minBeam20_Qua80 = Find_ColMaxValue('Time0.8 Beam20_Qua80',0.0801, 0.10 ,PeakBeam20_Qua80)
T8maxBeam20_Qua40, T8minBeam20_Qua40 = Find_ColMaxValue('Time0.8 Beam20_Qua40',0.0801, 0.10 ,PeakBeam20_Qua40)
T8maxBeam20_Qua20, T8minBeam20_Qua20 = Find_ColMaxValue('Time0.8 Beam20_Qua20',0.0801, 0.10 ,PeakBeam20_Qua20)
T8maxBeam20_Qua10, T8minBeam20_Qua10 = Find_ColMaxValue('Time0.8 Beam20_Qua10',0.0801, 0.10 ,PeakBeam20_Qua10)
# --------------20m Distributed Beam and Node Boundary Condition ------------------
T8maxBeamNode20_Qua80, T8minBeamNode20_Qua80 = Find_ColMaxValue('Time0.8 BeamNode20_Qua80',0.0801, 0.10 ,PeakBeamNode20_Qua80)
T8maxBeamNode20_Qua40, T8minBeamNode20_Qua40 = Find_ColMaxValue('Time0.8 BeamNode20_Qua40',0.0801, 0.10 ,PeakBeamNode20_Qua40)
T8maxBeamNode20_Qua20, T8minBeamNode20_Qua20 = Find_ColMaxValue('Time0.8 BeamNode20_Qua20',0.0801, 0.10 ,PeakBeamNode20_Qua20)
T8maxBeamNode20_Qua10, T8minBeamNode20_Qua10 = Find_ColMaxValue('Time0.8 BeamNode20_Qua10',0.0801, 0.10 ,PeakBeamNode20_Qua10)

# --------------10m Tie BC -------------------            
T8maxTie10_Qua80, T8minTie10_Qua80 = Find_ColMaxValue('Time0.8 Tie10_Qua80',0.0801, 0.10 ,PeakTie10_Qua80)
T8maxTie10_Qua40, T8minTie10_Qua40 = Find_ColMaxValue('Time0.8 Tie10_Qua40',0.0801, 0.10 ,PeakTie10_Qua40)
T8maxTie10_Qua20, T8minTie10_Qua20 = Find_ColMaxValue('Time0.8 Tie10_Qua20',0.0801, 0.10 ,PeakTie10_Qua20)
T8maxTie10_Qua10, T8minTie10_Qua10 = Find_ColMaxValue('Time0.8 Tie10_Qua10',0.0801, 0.10 ,PeakTie10_Qua10)
# --------------10m LK Dashpot BC -------------------
T8maxLK10_Qua80, T8minLK10_Qua80 = Find_ColMaxValue('Time0.8 LK10_Qua80',0.0801, 0.10 ,PeakLK10_Qua80)
T8maxLK10_Qua40, T8minLK10_Qua40 = Find_ColMaxValue('Time0.8 LK10_Qua40',0.0801, 0.10 ,PeakLK10_Qua40)
T8maxLK10_Qua20, T8minLK10_Qua20 = Find_ColMaxValue('Time0.8 LK10_Qua20',0.0801, 0.10 ,PeakLK10_Qua20)
T8maxLK10_Qua10, T8minLK10_Qua10 = Find_ColMaxValue('Time0.8 LK10_Qua10',0.0801, 0.10 ,PeakLK10_Qua10)
# --------------10m Distributed Beam Boundary Condition -------------------
T8maxBeam10_Qua80, T8minBeam10_Qua80 = Find_ColMaxValue('Time0.8 Beam10_Qua80',0.0801, 0.10 ,PeakBeam10_Qua80)
T8maxBeam10_Qua40, T8minBeam10_Qua40 = Find_ColMaxValue('Time0.8 Beam10_Qua40',0.0801, 0.10 ,PeakBeam10_Qua40)
T8maxBeam10_Qua20, T8minBeam10_Qua20 = Find_ColMaxValue('Time0.8 Beam10_Qua20',0.0801, 0.10 ,PeakBeam10_Qua20)
T8maxBeam10_Qua10, T8minBeam10_Qua10 = Find_ColMaxValue('Time0.8 Beam10_Qua10',0.0801, 0.10 ,PeakBeam10_Qua10)
# --------------10m Distributed Beam and Node Boundary Condition ------------------
T8maxBeamNode10_Qua80, T8minBeamNode10_Qua80 = Find_ColMaxValue('Time0.8 BeamNode10_Qua80',0.0801, 0.10 ,PeakBeamNode10_Qua80)
T8maxBeamNode10_Qua40, T8minBeamNode10_Qua40 = Find_ColMaxValue('Time0.8 BeamNode10_Qua40',0.0801, 0.10 ,PeakBeamNode10_Qua40)
T8maxBeamNode10_Qua20, T8minBeamNode10_Qua20 = Find_ColMaxValue('Time0.8 BeamNode10_Qua20',0.0801, 0.10 ,PeakBeamNode10_Qua20)
T8maxBeamNode10_Qua10, T8minBeamNode10_Qua10 = Find_ColMaxValue('Time0.8 BeamNode10_Qua10',0.0801, 0.10 ,PeakBeamNode10_Qua10)

# --------------1m Tie BC -------------------            
T8maxTie1_Qua80, T8minTie1_Qua80 = Find_ColMaxValue('Time0.8 Tie1_Qua80',0.0801, 0.10 ,PeakTie1_Qua80)
T8maxTie1_Qua40, T8minTie1_Qua40 = Find_ColMaxValue('Time0.8 Tie1_Qua40',0.0801, 0.10 ,PeakTie1_Qua40)
T8maxTie1_Qua20, T8minTie1_Qua20 = Find_ColMaxValue('Time0.8 Tie1_Qua20',0.0801, 0.10 ,PeakTie1_Qua20)
T8maxTie1_Qua10, T8minTie1_Qua10 = Find_ColMaxValue('Time0.8 Tie1_Qua10',0.0801, 0.10 ,PeakTie1_Qua10)
# --------------1m LK Dashpot BC -------------------
T8maxLK1_Qua80, T8minLK1_Qua80 = Find_ColMaxValue('Time0.8 LK1_Qua80',0.0801, 0.10 ,PeakLK1_Qua80)
T8maxLK1_Qua40, T8minLK1_Qua40 = Find_ColMaxValue('Time0.8 LK1_Qua40',0.0801, 0.10 ,PeakLK1_Qua40)
T8maxLK1_Qua20, T8minLK1_Qua20 = Find_ColMaxValue('Time0.8 LK1_Qua20',0.0801, 0.10 ,PeakLK1_Qua20)
T8maxLK1_Qua10, T8minLK1_Qua10 = Find_ColMaxValue('Time0.8 LK1_Qua10',0.0801, 0.10 ,PeakLK1_Qua10)
# --------------1m Distributed Beam Boundary Condition -------------------
T8maxBeam1_Qua80, T8minBeam1_Qua80 = Find_ColMaxValue('Time0.8 Beam1_Qua80',0.0801, 0.10 ,PeakBeam1_Qua80)
T8maxBeam1_Qua40, T8minBeam1_Qua40 = Find_ColMaxValue('Time0.8 Beam1_Qua40',0.0801, 0.10 ,PeakBeam1_Qua40)
T8maxBeam1_Qua20, T8minBeam1_Qua20 = Find_ColMaxValue('Time0.8 Beam1_Qua20',0.0801, 0.10 ,PeakBeam1_Qua20)
T8maxBeam1_Qua10, T8minBeam1_Qua10 = Find_ColMaxValue('Time0.8 Beam1_Qua10',0.0801, 0.10 ,PeakBeam1_Qua10)
# --------------1m Distributed Beam and Node Boundary Condition ------------------
T8maxBeamNode1_Qua80, T8minBeamNode1_Qua80 = Find_ColMaxValue('Time0.8 BeamNode1_Qua80',0.0801, 0.10 ,PeakBeamNode1_Qua80)
T8maxBeamNode1_Qua40, T8minBeamNode1_Qua40 = Find_ColMaxValue('Time0.8 BeamNode1_Qua40',0.0801, 0.10 ,PeakBeamNode1_Qua40)
T8maxBeamNode1_Qua20, T8minBeamNode1_Qua20 = Find_ColMaxValue('Time0.8 BeamNode1_Qua20',0.0801, 0.10 ,PeakBeamNode1_Qua20)
T8maxBeamNode1_Qua10, T8minBeamNode1_Qua10 = Find_ColMaxValue('Time0.8 BeamNode1_Qua10',0.0801, 0.10 ,PeakBeamNode1_Qua10)

# ============================= Three Quarter Node ====================================================
# ------------W20m Tie BC Error Peak Value-----------------------
T8QuaTie20_error = np.zeros((4,3))
errMatrix(T8QuaTie20_error,T8maxTie20_Qua80,T8minTie20_Qua80,T8maxTie20_Qua40,T8minTie20_Qua40,T8maxTie20_Qua20,T8minTie20_Qua20,T8maxTie20_Qua10,T8minTie20_Qua10)
# ------------W20m LK BC Error Peak Value-----------------------
T8QuaLK20_error = np.zeros((4,3))
errMatrix(T8QuaLK20_error,T8maxLK20_Qua80,T8minLK20_Qua80,T8maxLK20_Qua40,T8minLK20_Qua40,T8maxLK20_Qua20,T8minLK20_Qua20,T8maxLK20_Qua10,T8minLK20_Qua10)
# ------------W20m Distributed Beam BC Error Peak Value-----------------------
T8QuaBeam20_error = np.zeros((4,3))
errMatrix(T8QuaBeam20_error,T8maxBeam20_Qua80,T8minBeam20_Qua80,T8maxBeam20_Qua40,T8minBeam20_Qua40,T8maxBeam20_Qua20,T8minBeam20_Qua20,T8maxBeam20_Qua10,T8minBeam20_Qua10)
# ------------W20m Distributed Beam and Node BC Error Peak Value-----------------------
T8QuaBN20_error = np.zeros((4,3))
errMatrix(T8QuaBN20_error,T8maxBeamNode20_Qua80,T8minBeamNode20_Qua80,T8maxBeamNode20_Qua40,T8minBeamNode20_Qua40,T8maxBeamNode20_Qua20,T8minBeamNode20_Qua20,T8maxBeamNode20_Qua10,T8minBeamNode20_Qua10)

# ------------W10m Tie BC Error Peak Value-----------------------
T8QuaTie10_error = np.zeros((4,3))
errMatrix(T8QuaTie10_error, T8maxTie10_Qua80,T8minTie10_Qua80, T8maxTie10_Qua40,T8minTie10_Qua40, T8maxTie10_Qua20,T8minTie10_Qua20, T8maxTie10_Qua10,T8minTie10_Qua10)
# ------------W10m LK BC Error Peak Value-----------------------
T8QuaLK10_error = np.zeros((4,3))
errMatrix(T8QuaLK10_error, T8maxLK10_Qua80,T8minLK10_Qua80, T8maxLK10_Qua40,T8minLK10_Qua40, T8maxLK10_Qua20,T8minLK10_Qua20, T8maxLK10_Qua10,T8minLK10_Qua10)
# ------------W10m Distributed Beam BC Error Peak Value-----------------------
T8QuaBeam10_error = np.zeros((4,3))
errMatrix(T8QuaBeam10_error, T8maxBeam10_Qua80,T8minBeam10_Qua80, T8maxBeam10_Qua40,T8minBeam10_Qua40, T8maxBeam10_Qua20,T8minBeam10_Qua20, T8maxBeam10_Qua10,T8minBeam10_Qua10)
# ------------W10m Distributed Beam and Node BC Error Peak Value-----------------------
T8QuaBN10_error = np.zeros((4,3))
errMatrix(T8QuaBN10_error, T8maxBeamNode10_Qua80,T8minBeamNode10_Qua80, T8maxBeamNode10_Qua40,T8minBeamNode10_Qua40, T8maxBeamNode10_Qua20,T8minBeamNode10_Qua20, T8maxBeamNode10_Qua10,T8minBeamNode10_Qua10)

# ------------W1m Tie BC Error Peak Value-----------------------
T8QuaTie1_error = np.zeros((4,3))
errMatrix(T8QuaTie1_error, T8maxTie1_Qua80,T8minTie1_Qua80, T8maxTie1_Qua40,T8minTie1_Qua40, T8maxTie1_Qua20,T8minTie1_Qua20, T8maxTie1_Qua10,T8minTie1_Qua10)
# ------------W1m LK BC Error Peak Value-----------------------
T8QuaLK1_error = np.zeros((4,3))
errMatrix(T8QuaLK1_error, T8maxLK1_Qua80,T8minLK1_Qua80, T8maxLK1_Qua40,T8minLK1_Qua40, T8maxLK1_Qua20,T8minLK1_Qua20, T8maxLK1_Qua10,T8minLK1_Qua10)
# ------------W1m Distributed Beam BC Error Peak Value-----------------------
T8QuaBeam1_error = np.zeros((4,3))
errMatrix(T8QuaBeam1_error, T8maxBeam1_Qua80,T8minBeam1_Qua80, T8maxBeam1_Qua40,T8minBeam1_Qua40, T8maxBeam1_Qua20,T8minBeam1_Qua20, T8maxBeam1_Qua10,T8minBeam1_Qua10)
# ------------W1m Distributed Beam and Node BC Error Peak Value-----------------------
T8QuaBN1_error = np.zeros((4,3))
errMatrix(T8QuaBN1_error, T8maxBeamNode1_Qua80,T8minBeamNode1_Qua80, T8maxBeamNode1_Qua40,T8minBeamNode1_Qua40, T8maxBeamNode1_Qua20,T8minBeamNode1_Qua20, T8maxBeamNode1_Qua10,T8minBeamNode1_Qua10)

# calculate_Error()
T8MidTieErr20 = np.zeros((3,3))
T8MidLKErr20 = np.zeros((4,3))
T8MidBeamErr20 = np.zeros((4,3))
T8MidBNErr20 = np.zeros((4,3))

T8MidTieErr10 = np.zeros((4,3))
T8MidLKErr10 = np.zeros((4,3))
T8MidBeamErr10 = np.zeros((4,3))
T8MidBNErr10 = np.zeros((4,3))

T8MidTieErr1 = np.zeros((4,3))
T8MidLKErr1 = np.zeros((4,3))
T8MidBeamErr1 = np.zeros((4,3))
T8MidBNErr1 = np.zeros((4,3))

# -------- W20 Relative Error --------------   
Calculate_Error(Mesh20m_Size, T8MidTieErr20, T8MidTie20_error)
Calculate_Error(Mesh_Size, T8MidLKErr20, T8MidLK20_error)      
Calculate_Error(Mesh_Size, T8MidBeamErr20, T8MidBeam20_error)
Calculate_Error(Mesh_Size, T8MidBNErr20, T8MidBN20_error)   
# -------- W10 Relative Error --------------   
Calculate_Error(Mesh_Size, T8MidTieErr10, T8MidTie10_error)
Calculate_Error(Mesh_Size, T8MidLKErr10, T8MidLK10_error)      
Calculate_Error(Mesh_Size, T8MidBeamErr10, T8MidBeam10_error)
Calculate_Error(Mesh_Size, T8MidBNErr10, T8MidBN10_error)   
# -------- W1 Relative Error --------------   
Calculate_Error(Mesh_Size, T8MidTieErr1, T8MidTie1_error)
Calculate_Error(Mesh_Size, T8MidLKErr1, T8MidLK1_error)      
Calculate_Error(Mesh_Size, T8MidBeamErr1, T8MidBeam1_error)
Calculate_Error(Mesh_Size, T8MidBNErr1, T8MidBN1_error)   

# ------- Three Quarter Err ----------------
T8QuaTieErr20 = np.zeros((4,3))
T8QuaLKErr20 = np.zeros((4,3))
T8QuaBeamErr20 = np.zeros((4,3))
T8QuaBNErr20 = np.zeros((4,3))

T8QuaTieErr10 = np.zeros((4,3))
T8QuaLKErr10 = np.zeros((4,3))
T8QuaBeamErr10 = np.zeros((4,3))
T8QuaBNErr10 = np.zeros((4,3))

T8QuaTieErr1 = np.zeros((4,3))
T8QuaLKErr1 = np.zeros((4,3))
T8QuaBeamErr1 = np.zeros((4,3))
T8QuaBNErr1 = np.zeros((4,3))

# -------- W20 Relative Error --------------   
Calculate_Error(Mesh_Size, T8QuaTieErr20, T8QuaTie20_error)
Calculate_Error(Mesh_Size, T8QuaLKErr20, T8QuaLK20_error)      
Calculate_Error(Mesh_Size, T8QuaBeamErr20, T8QuaBeam20_error)
Calculate_Error(Mesh_Size, T8QuaBNErr20, T8QuaBN20_error)   
# -------- W10 Relative Error --------------   
Calculate_Error(Mesh_Size, T8QuaTieErr10, T8QuaTie10_error)
Calculate_Error(Mesh_Size, T8QuaLKErr10, T8QuaLK10_error)      
Calculate_Error(Mesh_Size, T8QuaBeamErr10, T8QuaBeam10_error)
Calculate_Error(Mesh_Size, T8QuaBNErr10, T8QuaBN10_error)   
# -------- W1 Relative Error --------------   
Calculate_Error(Mesh_Size, T8QuaTieErr1, T8QuaTie1_error)
Calculate_Error(Mesh_Size, T8QuaLKErr1, T8QuaLK1_error)      
Calculate_Error(Mesh_Size, T8QuaBeamErr1, T8QuaBeam1_error)
Calculate_Error(Mesh_Size, T8QuaBNErr1, T8QuaBN1_error)   

# # -----------------Time:0.08~0.1s Maximum Middle Node Relative Error -------------------------
# fig9, (ax25,ax26,ax27) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
# fig9.suptitle(f'Ground Surface Different Boundary Maximum Velocity Compare (TopForce) \n t = 0.08~0.10s (Middle node)',x=0.50,y =0.95,fontsize = 20)
# fig9.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
# fig9.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax25 = plt.subplot(311)
# DifferTime_elemetError(1,T8MidTieErr20, T8MidLKErr20, T8MidBeamErr20, T8MidBNErr20)
# ax25.set_title(f"SW 20m",fontsize =18, x=0.20, y=0.45)

# ax26 = plt.subplot(312)
# DifferTime_elemetError(1,T8MidTieErr10, T8MidLKErr10, T8MidBeamErr10, T8MidBNErr10)
# ax26.set_title(f"SW 10m",fontsize =18, x=0.20, y=0.45)

# ax27 = plt.subplot(313)
# DifferTime_elemetError(1,T8MidTieErr1, T8MidLKErr1, T8MidBeamErr1, T8MidBNErr1)
# ax27.set_title(f"SW 1m",fontsize =18, x=0.20, y=0.65)


# for ax in [ax25,ax26,ax27]:
#     formatter = ticker.ScalarFormatter(useMathText =True)
#     formatter.set_scientific(True)
#     formatter.set_powerlimits((0,0))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
#     ax.yaxis.set_major_formatter(formatter)
#     ax.xaxis.set_major_formatter(formatter)
#     ax.yaxis.get_offset_text().set(size=18)
#     ax.xaxis.get_offset_text().set(size=18)

# # -----------------Time:0.08~0.1s Minimum Middle Node Relative Error -------------------------
# fig10, (ax28,ax29,ax30) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
# fig10.suptitle(f'Ground Surface Different Boundary Minimum Velocity Compare (TopForce) \n t = 0.08~0.10s (Middle node)',x=0.50,y =0.95,fontsize = 20)
# fig10.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
# fig10.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax28 = plt.subplot(311)
# DifferTime_elemetError(2,T8MidTieErr20, T8MidLKErr20, T8MidBeamErr20, T8MidBNErr20)
# ax28.set_title(f"SW 20m",fontsize =18, x=0.20, y=0.45)

# ax29 = plt.subplot(312)
# DifferTime_elemetError(2,T8MidTieErr10, T8MidLKErr10, T8MidBeamErr10, T8MidBNErr10)
# ax29.set_title(f"SW 10m",fontsize =18, x=0.20, y=0.45)

# ax30 = plt.subplot(313)
# DifferTime_elemetError(2,T8MidTieErr1, T8MidLKErr1, T8MidBeamErr1, T8MidBNErr1)
# ax30.set_title(f"SW 1m",fontsize =18, x=0.20, y=0.65)


# for ax in [ax28,ax29,ax30]:
#     formatter = ticker.ScalarFormatter(useMathText =True)
#     formatter.set_scientific(True)
#     formatter.set_powerlimits((0,0))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
#     ax.yaxis.set_major_formatter(formatter)
#     ax.xaxis.set_major_formatter(formatter)
#     ax.yaxis.get_offset_text().set(size=18)
#     ax.xaxis.get_offset_text().set(size=18)

# # ----------------- Three Quarter Node Relative Error -------------------------
# x_axis = 0.125
# fig11, (ax31,ax32,ax33) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
# fig11.suptitle(f'Ground Surface Different Boundary Maximum Velocity Compare (TopForce)\n t = 0.08~0.10s (Three Quarter node)',x=0.50,y =0.95,fontsize = 20)
# fig11.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
# fig11.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax31 = plt.subplot(311)
# DifferTime_elemetError(1,T8QuaTieErr20, T8QuaLKErr20, T8QuaBeamErr20, T8QuaBNErr20)
# ax31.set_title(f"SW 20m",fontsize =18, x=0.15, y=0.76)

# ax32 = plt.subplot(312)
# DifferTime_elemetError(1,T8QuaTieErr10, T8QuaLKErr10, T8QuaBeamErr10, T8QuaBNErr10)
# ax32.set_title(f"SW 10m",fontsize =18, x=0.15, y=0.45)

# ax33 = plt.subplot(313)
# DifferTime_elemetError(1,T8QuaTieErr1, T8QuaLKErr1, T8QuaBeamErr1, T8QuaBNErr1)
# ax33.set_title(f"SW 1m",fontsize =18, x=0.15, y=0.45)

# for ax in [ax31,ax32,ax33]:
#     formatter = ticker.ScalarFormatter(useMathText =True)
#     formatter.set_scientific(True)
#     formatter.set_powerlimits((0,0))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
#     ax.yaxis.set_major_formatter(formatter)
#     ax.xaxis.set_major_formatter(formatter)
#     ax.yaxis.get_offset_text().set(size=18)
#     ax.xaxis.get_offset_text().set(size=18)

# fig12, (ax34,ax35,ax36) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
# fig12.suptitle(f'Ground Surface Different Boundary Minimum Velocity Compare (TopForce)\n t = 0.08~0.10s (Three Quarter node)',x=0.50,y =0.95,fontsize = 20)
# fig12.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
# fig12.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax34 = plt.subplot(311)
# DifferTime_elemetError(2,T8QuaTieErr20, T8QuaLKErr20, T8QuaBeamErr20, T8QuaBNErr20)
# ax34.set_title(f"SW 20m",fontsize =18, x=0.15, y=0.25)

# ax35 = plt.subplot(312)
# DifferTime_elemetError(2,T8QuaTieErr10, T8QuaLKErr10, T8QuaBeamErr10, T8QuaBNErr10)
# ax35.set_title(f"SW 10m",fontsize =18, x=0.90, y=0.62)

# ax36 = plt.subplot(313)
# DifferTime_elemetError(2,T8QuaTieErr1, T8QuaLKErr1, T8QuaBeamErr1, T8QuaBNErr1)
# ax36.set_title(f"SW 1m",fontsize =18, x=0.25, y=0.80)


# for ax in [ax34,ax35,ax36]:
#     formatter = ticker.ScalarFormatter(useMathText =True)
#     formatter.set_scientific(True)
#     formatter.set_powerlimits((0,0))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
#     ax.yaxis.set_major_formatter(formatter)
#     ax.xaxis.set_major_formatter(formatter)
#     ax.yaxis.get_offset_text().set(size=18)
#     ax.xaxis.get_offset_text().set(size=18)
# =============== Time At 0.08~0.10 s Error Compare ===========================
# --------------20m Tie BC -------------------            
T10maxTie20_Mid80, T10minTie20_Mid80 = Find_ColMaxValue('Time1.0 Tie20_Mid80',0.10, 0.20 ,PeakTie20_Mid80)
T10maxTie20_Mid40, T10minTie20_Mid40 = Find_ColMaxValue('Time0.8 Tie20_Mid40',0.10, 0.20 ,PeakTie20_Mid40)
T10maxTie20_Mid20, T10minTie20_Mid20 = Find_ColMaxValue('Time0.8 Tie20_Mid20',0.10, 0.20 ,PeakTie20_Mid20)
T10maxTie20_Mid10, T10minTie20_Mid10 = Find_ColMaxValue('Time0.8 Tie20_Mid10',0.10, 0.20 ,PeakTie20_Mid10)
# --------------20m LK Dashpot BC -------------------
T10maxLK20_Mid80, T10minLK20_Mid80 = Find_ColMaxValue('Time1.0 LK20_Mid80',0.10, 0.20 ,PeakLK20_Mid80)
T10maxLK20_Mid40, T10minLK20_Mid40 = Find_ColMaxValue('Time1.0 LK20_Mid40',0.10, 0.20,PeakLK20_Mid40)
T10maxLK20_Mid20, T10minLK20_Mid20 = Find_ColMaxValue('Time1.0 LK20_Mid20',0.10, 0.20 ,PeakLK20_Mid20)
T10maxLK20_Mid10, T10minLK20_Mid10 = Find_ColMaxValue('Time1.0 LK20_Mid10',0.10, 0.20 ,PeakLK20_Mid10)
# --------------20m Distributed Beam Boundary Condition -------------------
T10maxBeam20_Mid80, T10minBeam20_Mid80 = Find_ColMaxValue('Time1.0 Beam20_Mid80',0.10, 0.20 ,PeakBeam20_Mid80)
T10maxBeam20_Mid40, T10minBeam20_Mid40 = Find_ColMaxValue('Time1.0 Beam20_Mid40',0.10, 0.20 ,PeakBeam20_Mid40)
T10maxBeam20_Mid20, T10minBeam20_Mid20 = Find_ColMaxValue('Time1.0 Beam20_Mid20',0.10, 0.20 ,PeakBeam20_Mid20)
T10maxBeam20_Mid10, T10minBeam20_Mid10 = Find_ColMaxValue('Time1.0 Beam20_Mid10',0.10, 0.20 ,PeakBeam20_Mid10)
# --------------20m Distributed Beam and Node Boundary Condition ------------------
T10maxBeamNode20_Mid80, T10minBeamNode20_Mid80 = Find_ColMaxValue('Time1.0 BeamNode20_Mid80',0.10, 0.20 ,PeakBeamNode20_Mid80)
T10maxBeamNode20_Mid40, T10minBeamNode20_Mid40 = Find_ColMaxValue('Time1.0 BeamNode20_Mid40',0.10, 0.20 ,PeakBeamNode20_Mid40)
T10maxBeamNode20_Mid20, T10minBeamNode20_Mid20 = Find_ColMaxValue('Time1.0 BeamNode20_Mid20',0.10, 0.20 ,PeakBeamNode20_Mid20)
T10maxBeamNode20_Mid10, T10minBeamNode20_Mid10 = Find_ColMaxValue('Time1.0 BeamNode20_Mid10',0.10, 0.20 ,PeakBeamNode20_Mid10)

# --------------10m Tie BC -------------------            
T10maxTie10_Mid80, T10minTie10_Mid80 = Find_ColMaxValue('Time1.0 Tie10_Mid80',0.10, 0.20 ,PeakTie10_Mid80)
T10maxTie10_Mid40, T10minTie10_Mid40 = Find_ColMaxValue('Time1.0 Tie10_Mid40',0.10, 0.20 ,PeakTie10_Mid40)
T10maxTie10_Mid20, T10minTie10_Mid20 = Find_ColMaxValue('Time1.0 Tie10_Mid20',0.10, 0.20 ,PeakTie10_Mid20)
T10maxTie10_Mid10, T10minTie10_Mid10 = Find_ColMaxValue('Time1.0 Tie10_Mid10',0.10, 0.20 ,PeakTie10_Mid10)
# --------------10m LK Dashpot BC -------------------
T10maxLK10_Mid80, T10minLK10_Mid80 = Find_ColMaxValue('Time1.0 LK10_Mid80',0.10, 0.20 ,PeakLK10_Mid80)
T10maxLK10_Mid40, T10minLK10_Mid40 = Find_ColMaxValue('Time1.0 LK10_Mid40',0.10, 0.20 ,PeakLK10_Mid40)
T10maxLK10_Mid20, T10minLK10_Mid20 = Find_ColMaxValue('Time1.0 LK10_Mid20',0.10, 0.20 ,PeakLK10_Mid20)
T10maxLK10_Mid10, T10minLK10_Mid10 = Find_ColMaxValue('Time1.0 LK10_Mid10',0.10, 0.20 ,PeakLK10_Mid10)
# --------------10m Distributed Beam Boundary Condition -------------------
T10maxBeam10_Mid80, T10minBeam10_Mid80 = Find_ColMaxValue('Time1.0 Beam10_Mid80',0.10, 0.20 ,PeakBeam10_Mid80)
T10maxBeam10_Mid40, T10minBeam10_Mid40 = Find_ColMaxValue('Time1.0 Beam10_Mid40',0.10, 0.20 ,PeakBeam10_Mid40)
T10maxBeam10_Mid20, T10minBeam10_Mid20 = Find_ColMaxValue('Time1.0 Beam10_Mid20',0.10, 0.20 ,PeakBeam10_Mid20)
T10maxBeam10_Mid10, T10minBeam10_Mid10 = Find_ColMaxValue('Time1.0 Beam10_Mid10',0.10, 0.20 ,PeakBeam10_Mid10)
# --------------10m Distributed Beam and Node Boundary Condition ------------------
T10maxBeamNode10_Mid80, T10minBeamNode10_Mid80 = Find_ColMaxValue('Time1.0 BeamNode10_Mid80',0.10, 0.20 ,PeakBeamNode10_Mid80)
T10maxBeamNode10_Mid40, T10minBeamNode10_Mid40 = Find_ColMaxValue('Time1.0 BeamNode10_Mid40',0.10, 0.20 ,PeakBeamNode10_Mid40)
T10maxBeamNode10_Mid20, T10minBeamNode10_Mid20 = Find_ColMaxValue('Time1.0 BeamNode10_Mid20',0.10, 0.20 ,PeakBeamNode10_Mid20)
T10maxBeamNode10_Mid10, T10minBeamNode10_Mid10 = Find_ColMaxValue('Time1.0 BeamNode10_Mid10',0.10, 0.20 ,PeakBeamNode10_Mid10)

# # --------------1m Tie BC -------------------            
T10maxTie1_Mid80, T10minTie1_Mid80 = Find_ColMaxValue('Time1.0 Tie1_Mid80',0.10, 0.20 ,PeakTie1_Mid80)
T10maxTie1_Mid40, T10minTie1_Mid40 = Find_ColMaxValue('Time1.0 Tie1_Mid40',0.10, 0.20 ,PeakTie1_Mid40)
T10maxTie1_Mid20, T10minTie1_Mid20 = Find_ColMaxValue('Time1.0 Tie1_Mid20',0.10, 0.20 ,PeakTie1_Mid20)
T10maxTie1_Mid10, T10minTie1_Mid10 = Find_ColMaxValue('Time1.0 Tie1_Mid10',0.10, 0.20 ,PeakTie1_Mid10)
# --------------1m LK Dashpot BC -------------------
T10maxLK1_Mid80, T10minLK1_Mid80 = Find_ColMaxValue('Time1.0 LK1_Mid80',0.10, 0.20 ,PeakLK1_Mid80)
T10maxLK1_Mid40, T10minLK1_Mid40 = Find_ColMaxValue('Time1.0 LK1_Mid40',0.10, 0.20 ,PeakLK1_Mid40)
T10maxLK1_Mid20, T10minLK1_Mid20 = Find_ColMaxValue('Time1.0 LK1_Mid20',0.10, 0.20 ,PeakLK1_Mid20)
T10maxLK1_Mid10, T10minLK1_Mid10 = Find_ColMaxValue('Time1.0 LK1_Mid10',0.10, 0.20 ,PeakLK1_Mid10)
# --------------1m Distributed Beam Boundary Condition -------------------
T10maxBeam1_Mid80, T10minBeam1_Mid80 = Find_ColMaxValue('Time1.0 Beam1_Mid80',0.10, 0.20 ,PeakBeam1_Mid80)
T10maxBeam1_Mid40, T10minBeam1_Mid40 = Find_ColMaxValue('Time1.0 Beam1_Mid40',0.10, 0.20 ,PeakBeam1_Mid40)
T10maxBeam1_Mid20, T10minBeam1_Mid20 = Find_ColMaxValue('Time1.0 Beam1_Mid20',0.10, 0.20 ,PeakBeam1_Mid20)
T10maxBeam1_Mid10, T10minBeam1_Mid10 = Find_ColMaxValue('Time1.0 Beam1_Mid10',0.10, 0.20 ,PeakBeam1_Mid10)
# --------------1m Distributed Beam and Node Boundary Condition ------------------
T10maxBeamNode1_Mid80, T10minBeamNode1_Mid80 = Find_ColMaxValue('Time1.0 BeamNode1_Mid80',0.10, 0.20 ,PeakBeamNode1_Mid80)
T10maxBeamNode1_Mid40, T10minBeamNode1_Mid40 = Find_ColMaxValue('Time1.0 BeamNode1_Mid40',0.10, 0.20 ,PeakBeamNode1_Mid40)
T10maxBeamNode1_Mid20, T10minBeamNode1_Mid20 = Find_ColMaxValue('Time1.0 BeamNode1_Mid20',0.10, 0.20 ,PeakBeamNode1_Mid20)
T10maxBeamNode1_Mid10, T10minBeamNode1_Mid10 = Find_ColMaxValue('Time1.0 BeamNode1_Mid10',0.10, 0.20 ,PeakBeamNode1_Mid10)

# ============================= Middle Node ========================================
# ------------W20m Tie BC Error Peak Value-----------------------
T10MidTie20_error = np.zeros((3,3))
err20Mat(T10MidTie20_error,  T10maxTie20_Mid40,T8minTie20_Mid40, T10maxTie20_Mid20,T10minTie20_Mid20, T10maxTie20_Mid10,T10minTie20_Mid10)
# ------------W20m LK BC Error Peak Value-----------------------
T10MidLK20_error = np.zeros((4,3))
errMatrix(T10MidLK20_error, T10maxLK20_Mid80,T10minLK20_Mid80, T10maxLK20_Mid40,T10minLK20_Mid40, T10maxLK20_Mid20,T10minLK20_Mid20, T10maxLK20_Mid10,T10minLK20_Mid10)
# ------------W20m Distributed Beam BC Error Peak Value-----------------------
T10MidBeam20_error = np.zeros((4,3))
errMatrix(T10MidBeam20_error, T10maxBeam20_Mid80,T10minBeam20_Mid80, T10maxBeam20_Mid40,T10minBeam20_Mid40,T10maxBeam20_Mid20,T10minBeam20_Mid20,T10maxBeam20_Mid10,T10minBeam20_Mid10)
# ------------W20m Distributed Beam and Node BC Error Peak Value-----------------------
T10MidBN20_error = np.zeros((4,3))
errMatrix(T10MidBN20_error, T10maxBeamNode20_Mid80,T10minBeamNode20_Mid80, T10maxBeamNode20_Mid40,T10minBeamNode20_Mid40,T10maxBeamNode20_Mid20,T10minBeamNode20_Mid20,T10maxBeamNode20_Mid10,T10minBeamNode20_Mid10)

# ------------W10m Tie BC Error Peak Value-----------------------
T10MidTie10_error = np.zeros((4,3))
errMatrix(T10MidTie10_error, T10maxTie10_Mid80,T10minTie10_Mid80, T10maxTie10_Mid40,T10minTie10_Mid40, T10maxTie10_Mid20,T10minTie10_Mid20, T10maxTie10_Mid10,T10minTie10_Mid10)
# ------------W10m LK BC Error Peak Value-----------------------
T10MidLK10_error = np.zeros((4,3))
errMatrix(T10MidLK10_error, T10maxLK10_Mid80,T10minLK10_Mid80, T10maxLK10_Mid40,T10minLK10_Mid40, T10maxLK10_Mid20,T10minLK10_Mid20, T10maxLK10_Mid10,T10minLK10_Mid10)
# ------------W10m Distributed Beam BC Error Peak Value-----------------------
T10MidBeam10_error = np.zeros((4,3))
errMatrix(T10MidBeam10_error, T10maxBeam10_Mid80,T10minBeam10_Mid80, T10maxBeam10_Mid40,T10minBeam10_Mid40, T10maxBeam10_Mid20,T10minBeam10_Mid20, T10maxBeam10_Mid10,T10minBeam10_Mid10)
# ------------W10m Distributed Beam and Node BC Error Peak Value-----------------------
T10MidBN10_error = np.zeros((4,3))
errMatrix(T10MidBN10_error, T10maxBeamNode10_Mid80,T10minBeamNode10_Mid80, T10maxBeamNode10_Mid40,T10minBeamNode10_Mid40, T10maxBeamNode10_Mid20,T10minBeamNode10_Mid20, T10maxBeamNode10_Mid10,T10minBeamNode10_Mid10)

# ------------W1m Tie BC Error Peak Value-----------------------
T10MidTie1_error = np.zeros((4,3))
errMatrix(T10MidTie1_error, T10maxTie1_Mid80,T10minTie1_Mid80, T10maxTie1_Mid40,T10minTie1_Mid40, T10maxTie1_Mid20,T10minTie1_Mid20, T10maxTie1_Mid10,T10minTie1_Mid10)
# ------------W1m LK BC Error Peak Value-----------------------
T10MidLK1_error = np.zeros((4,3))
errMatrix(T10MidLK1_error, T10maxLK1_Mid80,T10minLK1_Mid80, T10maxLK1_Mid40,T10minLK1_Mid40, T10maxLK1_Mid20,T10minLK1_Mid20, T10maxLK1_Mid10,T10minLK1_Mid10)
# ------------W1m Distributed Beam BC Error Peak Value-----------------------
T10MidBeam1_error = np.zeros((4,3))
errMatrix(T10MidBeam1_error, T10maxBeam1_Mid80,T10minBeam1_Mid80, T10maxBeam1_Mid40,T10minBeam1_Mid40, T10maxBeam1_Mid20,T10minBeam1_Mid20, T10maxBeam1_Mid10,T10minBeam1_Mid10)
# ------------W1m Distributed Beam and Node BC Error Peak Value-----------------------
T10MidBN1_error = np.zeros((4,3))
errMatrix(T10MidBN1_error, T10maxBeamNode1_Mid80,T10minBeamNode1_Mid80, T10maxBeamNode1_Mid40,T10minBeamNode1_Mid40, T10maxBeamNode1_Mid20,T10minBeamNode1_Mid20, T10maxBeamNode1_Mid10,T10minBeamNode1_Mid10)

# ========================  Three-Quarter Node ==============================
# --------------20m Tie BC -------------------            
T10maxTie20_Qua80, T10minTie20_Qua80 = Find_ColMaxValue('Time1.0 Tie20_Qua80',0.10, 0.20 ,PeakTie20_Qua80)
T10maxTie20_Qua40, T10minTie20_Qua40 = Find_ColMaxValue('Time1.0 Tie20_Qua40',0.10, 0.20 ,PeakTie20_Qua40)
T10maxTie20_Qua20, T10minTie20_Qua20 = Find_ColMaxValue('Time1.0 Tie20_Qua20',0.10, 0.20 ,PeakTie20_Qua20)
T10maxTie20_Qua10, T10minTie20_Qua10 = Find_ColMaxValue('Time1.0 Tie20_Qua10',0.10, 0.20 ,PeakTie20_Qua10)
# --------------20m LK Dashpot BC -------------------
T10maxLK20_Qua80, T10minLK20_Qua80 = Find_ColMaxValue('Time1.0 LK20_Qua80',0.10, 0.20 ,PeakLK20_Qua80)
T10maxLK20_Qua40, T10minLK20_Qua40 = Find_ColMaxValue('Time1.0 LK20_Qua40',0.10, 0.20 ,PeakLK20_Qua40)
T10maxLK20_Qua20, T10minLK20_Qua20 = Find_ColMaxValue('Time1.0 LK20_Qua20',0.10, 0.20 ,PeakLK20_Qua20)
T10maxLK20_Qua10, T10minLK20_Qua10 = Find_ColMaxValue('Time1.0 LK20_Qua10',0.10, 0.20 ,PeakLK20_Qua10)
# --------------20m Distributed Beam Boundary Condition -------------------
T10maxBeam20_Qua80, T10minBeam20_Qua80 = Find_ColMaxValue('Time1.0 Beam20_Qua80',0.10, 0.20 ,PeakBeam20_Qua80)
T10maxBeam20_Qua40, T10minBeam20_Qua40 = Find_ColMaxValue('Time1.0 Beam20_Qua40',0.10, 0.20 ,PeakBeam20_Qua40)
T10maxBeam20_Qua20, T10minBeam20_Qua20 = Find_ColMaxValue('Time1.0 Beam20_Qua20',0.10, 0.20 ,PeakBeam20_Qua20)
T10maxBeam20_Qua10, T10minBeam20_Qua10 = Find_ColMaxValue('Time1.0 Beam20_Qua10',0.10, 0.20 ,PeakBeam20_Qua10)
# --------------20m Distributed Beam and Node Boundary Condition ------------------
T10maxBeamNode20_Qua80, T10minBeamNode20_Qua80 = Find_ColMaxValue('Time1.0 BeamNode20_Qua80',0.10, 0.20 ,PeakBeamNode20_Qua80)
T10maxBeamNode20_Qua40, T10minBeamNode20_Qua40 = Find_ColMaxValue('Time1.0 BeamNode20_Qua40',0.10, 0.20 ,PeakBeamNode20_Qua40)
T10maxBeamNode20_Qua20, T10minBeamNode20_Qua20 = Find_ColMaxValue('Time1.0  BeamNode20_Qua20',0.10, 0.20 ,PeakBeamNode20_Qua20)
T10maxBeamNode20_Qua10, T10minBeamNode20_Qua10 = Find_ColMaxValue('Time1.0  BeamNode20_Qua10',0.10, 0.20 ,PeakBeamNode20_Qua10)

# --------------10m Tie BC -------------------            
T10maxTie10_Qua80, T10minTie10_Qua80 = Find_ColMaxValue('Time1.0 Tie10_Qua80',0.10, 0.20 ,PeakTie10_Qua80)
T10maxTie10_Qua40, T10minTie10_Qua40 = Find_ColMaxValue('Time1.0 Tie10_Qua40',0.10, 0.20 ,PeakTie10_Qua40)
T10maxTie10_Qua20, T10minTie10_Qua20 = Find_ColMaxValue('Time1.0 Tie10_Qua20',0.10, 0.20 ,PeakTie10_Qua20)
T10maxTie10_Qua10, T10minTie10_Qua10 = Find_ColMaxValue('Time1.0 Tie10_Qua10',0.10, 0.20 ,PeakTie10_Qua10)
# --------------10m LK Dashpot BC -------------------
T10maxLK10_Qua80, T10minLK10_Qua80 = Find_ColMaxValue('Time1.0 LK10_Qua80',0.10, 0.20 ,PeakLK10_Qua80)
T10maxLK10_Qua40, T10minLK10_Qua40 = Find_ColMaxValue('Time1.0 LK10_Qua40',0.10, 0.20 ,PeakLK10_Qua40)
T10maxLK10_Qua20, T10minLK10_Qua20 = Find_ColMaxValue('Time1.0 LK10_Qua20',0.10, 0.20 ,PeakLK10_Qua20)
T10maxLK10_Qua10, T10minLK10_Qua10 = Find_ColMaxValue('Time1.0 LK10_Qua10',0.10, 0.20 ,PeakLK10_Qua10)
# --------------10m Distributed Beam Boundary Condition -------------------
T10maxBeam10_Qua80, T10minBeam10_Qua80 = Find_ColMaxValue('Time1.0 Beam10_Qua80',0.10, 0.20 ,PeakBeam10_Qua80)
T10maxBeam10_Qua40, T10minBeam10_Qua40 = Find_ColMaxValue('Time1.0 Beam10_Qua40',0.10, 0.20 ,PeakBeam10_Qua40)
T10maxBeam10_Qua20, T10minBeam10_Qua20 = Find_ColMaxValue('Time1.0 Beam10_Qua20',0.10, 0.20 ,PeakBeam10_Qua20)
T10maxBeam10_Qua10, T10minBeam10_Qua10 = Find_ColMaxValue('Time1.0 Beam10_Qua10',0.10, 0.20 ,PeakBeam10_Qua10)
# --------------10m Distributed Beam and Node Boundary Condition ------------------
T10maxBeamNode10_Qua80, T10minBeamNode10_Qua80 = Find_ColMaxValue('Time1.0 BeamNode10_Qua80',0.10, 0.20 ,PeakBeamNode10_Qua80)
T10maxBeamNode10_Qua40, T10minBeamNode10_Qua40 = Find_ColMaxValue('Time1.0 BeamNode10_Qua40',0.10, 0.20 ,PeakBeamNode10_Qua40)
T10maxBeamNode10_Qua20, T10minBeamNode10_Qua20 = Find_ColMaxValue('Time1.0 BeamNode10_Qua20',0.10, 0.20 ,PeakBeamNode10_Qua20)
T10maxBeamNode10_Qua10, T10minBeamNode10_Qua10 = Find_ColMaxValue('Time1.0 BeamNode10_Qua10',0.10, 0.20 ,PeakBeamNode10_Qua10)

# --------------1m Tie BC -------------------            
T10maxTie1_Qua80, T10minTie1_Qua80 = Find_ColMaxValue('Time1.0 Tie1_Qua80',0.10, 0.20 ,PeakTie1_Qua80)
T10maxTie1_Qua40, T10minTie1_Qua40 = Find_ColMaxValue('Time1.0 Tie1_Qua40',0.10, 0.20 ,PeakTie1_Qua40)
T10maxTie1_Qua20, T10minTie1_Qua20 = Find_ColMaxValue('Time1.0  Tie1_Qua20',0.10, 0.20 ,PeakTie1_Qua20)
T10maxTie1_Qua10, T10minTie1_Qua10 = Find_ColMaxValue('Time1.0  Tie1_Qua10',0.10, 0.20 ,PeakTie1_Qua10)
# --------------1m LK Dashpot BC -------------------
T10maxLK1_Qua80, T10minLK1_Qua80 = Find_ColMaxValue('Time1.0  LK1_Qua80',0.10, 0.20 ,PeakLK1_Qua80)
T10maxLK1_Qua40, T10minLK1_Qua40 = Find_ColMaxValue('Time1.0  LK1_Qua40',0.10, 0.20 ,PeakLK1_Qua40)
T10maxLK1_Qua20, T10minLK1_Qua20 = Find_ColMaxValue('Time1.0  LK1_Qua20',0.10, 0.20 ,PeakLK1_Qua20)
T10maxLK1_Qua10, T10minLK1_Qua10 = Find_ColMaxValue('Time1.0  LK1_Qua10',0.10, 0.20 ,PeakLK1_Qua10)
# --------------1m Distributed Beam Boundary Condition -------------------
T10maxBeam1_Qua80, T10minBeam1_Qua80 = Find_ColMaxValue('Time1.0 Beam1_Qua80',0.10, 0.20 ,PeakBeam1_Qua80)
T10maxBeam1_Qua40, T10minBeam1_Qua40 = Find_ColMaxValue('Time1.0 Beam1_Qua40',0.10, 0.20 ,PeakBeam1_Qua40)
T10maxBeam1_Qua20, T10minBeam1_Qua20 = Find_ColMaxValue('Time1.0 Beam1_Qua20',0.10, 0.20 ,PeakBeam1_Qua20)
T10maxBeam1_Qua10, T10minBeam1_Qua10 = Find_ColMaxValue('Time1.0 Beam1_Qua10',0.10, 0.20 ,PeakBeam1_Qua10)
# --------------1m Distributed Beam and Node Boundary Condition ------------------
T10maxBeamNode1_Qua80, T10minBeamNode1_Qua80 = Find_ColMaxValue('Time1.0 BeamNode1_Qua80',0.10, 0.20 ,PeakBeamNode1_Qua80)
T10maxBeamNode1_Qua40, T10minBeamNode1_Qua40 = Find_ColMaxValue('Time1.0 BeamNode1_Qua40',0.10, 0.20 ,PeakBeamNode1_Qua40)
T10maxBeamNode1_Qua20, T10minBeamNode1_Qua20 = Find_ColMaxValue('Time1.0 BeamNode1_Qua20',0.10, 0.20 ,PeakBeamNode1_Qua20)
T10maxBeamNode1_Qua10, T10minBeamNode1_Qua10 = Find_ColMaxValue('Time1.0 BeamNode1_Qua10',0.10, 0.20 ,PeakBeamNode1_Qua10)

# calculate_Error()
T10MidTieErr20 = np.zeros((3,3))
T10MidLKErr20 = np.zeros((4,3))
T10MidBeamErr20 = np.zeros((4,3))
T10MidBNErr20 = np.zeros((4,3))

T10MidTieErr10 = np.zeros((4,3))
T10MidLKErr10 = np.zeros((4,3))
T10MidBeamErr10 = np.zeros((4,3))
T10MidBNErr10 = np.zeros((4,3))

T10MidTieErr1 = np.zeros((4,3))
T10MidLKErr1 = np.zeros((4,3))
T10MidBeamErr1 = np.zeros((4,3))
T10MidBNErr1 = np.zeros((4,3))

# -------- W20 Relative Error --------------   
Calculate_Error(Mesh20m_Size, T10MidTieErr20, T10MidTie20_error)
Calculate_Error(Mesh_Size, T10MidLKErr20, T10MidLK20_error)      
Calculate_Error(Mesh_Size, T10MidBeamErr20, T10MidBeam20_error)
Calculate_Error(Mesh_Size, T10MidBNErr20, T10MidBN20_error)   
# -------- W10 Relative Error --------------   
Calculate_Error(Mesh_Size, T10MidTieErr10, T10MidTie10_error)
Calculate_Error(Mesh_Size, T10MidLKErr10, T10MidLK10_error)      
Calculate_Error(Mesh_Size, T10MidBeamErr10, T10MidBeam10_error)
Calculate_Error(Mesh_Size, T10MidBNErr10, T10MidBN10_error)   
# -------- W1 Relative Error --------------   
Calculate_Error(Mesh_Size, T10MidTieErr1, T10MidTie1_error)
Calculate_Error(Mesh_Size, T10MidLKErr1, T10MidLK1_error)      
Calculate_Error(Mesh_Size, T10MidBeamErr1, T10MidBeam1_error)
Calculate_Error(Mesh_Size, T10MidBNErr1, T10MidBN1_error)   

# ============================= Three Quarter Node ====================================================
# ------------W20m Tie BC Error Peak Value-----------------------
T10QuaTie20_error = np.zeros((4,3))
errMatrix(T10QuaTie20_error,T10maxTie20_Qua80,T10minTie20_Qua80,T10maxTie20_Qua40,T10minTie20_Qua40,T10maxTie20_Qua20,T10minTie20_Qua20,T10maxTie20_Qua10,T10minTie20_Qua10)
# ------------W20m LK BC Error Peak Value-----------------------
T10QuaLK20_error = np.zeros((4,3))
errMatrix(T10QuaLK20_error,T10maxLK20_Qua80,T10minLK20_Qua80,T10maxLK20_Qua40,T10minLK20_Qua40,T10maxLK20_Qua20,T10minLK20_Qua20,T10maxLK20_Qua10,T10minLK20_Qua10)
# ------------W20m Distributed Beam BC Error Peak Value-----------------------
T10QuaBeam20_error = np.zeros((4,3))
errMatrix(T10QuaBeam20_error,T10maxBeam20_Qua80,T10minBeam20_Qua80,T10maxBeam20_Qua40,T10minBeam20_Qua40,T10maxBeam20_Qua20,T10minBeam20_Qua20,T10maxBeam20_Qua10,T10minBeam20_Qua10)
# ------------W20m Distributed Beam and Node BC Error Peak Value-----------------------
T10QuaBN20_error = np.zeros((4,3))
errMatrix(T10QuaBN20_error,T10maxBeamNode20_Qua80,T10minBeamNode20_Qua80,T10maxBeamNode20_Qua40,T10minBeamNode20_Qua40,T10maxBeamNode20_Qua20,T10minBeamNode20_Qua20,T10maxBeamNode20_Qua10,T10minBeamNode20_Qua10)

# ------------W10m Tie BC Error Peak Value-----------------------
T10QuaTie10_error = np.zeros((4,3))
errMatrix(T10QuaTie10_error, T10maxTie10_Qua80,T10minTie10_Qua80, T10maxTie10_Qua40,T10minTie10_Qua40, T10maxTie10_Qua20,T10minTie10_Qua20, T10maxTie10_Qua10,T10minTie10_Qua10)
# ------------W10m LK BC Error Peak Value-----------------------
T10QuaLK10_error = np.zeros((4,3))
errMatrix(T10QuaLK10_error, T10maxLK10_Qua80,T10minLK10_Qua80, T10maxLK10_Qua40,T10minLK10_Qua40, T10maxLK10_Qua20,T10minLK10_Qua20, T10maxLK10_Qua10,T10minLK10_Qua10)
# ------------W10m Distributed Beam BC Error Peak Value-----------------------
T10QuaBeam10_error = np.zeros((4,3))
errMatrix(T10QuaBeam10_error, T10maxBeam10_Qua80,T10minBeam10_Qua80, T10maxBeam10_Qua40,T10minBeam10_Qua40, T10maxBeam10_Qua20,T10minBeam10_Qua20, T10maxBeam10_Qua10,T10minBeam10_Qua10)
# ------------W10m Distributed Beam and Node BC Error Peak Value-----------------------
T10QuaBN10_error = np.zeros((4,3))
errMatrix(T10QuaBN10_error, T10maxBeamNode10_Qua80,T10minBeamNode10_Qua80, T10maxBeamNode10_Qua40,T10minBeamNode10_Qua40, T10maxBeamNode10_Qua20,T10minBeamNode10_Qua20, T10maxBeamNode10_Qua10,T10minBeamNode10_Qua10)

# ------------W1m Tie BC Error Peak Value-----------------------
T10QuaTie1_error = np.zeros((4,3))
errMatrix(T10QuaTie1_error, T10maxTie1_Qua80,T10minTie1_Qua80, T10maxTie1_Qua40,T10minTie1_Qua40, T10maxTie1_Qua20,T10minTie1_Qua20, T10maxTie1_Qua10,T10minTie1_Qua10)
# ------------W1m LK BC Error Peak Value-----------------------
T10QuaLK1_error = np.zeros((4,3))
errMatrix(T10QuaLK1_error, T10maxLK1_Qua80,T10minLK1_Qua80, T10maxLK1_Qua40,T10minLK1_Qua40, T10maxLK1_Qua20,T10minLK1_Qua20, T10maxLK1_Qua10,T10minLK1_Qua10)
# ------------W1m Distributed Beam BC Error Peak Value-----------------------
T10QuaBeam1_error = np.zeros((4,3))
errMatrix(T10QuaBeam1_error, T10maxBeam1_Qua80,T10minBeam1_Qua80, T10maxBeam1_Qua40,T10minBeam1_Qua40, T10maxBeam1_Qua20,T10minBeam1_Qua20, T10maxBeam1_Qua10,T10minBeam1_Qua10)
# ------------W1m Distributed Beam and Node BC Error Peak Value-----------------------
T10QuaBN1_error = np.zeros((4,3))
errMatrix(T10QuaBN1_error, T10maxBeamNode1_Qua80,T10minBeamNode1_Qua80, T10maxBeamNode1_Qua40,T10minBeamNode1_Qua40, T10maxBeamNode1_Qua20,T10minBeamNode1_Qua20, T10maxBeamNode1_Qua10,T10minBeamNode1_Qua10)

# ------- Three Quarter Err ----------------
T10QuaTieErr20 = np.zeros((4,3))
T10QuaLKErr20 = np.zeros((4,3))
T10QuaBeamErr20 = np.zeros((4,3))
T10QuaBNErr20 = np.zeros((4,3))

T10QuaTieErr10 = np.zeros((4,3))
T10QuaLKErr10 = np.zeros((4,3))
T10QuaBeamErr10 = np.zeros((4,3))
T10QuaBNErr10 = np.zeros((4,3))

T10QuaTieErr1 = np.zeros((4,3))
T10QuaLKErr1 = np.zeros((4,3))
T10QuaBeamErr1 = np.zeros((4,3))
T10QuaBNErr1 = np.zeros((4,3))

# -------- W20 Relative Error --------------   
Calculate_Error(Mesh_Size, T10QuaTieErr20, T10QuaTie20_error)
Calculate_Error(Mesh_Size, T10QuaLKErr20, T10QuaLK20_error)      
Calculate_Error(Mesh_Size, T10QuaBeamErr20, T10QuaBeam20_error)
Calculate_Error(Mesh_Size, T10QuaBNErr20, T10QuaBN20_error)   
# -------- W10 Relative Error --------------   
Calculate_Error(Mesh_Size, T10QuaTieErr10, T10QuaTie10_error)
Calculate_Error(Mesh_Size, T10QuaLKErr10, T10QuaLK10_error)      
Calculate_Error(Mesh_Size, T10QuaBeamErr10, T10QuaBeam10_error)
Calculate_Error(Mesh_Size, T10QuaBNErr10, T10QuaBN10_error)   
# -------- W1 Relative Error --------------   
Calculate_Error(Mesh_Size, T10QuaTieErr1, T10QuaTie1_error)
Calculate_Error(Mesh_Size, T10QuaLKErr1, T10QuaLK1_error)      
Calculate_Error(Mesh_Size, T10QuaBeamErr1, T10QuaBeam1_error)
Calculate_Error(Mesh_Size, T10QuaBNErr1, T10QuaBN1_error)   
# # -----------------Time:0.10~0.20s Maximum Middle Node Relative Error -------------------------
# fig13, (ax37,ax38,ax39) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
# fig13.suptitle(f'Ground Surface Different Boundary Maximum Velocity Compare (TopForce) \n t = 0.10~0.20s (Middle node)',x=0.50,y =0.95,fontsize = 20)
# fig13.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
# fig13.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax37 = plt.subplot(311)
# DifferTime_elemetError(1,T10MidTieErr20, T10MidLKErr20, T10MidBeamErr20, T10MidBNErr20)
# ax37.set_title(f"SW 20m",fontsize =18, x=0.85, y=0.45)

# ax38 = plt.subplot(312)
# DifferTime_elemetError(1,T10MidTieErr10, T10MidLKErr10, T10MidBeamErr10, T10MidBNErr10)
# ax38.set_title(f"SW 10m",fontsize =18, x=0.20, y=0.45)

# ax39 = plt.subplot(313)
# DifferTime_elemetError(1,T10MidTieErr1, T10MidLKErr1, T10MidBeamErr1, T10MidBNErr1)
# ax39.set_title(f"SW 1m",fontsize =18, x=0.20, y=0.45)


# for ax in [ax37,ax38,ax39]:
#     formatter = ticker.ScalarFormatter(useMathText =True)
#     formatter.set_scientific(True)
#     formatter.set_powerlimits((0,0))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
#     ax.yaxis.set_major_formatter(formatter)
#     ax.xaxis.set_major_formatter(formatter)
#     ax.yaxis.get_offset_text().set(size=18)
#     ax.xaxis.get_offset_text().set(size=18)

# # # -----------------Time:0.10~ 0.20s Minimum Middle Node Relative Error -------------------------
# fig14, (ax40,ax41,ax42) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
# fig14.suptitle(f'Ground Surface Different Boundary Minimum Velocity Compare (TopForce) \n t = 0.10~0.20s (Middle node)',x=0.50,y =0.95,fontsize = 20)
# fig14.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
# fig14.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax40 = plt.subplot(311)
# DifferTime_elemetError(2,T10MidTieErr20, T10MidLKErr20, T10MidBeamErr20, T10MidBNErr20)
# ax40.set_title(f"SW 20m",fontsize =18, x=0.20, y=0.45)

# ax41 = plt.subplot(312)
# DifferTime_elemetError(2,T10MidTieErr10, T10MidLKErr10, T10MidBeamErr10, T10MidBNErr10)
# ax41.set_title(f"SW 10m",fontsize =18, x=0.70, y=0.45)

# ax42 = plt.subplot(313)
# DifferTime_elemetError(2,T10MidTieErr1, T10MidLKErr1, T10MidBeamErr1, T10MidBNErr1)
# ax42.set_title(f"SW 1m",fontsize =18, x=0.20, y=0.22)


# for ax in [ax40,ax41,ax42]:
#     formatter = ticker.ScalarFormatter(useMathText =True)
#     formatter.set_scientific(True)
#     formatter.set_powerlimits((0,0))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
#     ax.yaxis.set_major_formatter(formatter)
#     ax.xaxis.set_major_formatter(formatter)
#     ax.yaxis.get_offset_text().set(size=18)
#     ax.xaxis.get_offset_text().set(size=18)

# # # -----------------Time:0.10~ 0.20s Maximum Three Quarter Node Relative Error -------------------------
# x_axis = 0.125
# fig15, (ax43,ax44,ax45) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
# fig15.suptitle(f'Ground Surface Different Boundary Maximum Velocity Compare (TopForce)\n t = 0.10~0.20s (Three Quarter node)',x=0.50,y =0.95,fontsize = 20)
# fig15.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
# fig15.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax43 = plt.subplot(311)
# DifferTime_elemetError(1,T10QuaTieErr20, T10QuaLKErr20, T10QuaBeamErr20, T10QuaBNErr20)
# ax43.set_title(f"SW 20m",fontsize =18, x=0.15, y=0.42)

# ax44 = plt.subplot(312)
# DifferTime_elemetError(1,T10QuaTieErr10, T10QuaLKErr10, T10QuaBeamErr10, T10QuaBNErr10)
# ax44.set_title(f"SW 10m",fontsize =18, x=0.15, y=0.44)

# ax45 = plt.subplot(313)
# DifferTime_elemetError(1,T10QuaTieErr1, T10QuaLKErr1, T10QuaBeamErr1, T10QuaBNErr1)
# ax45.set_title(f"SW 1m",fontsize =18, x=0.10, y=0.45)

# for ax in [ax43,ax44,ax45]:
#     formatter = ticker.ScalarFormatter(useMathText =True)
#     formatter.set_scientific(True)
#     formatter.set_powerlimits((0,0))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
#     ax.yaxis.set_major_formatter(formatter)
#     ax.xaxis.set_major_formatter(formatter)
#     ax.yaxis.get_offset_text().set(size=18)
#     ax.xaxis.get_offset_text().set(size=18)

# fig16, (ax46,ax47,ax48) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
# fig16.suptitle(f'Ground Surface Different Boundary Minimum Velocity Compare (TopForce)\n t = 0.10~0.20s (Three Quarter node)',x=0.50,y =0.95,fontsize = 20)
# fig16.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
# fig16.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

# ax46 = plt.subplot(311)
# DifferTime_elemetError(2,T10QuaTieErr20, T10QuaLKErr20, T10QuaBeamErr20, T10QuaBNErr20)
# ax46.set_title(f"SW 20m",fontsize =18, x=0.15, y=0.45)

# ax47 = plt.subplot(312)
# DifferTime_elemetError(2,T10QuaTieErr10, T10QuaLKErr10, T10QuaBeamErr10, T10QuaBNErr10)
# ax47.set_title(f"SW 10m",fontsize =18, x=0.15, y=0.45)

# ax48 = plt.subplot(313)
# DifferTime_elemetError(2,T10QuaTieErr1, T10QuaLKErr1, T10QuaBeamErr1, T10QuaBNErr1)
# ax48.set_title(f"SW 1m",fontsize =18, x=0.25, y=0.80)


# for ax in [ax46,ax47,ax48]:
#     formatter = ticker.ScalarFormatter(useMathText =True)
#     formatter.set_scientific(True)
#     formatter.set_powerlimits((0,0))
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
#     ax.yaxis.set_major_formatter(formatter)
#     ax.xaxis.set_major_formatter(formatter)
#     ax.yaxis.get_offset_text().set(size=18)
#     ax.xaxis.get_offset_text().set(size=18)
