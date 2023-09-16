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
ny = 10
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

# ============== Build Beam element (100~108) (ele 81~88) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(100+j,0.125*j,0.0)
    mass(100+j,1,1,1)
# -------- fix rotate dof ------------
    fix(100+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 81+k, 100+k, 101+k, A,E1,Iz, 1, '-release', 3)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,100+k,1,2)

# ============================ Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 109,110~ 125,126)-> for S wave------------
    node(109+2*l, 0.125*l, 0.0)
    node(110+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(109+2*l, 0, 1, 1)      # x dir dashpot　
    fix(110+2*l, 1, 1, 1)      # fixed end to let soil fix
 
# ------------- Normal dashpot (node 113,114~ 127,128)-> for P wave ------------
    node(127+2*l, 0.125*l, 0.0)
    node(128+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(127+2*l, 1, 0, 1)      # y dir dashpot　
    fix(128+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k,109+2*k,1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+k,127+2*k,2)

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
element('zeroLength',89,110,109, '-mat',4001,'-dir',xdir)  # node 1: Left side

element('zeroLength',90,112,111, '-mat',4003,'-dir',xdir)
element('zeroLength',91,114,113, '-mat',4003,'-dir',xdir)
element('zeroLength',92,116,115, '-mat',4003,'-dir',xdir)
element('zeroLength',93,118,117, '-mat',4003,'-dir',xdir)
element('zeroLength',94,120,119, '-mat',4003,'-dir',xdir)
element('zeroLength',95,122,121, '-mat',4003,'-dir',xdir)
element('zeroLength',96,124,123, '-mat',4003,'-dir',xdir)

element('zeroLength',97,126,125, '-mat',4001,'-dir',xdir)  # node 8: Right side

# # ------ Normal dashpot element: Vp with y dir
element('zeroLength',98, 128, 127, '-mat',4000,'-dir',ydir)  # node 1: Left side

element('zeroLength',99, 130, 129, '-mat',4002,'-dir',ydir)
element('zeroLength',100,132,131, '-mat',4002,'-dir',ydir)
element('zeroLength',101,134,133, '-mat',4002,'-dir',ydir)
element('zeroLength',102,136,135, '-mat',4002,'-dir',ydir)
element('zeroLength',103,138,137, '-mat',4002,'-dir',ydir)
element('zeroLength',104,140,139, '-mat',4002,'-dir',ydir)
element('zeroLength',105,142,141, '-mat',4002,'-dir',ydir)

element('zeroLength',106,144,143, '-mat',4000,'-dir',ydir)  # node 8: Left side

print("Finished creating Bottom dashpot material and element...")

# # # # ============================== P wave =================================
# # # # ------------ Side Load Pattern ------------------------------
# # # for g in range(100):
# # # # ------- timeSeries ID: 800~899 (global x force) ----------------------
# # #     timeSeries('Path',800+g, '-filePath',f'P_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
# # #     pattern('Plain',804+g, 800+g)
# # # # ---------- x direction : Sideforce ---------------------
# # # # ---------- Distributed at Left Side Beam ----------------------
# # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# # # # ---------- Distributed at Right Side Beam ----------------------
# # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',+20,0)   # for local axes Wy +

# # # for g in range(100):
# # # # ------- timeSeries ID: 900~999 (global y force)----------------------
# # # # ---------- y direction : Sideforce --------------------
# # #     timeSeries('Path',900+g, '-filePath',f'P_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
# # #     pattern('Plain',904+g, 900+g)
# # # # ---------- For P wave : y direction ---------------------
# # # # ---------- Distributed at Left Side Beam ----------------------
# # #     eleLoad('-ele',2228+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # # # ---------- Distributed at Right Side Beam ----------------------
# # #     eleLoad('-ele',2428+g, '-type', '-beamUniform',0,+20,0)   # for local axes Wx +
    
# # # ============================== S wave ======================================
# # # ------------ Side Load Pattern ------------------------------
# # for g in range(100):
# # # ------- timeSeries ID: 800~899 ----------------------
# #     timeSeries('Path',800+g, '-filePath',f'S_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
# #     pattern('Plain',804+g, 800+g)
# # # ---------- x direction : Sideforce ---------------------
# # # ---------- Distributed at Left Side Beam ----------------------
# #     eleLoad('-ele',2228+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# # # ---------- Distributed at Right Side Beam ----------------------
# #     eleLoad('-ele',2428+g, '-type', '-beamUniform',-20,0)   # for local axes Wy +

# # for g in range(100):
# # # ------- timeSeries ID: 900~999 ----------------------
# # # ---------- y direction : Sideforce --------------------
# #     timeSeries('Path',900+g, '-filePath',f'S_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
# #     pattern('Plain',904+g, 900+g)
# # # ---------- For P wave : y direction ---------------------
# # # ---------- Distributed at Left Side Beam ----------------------
# #     eleLoad('-ele',2228+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # # ---------- Distributed at Right Side Beam ----------------------
# #     eleLoad('-ele',2428+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wx -
# # print("finish SideBeam Force InputFile Apply")

#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
# timeSeries('Path',702, '-filePath','fs200_10row.txt','-dt',5e-4)
timeSeries('Path',704, '-filePath','TopForce10row.txt','-dt',2.67e-4)

# # # timeSeries('Linear',705)

pattern('Plain',703, 704)
load(95,0,-1)
# # # ------------- P wave -----------------------------
# # eleLoad('-ele', 71, '-type','-beamUniform',20,0)
# # eleLoad('-ele', 72, '-type','-beamUniform',20,0)
# # eleLoad('-ele', 73, '-type','-beamUniform',20,0)
# # eleLoad('-ele', 74, '-type','-beamUniform',20,0)
# # eleLoad('-ele', 75, '-type','-beamUniform',20,0)
# # eleLoad('-ele', 76, '-type','-beamUniform',20,0)
# # eleLoad('-ele', 77, '-type','-beamUniform',20,0)

# # ------------- S wave -----------------------------
# eleLoad('-ele', 81, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 82, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 83, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 84, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 85, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 86, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 87, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 88, '-type','-beamUniform',0,20,0)

print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# -------------- Recorder --------------------------------
# recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# ------------- left column -------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele41.out', '-time', '-ele',41, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele73.out', '-time', '-ele',73, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node46.out', '-time', '-node',46,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node91.out', '-time', '-node',91,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', 'Stress/ele5.out', '-time', '-ele',5, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele45.out', '-time', '-ele',45, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele77.out', '-time', '-ele',77, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node5.out', '-time', '-node',5,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node50.out', '-time', '-node',50,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node95.out', '-time', '-node',95,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', 'Stress/ele8.out', '-time', '-ele',8, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele48.out', '-time', '-ele',48, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele80.out', '-time', '-ele',80, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node9.out', '-time', '-node',9,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node54.out', '-time', '-node',54,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node99.out', '-time', '-node',99,'-dof',1,2,3,'vel')

# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele75.out', '-time', '-ele',75, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node93.out', '-time', '-node',93,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele79.out', '-time', '-ele',79, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node97.out', '-time', '-node',97,'-dof',1,2,3,'vel')


system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(800,2.67e-4)
print("finish analyze:0 ~ 0.8s")

# # printModel('-ele', 701,702,703,704,705,707)
# --------- end to calculate time -------------
end = time.time()
print(end - start)
