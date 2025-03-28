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

nx = 80
ny = 10
e1 = 1
n1 = 1
eleArgs = [1, 'PlaneStrain', 2000]
points = [1, 0.0,   0.0, 
          2, 10,  0.0, 
          3, 10,  10.0, 
          4, 0.0,   10.0]
block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)

# # -------- Soil B.C ---------------
# for i in range(ny+1):
#     equalDOF(81*i+1,81*i+81,1,2)

# ============== Build Beam element (892~972) (ele 801~880) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(892+j,0.125*j,0.0)
    mass(892+j,1,1,1)
# -------- fix rotate dof ------------
    fix(892+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 801+k, 892+k, 893+k, A,E1,Iz, 1, '-release', 3)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,892+k,1,2)

# ============================ Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 973,974~ 1133,1134)-> for S wave------------
    node(973+2*l, 0.125*l, 0.0)
    node(974+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(973+2*l, 0, 1, 1)      # x dir dashpot　
    fix(974+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 1135,1136~ 1295,1296)-> for P wave ------------
    node(1135+2*l, 0.125*l, 0.0)
    node(1136+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(1135+2*l, 1, 0, 1)      # y dir dashpot　
    fix(1136+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k,973+2*k,1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+k,1135+2*k,2)

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
element('zeroLength',881, 974,973, '-mat',4001,'-dir',xdir)  # node 1: Left side
element('zeroLength',961, 1134,1133, '-mat',4001,'-dir',xdir)  # node 101: Left side

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',962, 1136,1135, '-mat',4000,'-dir',ydir)  # node 1: Left side
element('zeroLength',1042, 1296,1295, '-mat',4000,'-dir',ydir)  # node 101: Left side

for q in range(1,nx): #1,nx / nx+1
# -------- Traction dashpot element: Vs with x dir (ele 881~961) ------------------
    element('zeroLength',881+q, 974+2*q,973+2*q, '-mat',4003,'-dir',xdir)

# -------- Normal dashpot element: Vp with y dir (ele 962~1042) ------------------
    element('zeroLength',962+q, 1136+2*q,1135+2*q, '-mat',4002,'-dir',ydir)

print("Finished creating dashpot material and element...")
# ============ Soil Left and Right "Side" Dashpot =====================================
soilLength = 10 # m
yMesh = soilLength/ny # Y row MeshSize
for l in range(ny+1):
# ========= Left Side =============
# --------- Normal dashpot (node 1297,1298~ 1317,1318)-> for S wave------------
    node(1297+2*l, 0.0, yMesh*l)
    node(1298+2*l, 0.0, yMesh*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(1297+2*l, 0, 1, 1)      # x dir dashpot　
    fix(1298+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 1319,1320~ 1339,1340)-> for P wave------------
    node(1319+2*l, 0.0, yMesh*l)
    node(1320+2*l, 0.0, yMesh*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(1319+2*l, 1, 0, 1)      # y dir dashpot　
    fix(1320+2*l, 1, 1, 1)      # fixed end to let soil fix

# ========= Right Side =============
# --------- Normal dashpot (node 1341,1342~ 1361,1362)-> for S wave------------
    node(1341+2*l, 10.0, yMesh*l)
    node(1342+2*l, 10.0, yMesh*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(1341+2*l, 0, 1, 1)      # x dir dashpot　
    fix(1342+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 1363,1364~ 1383,1384)-> for P wave------------
    node(1363+2*l, 10.0, yMesh*l)
    node(1364+2*l, 10.0, yMesh*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(1363+2*l, 1, 0, 1)      # y dir dashpot　
    fix(1364+2*l, 1, 1, 1)      # fixed end to let soil fix
 
# ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------
for l in range(ny+1):
# ========= Left Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(1+81*l, 1297+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(1+81*l, 1319+2*l, 2)  # y dir

# ========= Right Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(81+81*l, 1341+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(81+81*l, 1363+2*l, 2)  # y dir
  
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
element('zeroLength',1043, 1298, 1297, '-mat',4004,'-dir',xdir)  # node 1:  -> Smp
element('zeroLength',1053, 1318, 1317, '-mat',4004,'-dir',xdir)  # node 801:  -> Smp
#  ----------- Left side Traction: P wave ----------
element('zeroLength',1054, 1320, 1319, '-mat',4005,'-dir',ydir)  # node 1 -> Sms
element('zeroLength',1064, 1340, 1339, '-mat',4005,'-dir',ydir)  # node 801 -> Sms

#  ----------- Right side Normal: S wave ----------
element('zeroLength',1065, 1342, 1341, '-mat',4004,'-dir',xdir)  # node 8 -> Smp
element('zeroLength',1075, 1362, 1361, '-mat',4004,'-dir',xdir)  # node 808 -> Smp
#  ----------- Right side Traction: P wave ----------
element('zeroLength',1076, 1364, 1363, '-mat',4005,'-dir',ydir)  # node 8 -> Sms
element('zeroLength',1086, 1384, 1383, '-mat',4005,'-dir',ydir)  # node 808 -> Sms

for w in range(1,ny): #1,ny
#----------- Left side Normal Dashpot: (ele 1043~1053)---------- -> Smp
    element('zeroLength',1043+w, 1298+2*w, 1297+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Left side Traction Dashpot: (ele 1054~1064) ---------- -> Sms
    element('zeroLength',1054+w, 1320+2*w, 1319+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

#----------- Right side Normal Dashpot:(ele 1065 ~ 1075) ---------- -> Smp
    element('zeroLength',1065+w, 1342+2*w, 1341+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Right side Traction Dashpot: (ele 1076 ~ 1086) ----------  -> Sms
    element('zeroLength',1076+w, 1364+2*w, 1363+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

print("Finished creating Side dashpot material and element...")

# # # # # ============================== P wave =================================
# # # # # ------------ Side Load Pattern ------------------------------
# # # # for g in range(100):
# # # # # ------- timeSeries ID: 800~899 (global x force) ----------------------
# # # #     timeSeries('Path',800+g, '-filePath',f'P_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
# # # #     pattern('Plain',804+g, 800+g)
# # # # # ---------- x direction : Sideforce ---------------------
# # # # # ---------- Distributed at Left Side Beam ----------------------
# # # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# # # # # ---------- Distributed at Right Side Beam ----------------------
# # # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',+20,0)   # for local axes Wy +

# # # # for g in range(100):
# # # # # ------- timeSeries ID: 900~999 (global y force)----------------------
# # # # # ---------- y direction : Sideforce --------------------
# # # #     timeSeries('Path',900+g, '-filePath',f'P_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
# # # #     pattern('Plain',904+g, 900+g)
# # # # # ---------- For P wave : y direction ---------------------
# # # # # ---------- Distributed at Left Side Beam ----------------------
# # # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # # # # ---------- Distributed at Right Side Beam ----------------------
# # # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',0,+20,0)   # for local axes Wx +
    
# # # # ============================== S wave ======================================
# # # # ------------ Side Load Pattern ------------------------------
# # # for g in range(100):
# # # # ------- timeSeries ID: 800~899 ----------------------
# # #     timeSeries('Path',800+g, '-filePath',f'S_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
# # #     pattern('Plain',804+g, 800+g)
# # # # ---------- x direction : Sideforce ---------------------
# # # # ---------- Distributed at Left Side Beam ----------------------
# # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# # # # ---------- Distributed at Right Side Beam ----------------------
# # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',-20,0)   # for local axes Wy +

# # # for g in range(100):
# # # # ------- timeSeries ID: 900~999 ----------------------
# # # # ---------- y direction : Sideforce --------------------
# # #     timeSeries('Path',900+g, '-filePath',f'S_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
# # #     pattern('Plain',904+g, 900+g)
# # # # ---------- For P wave : y direction ---------------------
# # # # ---------- Distributed at Left Side Beam ----------------------
# # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # # # ---------- Distributed at Right Side Beam ----------------------
# # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wx -
# # # print("finish SideBeam Force InputFile Apply")

#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
timeSeries('Path',702, '-filePath','fs200_10row.txt','-dt',5e-4)
# timeSeries('Path',704, '-filePath','TopForce10row.txt','-dt',2.67e-4)

# # # timeSeries('Linear',705)

pattern('Plain',703, 702)
# load(851,0,-1)

# # ------------- P wave -----------------------------
# # for m in range(nx):
# #     eleLoad('-ele', 801+m, '-type','-beamUniform',20,0)

# ------------- S wave -----------------------------
for m in range(nx):
    eleLoad('-ele', 801+m, '-type','-beamUniform',0,20,0)

# print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# -------------- Recorder --------------------------------
# recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# ------------- left column -------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele401.out', '-time', '-ele',401, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele721.out', '-time', '-ele',721, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node406.out', '-time', '-node',406,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node811.out', '-time', '-node',811,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', 'Stress/ele41.out', '-time', '-ele',41, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele441.out', '-time', '-ele',441, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele761.out', '-time', '-ele',761, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node41.out', '-time', '-node',41,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node446.out', '-time', '-node',446,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node851.out', '-time', '-node',851,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', 'Stress/ele80.out', '-time', '-ele',80, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele480.out', '-time', '-ele',480, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele800.out', '-time', '-ele',800, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node81.out', '-time', '-node',81,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node486.out', '-time', '-node',486,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node891.out', '-time', '-node',891,'-dof',1,2,3,'vel')

# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele740.out', '-time', '-ele',740, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node831.out', '-time', '-node',831,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele781.out', '-time', '-ele',781, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node871.out', '-time', '-node',871,'-dof',1,2,3,'vel')


system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(800,5e-4)
print("finish analyze:0 ~ 0.8s")

# # printModel('-ele', 701,702,703,704,705,707)
# --------- end to calculate time -------------
end = time.time()
print(end - start)
