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
tns = L/cs # wave transport time
dcell = tns/Soil_100row #each cell time
dt = dcell/10 #eace cell have 10 steps
print(f"wave travel = {tns} ;dcell = {dcell} ;dt = {dt}")

time = np.arange(0.0,0.050005,dt)
Nt = len(time)
#----------- Soil Coordinate --------------
x = cs*time #m

def Incoming_wave(x,t):
    yIn = np.sin(w*(x-cs*t))
    return yIn

def Outcoming_wave(x,t):
    yOut = +np.sin(w*(x+cs*t))
    return yOut

Nele = 100
dy = L/Nele # 1, 0.1
dx= dy/10 # 0.1, 0.01 each element have 10 step dx

total_Transport = np.arange(0.0,20.1, dx)
XIn = np.zeros((len(total_Transport),Nele))

# ---------- Incoming wave -------------------
input_disp = 5 # 5
# X = 0~10 m 
for j in range(Nele):#Nele
    tin = time[input_disp+10*j] 
    x0 = dy*j + (dy/2)

    for i in range(1001): #1001      
        xii = x0 + dx*i 
        XIn[5+10*j+i,j] = Incoming_wave(xii,tin)  #from 0.05m to 9.95m

# ---------- Outcoming wave -------------------
XOut = np.zeros((len(total_Transport),Nele))
Output_disp = 5 # 9.95
# X = 10m ~ 20m
for j in range(Nele):# Nele
    tout = time[Output_disp+10*j] 
    x0 = 9.95-dy*j   #9.95-dy*j 

    for i in range(1001):      
        xoo = x0 + dx*i 
        XOut[995-10*j+i,99-j] = Outcoming_wave(xoo,tout)  #from 9.95m to 0.05m

total_time = np.arange(0.0,0.4001,dt) #5e-5 in 100row
wave1 = np.zeros((len(total_time),Nele))

# ===== New BC Sideforce on Left and Right ==============
SSideforce_10rowx = np.zeros((len(total_time),Nele))
SSideforce_10rowy = np.zeros((len(total_time),Nele))

# ===== Input Incoming Wave and Outcoming Wave to wave1 =======================
ForceX_Cofficient = (cp/cs)

vely_Coefficient =  2/(A*rho*cs)
for g in [i for i in range(Nele)]: #Nele
    to = int(10*g+5)
    for t in range(len(total_time)):
        if total_time[t] < 0.05:   #t < 1000:
            # wave1[to+t,g] += XIn[to+t,g]
            wave1[to+t,g] = wave1[to+t,g] + (vely_Coefficient* XIn[to+t,g])  # original wave transport
# # ----- Swave eta_p*(Vx) --------------------------
            SSideforce_10rowx[to+t,g] = SSideforce_10rowx[to+t,g] + (ForceX_Cofficient *XIn[to+t,g])
# # ----- Swave sigma xy --------------------------            
            SSideforce_10rowy[to+t,g] = SSideforce_10rowy[to+t,g] + (XIn[to+t,g])
    
        if total_time[t] >= 0.05 and total_time[t] < 0.1:  #t >= 1000 and t < 2000:
            # wave1[to+t,99-g] += XOut[t-to,99-g]
            wave1[to+t,99-g] = wave1[to+t,99-g] + (vely_Coefficient* XOut[t-to,99-g])  # original wave transport
# # ----- Swave eta_p*(Vx) --------------------------
            SSideforce_10rowx[to+t,99-g] = SSideforce_10rowx[to+t,99-g] + (ForceX_Cofficient *XOut[t-to,99-g])
