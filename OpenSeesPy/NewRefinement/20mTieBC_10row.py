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
ny = 10
e1 = 1
n1 = 1
eleArgs = [1, 'PlaneStrain', 2000]
points = [1, 0.0,   0.0, 
          2, 20,  0.0, 
          3, 20,  10.0, 
          4, 0.0,   10.0]
block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)
# printModel('-ele',1481,1561)
# -------- Soil B.C ---------------
for i in range(ny+1):
    equalDOF(161*i+1,161*i+161,1,2)

# ============== Build Beam element (1772~1932) (ele 1601~1760) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(1772+j,0.125*j,0.0)
    mass(1772+j,1,1,1)
# -------- fix rotate dof ------------
    fix(1772+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 1601+k, 1772+k, 1773+k, A,E1,Iz, 1, '-release', 3)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,1772+k,1,2)

# ============================ Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 1933,1934~ 2253,2254)-> for S wave------------
    node(1933+2*l, 0.125*l, 0.0)
    node(1934+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(1933+2*l, 0, 1, 1)      # x dir dashpot　
    fix(1934+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 2255,2256~ 2575,2576)-> for P wave ------------
    node(2255+2*l, 0.125*l, 0.0)
    node(2256+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(2255+2*l, 1, 0, 1)      # y dir dashpot　
    fix(2256+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k,1933+2*k,1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+k,2255+2*k,2)

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
# # ------ Traction dashpot element: Vs with x dir
# element('zeroLength',1761, 1934,1933, '-mat',4001,'-dir',xdir)  # node 1: Left side
# element('zeroLength',1921, 2254,2253, '-mat',4001,'-dir',xdir)  # node 101: Left side

# # ------ Normal dashpot element: Vp with y dir
# element('zeroLength',1922, 2256,2255, '-mat',4000,'-dir',ydir)  # node 1: Left side
# element('zeroLength',2082, 2576,2575, '-mat',4000,'-dir',ydir)  # node 101: Left side

for q in range(nx+1): #1,nx / nx+1
# -------- Traction dashpot element: Vs with x dir (ele 1761~1921) ------------------
    element('zeroLength',1761+q, 1934+2*q,1933+2*q, '-mat',4003,'-dir',xdir)
# -------- Normal dashpot element: Vp with y dir (ele 1922~2082) ------------------
    element('zeroLength',1922+q, 2256+2*q,2255+2*q, '-mat',4002,'-dir',ydir)

print("Finished creating dashpot material and element...")
# # # # # # ============================== P wave =================================
# # # # # # ------------ Side Load Pattern ------------------------------
# # # # # for g in range(100):
# # # # # # ------- timeSeries ID: 800~899 (global x force) ----------------------
# # # # #     timeSeries('Path',800+g, '-filePath',f'P_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
# # # # #     pattern('Plain',804+g, 800+g)
# # # # # # ---------- x direction : Sideforce ---------------------
# # # # # # ---------- Distributed at Left Side Beam ----------------------
# # # # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# # # # # # ---------- Distributed at Right Side Beam ----------------------
# # # # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',+20,0)   # for local axes Wy +

# # # # # for g in range(100):
# # # # # # ------- timeSeries ID: 900~999 (global y force)----------------------
# # # # # # ---------- y direction : Sideforce --------------------
# # # # #     timeSeries('Path',900+g, '-filePath',f'P_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
# # # # #     pattern('Plain',904+g, 900+g)
# # # # # # ---------- For P wave : y direction ---------------------
# # # # # # ---------- Distributed at Left Side Beam ----------------------
# # # # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # # # # # ---------- Distributed at Right Side Beam ----------------------
# # # # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',0,+20,0)   # for local axes Wx +
    
# # # # # ============================== S wave ======================================
# # # # # ------------ Side Load Pattern ------------------------------
# # # # for g in range(100):
# # # # # ------- timeSeries ID: 800~899 ----------------------
# # # #     timeSeries('Path',800+g, '-filePath',f'S_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
# # # #     pattern('Plain',804+g, 800+g)
# # # # # ---------- x direction : Sideforce ---------------------
# # # # # ---------- Distributed at Left Side Beam ----------------------
# # # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# # # # # ---------- Distributed at Right Side Beam ----------------------
# # # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',-20,0)   # for local axes Wy +

# # # # for g in range(100):
# # # # # ------- timeSeries ID: 900~999 ----------------------
# # # # # ---------- y direction : Sideforce --------------------
# # # #     timeSeries('Path',900+g, '-filePath',f'S_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
# # # #     pattern('Plain',904+g, 900+g)
# # # # # ---------- For P wave : y direction ---------------------
# # # # # ---------- Distributed at Left Side Beam ----------------------
# # # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # # # # ---------- Distributed at Right Side Beam ----------------------
# # # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wx -
# # # # print("finish SideBeam Force InputFile Apply")

#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
timeSeries('Path',702, '-filePath','fs200_10row.txt','-dt',5e-4)
# timeSeries('Path',704, '-filePath','topForce.txt','-dt',1e-4)

# # # # timeSeries('Linear',705)

pattern('Plain',703, 702)
# # load(803,0,-1)
# # load(805,0,-2)
# # ------------- P wave -----------------------------
# # for m in range(nx):
# #     eleLoad('-ele', 801+m, '-type','-beamUniform',20,0)

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
recorder('Element', '-file', 'Stress/ele1441.out', '-time', '-ele',1441, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node806.out', '-time', '-node',806,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node1611.out', '-time', '-node',1611,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', 'Stress/ele81.out', '-time', '-ele',81, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele881.out', '-time', '-ele',881, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele1521.out', '-time', '-ele',1521, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node81.out', '-time', '-node',81,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node886.out', '-time', '-node',886,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node1691.out', '-time', '-node',1691,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', 'Stress/ele160.out', '-time', '-ele',160, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele960.out', '-time', '-ele',960, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele1600.out', '-time', '-ele',1600, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node161.out', '-time', '-node',161,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node966.out', '-time', '-node',966,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node1771.out', '-time', '-node',1771,'-dof',1,2,3,'vel')

# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele1481.out', '-time', '-ele',1481, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node1651.out', '-time', '-node',1651,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele1561.out', '-time', '-ele',1561, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node1731.out', '-time', '-node',1731,'-dof',1,2,3,'vel')


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
