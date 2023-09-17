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
ny = 20
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

# ============== Build Beam element (1702~972) (ele 1601~1680) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(1702+j,0.125*j,0.0)
    mass(1702+j,1,1,1)
# -------- fix rotate dof ------------
    fix(1702+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 1601+k, 1702+k, 1703+k, A,E1,Iz, 1, '-release', 3)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,1702+k,1,2)

# ============================ Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 1783,1784~ 1943,1944)-> for S wave------------
    node(1783+2*l, 0.125*l, 0.0)
    node(1784+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(1783+2*l, 0, 1, 1)      # x dir dashpot　
    fix(1784+2*l, 1, 1, 1)      # fixed end to let soil fix
   
# ------------- Normal dashpot (node 1945,1946~ 2105,2106)-> for P wave ------------
    node(1945+2*l, 0.125*l, 0.0)
    node(1946+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(1945+2*l, 1, 0, 1)      # y dir dashpot　
    fix(1946+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k,1783+2*k,1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+k,1945+2*k,2)

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
element('zeroLength',1681, 1784,1783, '-mat',4001,'-dir',xdir)  # node 1: Left side
element('zeroLength',1761, 1944,1943, '-mat',4001,'-dir',xdir)  # node 101: Left side

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',1762, 1946,1945, '-mat',4000,'-dir',ydir)  # node 1: Left side
element('zeroLength',1842, 2106,2105, '-mat',4000,'-dir',ydir)  # node 101: Left side

for q in range(1,nx): #1,nx / nx+1
# -------- Traction dashpot element: Vs with x dir (ele 1681~1761) ------------------
    element('zeroLength',1681+q, 1784+2*q,1783+2*q, '-mat',4003,'-dir',xdir)

# -------- Normal dashpot element: Vp with y dir (ele 1762~1842) ------------------
    element('zeroLength',1762+q, 1946+2*q,1945+2*q, '-mat',4002,'-dir',ydir)

print("Finished creating dashpot material and element...")
# ============ Soil Left and Right "Side" Dashpot =====================================
soilLength = 10 # m
yMesh = soilLength/ny # Y row MeshSize
for l in range(ny+1):
# ========= Left Side =============
# --------- Normal dashpot (node 2107,2108~ 2147,2148)-> for S wave------------
    node(2107+2*l, 0.0, yMesh*l)
    node(2108+2*l, 0.0, yMesh*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(2107+2*l, 0, 1, 1)      # x dir dashpot　
    fix(2108+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 2149,2150~ 2189,2190)-> for P wave------------
    node(2149+2*l, 0.0, yMesh*l)
    node(2150+2*l, 0.0, yMesh*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(2149+2*l, 1, 0, 1)      # y dir dashpot　
    fix(2150+2*l, 1, 1, 1)      # fixed end to let soil fix

# ========= Right Side =============
# --------- Normal dashpot (node 2191,2192~ 2231,2232)-> for S wave------------
    node(2191+2*l, 10.0, yMesh*l)
    node(2192+2*l, 10.0, yMesh*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(2191+2*l, 0, 1, 1)      # x dir dashpot　
    fix(2192+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 2233,2234~ 2273,2274)-> for P wave------------
    node(2233+2*l, 10.0, yMesh*l)
    node(2234+2*l, 10.0, yMesh*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(2233+2*l, 1, 0, 1)      # y dir dashpot　
    fix(2234+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------
for l in range(ny+1):
# ========= Left Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(1+81*l, 2107+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(1+81*l, 2149+2*l, 2)  # y dir

# ========= Right Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(81+81*l, 2191+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(81+81*l, 2233+2*l, 2)  # y dir

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
element('zeroLength',1843, 2108, 2107, '-mat',4004,'-dir',xdir)  # node 1:  -> Smp
element('zeroLength',1863, 2148, 2147, '-mat',4004,'-dir',xdir)  # node 801:  -> Smp
#  ----------- Left side Traction: P wave ----------
element('zeroLength',1864, 2150, 2149, '-mat',4005,'-dir',ydir)  # node 1 -> Sms
element('zeroLength',1884, 2190, 2189, '-mat',4005,'-dir',ydir)  # node 801 -> Sms

#  ----------- Right side Normal: S wave ----------
element('zeroLength',1885, 2192, 2191, '-mat',4004,'-dir',xdir)  # node 8 -> Smp
element('zeroLength',1905, 2232, 2231, '-mat',4004,'-dir',xdir)  # node 808 -> Smp
#  ----------- Right side Traction: P wave ----------
element('zeroLength',1906, 2234, 2233, '-mat',4005,'-dir',ydir)  # node 8 -> Sms
element('zeroLength',1926, 2274 ,2273, '-mat',4005,'-dir',ydir)  # node 808 -> Sms

for w in range(1,ny): #1,ny
#----------- Left side Normal Dashpot: (ele 1843~1863)---------- -> Smp
    element('zeroLength',1843+w, 2108+2*w, 2107+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Left side Traction Dashpot: (ele 1864~1884) ---------- -> Sms
    element('zeroLength',1864+w, 2150+2*w, 2149+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

#----------- Right side Normal Dashpot:(ele 1885 ~ 1905) ---------- -> Smp
    element('zeroLength',1885+w, 2192+2*w, 2191+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Right side Traction Dashpot: (ele 1906 ~ 1926) ----------  -> Sms
    element('zeroLength',1906+w, 2234+2*w, 2233+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

print("Finished creating Side dashpot material and element...")

# ==================== Side Beam node (2275~2295 / 2296~2316) ====================
for i in range(ny+1):
# ----- Left Side: 2275~2295 -----------------
    node(2275+i, 0.0, yMesh*i)
    fix(2275+i,0,0,1)
# ----- Right Side: 2296~2316 -----------------
    node(2296+i,10.0,yMesh*i)
    fix(2296+i,0,0,1)

# ------------  Beam Element: 1927 ~ 1946 / 1947 ~ 1966 ------------------
for j in range(ny):
# ----- Left Side Beam:1927 ~ 1946 -----------------
    element('elasticBeamColumn', 1927+j, 2275+j, 2276+j, A,E1,Iz, 1, '-release', 3)
# ----- Right Side Beam:1947 ~ 1966 -----------------
    element('elasticBeamColumn', 1947+j, 2296+j, 2297+j, A,E1,Iz, 1, '-release', 3)

# --------- Side Beam and Soil BC -----------------
for j in range(ny+1):
    equalDOF(1+81*j,2275+j,1,2)
    equalDOF(81+81*j,2296+j,1,2)

# ============================== S wave ======================================
# ------------ Side Load Pattern ------------------------------
for g in range(ny):
# ------- timeSeries ID: 800~819 / Pattern ID: 804~823----------------------
    timeSeries('Path',800+g, '-filePath',f'SSideforce_20rowx/ele{1+g}.txt','-dt',2.5e-4)
    pattern('Plain',804+g, 800+g)
# ---------- x direction : Sideforce ---------------------
# ---------- Distributed at Left Side Beam ----------------------
    eleLoad('-ele',1927+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# ---------- Distributed at Right Side Beam ----------------------
    eleLoad('-ele',1947+g, '-type', '-beamUniform',-20,0)   # for local axes Wy +

for g in range(ny):
# ------- timeSeries ID: 820~839 / Pattern ID:824~843 ----------------------
# ---------- y direction : Sideforce --------------------
    timeSeries('Path',820+g, '-filePath',f'SSideforce_20rowy/ele{1+g}.txt','-dt',2.5e-4)
    pattern('Plain',824+g, 820+g)
# ---------- For P wave : y direction ---------------------
# ---------- Distributed at Left Side Beam ----------------------
    eleLoad('-ele',1927+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# ---------- Distributed at Right Side Beam ----------------------
    eleLoad('-ele',1947+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wx -

print("finish SideBeam Force InputFile Apply")

#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
timeSeries('Path',702, '-filePath','fs200_20row.txt','-dt',2.5e-4)
# timeSeries('Path',704, '-filePath','TopForce20row.txt','-dt',1.33e-4)

# # # timeSeries('Linear',705)

pattern('Plain',703, 702)
# load(1661,0,-1)

# ------------- P wave -----------------------------
# for m in range(nx):
#     eleLoad('-ele', 1601+m, '-type','-beamUniform',20,0)

# ------------- S wave -----------------------------
for m in range(nx):
    eleLoad('-ele', 1601+m, '-type','-beamUniform',0,20,0)

print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# -------------- Recorder --------------------------------
# recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# ------------- left column -------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele801.out', '-time', '-ele',801, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele1521.out', '-time', '-ele',1521, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node811.out', '-time', '-node',811,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node1621.out', '-time', '-node',1621,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', 'Stress/ele41.out', '-time', '-ele',41, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele841.out', '-time', '-ele',841, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele1561.out', '-time', '-ele',1561, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node41.out', '-time', '-node',41,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node851.out', '-time', '-node',851,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node1661.out', '-time', '-node',1661,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', 'Stress/ele80.out', '-time', '-ele',80, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele880.out', '-time', '-ele',880, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele1600.out', '-time', '-ele',1600, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node81.out', '-time', '-node',81,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node891.out', '-time', '-node',891,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node1701.out', '-time', '-node',1701,'-dof',1,2,3,'vel')

# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele1541.out', '-time', '-ele',1541, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node1641.out', '-time', '-node',1641,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele1581.out', '-time', '-ele',1581, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node1681.out', '-time', '-node',1681,'-dof',1,2,3,'vel')


system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(1600,2.5e-4)
print("finish analyze:0 ~ 0.8s")

# # printModel('-ele', 701,702,703,704,705,707)
# --------- end to calculate time -------------
end = time.time()
print(end - start)
