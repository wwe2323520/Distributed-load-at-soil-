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

# -------- Soil B.C ---------------
for i in range(ny+1):
    equalDOF(81*i+1,81*i+81,1,2)

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
timeSeries('Path',702, '-filePath','fs200_40row.txt','-dt',1.25e-4)
# timeSeries('Path',704, '-filePath','topForce.txt','-dt',1e-4)

# # # timeSeries('Linear',705)

pattern('Plain',703, 702)
# load(803,0,-1)
# load(805,0,-2)
# ------------- P wave -----------------------------
# for m in range(nx):
#     eleLoad('-ele', 1601+m, '-type','-beamUniform',20,0)

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
