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

E = 15005714.286
nu = 0.3
rho = 2020
nDMaterial('ElasticIsotropic', 2000, E, nu, rho)

nx = 7
ny = 20
e1 = 1
n1 = 1
eleArgs = [1, 'PlaneStrain', 2000]
points = [1, 0.0, 0.0, 
          2, 0.7, 0.0, 
          3, 0.7, 10.0, 
          4, 0.0, 10.0]
block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)

# -------- Soil B.C ---------------
for i in range(ny+1):
    equalDOF(8*i+1,8*i+8,1,2)

# ============== Build Beam element (169~176) (ele 141~147) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(169+j,0.1*j,0.0)
    mass(169+j,1,1,1)
# -------- fix rotate dof ------------
    fix(169+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 141+k, 169+k, 170+k, A,E1,Iz, 1, '-release', 3)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,169+k,1,2)

# ============================ Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 177,178~ 191,192)-> for S wave------------
    node(177+2*l, 0.1*l, 0.0)
    node(178+2*l, 0.1*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(177+2*l, 0, 1, 1)      # x dir dashpot　
    fix(178+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 193,194~ 207,208)-> for P wave ------------
    node(193+2*l, 0.1*l, 0.0)
    node(194+2*l, 0.1*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(193+2*l, 1, 0, 1)      # y dir dashpot　
    fix(194+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k,177+2*k,1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+k,193+2*k,2)

print("Finished creating all Bottom dashpot boundary conditions and equalDOF...")
# ------------------- ZeroLength to Build dashpot: Material ----------------------------------
rho = 2020   # kg/m3 
Vp = 100     # m/s 
Vs = 53.45224838248488     ;# m/s 
sizeX = 0.1  # m
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
element('zeroLength',148,178,177, '-mat',4001,'-dir',xdir)  # node 1: Left side

element('zeroLength',149,180,179, '-mat',4003,'-dir',xdir)
element('zeroLength',150,182,181, '-mat',4003,'-dir',xdir)
element('zeroLength',151,184,183, '-mat',4003,'-dir',xdir)
element('zeroLength',152,186,185, '-mat',4003,'-dir',xdir)
element('zeroLength',153,188,187, '-mat',4003,'-dir',xdir)
element('zeroLength',154,190,189, '-mat',4003,'-dir',xdir)

element('zeroLength',155,192,191, '-mat',4001,'-dir',xdir)  # node 8: Right side

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',156,194,193, '-mat',4000,'-dir',ydir)  # node 1: Left side

element('zeroLength',157,196,195, '-mat',4002,'-dir',ydir)
element('zeroLength',158,198,197, '-mat',4002,'-dir',ydir)
element('zeroLength',159,200,199, '-mat',4002,'-dir',ydir)
element('zeroLength',160,202,201, '-mat',4002,'-dir',ydir)
element('zeroLength',161,204,203, '-mat',4002,'-dir',ydir)
element('zeroLength',162,206,205, '-mat',4002,'-dir',ydir)

element('zeroLength',163,208,207, '-mat',4000,'-dir',ydir)  # node 8: Left side

print("Finished creating Bottom dashpot material and element...")

# # output_file = f"ele{col + 1}.txt"

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
# timeSeries('Path',702, '-filePath','2fs.txt','-dt',1e-4)
timeSeries('Path',704, '-filePath','topForce.txt','-dt',1e-4)

# # # timeSeries('Linear',705)

pattern('Plain',703, 704)
# load(803,0,-1)
load(165,0,-1)
# # ------------- P wave -----------------------------
# eleLoad('-ele', 141, '-type','-beamUniform',20,0)
# eleLoad('-ele', 142, '-type','-beamUniform',20,0)
# eleLoad('-ele', 143, '-type','-beamUniform',20,0)
# eleLoad('-ele', 144, '-type','-beamUniform',20,0)
# eleLoad('-ele', 145, '-type','-beamUniform',20,0)
# eleLoad('-ele', 146, '-type','-beamUniform',20,0)
# eleLoad('-ele', 147, '-type','-beamUniform',20,0)

# # ------------- S wave -----------------------------
# eleLoad('-ele', 141, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 142, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 143, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 144, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 145, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 146, '-type','-beamUniform',0,20,0)
# eleLoad('-ele', 147, '-type','-beamUniform',0,20,0)

print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# # -------------- Recorder --------------------------------
# # recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# # recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# # ------------- left column -------------
# recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
# recorder('Element', '-file', 'Stress/ele71.out', '-time', '-ele',71, 'material ',1,'stresses')
# recorder('Element', '-file', 'Stress/ele134.out', '-time', '-ele',134, 'material ',1,'stresses')

# recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
# recorder('Node', '-file', 'Velocity/node81.out', '-time', '-node',81,'-dof',1,2,3,'vel')
# recorder('Node', '-file', 'Velocity/node161.out', '-time', '-node',161,'-dof',1,2,3,'vel')
# # ------------- Center column -------------
# recorder('Element', '-file', 'Stress/ele4.out', '-time', '-ele',4, 'material ',1,'stresses')
# recorder('Element', '-file', 'Stress/ele74.out', '-time', '-ele',74, 'material ',1,'stresses')
# recorder('Element', '-file', 'Stress/ele137.out', '-time', '-ele',137, 'material ',1,'stresses')

# recorder('Node', '-file', 'Velocity/node4.out', '-time', '-node',4,'-dof',1,2,3,'vel')
# recorder('Node', '-file', 'Velocity/node84.out', '-time', '-node',84,'-dof',1,2,3,'vel')
# recorder('Node', '-file', 'Velocity/node164.out', '-time', '-node',164,'-dof',1,2,3,'vel')
# # ------------- Right column -------------
# recorder('Element', '-file', 'Stress/ele7.out', '-time', '-ele',7, 'material ',1,'stresses')
# recorder('Element', '-file', 'Stress/ele77.out', '-time', '-ele',77, 'material ',1,'stresses')
# recorder('Element', '-file', 'Stress/ele140.out', '-time', '-ele',140, 'material ',1,'stresses')

# recorder('Node', '-file', 'Velocity/node8.out', '-time', '-node',8,'-dof',1,2,3,'vel')
# recorder('Node', '-file', 'Velocity/node88.out', '-time', '-node',88,'-dof',1,2,3,'vel')
# recorder('Node', '-file', 'Velocity/node168.out', '-time', '-node',168,'-dof',1,2,3,'vel')

# ================= Create an output directory ===================
filename = '0.7mTieBC_20row_Top'
if not os.path.exists(filename):
    os.makedirs(filename)
recorder('PVD', filename, 'vel','eleResponse','stresses') #'eleResponse','stresses'

system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(8000,1e-4)
print("finish analyze:0 ~ 0.8s")

# # printModel('-ele', 701,702,703,704,705,707)
# --------- end to calculate time -------------
end = time.time()
print(end - start)