# # ----- Swave sigma xy --------------------------            
            SSideforce_10rowy[to+t,99-g] = SSideforce_10rowy[to+t,99-g] + (-XOut[t-to,99-g])
            
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
file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TieBC_80row/node12961.out"
file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TieBC_40row/node6521.out"
file3 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TieBC_20row/node3301.out"
file4 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TieBC_10row/node1691.out"
# --------- LK Dashpot Boundary Condition ----------------
file5 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideDash_80row/node12961.out"
file6 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideDash_40row/node6521.out"
file7 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideDash_20row/node3301.out"
file8 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideDash_10row/node1691.out"
# --------- Distributed Beam Boundary Condition ----------------
file9 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideBeam_80row/node12961.out"
file10 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideBeam_40row/node6521.out"
file11 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideBeam_20row/node3301.out"
file12 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideBeam_10row/node1691.out"
# --------- Distributed Beam and Node Boundary Condition ----------------
file13 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideNodeDash_80row/node12961.out"
file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideNodeDash_40row/node6521.out"
file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideNodeDash_20row/node3301.out"
file16 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideNodeDash_10row/node1691.out"

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
file17 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TieBC_80row/node6521.out"
file18 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TieBC_40row/node3281.out"
file19 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TieBC_20row/node1661.out"
file20 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TieBC_10row/node851.out"
# --------- LK Dashpot Boundary Condition ----------------
file21 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideDash_80row/node6521.out"
file22 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideDash_40row/node3281.out"
file23 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideDash_20row/node1661.out"
file24 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideDash_10row/node851.out"
# --------- Distributed Beam Boundary Condition ----------------
file25 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideBeam_80row/node6521.out"
file26 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideBeam_40row/node3281.out"
file27 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideBeam_20row/node1661.out"
file28 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideBeam_10row/node851.out"
# --------- Distributed Beam and Node Boundary Condition ----------------
file29 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideNodeDash_80row/node6521.out"
file30 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideNodeDash_40row/node3281.out"
file31 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideNodeDash_20row/node1661.out"
file32 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideNodeDash_10row/node851.out"

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
file33 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TieBC_80row/node725.out"
file34 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TieBC_40row/node365.out"
file35 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TieBC_20row/node185.out"
file36 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TieBC_10row/node95.out"
# --------- LK Dashpot Boundary Condition ----------------
file37 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideDash_80row/node725.out"
file38 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideDash_40row/node365.out"
file39 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideDash_20row/node185.out"
file40 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideDash_10row/node95.out"
# --------- Distributed Beam Boundary Condition ----------------
file41 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideBeam_80row/node725.out"
file42 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideBeam_40row/node365.out"
file43 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideBeam_20row/node185.out"
file44 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideBeam_10row/node95.out"
# --------- Distributed Beam and Node Boundary Condition ----------------
file45 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideNodeDash_80row/node725.out"
file46 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideNodeDash_40row/node365.out"
file47 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideNodeDash_20row/node185.out"
file48 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideNodeDash_10row/node95.out"

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
file49 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TieBC_80row/node13001.out"
file50 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TieBC_40row/node6561.out"
file51 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TieBC_20row/node3341.out"
file52 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/TieBC_10row/node1731.out"
# --------- LK Dashpot Boundary Condition ----------------
file53 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideDash_80row/node13001.out"
file54 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideDash_40row/node6561.out"
file55 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideDash_20row/node3341.out"
file56 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideDash_10row/node1731.out"
# --------- Distributed Beam Boundary Condition ----------------
file57 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideBeam_80row/node13001.out"
file58 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideBeam_40row/node6561.out"
file59 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideBeam_20row/node3341.out"
file60 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideBeam_10row/node1731.out"
# --------- Distributed Beam and Node Boundary Condition ----------------
file61 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideNodeDash_80row/node13001.out"
file62 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideNodeDash_40row/node6561.out"
file63 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideNodeDash_20row/node3341.out"
file64 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/20mRefinement/SideNodeDash_10row/node1731.out"

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
file65 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TieBC_80row/node6541.out"
file66 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TieBC_40row/node3301.out"
file67 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TieBC_20row/node1681.out"
file68 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/TieBC_10row/node871.out"
# --------- LK Dashpot Boundary Condition ----------------
file69 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideDash_80row/node6541.out"
file70 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideDash_40row/node3301.out"
file71 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideDash_20row/node1681.out"
file72 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideDash_10row/node871.out"
# --------- Distributed Beam Boundary Condition ----------------
file73 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideBeam_80row/node6541.out"
file74 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideBeam_40row/node3301.out"
file75 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideBeam_20row/node1681.out"
file76 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideBeam_10row/node871.out"
# --------- Distributed Beam and Node Boundary Condition ----------------
file77 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideNodeDash_80row/node6541.out"
file78 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideNodeDash_40row/node3301.out"
file79 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideNodeDash_20row/node1681.out"
file80 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/10mRefinement/SideNodeDash_10row/node871.out"

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
file81 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TieBC_80row/node727.out"
file82 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TieBC_40row/node367.out"
file83 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TieBC_20row/node187.out"
file84 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/TieBC_10row/node97.out"
# --------- LK Dashpot Boundary Condition ----------------
file85 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideDash_80row/node727.out"
file86 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideDash_40row/node367.out"
file87 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideDash_20row/node187.out"
file88 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideDash_10row/node97.out"
# --------- Distributed Beam Boundary Condition ----------------
file89 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideBeam_80row/node727.out"
file90 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideBeam_40row/node367.out"
file91 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideBeam_20row/node187.out"
file92 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideBeam_10row/node97.out"
# --------- Distributed Beam and Node Boundary Condition ----------------
file93 =  f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideNodeDash_80row/node727.out"
file94 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideNodeDash_40row/node367.out"
file95 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideNodeDash_20row/node187.out"
file96 = f"D:/shiang/opensees/20220330/OpenSeesPy/Velocity/1mRefinement/SideNodeDash_10row/node97.out"

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

