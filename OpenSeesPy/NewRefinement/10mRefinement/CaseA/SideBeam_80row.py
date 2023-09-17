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
ny = 80
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

# ============== Build Beam element (6562~6642) (ele 6401~6480) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(6562+j,0.125*j,0.0)
    mass(6562+j,1,1,1)
# -------- fix rotate dof ------------
    fix(6562+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 6401+k, 6562+k, 6563+k, A,E1,Iz, 1, '-release', 3)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,6562+k,1,2)

# ============================ Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 6643,6644~ 6803,6804)-> for S wave------------
    node(6643+2*l, 0.125*l, 0.0)
    node(6644+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(6643+2*l, 0, 1, 1)      # x dir dashpot　
    fix(6644+2*l, 1, 1, 1)      # fixed end to let soil fix
 
# ------------- Normal dashpot (node 6805,6806~ 6965,6966)-> for P wave ------------
    node(6805+2*l, 0.125*l, 0.0)
    node(6806+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(6805+2*l, 1, 0, 1)      # y dir dashpot　
    fix(6806+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k,6643+2*k,1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+k,6805+2*k,2)

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
element('zeroLength',6481, 6644,6643, '-mat',4001,'-dir',xdir)  # node 1: Left side
element('zeroLength',6561, 6804,6803, '-mat',4001,'-dir',xdir)  # node 101: Left side

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',6562, 6806,6805, '-mat',4000,'-dir',ydir)  # node 1: Left side
element('zeroLength',6642, 6966,6965, '-mat',4000,'-dir',ydir)  # node 101: Left side

for q in range(1,nx): #1,nx / nx+1
# -------- Traction dashpot element: Vs with x dir (ele 6481~6561) ------------------
    element('zeroLength',6481+q, 6644+2*q,6643+2*q, '-mat',4003,'-dir',xdir)
 
# -------- Normal dashpot element: Vp with y dir (ele 6562~6642) ------------------
    element('zeroLength',6562+q, 6806+2*q,6805+2*q, '-mat',4002,'-dir',ydir)

print("Finished creating dashpot material and element...")
# ============ Soil Left and Right "Side" Dashpot =====================================
soilLength = 10 # m
yMesh = soilLength/ny # Y row MeshSize
for l in range(ny+1):
# ========= Left Side =============
# --------- Normal dashpot (node 6967,6968~ 7127,7128)-> for S wave------------
    node(6967+2*l, 0.0, yMesh*l)
    node(6968+2*l, 0.0, yMesh*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(6967+2*l, 0, 1, 1)      # x dir dashpot　
    fix(6968+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 7129,7130~ 7289,7290)-> for P wave------------
    node(7129+2*l, 0.0, yMesh*l)
    node(7130+2*l, 0.0, yMesh*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(7129+2*l, 1, 0, 1)      # y dir dashpot　
    fix(7130+2*l, 1, 1, 1)      # fixed end to let soil fix

# ========= Right Side =============
# --------- Normal dashpot (node 7291,7292~ 7451,7452)-> for S wave------------
    node(7291+2*l, 10.0, yMesh*l)
    node(7292+2*l, 10.0, yMesh*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(7291+2*l, 0, 1, 1)      # x dir dashpot　
    fix(7292+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 7453,7454~ 7613,7614)-> for P wave------------
    node(7453+2*l, 10.0, yMesh*l)
    node(7454+2*l, 10.0, yMesh*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(7453+2*l, 1, 0, 1)      # y dir dashpot　
    fix(7454+2*l, 1, 1, 1)      # fixed end to let soil fix
 
# ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------
for l in range(ny+1):
# ========= Left Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(1+81*l, 6967+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(1+81*l, 7129+2*l, 2)  # y dir

# ========= Right Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(81+81*l, 7291+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(81+81*l, 7453+2*l, 2)  # y dir

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
element('zeroLength',6643, 6968, 6967, '-mat',4004,'-dir',xdir)  # node 1:  -> Smp
element('zeroLength',6723, 7128, 7127, '-mat',4004,'-dir',xdir)  # node 801:  -> Smp
#  ----------- Left side Traction: P wave ----------
element('zeroLength',6724, 7130, 7129, '-mat',4005,'-dir',ydir)  # node 1 -> Sms
element('zeroLength',6804, 7290, 7289, '-mat',4005,'-dir',ydir)  # node 801 -> Sms

#  ----------- Right side Normal: S wave ----------
element('zeroLength',6805, 7292, 7291, '-mat',4004,'-dir',xdir)  # node 8 -> Smp
element('zeroLength',6885, 7452, 7451, '-mat',4004,'-dir',xdir)  # node 808 -> Smp
#  ----------- Right side Traction: P wave ----------
element('zeroLength',6886, 7454, 7453, '-mat',4005,'-dir',ydir)  # node 8 -> Sms
element('zeroLength',6966, 7614 ,7613, '-mat',4005,'-dir',ydir)  # node 808 -> Sms

for w in range(1,ny): #1,ny
#----------- Left side Normal Dashpot: (ele 6643~6723)---------- -> Smp
    element('zeroLength',6643+w, 6968+2*w, 6967+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Left side Traction Dashpot: (ele 6724~6804) ---------- -> Sms
    element('zeroLength',6724+w, 7130+2*w, 7129+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

#----------- Right side Normal Dashpot:(ele 6805 ~ 6885) ---------- -> Smp
    element('zeroLength',6805+w, 7292+2*w, 7291+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Right side Traction Dashpot: (ele 6886 ~ 6966) ----------  -> Sms
    element('zeroLength',6886+w, 7454+2*w, 7453+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

print("Finished creating Side dashpot material and element...")

# ==================== Side Beam node (7615~7695 / 7696~7776) ====================
for i in range(ny+1):
# ----- Left Side: 7615~7695 -----------------
    node(7615+i, 0.0, yMesh*i)
    fix(7615+i,0,0,1)
# ----- Right Side: 7696~7776 -----------------
    node(7696+i, 10.0,yMesh*i)
    fix(7696+i,0,0,1)

# ------------  Beam Element: 6967 ~ 7046 / 7047 ~ 7126 ------------------
for j in range(ny):
# ----- Left Side Beam:6967 ~ 7046 -----------------
    element('elasticBeamColumn', 6967+j, 7615+j, 7616+j, A,E1,Iz, 1, '-release', 3)
# ----- Right Side Beam:7047 ~ 7126 -----------------
    element('elasticBeamColumn', 7047+j, 7696+j, 7697+j, A,E1,Iz, 1, '-release', 3)

# --------- Side Beam and Soil BC -----------------
for j in range(ny+1):
    equalDOF(1+81*j,7615+j,1,2)
    equalDOF(81+81*j,7696+j,1,2)

# ============================== S wave ======================================
# ------------ Side Load Pattern ------------------------------
for g in range(ny):
# ------- timeSeries ID: 800~879 / Pattern ID: 804~883----------------------
    timeSeries('Path',800+g, '-filePath',f'SSideforce_80rowx/ele{1+g}.txt','-dt',6.25e-5)
    pattern('Plain',804+g, 800+g)
# ---------- x direction : Sideforce ---------------------
# ---------- Distributed at Left Side Beam ----------------------
    eleLoad('-ele',6967+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# ---------- Distributed at Right Side Beam ----------------------
    eleLoad('-ele',7047+g, '-type', '-beamUniform',-20,0)   # for local axes Wy +
 
for g in range(ny):
# ------- timeSeries ID: 880~959 / Pattern ID:884~963 ----------------------
# ---------- y direction : Sideforce --------------------
    timeSeries('Path',880+g, '-filePath',f'SSideforce_80rowy/ele{1+g}.txt','-dt',6.25e-5)
    pattern('Plain',884+g, 880+g)
# ---------- For P wave : y direction ---------------------
# ---------- Distributed at Left Side Beam ----------------------
    eleLoad('-ele',6967+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# ---------- Distributed at Right Side Beam ----------------------
    eleLoad('-ele',7047+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wx -

print("finish SideBeam Force InputFile Apply")

#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
timeSeries('Path',702, '-filePath','fs200_80row.txt','-dt',6.25e-05)
# timeSeries('Path',704, '-filePath','TopForce80row.txt','-dt',3.34e-05)

# # # timeSeries('Linear',705)

pattern('Plain',703, 702)
# load(6521,0,-1)

# ------------- P wave -----------------------------
# for m in range(nx):
#     eleLoad('-ele', 1601+m, '-type','-beamUniform',20,0)

# ------------- S wave -----------------------------
for m in range(nx):
    eleLoad('-ele', 6401+m, '-type','-beamUniform',0,20,0)

print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# -------------- Recorder --------------------------------
# recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# ------------- left column -------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele3201.out', '-time', '-ele',3201, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele6321.out', '-time', '-ele',6321, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node3241.out', '-time', '-node',3241,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node6481.out', '-time', '-node',6481,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', 'Stress/ele41.out', '-time', '-ele',41, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele3241.out', '-time', '-ele',3241, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele6361.out', '-time', '-ele',6361, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node41.out', '-time', '-node',41,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node3281.out', '-time', '-node',3281,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node6521.out', '-time', '-node',6521,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', 'Stress/ele80.out', '-time', '-ele',80, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele3280.out', '-time', '-ele',3280, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele6400.out', '-time', '-ele',6400, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node81.out', '-time', '-node',81,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node3321.out', '-time', '-node',3321,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node6561.out', '-time', '-node',6561,'-dof',1,2,3,'vel')

# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele6341.out', '-time', '-ele',6341, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node6501.out', '-time', '-node',6501,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele6381.out', '-time', '-ele',6381, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node6541.out', '-time', '-node',6541,'-dof',1,2,3,'vel')


system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(6400,6.25e-05)
print("finish analyze:0 ~ 0.8s")

# # printModel('-ele', 701,702,703,704,705,707)
# --------- end to calculate time -------------
end = time.time()
print(end - start)
