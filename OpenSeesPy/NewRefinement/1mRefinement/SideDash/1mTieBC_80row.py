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

E = 208000000
nu = 0.3
rho = 2000
nDMaterial('ElasticIsotropic', 2000, E, nu, rho)

nx = 8
ny = 80
e1 = 1
n1 = 1
eleArgs = [1, 'PlaneStrain', 2000]
points = [1, 0.0,   0.0, 
          2, 1.0,  0.0, 
          3, 1.0,  10.0, 
          4, 0.0,   10.0]
block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)

# -------- Soil B.C ---------------
for i in range(ny+1):
    equalDOF(9*i+1,9*i+9,1,2)

# ============== Build Beam element (730~738) (ele 641~648) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(730+j,0.125*j,0.0)
    mass(730+j,1,1,1)
# -------- fix rotate dof ------------
    fix(730+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 641+k, 730+k, 731+k, A,E1,Iz, 1, '-release', 3)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,730+k,1,2)

# ============================ Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 739,740~ 755,756)-> for S wave------------
    node(739+2*l, 0.125*l, 0.0)
    node(740+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(739+2*l, 0, 1, 1)      # x dir dashpot　
    fix(740+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 757,758~ 773,774)-> for P wave ------------
    node(757+2*l, 0.125*l, 0.0)
    node(758+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(757+2*l, 1, 0, 1)      # y dir dashpot　
    fix(758+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k,739+2*k,1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+k,757+2*k,2)

print("Finished creating all Bottom dashpot boundary conditions and equalDOF...")
# ------------------- ZeroLength to Build dashpot: Material ----------------------------------
rho = 2000   # kg/m3 
Vp = 374.166    # m/s 
Vs = 200     ;# m/s 
sizeX = 0.125  # m
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
element('zeroLength',649,740,739, '-mat',4001,'-dir',xdir)  # node 1: Left side

element('zeroLength',650,742,741, '-mat',4003,'-dir',xdir)
element('zeroLength',651,744,743, '-mat',4003,'-dir',xdir)
element('zeroLength',652,746,745, '-mat',4003,'-dir',xdir)
element('zeroLength',653,748,747, '-mat',4003,'-dir',xdir)
element('zeroLength',654,750,749, '-mat',4003,'-dir',xdir)
element('zeroLength',655,752,751, '-mat',4003,'-dir',xdir)
element('zeroLength',656,754,753, '-mat',4003,'-dir',xdir)

element('zeroLength',657,756,755, '-mat',4001,'-dir',xdir)  # node 8: Right side

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',658, 758, 757, '-mat',4000,'-dir',ydir)  # node 1: Left side

element('zeroLength',659, 760, 759, '-mat',4002,'-dir',ydir)
element('zeroLength',660,762,761, '-mat',4002,'-dir',ydir)
element('zeroLength',661,764,763, '-mat',4002,'-dir',ydir)
element('zeroLength',662,766,765, '-mat',4002,'-dir',ydir)
element('zeroLength',663,768,767, '-mat',4002,'-dir',ydir)
element('zeroLength',664,770,769, '-mat',4002,'-dir',ydir)
element('zeroLength',665,772,771, '-mat',4002,'-dir',ydir)

element('zeroLength',666,774,773, '-mat',4000,'-dir',ydir)  # node 8: Left side

print("Finished creating Bottom dashpot material and element...")

# ============== Soil Left and Right "Side" Dashpot =====================================
soilLength = 10 #m
yMesh = soilLength/ny # Y row MeshSize
for l in range(ny+1):
# ========= Left Side =============
# --------- Normal dashpot (node 775,776~ 935,936)-> for S wave------------
    node(775+2*l, 0.0, yMesh*l)
    node(776+2*l, 0.0, yMesh*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(775+2*l, 0, 1, 1)      # x dir dashpot　
    fix(776+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 937,938~ 1097,1098)-> for P wave------------
    node(937+2*l, 0.0, yMesh*l)
    node(938+2*l, 0.0, yMesh*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(937+2*l, 1, 0, 1)      # y dir dashpot　
    fix(938+2*l, 1, 1, 1)      # fixed end to let soil fix

# ========= Right Side =============
# --------- Normal dashpot (node 1099,1100~ 1259,1260)-> for S wave------------
    node(1099+2*l, 1.0, yMesh*l)
    node(1100+2*l, 1.0, yMesh*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(1099+2*l, 0, 1, 1)      # x dir dashpot　
    fix(1100+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 1261,1262~ 1421,1422)-> for P wave------------
    node(1261+2*l, 1.0, yMesh*l)
    node(1262+2*l, 1.0, yMesh*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(1261+2*l, 1, 0, 1)      # y dir dashpot　
    fix(1262+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------
for l in range(ny+1):
# ========= Left Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(1+9*l, 775+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(1+9*l, 937+2*l, 2)  # y dir

# ========= Right Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(9+9*l, 1099+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(9+9*l, 1261+2*l, 2)  # y dir

print("Finished creating all Side dashpot boundary conditions and equalDOF...")
# ------------- Side dashpot material -----------------------
sizeX1 = yMesh
S_Smp = 0.5*rho*Vp*sizeX1    # side Normal dashpot for S wave   ; lower/Upper  Left and Right corner node
S_Sms = 0.5*rho*Vs*sizeX1    # side Traction dashpot for P wave ; lower/Upper Left and Right corner node

S_Cmp = 1.0*rho*Vp*sizeX1    # side Normal dashpot for S wave: Netwon
S_Cms = 1.0*rho*Vs*sizeX1    # side Traction dashpot for P wave: Netwon

uniaxialMaterial('Viscous',4004, S_Smp, 1)    # "S" wave: Side node
uniaxialMaterial('Viscous',4005, S_Sms, 1)    # "P" wave: Side node

uniaxialMaterial('Viscous',4006, S_Cmp, 1)    # "S" wave: Center node
uniaxialMaterial('Viscous',4007, S_Cms, 1)    # "P" wave: Center node

# =============== Right and Left NODE :different dashpot element==================
#  ----------- Left side Normal: S wave ----------
element('zeroLength',667, 776, 775, '-mat',4004,'-dir',xdir)  # node 1:  -> Smp
element('zeroLength',747, 936, 935, '-mat',4004,'-dir',xdir)  # node 801:  -> Smp
#  ----------- Left side Traction: P wave ----------
element('zeroLength',748, 938, 937, '-mat',4005,'-dir',ydir)  # node 1 -> Sms
element('zeroLength',828, 1098, 1097, '-mat',4005,'-dir',ydir)  # node 801 -> Sms

#  ----------- Right side Normal: S wave ----------
element('zeroLength',829, 1100, 1099, '-mat',4004,'-dir',xdir)  # node 8 -> Smp
element('zeroLength',909, 1260, 1259, '-mat',4004,'-dir',xdir)  # node 808 -> Smp
#  ----------- Right side Traction: P wave ----------
element('zeroLength',910, 1262, 1261, '-mat',4005,'-dir',ydir)  # node 8 -> Sms
element('zeroLength',990, 1422, 1421, '-mat',4005,'-dir',ydir)  # node 808 -> Sms

for w in range(1,ny): #1,ny
#----------- Left side Normal Dashpot: (ele 667~747)---------- -> Smp
    element('zeroLength',667+w, 776+2*w, 775+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
# #----------- Left side Traction Dashpot: (ele 748~828) ---------- -> Sms
    element('zeroLength',748+w, 938+2*w, 937+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

#----------- Right side Normal Dashpot:(ele 829 ~ 909) ---------- -> Smp
    element('zeroLength',829+w, 1100+2*w, 1099+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Right side Traction Dashpot: (ele 910 ~ 990) ----------  -> Sms
    element('zeroLength',910+w, 1262+2*w, 1261+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

print("Finished creating Side dashpot material and element...")
# # # # # # # ============================== P wave =================================
# # # # # # # ------------ Side Load Pattern ------------------------------
# # # # # # for g in range(100):
# # # # # # # ------- timeSeries ID: 800~899 (global x force) ----------------------
# # # # # #     timeSeries('Path',800+g, '-filePath',f'P_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
# # # # # #     pattern('Plain',804+g, 800+g)
# # # # # # # ---------- x direction : Sideforce ---------------------
# # # # # # # ---------- Distributed at Left Side Beam ----------------------
# # # # # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# # # # # # # ---------- Distributed at Right Side Beam ----------------------
# # # # # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',+20,0)   # for local axes Wy +

# # # # # # for g in range(100):
# # # # # # # ------- timeSeries ID: 900~999 (global y force)----------------------
# # # # # # # ---------- y direction : Sideforce --------------------
# # # # # #     timeSeries('Path',900+g, '-filePath',f'P_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
# # # # # #     pattern('Plain',904+g, 900+g)
# # # # # # # ---------- For P wave : y direction ---------------------
# # # # # # # ---------- Distributed at Left Side Beam ----------------------
# # # # # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # # # # # # ---------- Distributed at Right Side Beam ----------------------
# # # # # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',0,+20,0)   # for local axes Wx +
    
# # # # # # ============================== S wave ======================================
# # # # # # ------------ Side Load Pattern ------------------------------
# # # # # for g in range(100):
# # # # # # ------- timeSeries ID: 800~899 ----------------------
# # # # #     timeSeries('Path',800+g, '-filePath',f'S_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
# # # # #     pattern('Plain',804+g, 800+g)
# # # # # # ---------- x direction : Sideforce ---------------------
# # # # # # ---------- Distributed at Left Side Beam ----------------------
# # # # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# # # # # # ---------- Distributed at Right Side Beam ----------------------
# # # # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',-20,0)   # for local axes Wy +

# # # # # for g in range(100):
# # # # # # ------- timeSeries ID: 900~999 ----------------------
# # # # # # ---------- y direction : Sideforce --------------------
# # # # #     timeSeries('Path',900+g, '-filePath',f'S_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
# # # # #     pattern('Plain',904+g, 900+g)
# # # # # # ---------- For P wave : y direction ---------------------
# # # # # # ---------- Distributed at Left Side Beam ----------------------
# # # # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # # # # # ---------- Distributed at Right Side Beam ----------------------
# # # # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wx -
# # # # # print("finish SideBeam Force InputFile Apply")

#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
timeSeries('Path',702, '-filePath','fs200_80row.txt','-dt',6.25e-5)
# timeSeries('Path',704, '-filePath','TopForce80row.txt','-dt',3.34e-05)

# # timeSeries('Linear',705)

pattern('Plain',703, 702)
# load(725,0,-1)

# # # # # ------------- P wave -----------------------------
# # # # eleLoad('-ele', 71, '-type','-beamUniform',20,0)
# # # # eleLoad('-ele', 72, '-type','-beamUniform',20,0)
# # # # eleLoad('-ele', 73, '-type','-beamUniform',20,0)
# # # # eleLoad('-ele', 74, '-type','-beamUniform',20,0)
# # # # eleLoad('-ele', 75, '-type','-beamUniform',20,0)
# # # # eleLoad('-ele', 76, '-type','-beamUniform',20,0)
# # # # eleLoad('-ele', 77, '-type','-beamUniform',20,0)

# ------------- S wave -----------------------------
eleLoad('-ele', 641, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 642, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 643, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 644, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 645, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 646, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 647, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 648, '-type','-beamUniform',0,20,0)

print("finish Input Force File:0 ~ 0.1s(+1), Input Stress B.C:0.2~0.3s(-1)")

# -------------- Recorder --------------------------------
# recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# ------------- left column -------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele321.out', '-time', '-ele',321, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele633.out', '-time', '-ele',633, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node361.out', '-time', '-node',361,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node721.out', '-time', '-node',721,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', 'Stress/ele5.out', '-time', '-ele',5, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele325.out', '-time', '-ele',325, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele637.out', '-time', '-ele',637, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node5.out', '-time', '-node',5,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node365.out', '-time', '-node',365,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node725.out', '-time', '-node',725,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', 'Stress/ele8.out', '-time', '-ele',8, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele328.out', '-time', '-ele',328, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele640.out', '-time', '-ele',640, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node9.out', '-time', '-node',9,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node369.out', '-time', '-node',369,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node729.out', '-time', '-node',729,'-dof',1,2,3,'vel')

# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele635.out', '-time', '-ele',635, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node723.out', '-time', '-node',723,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele639.out', '-time', '-ele',639, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node727.out', '-time', '-node',727,'-dof',1,2,3,'vel')


system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(6400,6.25e-5)
print("finish analyze:0 ~ 0.8s")

# # # # printModel('-ele', 701,702,703,704,705,707)
# --------- end to calculate time -------------
end = time.time()
print(end - start)
