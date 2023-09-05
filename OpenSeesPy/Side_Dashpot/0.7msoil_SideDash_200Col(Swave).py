# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 19:39:36 2023

@author: User
"""
import matplotlib.pyplot as plt
import time
import os 
import numpy as np
from openseespy.opensees import *

wipe()
# -------- Start calculaate time -----------------
start = time.time()
print("The time used to execute this is given below")

model('basic', '-ndm', 2, '-ndf' , 2)

E = 15005714.286
nu = 0.3
rho = 2020
nDMaterial('ElasticIsotropic', 2000, E, nu, rho)

nx = 7
ny = 200
e1 = 1
n1 = 1
eleArgs = [1, 'PlaneStrain', 2000]
points = [1, 0.0, 0.0, 
          2, 0.7, 0.0, 
          3, 0.7, 10.0, 
          4, 0.0, 10.0]
block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)

# -------- Soil B.C ---------------
for i in range(ny+1):
    equalDOF(8*i+1,8*i+8,1,2)

# ============== Build Beam element (1609~1616) (ele 1401~1407) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(1609+j,0.1*j,0.0)
    mass(1609+j,1,1,1)
# -------- fix rotate dof ------------
    fix(1609+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 1401+k, 1609+k, 1610+k, A,E1,Iz, 1, '-release', 3)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,1609+k,1,2)

# ============================ Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 1617,1618~ 1631,1632)-> for S wave------------
    node(1617+2*l, 0.1*l, 0.0)
    node(1618+2*l, 0.1*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(1617+2*l, 0, 1, 1)      # x dir dashpot　
    fix(1618+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 1633,1634~ 1647,1648)-> for P wave ------------
    node(1633+2*l, 0.1*l, 0.0)
    node(1634+2*l, 0.1*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(1633+2*l, 1, 0, 1)      # y dir dashpot　
    fix(1634+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k,1617+2*k,1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+k,1633+2*k,2)

print("Finished creating all Bottom dashpot boundary conditions and equalDOF...")
# ------------------- ZeroLength to Build dashpot: Material ----------------------------------
rho = 2020   # kg/m3 
Vp = 100     # m/s 
Vs = 53.45224838248488     ;# m/s 
sizeX = 0.1  # m
B_Smp = 0.5*rho*Vp*sizeX      # lower Left and Right corner node dashpot :N (newton)
B_Sms = 0.5*rho*Vs*sizeX      # lower Left and Right corner node dashpot :N (newton)

B_Cmp = 1.0*rho*Vp*sizeX      # Bottom Center node dashpot :N (newton)
B_Cms = 1.0*rho*Vs*sizeX      # Bottom Center node dashpot :N (newton)

uniaxialMaterial('Viscous',4000, B_Smp, 1)    # P wave: Side node
uniaxialMaterial('Viscous',4001, B_Sms, 1)    # S wave: Side node

uniaxialMaterial('Viscous',4002, B_Cmp, 1)    # P wave: Center node
uniaxialMaterial('Viscous',4003, B_Cms, 1)    # S wave: Center node

#----------- dashpot elements: Vs with x dir / Vp with y-dir------------------
xdir = 1
ydir = 2
# ------ Traction dashpot element: Vs with x dir
element('zeroLength',1408,1618,1617, '-mat',4001,'-dir',xdir)  # node 1: Left side

element('zeroLength',1409,1620,1619, '-mat',4003,'-dir',xdir)
element('zeroLength',1410,1622,1621, '-mat',4003,'-dir',xdir)
element('zeroLength',1411,1624,1623, '-mat',4003,'-dir',xdir)
element('zeroLength',1412,1626,1625, '-mat',4003,'-dir',xdir)
element('zeroLength',1413,1628,1627, '-mat',4003,'-dir',xdir)
element('zeroLength',1414,1630,1629, '-mat',4003,'-dir',xdir)

element('zeroLength',1415,1632,1631, '-mat',4001,'-dir',xdir)  # node 8: Right side

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',1416,1634,1633, '-mat',4000,'-dir',ydir)  # node 1: Left side

element('zeroLength',1417,1636,1635, '-mat',4002,'-dir',ydir)
element('zeroLength',1418,1638,1637, '-mat',4002,'-dir',ydir)
element('zeroLength',1419,1640,1639, '-mat',4002,'-dir',ydir)
element('zeroLength',1420,1642,1641, '-mat',4002,'-dir',ydir)
element('zeroLength',1421,1644,1643, '-mat',4002,'-dir',ydir)
element('zeroLength',1422,1646,1645, '-mat',4002,'-dir',ydir)

element('zeroLength',1423,1648,1647, '-mat',4000,'-dir',ydir)  # node 8: Left side

print("Finished creating Bottom dashpot material and element...")

# ============== Soil Left and Right "Side" Dashpot =====================================
for l in range(ny+1):
# ========= Left Side =============
# --------- Normal dashpot (node 1649,1650~ 2049 ,2050)-> for S wave------------
    node(1649+2*l, 0.0, 0.05*l)
    node(1650+2*l, 0.0, 0.05*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(1649+2*l, 0, 1, 1)      # x dir dashpot　
    fix(1650+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 2051,2052~ 2451,2452)-> for P wave------------
    node(2051+2*l, 0.0, 0.05*l)
    node(2052+2*l, 0.0, 0.05*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(2051+2*l, 1, 0, 1)      # y dir dashpot　
    fix(2052+2*l, 1, 1, 1)      # fixed end to let soil fix

# ========= Right Side =============
# --------- Normal dashpot (node 2453,2454~ 2853,2854)-> for S wave------------
    node(2453+2*l, 0.7, 0.05*l)
    node(2454+2*l, 0.7, 0.05*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(2453+2*l, 0, 1, 1)      # x dir dashpot　
    fix(2454+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 2855,2855~ 3255,3256)-> for P wave------------
    node(2855+2*l, 0.7, 0.05*l)
    node(2856+2*l, 0.7, 0.05*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(2855+2*l, 1, 0, 1)      # y dir dashpot　
    fix(2856+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------
for l in range(ny+1):
# ========= Left Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(1+8*l, 1649+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(1+8*l, 2051+2*l, 2)  # y dir

# ========= Right Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(8+8*l, 2453+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(8+8*l, 2855+2*l, 2)  # y dir

print("Finished creating all Side dashpot boundary conditions and equalDOF...")
# ------------- Side dashpot material -----------------------
S_Smp = 0.5*rho*Vp*sizeX    # side Normal dashpot for S wave   ; lower/Upper  Left and Right corner node
S_Sms = 0.5*rho*Vs*sizeX    # side Traction dashpot for P wave ; lower/Upper Left and Right corner node

S_Cmp = 1.0*rho*Vp*sizeX    # side Normal dashpot for S wave: Netwon
S_Cms = 1.0*rho*Vs*sizeX    # side Traction dashpot for P wave: Netwon

uniaxialMaterial('Viscous',4004, S_Smp, 1)    # "S" wave: Side node
uniaxialMaterial('Viscous',4005, S_Sms, 1)    # "P" wave: Side node

uniaxialMaterial('Viscous',4006, S_Cmp, 1)    # "S" wave: Center node
uniaxialMaterial('Viscous',4007, S_Cms, 1)    # "P" wave: Center node

# =============== Right and Left NODE :different dashpot element==================
#  ----------- Left side Normal: S wave ----------
element('zeroLength',1424, 1650, 1649, '-mat',4004,'-dir',xdir)  # node 1:  -> Smp
element('zeroLength',1624, 2050, 2049, '-mat',4004,'-dir',xdir)  # node 801:  -> Smp
#  ----------- Left side Traction: P wave ----------
element('zeroLength',1625, 2052, 2051, '-mat',4005,'-dir',ydir)  # node 1 -> Sms
element('zeroLength',1825, 2452, 2451, '-mat',4005,'-dir',ydir)  # node 801 -> Sms

#  ----------- Right side Normal: S wave ----------
element('zeroLength',1826, 2454, 2453, '-mat',4004,'-dir',xdir)  # node 8 -> Smp
element('zeroLength',2026, 2854, 2853, '-mat',4004,'-dir',xdir)  # node 808 -> Smp
#  ----------- Right side Traction: P wave ----------
element('zeroLength',2027, 2856, 2855, '-mat',4005,'-dir',ydir)  # node 8 -> Sms
element('zeroLength',2227, 3256, 3255, '-mat',4005,'-dir',ydir)  # node 808 -> Sms

for w in range(1,ny): #1,ny
#----------- Left side Normal Dashpot: (ele 1424~1624)---------- -> Smp
    element('zeroLength',1424+w, 1650+2*w, 1649+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
# #----------- Left side Traction Dashpot: (ele 1625~1825) ---------- -> Sms
    element('zeroLength',1625+w, 2052+2*w, 2051+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

#----------- Right side Normal Dashpot:(ele 1826 ~ 2026) ---------- -> Smp
    element('zeroLength',1826+w, 2454+2*w, 2453+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Right side Traction Dashpot: (ele 2027 ~ 2227) ----------  -> Sms
    element('zeroLength',2027+w, 2856+2*w, 2855+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

print("Finished creating Side dashpot material and element...")

# # ==================== Side Beam node (3257~3457 / 3458~3658) ====================
# for i in range(ny+1):
# # ----- Left Side: 3257~3457 -----------------
#     node(3257+i, 0.0, 0.05*i)
#     fix(3257+i,0,0,1)
# # ----- Right Side: 3458~3658 -----------------
#     node(3458+i,0.7,0.05*i)
#     fix(3458+i,0,0,1)

# # ------------  Beam Element: 2228 ~ 2427 / 2428 ~ 2627 ------------------
# for j in range(ny):
# # ----- Left Side Beam:2228 ~ 2427 -----------------
#     element('elasticBeamColumn', 2228+j, 3257+j, 3258+j, A,E1,Iz, 1, '-release', 3)
# # ----- Right Side Beam:2428 ~ 2627 -----------------
#     element('elasticBeamColumn', 2428+j, 3458+j, 3459+j, A,E1,Iz, 1, '-release', 3)

# # --------- Side Beam and Soil BC -----------------
# for j in range(ny+1):
#     equalDOF(1+8*j,3257+j,1,2)
#     equalDOF(8+8*j,3458+j,1,2)

# output_file = f"ele{col + 1}.txt"

# # ============================== P wave =================================
# # ------------ Side Load Pattern ------------------------------
# for g in range(100):
# # ------- timeSeries ID: 800~899 (global x force) ----------------------
#     timeSeries('Path',800+g, '-filePath',f'P_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
#     pattern('Plain',804+g, 800+g)
# # ---------- x direction : Sideforce ---------------------
# # ---------- Distributed at Left Side Beam ----------------------
#     eleLoad('-ele',2228+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# # ---------- Distributed at Right Side Beam ----------------------
#     eleLoad('-ele',2428+g, '-type', '-beamUniform',+20,0)   # for local axes Wy +

# for g in range(100):
# # ------- timeSeries ID: 900~999 (global y force)----------------------
# # ---------- y direction : Sideforce --------------------
#     timeSeries('Path',900+g, '-filePath',f'P_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
#     pattern('Plain',904+g, 900+g)
# # ---------- For P wave : y direction ---------------------
# # ---------- Distributed at Left Side Beam ----------------------
#     eleLoad('-ele',2228+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # ---------- Distributed at Right Side Beam ----------------------
#     eleLoad('-ele',2428+g, '-type', '-beamUniform',0,+20,0)   # for local axes Wx +
    
# # ============================== S wave ======================================
# # ------------ Side Load Pattern ------------------------------
# for g in range(100):
# # ------- timeSeries ID: 800~899 ----------------------
#     timeSeries('Path',800+g, '-filePath',f'S_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
#     pattern('Plain',804+g, 800+g)
# # ---------- x direction : Sideforce ---------------------
# # ---------- Distributed at Left Side Beam ----------------------
#     eleLoad('-ele',2228+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# # ---------- Distributed at Right Side Beam ----------------------
#     eleLoad('-ele',2428+g, '-type', '-beamUniform',-20,0)   # for local axes Wy +

# for g in range(100):
# # ------- timeSeries ID: 900~999 ----------------------
# # ---------- y direction : Sideforce --------------------
#     timeSeries('Path',900+g, '-filePath',f'S_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
#     pattern('Plain',904+g, 900+g)
# # ---------- For P wave : y direction ---------------------
# # ---------- Distributed at Left Side Beam ----------------------
#     eleLoad('-ele',2228+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # ---------- Distributed at Right Side Beam ----------------------
#     eleLoad('-ele',2428+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wx -
# print("finish SideBeam Force InputFile Apply")

#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
timeSeries('Path',702, '-filePath','2fs.txt','-dt',1e-4)
# timeSeries('Path',704, '-filePath','topForce.txt','-dt',1e-4)

# # # timeSeries('Linear',705)

pattern('Plain',703, 702)
# load(803,0,-1)
# load(805,0,-2)
# # ------------- P wave -----------------------------
# eleLoad('-ele', 1401, '-type','-beamUniform',20,0)
# eleLoad('-ele', 1402, '-type','-beamUniform',20,0)
# eleLoad('-ele', 1403, '-type','-beamUniform',20,0)
# eleLoad('-ele', 1404, '-type','-beamUniform',20,0)
# eleLoad('-ele', 1405, '-type','-beamUniform',20,0)
# eleLoad('-ele', 1406, '-type','-beamUniform',20,0)
# eleLoad('-ele', 1407, '-type','-beamUniform',20,0)

# ------------- S wave -----------------------------
eleLoad('-ele', 1401, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 1402, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 1403, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 1404, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 1405, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 1406, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 1407, '-type','-beamUniform',0,20,0)

print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# -------------- Recorder --------------------------------
# recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# ------------- left column -------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele701.out', '-time', '-ele',701, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele1394.out', '-time', '-ele',1394, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node801.out', '-time', '-node',801,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node1601.out', '-time', '-node',1601,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', 'Stress/ele4.out', '-time', '-ele',4, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele704.out', '-time', '-ele',704, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele1397.out', '-time', '-ele',1397, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node4.out', '-time', '-node',4,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node804.out', '-time', '-node',804,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node1604.out', '-time', '-node',1604,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', 'Stress/ele7.out', '-time', '-ele',7, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele707.out', '-time', '-ele',707, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele1400.out', '-time', '-ele',1400, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node8.out', '-time', '-node',8,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node808.out', '-time', '-node',808,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node1608.out', '-time', '-node',1608,'-dof',1,2,3,'vel')

# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele1395.out', '-time', '-ele',1395, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node1603.out', '-time', '-node',1603,'-dof',1,2,3,'vel')

# # ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele1399.out', '-time', '-ele',1399, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node1606.out', '-time', '-node',1606,'-dof',1,2,3,'vel')


system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(8000,1e-4)
print("finish analyze:0 ~ 0.8s")

# # printModel('-ele', 701,702,703,704,705,707)
# --------- end to calculate time -------------
end = time.time()
print(end - start)

