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

nx = 160
ny = 80
e1 = 1
n1 = 1
eleArgs = [1, 'PlaneStrain', 2000]
points = [1, 0.0,   0.0, 
          2, 20,  0.0, 
          3, 20,  10.0, 
          4, 0.0,   10.0]
block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)

# # -------- Soil B.C ---------------
# for i in range(ny+1):
#     equalDOF(161*i+1,161*i+161,1,2)

# ============== Build Beam element (13042~13202) (ele 12801~12960) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(13042+j,0.125*j,0.0)
    mass(13042+j,1,1,1)
# -------- fix rotate dof ------------
    fix(13042+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 12801+k, 13042+k, 13043+k, A,E1,Iz, 1, '-release', 3)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,13042+k,1,2)

# ============================ Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 13203,13204~ 13523,13524)-> for S wave------------
    node(13203+2*l, 0.125*l, 0.0)
    node(13204+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(13203+2*l, 0, 1, 1)      # x dir dashpot　
    fix(13204+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 13525,13526~ 13845,13846)-> for P wave ------------
    node(13525+2*l, 0.125*l, 0.0)
    node(13526+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(13525+2*l, 1, 0, 1)      # y dir dashpot　
    fix(13526+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k,13203+2*k,1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+k,13525+2*k,2)
  
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
element('zeroLength',12961, 13204,13203, '-mat',4001,'-dir',xdir)  # node 1: Left side
element('zeroLength',13121, 13524,13523, '-mat',4001,'-dir',xdir)  # node 101: Left side

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',13122, 13526,13525, '-mat',4000,'-dir',ydir)  # node 1: Left side
element('zeroLength',13282, 13846,13845, '-mat',4000,'-dir',ydir)  # node 101: Left side

for q in range(1,nx): #1,nx / nx+1
# -------- Traction dashpot element: Vs with x dir (ele 12961~13121) ------------------
    element('zeroLength',12961+q, 13204+2*q,13203+2*q, '-mat',4003,'-dir',xdir)
# -------- Normal dashpot element: Vp with y dir (ele 13122~13282) ------------------
    element('zeroLength',13122+q, 13526+2*q,13525+2*q, '-mat',4002,'-dir',ydir)

print("Finished creating dashpot material and element...")
# ============ Soil Left and Right "Side" Dashpot =====================================
soilLength = 10 # m
yMesh = soilLength/ny # Y row MeshSize
for l in range(ny+1):
# ========= Left Side =============
# --------- Normal dashpot (node 13847,13848~ 14007,14008)-> for S wave------------
    node(13847+2*l, 0.0, yMesh*l)
    node(13848+2*l, 0.0, yMesh*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(13847+2*l, 0, 1, 1)      # x dir dashpot　
    fix(13848+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 14009,14010~ 14169,14170)-> for P wave------------
    node(14009+2*l, 0.0, yMesh*l)
    node(14010+2*l, 0.0, yMesh*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(14009+2*l, 1, 0, 1)      # y dir dashpot　
    fix(14010+2*l, 1, 1, 1)      # fixed end to let soil fix

# ========= Right Side =============
# --------- Normal dashpot (node 14171,14172~ 14331,14332)-> for S wave------------
    node(14171+2*l, 20.0, yMesh*l)
    node(14172+2*l, 20.0, yMesh*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(14171+2*l, 0, 1, 1)      # x dir dashpot　
    fix(14172+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 14333,14334~ 14493,14494)-> for P wave------------
    node(14333+2*l, 20.0, yMesh*l)
    node(14334+2*l, 20.0, yMesh*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(14333+2*l, 1, 0, 1)      # y dir dashpot　
    fix(14334+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------
for l in range(ny+1):
# ========= Left Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(1+161*l, 13847+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(1+161*l, 14009+2*l, 2)  # y dir

# ========= Right Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(161+161*l, 14171+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(161+161*l, 14333+2*l, 2)  # y dir

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
element('zeroLength',13283, 13848, 13847, '-mat',4004,'-dir',xdir)  # node 1:  -> Smp
element('zeroLength',13363, 14008, 14007, '-mat',4004,'-dir',xdir)  # node 801:  -> Smp
#  ----------- Left side Traction: P wave ----------
element('zeroLength',13364, 14010, 14009, '-mat',4005,'-dir',ydir)  # node 1 -> Sms
element('zeroLength',13444, 14170, 14169, '-mat',4005,'-dir',ydir)  # node 801 -> Sms

#  ----------- Right side Normal: S wave ----------
element('zeroLength',13445, 14172, 14171, '-mat',4004,'-dir',xdir)  # node 8 -> Smp
element('zeroLength',13525, 14332, 14331, '-mat',4004,'-dir',xdir)  # node 808 -> Smp
#  ----------- Right side Traction: P wave ----------
element('zeroLength',13526, 14334, 14333, '-mat',4005,'-dir',ydir)  # node 8 -> Sms
element('zeroLength',13606, 14494, 14493, '-mat',4005,'-dir',ydir)  # node 808 -> Sms

for w in range(1,ny): #1,ny
#----------- Left side Normal Dashpot: (ele 13283~13363)---------- -> Smp
    element('zeroLength',13283+w, 13848+2*w, 13847+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Left side Traction Dashpot: (ele 13364~13444) ---------- -> Sms
    element('zeroLength',13364+w, 14010+2*w, 14009+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

#----------- Right side Normal Dashpot:(ele 13445 ~ 13525) ---------- -> Smp
    element('zeroLength',13445+w, 14172+2*w, 14171+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Right side Traction Dashpot: (ele 13526 ~ 13606) ----------  -> Sms
    element('zeroLength',13526+w, 14334+2*w, 14333+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

print("Finished creating Side dashpot material and element...")

# # # # # # # # # ============================== P wave =================================
# # # # # # # # # ------------ Side Load Pattern ------------------------------
# # # # # # # # for g in range(100):
# # # # # # # # # ------- timeSeries ID: 800~899 (global x force) ----------------------
# # # # # # # #     timeSeries('Path',800+g, '-filePath',f'P_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
# # # # # # # #     pattern('Plain',804+g, 800+g)
# # # # # # # # # ---------- x direction : Sideforce ---------------------
# # # # # # # # # ---------- Distributed at Left Side Beam ----------------------
# # # # # # # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# # # # # # # # # ---------- Distributed at Right Side Beam ----------------------
# # # # # # # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',+20,0)   # for local axes Wy +

# # # # # # # # for g in range(100):
# # # # # # # # # ------- timeSeries ID: 900~999 (global y force)----------------------
# # # # # # # # # ---------- y direction : Sideforce --------------------
# # # # # # # #     timeSeries('Path',900+g, '-filePath',f'P_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
# # # # # # # #     pattern('Plain',904+g, 900+g)
# # # # # # # # # ---------- For P wave : y direction ---------------------
# # # # # # # # # ---------- Distributed at Left Side Beam ----------------------
# # # # # # # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # # # # # # # # ---------- Distributed at Right Side Beam ----------------------
# # # # # # # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',0,+20,0)   # for local axes Wx +
    
# # # # # # # # ============================== S wave ======================================
# # # # # # # # ------------ Side Load Pattern ------------------------------
# # # # # # # for g in range(100):
# # # # # # # # ------- timeSeries ID: 800~899 ----------------------
# # # # # # #     timeSeries('Path',800+g, '-filePath',f'S_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
# # # # # # #     pattern('Plain',804+g, 800+g)
# # # # # # # # ---------- x direction : Sideforce ---------------------
# # # # # # # # ---------- Distributed at Left Side Beam ----------------------
# # # # # # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# # # # # # # # ---------- Distributed at Right Side Beam ----------------------
# # # # # # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',-20,0)   # for local axes Wy +

# # # # # # # for g in range(100):
# # # # # # # # ------- timeSeries ID: 900~999 ----------------------
# # # # # # # # ---------- y direction : Sideforce --------------------
# # # # # # #     timeSeries('Path',900+g, '-filePath',f'S_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
# # # # # # #     pattern('Plain',904+g, 900+g)
# # # # # # # # ---------- For P wave : y direction ---------------------
# # # # # # # # ---------- Distributed at Left Side Beam ----------------------
# # # # # # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # # # # # # # ---------- Distributed at Right Side Beam ----------------------
# # # # # # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wx -
# # # # # # # print("finish SideBeam Force InputFile Apply")

#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
timeSeries('Path',702, '-filePath','fs200_80row.txt','-dt',6.25e-5)
# timeSeries('Path',704, '-filePath','TopForce80row.txt','-dt',3.34e-05)

# # # # # # timeSeries('Linear',705)

pattern('Plain',703, 702)
# load(12961,0,-1)

# # # # ------------- P wave -----------------------------
# # # # for m in range(nx):
# # # #     eleLoad('-ele', 801+m, '-type','-beamUniform',20,0)

# ------------- S wave -----------------------------
for m in range(nx):
    eleLoad('-ele', 12801+m, '-type','-beamUniform',0,20,0)

print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# # -------------- Recorder --------------------------------
# recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# ------------- left column -------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele6401.out', '-time', '-ele',6401, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele12641.out', '-time', '-ele',12641, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node6441.out', '-time', '-node',6441,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node12881.out', '-time', '-node',12881,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', 'Stress/ele81.out', '-time', '-ele',81, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele6481.out', '-time', '-ele',6481, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele12721.out', '-time', '-ele',12721, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node81.out', '-time', '-node',81,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node6521.out', '-time', '-node',6521,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node12961.out', '-time', '-node',12961,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', 'Stress/ele160.out', '-time', '-ele',160, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele6560.out', '-time', '-ele',6560, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele12800.out', '-time', '-ele',12800, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node161.out', '-time', '-node',161,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node6601.out', '-time', '-node',6601,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node13041.out', '-time', '-node',13041,'-dof',1,2,3,'vel')

# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele12681.out', '-time', '-ele',12681, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node12921.out', '-time', '-node',12921,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele12761.out', '-time', '-ele',12761, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node13001.out', '-time', '-node',13001,'-dof',1,2,3,'vel')


system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(6400,6.25e-5)
print("finish analyze:0 ~ 0.8s")

# # printModel('-ele', 701,702,703,704,705,707)
# --------- end to calculate time -------------
end = time.time()
print(end - start)