plt_axis2 = 1
# # ------- wave put into the timeSeries ---------------
def Differ_BCVel(total_time,wave1,Mid80row,Mid40row,Mid20row,Mid10row):
    # plt.figure(figsize=(8,6))
    font_props = {'family': 'Arial', 'size': 9}
    # plt.xlabel("time (s)",fontsize=18)
    # plt.ylabel(r"$V_x$  $(m/s)$",fontsize=18)
    # plt.title(titleName,x=0.75,y=0.25, fontsize = 20)
    
    plt.plot(total_time,wave1[:,99],label =r'$\mathrm{Analytical}$',color= 'black',linewidth=2.0)
    plt.plot(Mid80row[:,0],Mid80row[:,plt_axis2],label ='Tie BC', ls = '--',color= 'darkorange',linewidth=6.0)
    plt.plot(Mid40row[:,0],Mid40row[:,plt_axis2],label ='LK Dashpot BC', ls = '-.',color= 'limegreen',linewidth=5.0)
    plt.plot(Mid20row[:,0],Mid20row[:,plt_axis2],label ='Beam BC', ls = ':',color= 'blue',linewidth=4.0)
    plt.plot(Mid10row[:,0],Mid10row[:,plt_axis2],label ='Beam and Node Dashpot BC', ls = '-',color= 'red',linewidth=2.0)
    
    plt.legend(loc=(0.025,0.0),prop=font_props,framealpha=0.0) #ncol=2,fontsize=16 loc='lower left'
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xlim(0.0, 0.20)
    # plt.xlim(0.050, 0.070)
    plt.grid(True)


# =========================== Different Boundary compare at Different Mesh Size =================================
x_axis = 0.025 # 0.1 0.05
# x_axis = 0.0025 # 0.1 0.05
row_heights = [3, 3, 3]
fig1, (ax1,ax2,ax3) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
fig1.suptitle(f'Different Boundary '+ r'$\Delta_C='+ '0.125' + r'\mathrm{m}$' + '\n(Middle node)',x=0.50,y =0.97,fontsize = 20)
fig1.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig1.text(0.45,0.04, 'time t (s)', va= 'center', fontsize=20)

ax1 = plt.subplot(311)
Differ_BCVel(total_time,wave1, Tie_W20_Mid80row, LK_W20_Mid80row, Beam_W20_Mid80row, BeamNode_W20_Mid80row)
ax1.set_title(f"SW 20m",fontsize =18, x=0.50, y=0.78)

ax2 = plt.subplot(312)
Differ_BCVel(total_time,wave1, Tie_W10_Mid80row, LK_W10_Mid80row, Beam_W10_Mid80row, BeamNode_W10_Mid80row)
ax2.set_title(f"SW 10m",fontsize =18, x=0.50, y=0.78)

ax3 = plt.subplot(313)
Differ_BCVel(total_time,wave1, Tie_W1_Mid80row, LK_W1_Mid80row, Beam_W1_Mid80row, BeamNode_W1_Mid80row)
ax3.set_title(f"SW 1m",fontsize =18, x=0.50, y=0.78)

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
fig2.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig2.text(0.45,0.04, 'time t (s)', va= 'center', fontsize=20)

ax4 = plt.subplot(311)
Differ_BCVel(total_time,wave1, Tie_W20_Mid40row, LK_W20_Mid40row, Beam_W20_Mid40row, BeamNode_W20_Mid40row)
ax4.set_title(f"SW 20m",fontsize =18, x=0.50, y=0.78)

ax5 = plt.subplot(312)
Differ_BCVel(total_time,wave1, Tie_W10_Mid40row, LK_W10_Mid40row, Beam_W10_Mid40row, BeamNode_W10_Mid40row)
ax5.set_title(f"SW 10m",fontsize =18, x=0.50, y=0.78)

ax6 = plt.subplot(313)
Differ_BCVel(total_time,wave1, Tie_W1_Mid40row, LK_W1_Mid40row, Beam_W1_Mid40row, BeamNode_W1_Mid40row)
ax6.set_title(f"SW 1m",fontsize =18, x=0.50, y=0.78)

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
fig3.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig3.text(0.45,0.04, 'time t (s)', va= 'center', fontsize=20)

ax7 = plt.subplot(311)
Differ_BCVel(total_time,wave1, Tie_W20_Mid20row, LK_W20_Mid20row, Beam_W20_Mid20row, BeamNode_W20_Mid20row)
ax7.set_title(f"SW 20m",fontsize =18, x=0.50, y=0.78)

ax8 = plt.subplot(312)
Differ_BCVel(total_time,wave1, Tie_W10_Mid20row, LK_W10_Mid20row, Beam_W10_Mid20row, BeamNode_W10_Mid20row)
ax8.set_title(f"SW 10m",fontsize =18, x=0.50, y=0.78)

