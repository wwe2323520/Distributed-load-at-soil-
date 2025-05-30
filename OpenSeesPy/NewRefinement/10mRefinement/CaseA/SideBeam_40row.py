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
ny = 40
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

# ============== Build Beam element (3322~3402) (ele 3201~3280) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(3322+j,0.125*j,0.0)
    mass(3322+j,1,1,1)
# -------- fix rotate dof ------------
    fix(3322+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 3201+k, 3322+k, 3323+k, A,E1,Iz, 1, '-release', 3)
 
# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,3322+k,1,2)

# ============================ Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 3403,3404~ 3563,3564)-> for S wave------------
    node(3403+2*l, 0.125*l, 0.0)
    node(3404+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(3403+2*l, 0, 1, 1)      # x dir dashpot　
    fix(3404+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 3565,3566~ 3725,3726)-> for P wave ------------
    node(3565+2*l, 0.125*l, 0.0)
    node(3566+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(3565+2*l, 1, 0, 1)      # y dir dashpot　
    fix(3566+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k,3403+2*k,1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+k,3565+2*k,2)

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
element('zeroLength',3281, 3404,3403, '-mat',4001,'-dir',xdir)  # node 1: Left side
element('zeroLength',3361, 3564,3563, '-mat',4001,'-dir',xdir)  # node 101: Left side

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',3362, 3566,3565, '-mat',4000,'-dir',ydir)  # node 1: Left side
element('zeroLength',3442, 3726,3725, '-mat',4000,'-dir',ydir)  # node 101: Left side

for q in range(1,nx): #1,nx / nx+1
# -------- Traction dashpot element: Vs with x dir (ele 3281~3361) ------------------
    element('zeroLength',3281+q, 3404+2*q,3403+2*q, '-mat',4003,'-dir',xdir)
 
# -------- Normal dashpot element: Vp with y dir (ele 3362~3442) ------------------
    element('zeroLength',3362+q, 3566+2*q,3565+2*q, '-mat',4002,'-dir',ydir)

print("Finished creating dashpot material and element...")
# ============ Soil Left and Right "Side" Dashpot =====================================
soilLength = 10 # m
yMesh = soilLength/ny # Y row MeshSize
for l in range(ny+1):
# ========= Left Side =============
# --------- Normal dashpot (node 3727,3728~ 3807,3808)-> for S wave------------
    node(3727+2*l, 0.0, yMesh*l)
    node(3728+2*l, 0.0, yMesh*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(3727+2*l, 0, 1, 1)      # x dir dashpot　
    fix(3728+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 3809,2150~ 3889,3890)-> for P wave------------
    node(3809+2*l, 0.0, yMesh*l)
    node(3810+2*l, 0.0, yMesh*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(3809+2*l, 1, 0, 1)      # y dir dashpot　
    fix(3810+2*l, 1, 1, 1)      # fixed end to let soil fix

# ========= Right Side =============
# --------- Normal dashpot (node 3891,3892~ 3971,3972)-> for S wave------------
    node(3891+2*l, 10.0, yMesh*l)
    node(3892+2*l, 10.0, yMesh*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(3891+2*l, 0, 1, 1)      # x dir dashpot　
    fix(3892+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 3973,3974~ 4053,4054)-> for P wave------------
    node(3973+2*l, 10.0, yMesh*l)
    node(3974+2*l, 10.0, yMesh*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(3973+2*l, 1, 0, 1)      # y dir dashpot　
    fix(3974+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------
for l in range(ny+1):
# ========= Left Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(1+81*l, 3727+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(1+81*l, 3809+2*l, 2)  # y dir

# ========= Right Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(81+81*l, 3891+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(81+81*l, 3973+2*l, 2)  # y dir

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
element('zeroLength',3443, 3728, 3727, '-mat',4004,'-dir',xdir)  # node 1:  -> Smp
element('zeroLength',3483, 3808, 3807, '-mat',4004,'-dir',xdir)  # node 801:  -> Smp
#  ----------- Left side Traction: P wave ----------
element('zeroLength',3484, 3810, 3809, '-mat',4005,'-dir',ydir)  # node 1 -> Sms
element('zeroLength',3524, 3890, 3889, '-mat',4005,'-dir',ydir)  # node 801 -> Sms

#  ----------- Right side Normal: S wave ----------
element('zeroLength',3525, 3892, 3891, '-mat',4004,'-dir',xdir)  # node 8 -> Smp
element('zeroLength',3565, 3972, 3971, '-mat',4004,'-dir',xdir)  # node 808 -> Smp
#  ----------- Right side Traction: P wave ----------
element('zeroLength',3566, 3974, 3973, '-mat',4005,'-dir',ydir)  # node 8 -> Sms
element('zeroLength',3606, 4054 ,4053, '-mat',4005,'-dir',ydir)  # node 808 -> Sms

for w in range(1,ny): #1,ny
#----------- Left side Normal Dashpot: (ele 3443~3483)---------- -> Smp
    element('zeroLength',3443+w, 3728+2*w, 3727+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Left side Traction Dashpot: (ele 3484~3524) ---------- -> Sms
    element('zeroLength',3484+w, 3810+2*w, 3809+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

#----------- Right side Normal Dashpot:(ele 3525 ~ 3565) ---------- -> Smp
    element('zeroLength',3525+w, 3892+2*w, 3891+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Right side Traction Dashpot: (ele 3566 ~ 3606) ----------  -> Sms
    element('zeroLength',3566+w, 3974+2*w, 3973+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

print("Finished creating Side dashpot material and element...")

# ==================== Side Beam node (4055~4095 / 4096~4136) ====================
for i in range(ny+1):
# ----- Left Side: 4055~4095 -----------------
    node(4055+i, 0.0, yMesh*i)
    fix(4055+i,0,0,1)
# ----- Right Side: 4096~4136 -----------------
    node(4096+i,10.0,yMesh*i)
    fix(4096+i,0,0,1)

# ------------  Beam Element: 3607 ~ 3646 / 3647 ~ 3686 ------------------
for j in range(ny):
# ----- Left Side Beam:3607 ~ 3646 -----------------
    element('elasticBeamColumn', 3607+j, 4055+j, 4056+j, A,E1,Iz, 1, '-release', 3)
# ----- Right Side Beam:3647 ~ 3686 -----------------
    element('elasticBeamColumn', 3647+j, 4096+j, 4097+j, A,E1,Iz, 1, '-release', 3)

# --------- Side Beam and Soil BC -----------------
for j in range(ny+1):
    equalDOF(1+81*j,4055+j,1,2)
    equalDOF(81+81*j,4096+j,1,2)
 
# ============================== S wave ======================================
# ------------ Side Load Pattern ------------------------------
for g in range(ny):
# ------- timeSeries ID: 800~839 / Pattern ID: 804~843----------------------
    timeSeries('Path',800+g, '-filePath',f'SSideforce_40rowx/ele{1+g}.txt','-dt',1.25e-4)
    pattern('Plain',804+g, 800+g)
# ---------- x direction : Sideforce ---------------------
# ---------- Distributed at Left Side Beam ----------------------
    eleLoad('-ele',3607+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# ---------- Distributed at Right Side Beam ----------------------
    eleLoad('-ele',3647+g, '-type', '-beamUniform',-20,0)   # for local axes Wy +

for g in range(ny):
# ------- timeSeries ID: 840~879 / Pattern ID:844~883 ----------------------
# ---------- y direction : Sideforce --------------------
    timeSeries('Path',840+g, '-filePath',f'SSideforce_40rowy/ele{1+g}.txt','-dt',1.25e-4)
    pattern('Plain',844+g, 840+g)
# ---------- For P wave : y direction ---------------------
# ---------- Distributed at Left Side Beam ----------------------
    eleLoad('-ele',3607+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# ---------- Distributed at Right Side Beam ----------------------
    eleLoad('-ele',3647+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wx -

print("finish SideBeam Force InputFile Apply")

#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
timeSeries('Path',702, '-filePath','fs200_40row.txt','-dt',1.25e-4)
# timeSeries('Path',704, '-filePath','TopForce40row.txt','-dt',6.68e-05)

# # # # timeSeries('Linear',705)

pattern('Plain',703, 702)
# load(3281,0,-1)

# # ------------- P wave -----------------------------
# # for m in range(nx):
# #     eleLoad('-ele', 1601+m, '-type','-beamUniform',20,0)

# ------------- S wave -----------------------------
for m in range(nx):
    eleLoad('-ele', 3201+m, '-type','-beamUniform',0,20,0)

print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# -------------- Recorder --------------------------------
# recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# ------------- left column -------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele1601.out', '-time', '-ele',1601, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele3121.out', '-time', '-ele',3121, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node1621.out', '-time', '-node',1621,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node3241.out', '-time', '-node',3241,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', 'Stress/ele41.out', '-time', '-ele',41, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele1641.out', '-time', '-ele',1641, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele3161.out', '-time', '-ele',3161, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node41.out', '-time', '-node',41,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node1661.out', '-time', '-node',1661,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node3281.out', '-time', '-node',3281,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', 'Stress/ele80.out', '-time', '-ele',80, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele1680.out', '-time', '-ele',1680, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele3200.out', '-time', '-ele',3200, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node81.out', '-time', '-node',81,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node1701.out', '-time', '-node',1701,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node3321.out', '-time', '-node',3321,'-dof',1,2,3,'vel')

# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele3141.out', '-time', '-ele',3141, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node3261.out', '-time', '-node',3261,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele3181.out', '-time', '-ele',3181, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node3301.out', '-time', '-node',3301,'-dof',1,2,3,'vel')


system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(3200,1.25e-4)
print("finish analyze:0 ~ 0.8s")

# # printModel('-ele', 701,702,703,704,705,707)
# --------- end to calculate time -------------
end = time.time()
print(end - start)
