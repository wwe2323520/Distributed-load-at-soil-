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

# # -------- Soil B.C ---------------
# for i in range(ny+1):
#     equalDOF(8*i+1,8*i+8,1,2)

# ============== Build Beam element (810~817) (ele 701~707)=========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(810+j, 0.10*j,0.0)
    mass(810+j,1,1,1)
# -------- fix rotate dof ------------
    fix(810+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1 #0.1*1
E1 = 1e-06 ; #1e-06 1e+6
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx): #nx
    element('elasticBeamColumn', 701+k, 810+k, 811+k, A,E1,Iz, 1,'-release', 3)

# # ==== Connect beam node with Bot Dashpot node: ele 900~913 ============
# E2 = 1e+20
# uniaxialMaterial('Elastic', 5000,E2)
# for o in range(2*nx):
#     element('twoNodeLink',900+o,810+o,811+o,'-mat',5000,'-dir',2)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,810+k,1,2)

# ============================Bottom Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 818,819~ 832,833)-> for S wave------------
    node(818+2*l, 0.10*l, 0.0)
    node(819+2*l, 0.10*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(818+2*l, 0, 1, 1)      # x dir dashpot　
    fix(819+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 834,835~ 848,849)-> for P wave ------------
    node(834+2*l, 0.10*l, 0.0)
    node(835+2*l, 0.10*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(834+2*l, 1, 0, 1)      # y dir dashpot　
    fix(835+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k, 818+2*k,1)
# --------------Normal dashpot: for P wave--------------------
    equalDOF(1+k, 834+2*k,2)

print("Finished creating all Bottom dashpot boundary conditions and equalDOF...")
# ------------------- ZeroLength to Build dashpot: Material ----------------------------------
rho = 2020   # kg/m3 
Vp = 100     # m/s 
Vs = 53.45224838248488     ;# m/s 
sizeX = 0.1   # m 0.1
B_Smp = 0.5*rho*Vp*sizeX      # lower Left and Right corner node dashpot :N (newton) 0.5
B_Sms = 0.5*rho*Vs*sizeX      # lower Left and Right corner node dashpot :N (newton) 0.5

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
element('zeroLength',800,819,818, '-mat',4001,'-dir',xdir)  # node 1: Left side

element('zeroLength',801,821,820, '-mat',4003,'-dir',xdir)
element('zeroLength',802,823,822, '-mat',4003,'-dir',xdir)
element('zeroLength',803,825,824, '-mat',4003,'-dir',xdir)
element('zeroLength',804,827,826, '-mat',4003,'-dir',xdir)
element('zeroLength',805,829,828, '-mat',4003,'-dir',xdir)
element('zeroLength',806,831,830, '-mat',4003,'-dir',xdir)

element('zeroLength',807,833,832, '-mat',4001,'-dir',xdir)

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',808,835,834, '-mat',4000,'-dir',ydir)  # node 1: Left side

element('zeroLength',809,837,836, '-mat',4002,'-dir',ydir)
element('zeroLength',810,839,838, '-mat',4002,'-dir',ydir)
element('zeroLength',811,841,840, '-mat',4002,'-dir',ydir)
element('zeroLength',812,843,842, '-mat',4002,'-dir',ydir)
element('zeroLength',813,845,844, '-mat',4002,'-dir',ydir)
element('zeroLength',814,847,846, '-mat',4002,'-dir',ydir)

element('zeroLength',815,849,848, '-mat',4000,'-dir',ydir)

print("Finished creating Bottom dashpot material and element...")

# ============ Side Beam Node =====================================
# ------- Left Side Beam Node (ndoe 850~1050) (ele 816~915)-------------------
for l in range(ny+1):
    node(850+2*l, 0.0, 0.1*l)
    mass(850+2*l, 1, 1, 1)

    if l < ny:
        node(851+2*l, 0.0, 0.05+0.10*l)
        mass(851+2*l,1,1,1)
        fix(851+2*l,0,0,1)
# -------- fix rotate dof ------------
    fix(850+2*l,0,0,1)
    
# ------- Right Side Beam Node (ndoe 1051~1251) (ele 916~1015) -------------------
for l in range(ny+1):
    node(1051+2*l, 0.7, 0.1*l)
    mass(1051+2*l, 1, 1, 1)

    if l < ny:
        node(1052+2*l, 0.7, 0.05+0.10*l)
        mass(1052+2*l,1,1,1)
        fix(1052+2*l,0,0,1)
# -------- fix rotate dof ------------
    fix(1051+2*l,0,0,1)

# ---- Left Beam -----------------
element('elasticBeamColumn', 816, 850, 852, A,E1,Iz, 1,'-release', 1)
element('elasticBeamColumn', 915, 1048, 1050, A,E1,Iz, 1,'-release', 2)
for k in range(1,ny-1): #ny
    element('elasticBeamColumn', 816+k, 850+2*k, 852+2*k, A,E1,Iz, 1)

# ---- Right Beam -----------------
element('elasticBeamColumn', 916, 1051, 1053, A,E1,Iz, 1,'-release', 1)
element('elasticBeamColumn', 1015, 1249, 1251, A,E1,Iz, 1,'-release', 2)
for k in range(1,ny-1): #ny
    element('elasticBeamColumn', 916+k, 1051+2*k, 1053+2*k, A,E1,Iz, 1)

# --------- Side Beam and Soil BC -----------------
for j in range(101):
    equalDOF(1+8*j,850+2*j,1,2)
    equalDOF(8+8*j,1051+2*j,1,2)

# ======== Connect beam node with Side Dashpot node =================
E2 = 1e+20
uniaxialMaterial('Elastic', 5000,E1)
# ---------- Left twoNodeLink element : ele 1016~1215 ---------------------------------
for o in range(2*ny):
    element('twoNodeLink',1016+o, 850+o, 851+o,'-mat',5000,'-dir',1,2)

# ---------- Right twoNodeLink element: ele 1216~1415  ---------------------------------
    element('twoNodeLink',1216+o, 1051+o, 1052+o,'-mat',5000,'-dir',1,2)

# ============== Soil Left and Right "Side" Dashpot =====================================
for l in range(ny):
# ========= Left Side =============
# --------- Normal dashpot (node 1252,1253~ 1450,1451)-> for S wave------------
    node(1252+2*l, 0.0, 0.05+0.1*l)
    node(1253+2*l, 0.0, 0.05+0.1*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(1252+2*l, 0, 1, 1)      # x dir dashpot　
    fix(1253+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 1452,1453~ 1650,1651)-> for P wave------------
    node(1452+2*l, 0.0, 0.05+0.1*l)
    node(1453+2*l, 0.0, 0.05+0.1*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(1452+2*l, 1, 0, 1)      # y dir dashpot　
    fix(1453+2*l, 1, 1, 1)      # fixed end to let soil fix

# ========= Right Side =============
# --------- Normal dashpot (node 1652,1653~ 1850,1851)-> for S wave------------
    node(1652+2*l, 0.7, 0.05+0.1*l)
    node(1653+2*l, 0.7, 0.05+0.1*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(1652+2*l, 0, 1, 1)      # x dir dashpot　
    fix(1653+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 1852,1853~ 2050,2051)-> for P wave------------
    node(1852+2*l, 0.7, 0.05+0.1*l)
    node(1853+2*l, 0.7, 0.05+0.1*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(1852+2*l, 1, 0, 1)      # y dir dashpot　
    fix(1853+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------
for l in range(ny):
# ========= Left Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(851+2*l, 1252+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(851+2*l, 1452+2*l, 2)  # y dir

# ========= Right Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(1052+2*l, 1652+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(1052+2*l, 1852+2*l, 2)  # y dir
print("Finished creating all Side dashpot boundary conditions and equalDOF...")

# ------------- Side dashpot material -----------------------
S_Smp = 1.0*rho*Vp*sizeX    # side Normal dashpot for S wave   ; lower/Upper  Left and Right corner node 0.5
S_Sms = 1.0*rho*Vs*sizeX    # side Traction dashpot for P wave ; lower/Upper Left and Right corner node 0.5

S_Cmp = 1.0*rho*Vp*sizeX    # side Normal dashpot for S wave: Netwon
S_Cms = 1.0*rho*Vs*sizeX    # side Traction dashpot for P wave: Netwon

uniaxialMaterial('Viscous',4004, S_Smp, 1)    # "S" wave: Side node
uniaxialMaterial('Viscous',4005, S_Sms, 1)    # "P" wave: Side node

uniaxialMaterial('Viscous',4006, S_Cmp, 1)    # "S" wave: Center node
uniaxialMaterial('Viscous',4007, S_Cms, 1)    # "P" wave: Center node

# =============== Right and Left NODE :different dashpot element==================
#  ----------- Left side Normal: S wave ----------
element('zeroLength',1416, 1253, 1252, '-mat',4004,'-dir',xdir)  # node 851:  -> Smp
element('zeroLength',1515, 1451, 1450, '-mat',4004,'-dir',xdir)  # node 1049:  -> Smp

#  ----------- Left side Traction: P wave ----------
element('zeroLength',1516, 1453, 1452, '-mat',4005,'-dir',ydir)  # node 851 -> Sms
element('zeroLength',1615, 1651, 1650, '-mat',4005,'-dir',ydir)  # node 1049 -> Sms

#  ----------- Right side Normal: S wave ----------
element('zeroLength',1616, 1653, 1652, '-mat',4004,'-dir',xdir)  # node 1052 -> Smp
element('zeroLength',1715, 1851, 1850, '-mat',4004,'-dir',xdir)  # node 1250 -> Smp
#  ----------- Right side Traction: P wave ----------
element('zeroLength',1716, 1853, 1852, '-mat',4005,'-dir',ydir)  # node 1052 -> Sms
element('zeroLength',1815, 2051, 2050, '-mat',4005,'-dir',ydir)  # node 1250 -> Sms

for w in range(1,ny-1): #1,ny
#----------- Left side Normal Dashpot: (ele 1416~1515)---------- -> Smp
    element('zeroLength',1416+w, 1253+2*w, 1252+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
# #----------- Left side Traction Dashpot: (ele 1516~1615) ---------- -> Sms
    element('zeroLength',1516+w, 1453+2*w, 1452+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

#----------- Right side Normal Dashpot:(ele 1616 ~ 1715) ---------- -> Smp
    element('zeroLength',1616+w, 1653+2*w, 1652+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Right side Traction Dashpot: (ele 1716 ~ 1815) ----------  -> Sms
    element('zeroLength',1716+w, 1853+2*w, 1852+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

print("Finished creating Side dashpot material and element...")

# # ==================== Side Load Pattern (Pwave) ============================
# # --------------------- Side Beam Distributed Force ------------------------------
# for g in range(100):
# # ------- timeSeries ID: 800~899 (global x force) ----------------------
#     timeSeries('Path',800+g, '-filePath',f'P_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
#     pattern('Plain',804+g, 800+g)
# # ---------- x direction : Sideforce  ---------------------
# # ---------- Distributed at Left Side Beam (ele 816~915)----------------------
#     eleLoad('-ele',816+g, '-type', '-beamUniform',-20,0)  # for local axes Wy
# # ---------- Distributed at Right Side Beam (ele 916~1015)----------------------
#     eleLoad('-ele',916+g, '-type', '-beamUniform',20,0)   # for local axes Wy

# # ------------------------- Side Node Force ----------------------------------------
# timeSeries('Path',900, '-filePath',f'P_Sideforce_y/ele{1}.txt','-dt',1e-4)
# pattern('Plain',904, 900)
# # ---- NodeForce at Left Side Corner -----
# load(851,0,1,0)
# # ---- NodeForce at Right Side Corner -----
# load(1052,0,1,0)

# timeSeries('Path',999, '-filePath',f'P_Sideforce_y/ele{100}.txt','-dt',1e-4)
# pattern('Plain',1003, 999)
# # ---- NodeForce at Left Side Corner -----
# load(1049,0,1,0)
# # ---- NodeForce at Right Side Corner -----
# load(1250,0,1,0)

# for g in range(1,ny-1): #101 1,100
# # ------- timeSeries ID: 900~1000 (global y force): node 2~100----------------------
# # ---------- y direction : Sideforce --------------------
#     timeSeries('Path',900+g, '-filePath',f'P_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
#     pattern('Plain',904+g, 900+g)
# # ---------- For P wave : y direction ---------------------
# # ---------- NodeForce at Left Side Beam ----------------------
#     load(851+2*g,0,1,0) #(0,2,0)
# # ---------- NodeForce at Right Side Beam ----------------------
#     load(1052+2*g,0,1,0) #(0,2,0)

# ==================== Side Load Pattern (Swave) ============================
# -------------------------- Side Node Force -------------------------------
timeSeries('Path',800, '-filePath',f'S_Sideforce_x/ele{1}.txt','-dt',1e-4)
pattern('Plain',804, 800)
# ---- NodeForce at Left Side Corner -----
load(851,1,0,0)
# ---- NodeForce at Right Side Corner -----
load(1052,1,0,0)

timeSeries('Path',899, '-filePath',f'S_Sideforce_x/ele{100}.txt','-dt',1e-4)
pattern('Plain',903, 899)
# ---- NodeForce at Left Side Corner -----
load(1049,1,0,0)
# ---- NodeForce at Right Side Corner -----
load(1250,1,0,0)

for g in range(1,ny-1): #1011,100
# ------- timeSeries ID: 800~899 (global y force)----------------------
# ---------- x direction : Nodeforce --------------------
    timeSeries('Path',800+g, '-filePath',f'S_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
    pattern('Plain',804+g, 800+g)
# ---------- For S wave : x direction ---------------------
# ---------- NodeForce at Left Side Beam ----------------------
    load(851+2*g,1,0,0)
# ---------- NodeForce at Right Side Beam ----------------------
    load(1052+2*g,1,0,0)

# ---------------------- Side Beam Distributed Force -------------------------------
for g in range(100):
# ------- timeSeries ID: 900~999 ----------------------
# ---------- y direction : Sideforce --------------------
    timeSeries('Path',900+g, '-filePath',f'S_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
    pattern('Plain',904+g, 900+g)
# ---------- For P wave : y direction ---------------------
# ---------- Distributed at Left Side Beam ----------------------
    eleLoad('-ele',816+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# ---------- Distributed at Right Side Beam ----------------------
    eleLoad('-ele',916+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wx -

print("finish SideBeam Force InputFile Apply")

#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
timeSeries('Path',702, '-filePath','2fs.txt','-dt',1e-4)
# timeSeries('Path',705, '-filePath','fp.txt','-dt',1e-4)
# timeSeries('Path',704, '-filePath','topForce.txt','-dt',1e-4)

pattern('Plain',703, 702)
# # ------------- P wave -----------------------------
# eleLoad('-ele', 701, '-type','-beamUniform',20,0)
# eleLoad('-ele', 702, '-type','-beamUniform',20,0)
# eleLoad('-ele', 703, '-type','-beamUniform',20,0)
# eleLoad('-ele', 704, '-type','-beamUniform',20,0)
# eleLoad('-ele', 705, '-type','-beamUniform',20,0)
# eleLoad('-ele', 706, '-type','-beamUniform',20,0)
# eleLoad('-ele', 707, '-type','-beamUniform',20,0)

# ------------- S wave -----------------------------
eleLoad('-ele', 701, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 702, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 703, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 704, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 705, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 706, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 707, '-type','-beamUniform',0,20,0)


# # # load(805,0,-1)
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
recorder('Node', '-file', 'Velocity/node951.out', '-time', '-node',951,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node1049.out', '-time', '-node',1049,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node1250.out', '-time', '-node',1250,'-dof',1,2,3,'vel')
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