ax9 = plt.subplot(313)
Differ_BCVel(total_time,wave1, Tie_W1_Mid20row, LK_W1_Mid20row, Beam_W1_Mid20row, BeamNode_W1_Mid20row)
ax9.set_title(f"SW 1m",fontsize =18, x=0.50, y=0.78)

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
fig4.text(0.03,0.5, r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$", va= 'center', rotation= 'vertical', fontsize=20)
fig4.text(0.45,0.04, 'time t (s)', va= 'center', fontsize=20)

ax10 = plt.subplot(311)
Differ_BCVel(total_time,wave1, Tie_W20_Mid10row, LK_W20_Mid10row, Beam_W20_Mid10row, BeamNode_W20_Mid10row)
ax10.set_title(f"SW 20m",fontsize =18, x=0.50, y=0.78)

ax11 = plt.subplot(312)
Differ_BCVel(total_time,wave1, Tie_W10_Mid10row, LK_W10_Mid10row, Beam_W10_Mid10row, BeamNode_W10_Mid10row)
ax11.set_title(f"SW 10m",fontsize =18, x=0.50, y=0.78)

ax12 = plt.subplot(313)
Differ_BCVel(total_time,wave1, Tie_W1_Mid10row, LK_W1_Mid10row, Beam_W1_Mid10row, BeamNode_W1_Mid10row)
ax12.set_title(f"SW 1m",fontsize =18, x=0.50, y=0.78)

for ax in [ax10,ax11,ax12]:
    formatter = ticker.ScalarFormatter(useMathText =True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set(size=18)
    ax.xaxis.get_offset_text().set(size=18)
    
    
    
def Find_ColMaxValue(column_index,ele80_Mid):
    # column_index = 1
    column = ele80_Mid[:, column_index]
    max_value = np.max(column)
    max_index = np.argmax(column)
    
    min_value = np.min(column)
    min_index = np.argmin(column)
    
    # print(f'max_value= {max_value}; max_index= {max_index}')
    # print(f'min_value= {min_value}; min_index= {min_index}')
    return(max_value,min_value)
# =========== Find Grounf Surface Max/ Min Peak Value ==========================
column_index = 1
Analysis_column = 99

# =================================== Middle Node ===================================
# ------------ Tie Boundary Condition -----------------------
maxTie20_Mid80, minTie20_Mid80 = Find_ColMaxValue(column_index,Tie_W20_Mid80row)
maxTie20_Mid40, minTie20_Mid40 = Find_ColMaxValue(column_index,Tie_W20_Mid40row)
maxTie20_Mid20, minTie20_Mid20 = Find_ColMaxValue(column_index,Tie_W20_Mid20row)
maxTie20_Mid10, minTie20_Mid10 = Find_ColMaxValue(column_index,Tie_W20_Mid10row)

maxTie10_Mid80, minTie10_Mid80 = Find_ColMaxValue(column_index,Tie_W10_Mid80row)
maxTie10_Mid40, minTie10_Mid40 = Find_ColMaxValue(column_index,Tie_W10_Mid40row)
maxTie10_Mid20, minTie10_Mid20 = Find_ColMaxValue(column_index,Tie_W10_Mid20row)
maxTie10_Mid10, minTie10_Mid10 = Find_ColMaxValue(column_index,Tie_W10_Mid10row)

maxTie1_Mid80, minTie1_Mid80 = Find_ColMaxValue(column_index,Tie_W1_Mid80row)
maxTie1_Mid40, minTie1_Mid40 = Find_ColMaxValue(column_index,Tie_W1_Mid40row)
maxTie1_Mid20, minTie1_Mid20 = Find_ColMaxValue(column_index,Tie_W1_Mid20row)
maxTie1_Mid10, minTie1_Mid10 = Find_ColMaxValue(column_index,Tie_W1_Mid10row)

# ------------ LK Dashpot Boundary Condition -----------------------
maxLK20_Mid80, minLK20_Mid80 = Find_ColMaxValue(column_index,LK_W20_Mid80row)
maxLK20_Mid40, minLK20_Mid40 = Find_ColMaxValue(column_index,LK_W20_Mid40row)
maxLK20_Mid20, minLK20_Mid20 = Find_ColMaxValue(column_index,LK_W20_Mid20row)
maxLK20_Mid10, minLK20_Mid10 = Find_ColMaxValue(column_index,LK_W20_Mid10row)

maxLK10_Mid80, minLK10_Mid80 = Find_ColMaxValue(column_index,LK_W10_Mid80row)
maxLK10_Mid40, minLK10_Mid40 = Find_ColMaxValue(column_index,LK_W10_Mid40row)
maxLK10_Mid20, minLK10_Mid20 = Find_ColMaxValue(column_index,LK_W10_Mid20row)
maxLK10_Mid10, minLK10_Mid10 = Find_ColMaxValue(column_index,LK_W10_Mid10row)

maxLK1_Mid80, minLK1_Mid80 = Find_ColMaxValue(column_index,LK_W1_Mid80row)
maxLK1_Mid40, minLK1_Mid40 = Find_ColMaxValue(column_index,LK_W1_Mid40row)
maxLK1_Mid20, minLK1_Mid20 = Find_ColMaxValue(column_index,LK_W1_Mid20row)
maxLK1_Mid10, minLK1_Mid10 = Find_ColMaxValue(column_index,LK_W1_Mid10row)
# ------------ Distributed Beam Boundary Condition -----------------------
maxBeam20_Mid80, minBeam20_Mid80 = Find_ColMaxValue(column_index,Beam_W20_Mid80row)
maxBeam20_Mid40, minBeam20_Mid40 = Find_ColMaxValue(column_index,Beam_W20_Mid40row)
maxBeam20_Mid20, minBeam20_Mid20 = Find_ColMaxValue(column_index,Beam_W20_Mid20row)
maxBeam20_Mid10, minBeam20_Mid10 = Find_ColMaxValue(column_index,Beam_W20_Mid10row)

maxBeam10_Mid80, minBeam10_Mid80 = Find_ColMaxValue(column_index,Beam_W10_Mid80row)
maxBeam10_Mid40, minBeam10_Mid40 = Find_ColMaxValue(column_index,Beam_W10_Mid40row)
maxBeam10_Mid20, minBeam10_Mid20 = Find_ColMaxValue(column_index,Beam_W10_Mid20row)
maxBeam10_Mid10, minBeam10_Mid10 = Find_ColMaxValue(column_index,Beam_W10_Mid10row)

maxBeam1_Mid80, minBeam1_Mid80 = Find_ColMaxValue(column_index,Beam_W1_Mid80row)
maxBeam1_Mid40, minBeam1_Mid40 = Find_ColMaxValue(column_index,Beam_W1_Mid40row)
maxBeam1_Mid20, minBeam1_Mid20 = Find_ColMaxValue(column_index,Beam_W1_Mid20row)
maxBeam1_Mid10, minBeam1_Mid10 = Find_ColMaxValue(column_index,Beam_W1_Mid10row)

# ------------ Distributed Beam and Node Boundary Condition -----------------------
maxBN20_Mid80, minBN20_Mid80 = Find_ColMaxValue(column_index,BeamNode_W20_Mid80row)
maxBN20_Mid40, minBN20_Mid40 = Find_ColMaxValue(column_index,BeamNode_W20_Mid40row)
maxBN20_Mid20, minBN20_Mid20 = Find_ColMaxValue(column_index,BeamNode_W20_Mid20row)
maxBN20_Mid10, minBN20_Mid10 = Find_ColMaxValue(column_index,BeamNode_W20_Mid10row)

maxBN10_Mid80, minBN10_Mid80 = Find_ColMaxValue(column_index,BeamNode_W10_Mid80row)
maxBN10_Mid40, minBN10_Mid40 = Find_ColMaxValue(column_index,BeamNode_W10_Mid40row)
maxBN10_Mid20, minBN10_Mid20 = Find_ColMaxValue(column_index,BeamNode_W10_Mid20row)
maxBN10_Mid10, minBN10_Mid10 = Find_ColMaxValue(column_index,BeamNode_W10_Mid10row)

maxBN1_Mid80, minBN1_Mid80 = Find_ColMaxValue(column_index,BeamNode_W1_Mid80row)
maxBN1_Mid40, minBN1_Mid40 = Find_ColMaxValue(column_index,BeamNode_W1_Mid40row)
maxBN1_Mid20, minBN1_Mid20 = Find_ColMaxValue(column_index,BeamNode_W1_Mid20row)
maxBN1_Mid10, minBN1_Mid10 = Find_ColMaxValue(column_index,BeamNode_W1_Mid10row)

# =================================== Three Quarter Node ===================================
# ------------ Tie Boundary Condition -----------------------
maxTie20_Qua80, minTie20_Qua80 = Find_ColMaxValue(column_index,Tie_W20_Qua80row)
maxTie20_Qua40, minTie20_Qua40 = Find_ColMaxValue(column_index,Tie_W20_Qua40row)
maxTie20_Qua20, minTie20_Qua20 = Find_ColMaxValue(column_index,Tie_W20_Qua20row)
maxTie20_Qua10, minTie20_Qua10 = Find_ColMaxValue(column_index,Tie_W20_Qua10row)

maxTie10_Qua80, minTie10_Qua80 = Find_ColMaxValue(column_index,Tie_W10_Qua80row)
maxTie10_Qua40, minTie10_Qua40 = Find_ColMaxValue(column_index,Tie_W10_Qua40row)
maxTie10_Qua20, minTie10_Qua20 = Find_ColMaxValue(column_index,Tie_W10_Qua20row)
maxTie10_Qua10, minTie10_Qua10 = Find_ColMaxValue(column_index,Tie_W10_Qua10row)

maxTie1_Qua80, minTie1_Qua80 = Find_ColMaxValue(column_index,Tie_W1_Qua80row)
maxTie1_Qua40, minTie1_Qua40 = Find_ColMaxValue(column_index,Tie_W1_Qua40row)
maxTie1_Qua20, minTie1_Qua20 = Find_ColMaxValue(column_index,Tie_W1_Qua20row)
maxTie1_Qua10, minTie1_Qua10 = Find_ColMaxValue(column_index,Tie_W1_Qua10row)

# ------------ LK Dashpot Boundary Condition -----------------------
maxLK20_Qua80, minLK20_Qua80 = Find_ColMaxValue(column_index,LK_W20_Qua80row)
maxLK20_Qua40, minLK20_Qua40 = Find_ColMaxValue(column_index,LK_W20_Qua40row)
maxLK20_Qua20, minLK20_Qua20 = Find_ColMaxValue(column_index,LK_W20_Qua20row)
maxLK20_Qua10, minLK20_Qua10 = Find_ColMaxValue(column_index,LK_W20_Qua10row)

maxLK10_Qua80, minLK10_Qua80 = Find_ColMaxValue(column_index,LK_W10_Qua80row)
maxLK10_Qua40, minLK10_Qua40 = Find_ColMaxValue(column_index,LK_W10_Qua40row)
maxLK10_Qua20, minLK10_Qua20 = Find_ColMaxValue(column_index,LK_W10_Qua20row)
maxLK10_Qua10, minLK10_Qua10 = Find_ColMaxValue(column_index,LK_W10_Qua10row)

maxLK1_Qua80, minLK1_Qua80 = Find_ColMaxValue(column_index,LK_W1_Qua80row)
maxLK1_Qua40, minLK1_Qua40 = Find_ColMaxValue(column_index,LK_W1_Qua40row)
maxLK1_Qua20, minLK1_Qua20 = Find_ColMaxValue(column_index,LK_W1_Qua20row)
maxLK1_Qua10, minLK1_Qua10 = Find_ColMaxValue(column_index,LK_W1_Qua10row)
# ------------ Distributed Beam Boundary Condition -----------------------
maxBeam20_Qua80, minBeam20_Qua80 = Find_ColMaxValue(column_index,Beam_W20_Qua80row)
maxBeam20_Qua40, minBeam20_Qua40 = Find_ColMaxValue(column_index,Beam_W20_Qua40row)
maxBeam20_Qua20, minBeam20_Qua20 = Find_ColMaxValue(column_index,Beam_W20_Qua20row)
maxBeam20_Qua10, minBeam20_Qua10 = Find_ColMaxValue(column_index,Beam_W20_Qua10row)

maxBeam10_Qua80, minBeam10_Qua80 = Find_ColMaxValue(column_index,Beam_W10_Qua80row)
maxBeam10_Qua40, minBeam10_Qua40 = Find_ColMaxValue(column_index,Beam_W10_Qua40row)
maxBeam10_Qua20, minBeam10_Qua20 = Find_ColMaxValue(column_index,Beam_W10_Qua20row)
maxBeam10_Qua10, minBeam10_Qua10 = Find_ColMaxValue(column_index,Beam_W10_Qua10row)

maxBeam1_Qua80, minBeam1_Qua80 = Find_ColMaxValue(column_index,Beam_W1_Qua80row)
maxBeam1_Qua40, minBeam1_Qua40 = Find_ColMaxValue(column_index,Beam_W1_Qua40row)
maxBeam1_Qua20, minBeam1_Qua20 = Find_ColMaxValue(column_index,Beam_W1_Qua20row)
maxBeam1_Qua10, minBeam1_Qua10 = Find_ColMaxValue(column_index,Beam_W1_Qua10row)

# ------------ Distributed Beam and Node Boundary Condition -----------------------
maxBN20_Qua80, minBN20_Qua80 = Find_ColMaxValue(column_index,BeamNode_W20_Qua80row)
maxBN20_Qua40, minBN20_Qua40 = Find_ColMaxValue(column_index,BeamNode_W20_Qua40row)
maxBN20_Qua20, minBN20_Qua20 = Find_ColMaxValue(column_index,BeamNode_W20_Qua20row)
maxBN20_Qua10, minBN20_Qua10 = Find_ColMaxValue(column_index,BeamNode_W20_Qua10row)

maxBN10_Qua80, minBN10_Qua80 = Find_ColMaxValue(column_index,BeamNode_W10_Qua80row)
maxBN10_Qua40, minBN10_Qua40 = Find_ColMaxValue(column_index,BeamNode_W10_Qua40row)
maxBN10_Qua20, minBN10_Qua20 = Find_ColMaxValue(column_index,BeamNode_W10_Qua20row)
maxBN10_Qua10, minBN10_Qua10 = Find_ColMaxValue(column_index,BeamNode_W10_Qua10row)

maxBN1_Qua80, minBN1_Qua80 = Find_ColMaxValue(column_index,BeamNode_W1_Qua80row)
maxBN1_Qua40, minBN1_Qua40 = Find_ColMaxValue(column_index,BeamNode_W1_Qua40row)
maxBN1_Qua20, minBN1_Qua20 = Find_ColMaxValue(column_index,BeamNode_W1_Qua20row)
maxBN1_Qua10, minBN1_Qua10 = Find_ColMaxValue(column_index,BeamNode_W1_Qua10row)

maxAnaly, minAnaly = Find_ColMaxValue(Analysis_column,wave1)
Mesh_Size = np.zeros(4)
ele = 80 
for m in range(len(Mesh_Size)):
    if m == 0 :    
        Mesh_Size[m] = L/ (ele)
    if m > 0:    
        Mesh_Size[m] = Mesh_Size[m-1]*2
        
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

# ============================= Middle Node ========================================
# ------------W20m Tie BC Error Peak Value-----------------------
MidTie20_error = np.zeros((4,3))
errMatrix(MidTie20_error,maxTie20_Mid80,minTie20_Mid80,maxTie20_Mid40,minTie20_Mid40,maxTie20_Mid20,minTie20_Mid20,maxTie20_Mid10,minTie20_Mid10)
# ------------W20m LK BC Error Peak Value-----------------------
MidLK20_error = np.zeros((4,3))
errMatrix(MidLK20_error,maxLK20_Mid80,minLK20_Mid80,maxLK20_Mid40,minLK20_Mid40,maxLK20_Mid20,minLK20_Mid20,maxLK20_Mid10,minLK20_Mid10)
# ------------W20m Distributed Beam BC Error Peak Value-----------------------
MidBeam20_error = np.zeros((4,3))
errMatrix(MidBeam20_error,maxBeam20_Mid80,minBeam20_Mid80,maxBeam20_Mid40,minBeam20_Mid40,maxBeam20_Mid20,minBeam20_Mid20,maxBeam20_Mid10,minBeam20_Mid10)
# ------------W20m Distributed Beam and Node BC Error Peak Value-----------------------
MidBN20_error = np.zeros((4,3))
errMatrix(MidBN20_error,maxBN20_Mid80,minBN20_Mid80,maxBN20_Mid40,minBN20_Mid40,maxBN20_Mid20,minBN20_Mid20,maxBN20_Mid10,minBN20_Mid10)

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
errMatrix(MidBN10_error, maxBN10_Mid80,minBN10_Mid80, maxBN10_Mid40,minBN10_Mid40, maxBN10_Mid20,minBN10_Mid20, maxBN10_Mid10,minBN10_Mid10)

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
errMatrix(MidBN1_error, maxBN1_Mid80,minBN1_Mid80, maxBN1_Mid40,minBN1_Mid40, maxBN1_Mid20,minBN1_Mid20, maxBN1_Mid10,minBN1_Mid10)

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
errMatrix(QuaBN20_error,maxBN20_Qua80,minBN20_Qua80,maxBN20_Qua40,minBN20_Qua40,maxBN20_Qua20,minBN20_Qua20,maxBN20_Qua10,minBN20_Qua10)

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
errMatrix(QuaBN10_error, maxBN10_Qua80,minBN10_Qua80, maxBN10_Qua40,minBN10_Qua40, maxBN10_Qua20,minBN10_Qua20, maxBN10_Qua10,minBN10_Qua10)

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
errMatrix(QuaBN1_error, maxBN1_Qua80,minBN1_Qua80, maxBN1_Qua40,minBN1_Qua40, maxBN1_Qua20,minBN1_Qua20, maxBN1_Qua10,minBN1_Qua10)

# calculate_Error()
MidTieErr20 = np.zeros((4,3))
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

def Calculate_Error(TieErr,Tie_error):
    for i in range(len(Mesh_Size)):
        TieErr[:,0] = Tie_error[:,0]
        TieErr[i,1] = (abs(Tie_error[i,1] - maxAnaly)/maxAnaly)*100
        TieErr[i,2] = (abs(Tie_error[i,2] - minAnaly)/minAnaly)*100

        # TieErr[i,1] = ((Tie_error[i,1] - maxAnaly)/maxAnaly)*100
        # TieErr[i,2] = ((Tie_error[i,2] - minAnaly)/minAnaly)*100
# -------- W20 Relative Error --------------   
Calculate_Error(MidTieErr20, MidTie20_error)
Calculate_Error(MidLKErr20, MidLK20_error)      
Calculate_Error(MidBeamErr20, MidBeam20_error)
Calculate_Error(MidBNErr20, MidBN20_error)   
# -------- W10 Relative Error --------------   
Calculate_Error(MidTieErr10, MidTie10_error)
Calculate_Error(MidLKErr10, MidLK10_error)      
Calculate_Error(MidBeamErr10, MidBeam10_error)
Calculate_Error(MidBNErr10, MidBN10_error)   
# -------- W1 Relative Error --------------   
Calculate_Error(MidTieErr1, MidTie1_error)
Calculate_Error(MidLKErr1, MidLK1_error)      
Calculate_Error(MidBeamErr1, MidBeam1_error)
Calculate_Error(MidBNErr1, MidBN1_error)   


# calculate_Error()
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
Calculate_Error(QuaTieErr20, QuaTie20_error)
Calculate_Error(QuaLKErr20, QuaLK20_error)      
Calculate_Error(QuaBeamErr20, QuaBeam20_error)
Calculate_Error(QuaBNErr20, QuaBN20_error)   
# -------- W10 Relative Error --------------   
Calculate_Error(QuaTieErr10, QuaTie10_error)
Calculate_Error(QuaLKErr10, QuaLK10_error)      
Calculate_Error(QuaBeamErr10, QuaBeam10_error)
Calculate_Error(QuaBNErr10, QuaBN10_error)   
# -------- W1 Relative Error --------------   
Calculate_Error(QuaTieErr1, QuaTie1_error)
Calculate_Error(QuaLKErr1, QuaLK1_error)      
Calculate_Error(QuaBeamErr1, QuaBeam1_error)
Calculate_Error(QuaBNErr1, QuaBN1_error)   


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
    plt.plot(BeamErr[:,0],BeamErr[:,Peak],marker = '<',markersize=8,markerfacecolor = 'white',label = 'Beam Boundary Condition')
    plt.plot(BNErr[:,0],BNErr[:,Peak],marker = 's',markersize=6,markerfacecolor = 'white',label = 'Beam and Node Dashpot Boundary Condition')
    
    plt.legend(loc='best',prop=font_props) #ncol=2,fontsize=16 frameon=False
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    # plt.xlim(0.0, 0.20)
    plt.grid(True)

x_axis = 0.125
figsize = (10,10)
# ----------------- Middle Node Relative Error -------------------------
fig5, (ax13,ax14,ax15) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
fig5.suptitle(f'Ground Surface Different Boundary Maximum Velocity Compare \n(Middle node)',x=0.50,y =0.95,fontsize = 20)
fig5.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
fig5.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

ax13 = plt.subplot(311)
DifferTime_elemetError(1,MidTieErr20, MidLKErr20, MidBeamErr20, MidBNErr20)
ax13.set_title(f"SW 20m",fontsize =18, x=0.20, y=0.45)

ax14 = plt.subplot(312)
DifferTime_elemetError(1,MidTieErr10, MidLKErr10, MidBeamErr10, MidBNErr10)
ax14.set_title(f"SW 10m",fontsize =18, x=0.20, y=0.45)

ax15 = plt.subplot(313)
DifferTime_elemetError(1,MidTieErr1, MidLKErr1, MidBeamErr1, MidBNErr1)
ax15.set_title(f"SW 1m",fontsize =18, x=0.20, y=0.45)


for ax in [ax13,ax14,ax15]:
    formatter = ticker.ScalarFormatter(useMathText =True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set(size=18)
    ax.xaxis.get_offset_text().set(size=18)

fig6, (ax16,ax17,ax18) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
fig6.suptitle(f'Ground Surface Different Boundary Minimum Velocity Compare \n(Middle node)',x=0.50,y =0.95,fontsize = 20)
fig6.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
fig6.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

ax16 = plt.subplot(311)
DifferTime_elemetError(2,MidTieErr20, MidLKErr20, MidBeamErr20, MidBNErr20)
ax16.set_title(f"SW 20m",fontsize =18, x=0.20, y=0.45)

ax17 = plt.subplot(312)
DifferTime_elemetError(2,MidTieErr10, MidLKErr10, MidBeamErr10, MidBNErr10)
ax17.set_title(f"SW 10m",fontsize =18, x=0.20, y=0.45)

ax18 = plt.subplot(313)
DifferTime_elemetError(2,MidTieErr1, MidLKErr1, MidBeamErr1, MidBNErr1)
ax18.set_title(f"SW 1m",fontsize =18, x=0.20, y=0.45)


for ax in [ax16,ax17,ax18]:
    formatter = ticker.ScalarFormatter(useMathText =True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set(size=18)
    ax.xaxis.get_offset_text().set(size=18)
    
# # ----------------- Three Quarter Node Relative Error -------------------------
# x_axis = 0.125
fig7, (ax19,ax20,ax21) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize= figsize)
fig7.suptitle(f'Ground Surface Different Boundary Maximum value Velocity \n(Three Quarter node)',x=0.50,y =0.95,fontsize = 20)
fig7.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
fig7.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

ax19 = plt.subplot(311)
DifferTime_elemetError(1,QuaTieErr20, QuaLKErr20, QuaBeamErr20, QuaBNErr20)
ax19.set_title(f"SW 20m",fontsize =18, x=0.20, y=0.45)

ax20 = plt.subplot(312)
DifferTime_elemetError(1,QuaTieErr10, QuaLKErr10, QuaBeamErr10, QuaBNErr10)
ax20.set_title(f"SW 10m",fontsize =18, x=0.20, y=0.45)

ax21 = plt.subplot(313)
DifferTime_elemetError(1,QuaTieErr1, QuaLKErr1, QuaBeamErr1, QuaBNErr1)
ax21.set_title(f"SW 1m",fontsize =18, x=0.20, y=0.45)

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
fig8.suptitle(f'Ground Surface Different Boundary Minimum Velocity Compare \n(Three Quarter node)',x=0.50,y =0.95,fontsize = 20)
fig8.text(0.045,0.5, r"Relative Error (%)", va= 'center', rotation= 'vertical', fontsize=20)
fig8.text(0.40,0.06,  f'Mesh size ' + r'$\Delta_c$  $\mathrm {(m)}$', va= 'center', fontsize=20)

ax22 = plt.subplot(311)
DifferTime_elemetError(2,QuaTieErr20, QuaLKErr20, QuaBeamErr20, QuaBNErr20)
ax22.set_title(f"SW 20m",fontsize =18, x=0.20, y=0.45)

ax23 = plt.subplot(312)
DifferTime_elemetError(2,QuaTieErr10, QuaLKErr10, QuaBeamErr10, QuaBNErr10)
ax23.set_title(f"SW 10m",fontsize =18, x=0.20, y=0.45)

ax24 = plt.subplot(313)
DifferTime_elemetError(2,QuaTieErr1, QuaLKErr1, QuaBeamErr1, QuaBNErr1)
ax24.set_title(f"SW 1m",fontsize =18, x=0.20, y=0.45)


for ax in [ax22,ax23,ax24]:
    formatter = ticker.ScalarFormatter(useMathText =True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.get_offset_text().set(size=18)
    ax.xaxis.get_offset_text().set(size=18)
    
