# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 11:02:11 2023

@author: User
"""
from openseespy.opensees import *
import opsvis as ops
import matplotlib.pyplot as plt
import time
import os

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
ny = 100
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

# ============== Build Beam element (810~824) (ele 701~707: left and Right release/Center no) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(810+2*j,0.10*j,0.0)
    mass(810+2*j,1,1,1)

    if j < nx:
        node(811+2*j,0.05+0.10*j,0.0)
        mass(811+2*j,1,1,1)
        fix(811+2*j,0,0,1)
# -------- fix rotate dof ------------
    fix(810+2*j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1 #0.1*1
E1 = 1e+20 ; #1e-06 1e+6
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

# element('elasticBeamColumn', 701, 810, 811, A,E1,Iz, 1, '-release', 1) 810--|811*|-812
# element('elasticBeamColumn', 702, 811, 812, A,E1,Iz, 1, '-release', 2)

for k in range(nx):
    element('elasticBeamColumn', 701+2*k, 810+2*k, 811+2*k, A,E1,Iz, 1, '-release', 1)
    element('elasticBeamColumn', 702+2*k, 811+2*k, 812+2*k, A,E1,Iz, 1, '-release', 2)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,810+2*k,1,2)

# ============================Bottom Beam element dashpot =============================== #
for l in range(nx):
# ------------- traction dashpot (node 825,826~ 837,838)-> for S wave------------
    node(825+2*l, 0.05 +0.10*l, 0.0)
    node(826+2*l, 0.05 +0.10*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(825+2*l, 0, 1, 1)      # x dir dashpot　
    fix(826+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 839,840~ 851,852)-> for P wave ------------
    node(839+2*l, 0.05 +0.10*l, 0.0)
    node(840+2*l, 0.05 +0.10*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(839+2*l, 1, 0, 1)      # y dir dashpot　
    fix(840+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx):
# --------------traction dashpot: for S wave------------------********* maybe 811+2*k, 825+2*k
    equalDOF(811+2*k,825+2*k,1)
# --------------Normal dashpot: for P wave------------------*************
    equalDOF(811+2*k,839+2*k,2)

print("Finished creating all Bottom dashpot boundary conditions and equalDOF...")
# ------------------- ZeroLength to Build dashpot: Material ----------------------------------
rho = 2020   # kg/m3 
Vp = 100     # m/s 
Vs = 53.45224838248488     ;# m/s 
sizeX = 0.1   # m 0.1
B_Smp = 1.0*rho*Vp*sizeX      # lower Left and Right corner node dashpot :N (newton) 0.5
B_Sms = 1.0*rho*Vs*sizeX      # lower Left and Right corner node dashpot :N (newton) 0.5

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
element('zeroLength',800,826,825, '-mat',4001,'-dir',xdir)  # node 1: Left side

element('zeroLength',801,828,827, '-mat',4003,'-dir',xdir)
element('zeroLength',802,830,829, '-mat',4003,'-dir',xdir)
element('zeroLength',803,832,831, '-mat',4003,'-dir',xdir)
element('zeroLength',804,834,833, '-mat',4003,'-dir',xdir)
element('zeroLength',805,836,835, '-mat',4003,'-dir',xdir)

element('zeroLength',806,838,837, '-mat',4001,'-dir',xdir)

# # ------ Normal dashpot element: Vp with y dir
element('zeroLength',808,840,839, '-mat',4000,'-dir',ydir)  # node 1: Left side

element('zeroLength',809,842,841, '-mat',4002,'-dir',ydir)
element('zeroLength',810,844,843, '-mat',4002,'-dir',ydir)
element('zeroLength',811,846,845, '-mat',4002,'-dir',ydir)
element('zeroLength',812,848,847, '-mat',4002,'-dir',ydir)
element('zeroLength',813,850,849, '-mat',4002,'-dir',ydir)

element('zeroLength',815,852,851, '-mat',4000,'-dir',ydir)

print("Finished creating Bottom dashpot material and element...")


# # ============== Soil Left and Right "Side" Dashpot =====================================
# for l in range(ny+1):
# # ========= Left Side =============
# # --------- Normal dashpot (node 850,851~ 1050,1051)-> for S wave------------
#     node(850+2*l, 0.0, 0.1*l)
#     node(851+2*l, 0.0, 0.1*l)
# # ---------- dashpot dir: Vs -> x dir ---------------------     
#     fix(850+2*l, 0, 1, 1)      # x dir dashpot　
#     fix(851+2*l, 1, 1, 1)      # fixed end to let soil fix

# # --------- Traction dashpot (node 1052,1053~ 1252,1253)-> for P wave------------
#     node(1052+2*l, 0.0, 0.1*l)
#     node(1053+2*l, 0.0, 0.1*l)
# # ---------- dashpot dir: Vp -> y dir ---------------------     
#     fix(1052+2*l, 1, 0, 1)      # y dir dashpot　
#     fix(1053+2*l, 1, 1, 1)      # fixed end to let soil fix

# # ========= Right Side =============
# # --------- Normal dashpot (node 1254,1255~ 1454,1455)-> for S wave------------
#     node(1254+2*l, 0.7, 0.1*l)
#     node(1255+2*l, 0.7, 0.1*l)
# # ---------- dashpot dir: Vs -> x dir ---------------------     
#     fix(1254+2*l, 0, 1, 1)      # x dir dashpot　
#     fix(1255+2*l, 1, 1, 1)      # fixed end to let soil fix

# # --------- Traction dashpot (node 1456,1457~ 1656,1657)-> for P wave------------
#     node(1456+2*l, 0.7, 0.1*l)
#     node(1457+2*l, 0.7, 0.1*l)
# # ---------- dashpot dir: Vp -> y dir ---------------------     
#     fix(1456+2*l, 1, 0, 1)      # y dir dashpot　
#     fix(1457+2*l, 1, 1, 1)      # fixed end to let soil fix
    
# # ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------
# for l in range(ny+1):
# # ========= Left Side =============
# # --------------Normal dashpot: for S wave------------------
#     equalDOF(1+8*l, 850+2*l, 1)  # x dir
# # --------------Traction dashpot: for P wave------------------
#     equalDOF(1+8*l, 1052+2*l, 2)  # y dir

# # ========= Right Side =============
# # --------------Normal dashpot: for S wave------------------
#     equalDOF(8+8*l, 1254+2*l, 1)  # x dir
# # --------------Traction dashpot: for P wave------------------
#     equalDOF(8+8*l, 1456+2*l, 2)  # y dir

# print("Finished creating all Side dashpot boundary conditions and equalDOF...")
# # ------------- Side dashpot material -----------------------
# S_Smp = 0.5*rho*Vp*sizeX    # side Normal dashpot for S wave   ; lower/Upper  Left and Right corner node
# S_Sms = 0.5*rho*Vs*sizeX    # side Traction dashpot for P wave ; lower/Upper Left and Right corner node

# S_Cmp = 1.0*rho*Vp*sizeX    # side Normal dashpot for S wave: Netwon
# S_Cms = 1.0*rho*Vs*sizeX    # side Traction dashpot for P wave: Netwon

# uniaxialMaterial('Viscous',4004, S_Smp, 1)    # "S" wave: Side node
# uniaxialMaterial('Viscous',4005, S_Sms, 1)    # "P" wave: Side node

# uniaxialMaterial('Viscous',4006, S_Cmp, 1)    # "S" wave: Center node
# uniaxialMaterial('Viscous',4007, S_Cms, 1)    # "P" wave: Center node

# # =============== Right and Left NODE :different dashpot element==================
# #  ----------- Left side Normal: S wave ----------
# element('zeroLength',817, 851, 850, '-mat',4004,'-dir',xdir)  # node 1:  -> Smp
# element('zeroLength',917, 1051, 1050, '-mat',4004,'-dir',xdir)  # node 801:  -> Smp
# #  ----------- Left side Traction: P wave ----------
# element('zeroLength',918, 1053, 1052, '-mat',4005,'-dir',ydir)  # node 1 -> Sms
# element('zeroLength',1018, 1253, 1252, '-mat',4005,'-dir',ydir)  # node 801 -> Sms

# #  ----------- Right side Normal: S wave ----------
# element('zeroLength',1019, 1255, 1254, '-mat',4004,'-dir',xdir)  # node 8 -> Smp
# element('zeroLength',1119, 1455, 1454, '-mat',4004,'-dir',xdir)  # node 808 -> Smp
# #  ----------- Right side Traction: P wave ----------
# element('zeroLength',1120, 1457, 1456, '-mat',4005,'-dir',ydir)  # node 8 -> Sms
# element('zeroLength',1220, 1657, 1656, '-mat',4005,'-dir',ydir)  # node 808 -> Sms

# for w in range(1,ny): #1,ny
# #----------- Left side Normal Dashpot: (ele 818~916)---------- -> Smp
#     element('zeroLength',817+w, 851+2*w, 850+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
# #----------- Left side Traction Dashpot: (ele 919~1017) ---------- -> Sms
#     element('zeroLength',918+w, 1053+2*w, 1052+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

# #----------- Right side Normal Dashpot:(ele 1020 ~ 1118) ---------- -> Smp
#     element('zeroLength',1019+w, 1255+2*w, 1254+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
# #----------- Right side Traction Dashpot: (ele 1121 ~ 1219) ----------  -> Sms
#     element('zeroLength',1120+w, 1457+2*w, 1456+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

# print("Finished creating Side dashpot material and element...")

#------------- Load Pattern ----------------------------
timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
# timeSeries('Path',702, '-filePath','2fs.txt','-dt',1e-4)
# timeSeries('Path',705, '-filePath','fp.txt','-dt',1e-4)
# timeSeries('Path',704, '-filePath','topForce.txt','-dt',1e-4)

pattern('Plain',703, 702)

# ------------- P wave -----------------------------
eleLoad('-ele', 701, '-type','-beamUniform',20,0)
eleLoad('-ele', 702, '-type','-beamUniform',20,0)
eleLoad('-ele', 703, '-type','-beamUniform',20,0)
eleLoad('-ele', 704, '-type','-beamUniform',20,0)
eleLoad('-ele', 705, '-type','-beamUniform',20,0)
eleLoad('-ele', 706, '-type','-beamUniform',20,0)
eleLoad('-ele', 707, '-type','-beamUniform',20,0)

# # ------------- S wave -----------------------------
# # eleLoad('-ele', 701, '-type','-beamUniform',0,20,0)
# # eleLoad('-ele', 702, '-type','-beamUniform',0,20,0)
# # eleLoad('-ele', 703, '-type','-beamUniform',0,20,0)
# # eleLoad('-ele', 704, '-type','-beamUniform',0,20,0)
# # eleLoad('-ele', 705, '-type','-beamUniform',0,20,0)
# # eleLoad('-ele', 706, '-type','-beamUniform',0,20,0)
# # eleLoad('-ele', 707, '-type','-beamUniform',0,20,0)

# # load(805,0,-1)
print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

#-------------- Recorder --------------------------------
# recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# ------------- left column -------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele351.out', '-time', '-ele',351, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele694.out', '-time', '-ele',694, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node401.out', '-time', '-node',401,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node801.out', '-time', '-node',801,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', 'Stress/ele4.out', '-time', '-ele',4, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele354.out', '-time', '-ele',354, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele697.out', '-time', '-ele',697, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node4.out', '-time', '-node',4,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node404.out', '-time', '-node',404,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node804.out', '-time', '-node',804,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', 'Stress/ele7.out', '-time', '-ele',7, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele357.out', '-time', '-ele',357, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele700.out', '-time', '-ele',700, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node8.out', '-time', '-node',8,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node408.out', '-time', '-node',408,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node808.out', '-time', '-node',808,'-dof',1,2,3,'vel')

# ------------ Dashpot Node --------------------
recorder('Node', '-file', 'Velocity/node811.out', '-time', '-node',811,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node817.out', '-time', '-node',817,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node823.out', '-time', '-node',823,'-dof',1,2,3,'vel')
# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele695.out', '-time', '-ele',695, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node803.out', '-time', '-node',803,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele699.out', '-time', '-ele',699, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node806.out', '-time', '-node',806,'-dof',1,2,3,'vel')

# # ================= Create an output directory ===================
# filename = 'Soil0.7m_TopSide'
# if not os.path.exists(filename):
#     os.makedirs(filename)
# recorder('PVD', filename, 'vel','eleResponse','stresses') #'eleResponse','stresses'


system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(8000,1e-4)
print("finish analyze:0 ~ 0.8s")

# printModel('-ele', 701,702,703,704,705,707)
# --------- end to calculate time -------------
end = time.time()
print(end - start)
