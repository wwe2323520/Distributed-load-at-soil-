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
ny = 40
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

# ============== Build Beam element (370~378) (ele 321~328) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(370+j,0.125*j,0.0)
    mass(370+j,1,1,1)
# -------- fix rotate dof ------------
    fix(370+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 321+k, 370+k, 371+k, A,E1,Iz, 1, '-release', 3)
# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,370+k,1,2)

# ============================ Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 379,380~ 395,396)-> for S wave------------
    node(379+2*l, 0.125*l, 0.0)
    node(380+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(379+2*l, 0, 1, 1)      # x dir dashpot　
    fix(380+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 397,398~ 413,414)-> for P wave ------------
    node(397+2*l, 0.125*l, 0.0)
    node(398+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(397+2*l, 1, 0, 1)      # y dir dashpot　
    fix(398+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k,379+2*k,1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+k,397+2*k,2)

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
element('zeroLength',329,380,379, '-mat',4001,'-dir',xdir)  # node 1: Left side

element('zeroLength',330,382,381, '-mat',4003,'-dir',xdir)
element('zeroLength',331,384,383, '-mat',4003,'-dir',xdir)
element('zeroLength',332,386,385, '-mat',4003,'-dir',xdir)
element('zeroLength',333,388,387, '-mat',4003,'-dir',xdir)
element('zeroLength',334,390,389, '-mat',4003,'-dir',xdir)
element('zeroLength',335,392,391, '-mat',4003,'-dir',xdir)
element('zeroLength',336,394,393, '-mat',4003,'-dir',xdir)

element('zeroLength',337,396,395, '-mat',4001,'-dir',xdir)  # node 8: Right side

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',338, 398, 397, '-mat',4000,'-dir',ydir)  # node 1: Left side

element('zeroLength',339, 400, 399, '-mat',4002,'-dir',ydir)
element('zeroLength',340,402,401, '-mat',4002,'-dir',ydir)
element('zeroLength',341,404,403, '-mat',4002,'-dir',ydir)
element('zeroLength',342,406,405, '-mat',4002,'-dir',ydir)
element('zeroLength',343,408,407, '-mat',4002,'-dir',ydir)
element('zeroLength',344,410,409, '-mat',4002,'-dir',ydir)
element('zeroLength',345,412,411, '-mat',4002,'-dir',ydir)

element('zeroLength',346,414,413, '-mat',4000,'-dir',ydir)  # node 8: Left side

print("Finished creating Bottom dashpot material and element...")

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
# timeSeries('Path',702, '-filePath','fs200_40row.txt','-dt',1.25e-4)
timeSeries('Path',704, '-filePath','TopForce40row.txt','-dt',6.68e-05)

# # # # # timeSeries('Linear',705)

pattern('Plain',703, 704)
load(365,0,-1)

# # # # ------------- P wave -----------------------------
# # # eleLoad('-ele', 71, '-type','-beamUniform',20,0)
# # # eleLoad('-ele', 72, '-type','-beamUniform',20,0)
# # # eleLoad('-ele', 73, '-type','-beamUniform',20,0)
# # # eleLoad('-ele', 74, '-type','-beamUniform',20,0)
# # # eleLoad('-ele', 75, '-type','-beamUniform',20,0)
# # # eleLoad('-ele', 76, '-type','-beamUniform',20,0)
# # # eleLoad('-ele', 77, '-type','-beamUniform',20,0)

# # ------------- S wave -----------------------------
# eleLoad('-ele', 321, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 322, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 323, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 324, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 325, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 326, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 327, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 328, '-type','-beamUniform',0,20,0)

print("finish Input Force File:0 ~ 0.1s(+1), Input Stress B.C:0.2~0.3s(-1)")

# -------------- Recorder --------------------------------
# recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# ------------- left column -------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele161.out', '-time', '-ele',161, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele313.out', '-time', '-ele',313, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node181.out', '-time', '-node',181,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node361.out', '-time', '-node',361,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', 'Stress/ele5.out', '-time', '-ele',5, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele165.out', '-time', '-ele',165, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele317.out', '-time', '-ele',317, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node5.out', '-time', '-node',5,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node185.out', '-time', '-node',185,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node365.out', '-time', '-node',365,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', 'Stress/ele8.out', '-time', '-ele',8, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele168.out', '-time', '-ele',168, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele320.out', '-time', '-ele',320, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node9.out', '-time', '-node',9,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node189.out', '-time', '-node',189,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node369.out', '-time', '-node',369,'-dof',1,2,3,'vel')

# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele315.out', '-time', '-ele',315, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node363.out', '-time', '-node',363,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele319.out', '-time', '-ele',319, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node367.out', '-time', '-node',367,'-dof',1,2,3,'vel')


system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(3200,6.68e-05)
print("finish analyze:0 ~ 0.8s")

# # # # printModel('-ele', 701,702,703,704,705,707)
# --------- end to calculate time -------------
end = time.time()
print(end - start)
