# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 11:02:11 2023

@author: User
"""
from openseespy.opensees import *
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

nx = 200
ny = 100
e1 = 1
n1 = 1
eleArgs = [1, 'PlaneStrain', 2000]
points = [1, 0.0, 0.0, 
          2, 20.0, 0.0, 
          3, 20.0, 10.0, 
          4, 0.0, 10.0]
block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)

# -------- Soil B.C (node 1~20301)---------------
# for i in range(ny+1):
#     equalDOF(201*i+1,201*i+201,1,2)

# ============== Build Beam element (20302~20502) (ele 20001~20200) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(20302+j,0.1*j,0.0)
    mass(20302+j,1,1,1)
# -------- fix rotate dof ------------
    fix(20302+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06   #1e-06 (M/EI); 1e+20
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 20001+k, 20302+k, 20303+k, A,E1,Iz, 1, '-release', 3)
# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,20302+k,1,2)

# ============================ Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 20503,20504~ 20903,20904)-> for S wave------------
    node(20503+2*l, 0.1*l, 0.0)
    node(20504+2*l, 0.1*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(20503+2*l, 0, 1, 1)      # x dir dashpot　
    fix(20504+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 20905,20906~ 21305,21306)-> for P wave ------------
    node(20905+2*l, 0.1*l, 0.0)
    node(20906+2*l, 0.1*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(20905+2*l, 1, 0, 1)      # y dir dashpot　
    fix(20906+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for l in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+l, 20503+2*l, 1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+l, 20905+2*l, 2)

print("Finished creating all dashpot boundary conditions and equalDOF...")
# ------------------- ZeroLength to Build dashpot: Material ----------------------------------
rho = 2020   # kg/m3 
Vp = 100     # m/s 
Vs = 53.45224838248488     ;# m/s 
sizeX = 0.1  # m
Smp = 0.5*rho*Vp*sizeX      # lower Left and Right corner node dashpot :N (newton)
Sms = 0.5*rho*Vs*sizeX      # lower Left and Right corner node dashpot :N (newton)

Cmp = 1.0*rho*Vp*sizeX      # Bottom Center node dashpot :N (newton)
Cms = 1.0*rho*Vs*sizeX      # Bottom Center node dashpot :N (newton)

uniaxialMaterial('Viscous',4000, Smp, 1)    # P wave: Side node
uniaxialMaterial('Viscous',4001, Sms, 1)    # S wave: Side node

uniaxialMaterial('Viscous',4002, Cmp, 1)    # P wave: Center node
uniaxialMaterial('Viscous',4003, Cms, 1)    # S wave: Center node

#----------- dashpot elements: Vs with x dir / Vp with y-dir------------------
xdir = 1
ydir = 2
# ------ Traction dashpot element: Vs with x dir
element('zeroLength',20201, 20504,20503, '-mat',4001,'-dir',xdir)  # node 1: Left side
element('zeroLength',20401, 20904,20903, '-mat',4001,'-dir',xdir)  # node 101: Left side

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',20402, 20906,20905, '-mat',4000,'-dir',ydir)  # node 1: Left side
element('zeroLength',20602, 21306,21305, '-mat',4000,'-dir',ydir)  # node 101: Left side

for q in range(1,nx): #1,nx
# -------- Traction dashpot element: Vs with x dir (ele 20202~20400) ------------------
    element('zeroLength',20201+q, 20504+2*q,20503+2*q, '-mat',4003,'-dir',xdir)

# -------- Normal dashpot element: Vp with y dir (ele 20403~20601) ------------------
    element('zeroLength',20402+q, 20906+2*q,20905+2*q, '-mat',4002,'-dir',ydir)

print("Finished creating dashpot material and element...")

# =============== Soil Left and Right "Side" Dashpot =============================== #
for o in range(ny+1):
# ======================== Left side ====================
# --------- Normal dashpot (node 21307,21308~ 21507,21508)-> for S wave------------
    node(21307+2*o, 0.0, 0.1*o)
    node(21308+2*o, 0.0, 0.1*o)

    fix(21307+2*o, 0 ,1 ,1)
    fix(21308+2*o, 1 ,1 ,1)

# --------- Traction dashpot (node 21509,21510~ 21709,21710)-> for P wave------------
    node(21509+2*o, 0.0, 0.1*o)
    node(21510+2*o, 0.0, 0.1*o)

    fix(21509+2*o, 1 ,0 ,1)
    fix(21510+2*o, 1 ,1 ,1)

# ======================== Right side ====================
# --------- Normal dashpot (node 21711,21712~ 21911,21912)-> for S wave------------
    node(21711+2*o, 20.0, 0.1*o)
    node(21712+2*o, 20.0, 0.1*o)

    fix(21711+2*o, 0 ,1 ,1)
    fix(21712+2*o, 1 ,1 ,1)

# --------- Traction dashpot (node 21913,21914~ 22113,22114)-> for P wave------------
    node(21913+2*o, 20.0, 0.1*o)
    node(21914+2*o, 20.0, 0.1*o)

    fix(21913+2*o, 1 ,0 ,1)
    fix(21914+2*o, 1 ,1 ,1)

# ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------
for o in range(ny+1):
# ========================== Left Side ============================
# --------------Normal dashpot: for S wave------------------
    equalDOF(1+201*o, 21307+2*o, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(1+201*o, 21509+2*o, 2)  # y dir

# ========================== Right Side ============================
# --------------Normal dashpot: for S wave------------------
    equalDOF(201+201*o, 21711+2*o, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(201+201*o, 21913+2*o, 2)  # y dir

print("Finished creating all Side dashpot boundary conditions and equalDOF...")
# ------------- Side dashpot material -----------------------
S_Smp = 0.5*rho*Vp*sizeX    # side Normal dashpot for S wave   ; lower/Upper  Left and Right corner node
S_Sms = 0.5*rho*Vs*sizeX    # side Traction dashpot for P wave ; lower/Upper Left and Right corner node

S_Cmp = 1.0*rho*Vp*sizeX    # side Normal dashpot for S wave: Netwon
S_Cms = 1.0*rho*Vs*sizeX    # side Traction dashpot for P wave: Netwon

uniaxialMaterial('Viscous',4004, S_Smp, 1)    # "S" wave: Side node
uniaxialMaterial('Viscous',4005, S_Sms, 1)    # "P" wave: Side node

uniaxialMaterial('Viscous',4006, S_Cmp, 1)    # "S" wave: Center node
uniaxialMaterial('Viscous',4007, S_Cms, 1)    # "P" wave: Center node

# =============== Right and Left NODE :different dashpot element==================
#  ----------- Left side Normal: S wave ----------
element('zeroLength',20603, 21308, 21307, '-mat',4004,'-dir',xdir)  # node 1:  -> Smp
element('zeroLength',20703, 21508, 21507, '-mat',4004,'-dir',xdir)  # node 801:  -> Smp
#  ----------- Left side Traction: P wave ----------
element('zeroLength',20704, 21510, 21509, '-mat',4005,'-dir',ydir)  # node 1 -> Sms
element('zeroLength',20804, 21710, 21709, '-mat',4005,'-dir',ydir)  # node 801 -> Sms

#  ----------- Right side Normal: S wave ----------
element('zeroLength',20805, 21712, 21711, '-mat',4004,'-dir',xdir)  # node 101:  -> Smp
element('zeroLength',20905, 21912, 21911, '-mat',4004,'-dir',xdir)  # node 10201:  -> Smp

#  ----------- Right side Traction: P wave ----------
element('zeroLength',20906, 21914, 21913, '-mat',4005,'-dir',ydir)  # node 101 -> Sms
element('zeroLength',21006, 22114, 22113, '-mat',4005,'-dir',ydir)  # node 10201 -> Sms

for w in range(1,ny): #1,ny  
#----------- Left side Normal Dashpot: (ele 20604~20702)---------- -> Smp
    element('zeroLength',20603+w, 21308+2*w, 21307+2*w, '-mat',4006,'-dir',xdir)  # center node：S wave
#----------- Left side Traction Dashpot: (ele 20705~20803) ---------- -> Sms
    element('zeroLength',20704+w, 21510+2*w, 21509+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

#----------- Right side Normal Dashpot: (ele 20806~20904)---------- -> Smp
    element('zeroLength',20805+w, 21712+2*w, 21711+2*w, '-mat',4006,'-dir',xdir)  # center node：S wave
#----------- Right side Traction Dashpot: (ele 20907~21005) ---------- -> Sms
    element('zeroLength',20906+w, 21914+2*w, 21913+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

print("Finished creating Side dashpot material and element...")

# ==================== Side Beam node (22115~22115 / 22216~22216) ====================
for i in range(ny+1):
# ----- Left Side: 22115~22115 -----------------
    node(22115+i, 0.0, 0.1*i)
    fix(22115+i, 0,0,1)
    
# ----- Right Side: 22216~ 22216 -----------------
    node(22216+i, 20.0, 0.1*i)
    fix(22216+i,0,0,1)

# ------------  Beam Element: 21007 ~ 21106 / 21107 ~ 21206 ------------------
for j in range(ny):
# ----- Left Side Beam:21007 ~ 21106 -----------------
    element('elasticBeamColumn', 21007+j, 22115+j, 22116+j, A,E1,Iz, 1, '-release', 3)
# ----- Right Side Beam:21107 ~ 21206 -----------------
    element('elasticBeamColumn', 21107+j, 22216+j, 22217+j, A,E1,Iz, 1, '-release', 3)

# --------- Side Beam and Soil BC -----------------
for j in range(101):
    equalDOF(1+201*j, 22115+j,1,2)
    equalDOF(201+201*j, 22216+j,1,2)

# # ============== Pwave ====================================
# # ------------ Side Load Pattern ------------------------------
# for g in range(100):
# # ------- timeSeries ID: 800~899 ---------------------
#     timeSeries('Path',800+g, '-filePath',f'P_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
#     pattern('Plain',804+g, 800+g) ;# 804~903
# # ----------x direction : Sideforce ---------------------
# # ---------- Distributed at Left Side Beam ----------------------
#     eleLoad('-ele',21007+g, '-type', '-beamUniform',-20,0)  # for local axes Wy
# # ---------- Distributed at Right Side Beam ----------------------
#     eleLoad('-ele',21107+g, '-type', '-beamUniform',20,0)   # for local axes Wy

# for g in range(100):
# # ------- timeSeries ID: 900~999 ----------------------
#     timeSeries('Path',900+g, '-filePath',f'P_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
#     pattern('Plain',904+g, 900+g) ;#  904~1003
# # ---------- y direction : Sideforce ---------------------
# # ---------- Distributed at Left Side Beam ----------------------
#     eleLoad('-ele',21007+g, '-type', '-beamUniform',0,20,0)  # for local axes Wy
# # ---------- Distributed at Right Side Beam ----------------------
#     eleLoad('-ele',21107+g, '-type', '-beamUniform',0,20,0)   # for local axes Wy

# ================= S wave ===================================
# ------------ Side Load Pattern：Side Node Force ------------------------------
timeSeries('Path',800, '-filePath',f'S_Nodeforce_x/node{1}.txt','-dt',1e-4)
pattern('Plain',804, 800)
# ---- NodeForce at Left Side Corner -----
load(22115,1,0,0)
# ---- NodeForce at Right Side Corner -----
load(22216,1,0,0)

timeSeries('Path',900, '-filePath',f'S_Nodeforce_x/node{101}.txt','-dt',1e-4)
pattern('Plain',904, 900)
# ---- NodeForce at Left Side Corner -----
load(22215,1,0,0)
# ---- NodeForce at Right Side Corner -----
load(22316,1,0,0)

for g in range(1,100): # 101 Center Node
# ------- timeSeries ID: 800~899 ---------------------
    timeSeries('Path',800+g, '-filePath',f'S_Nodeforce_x/node{1+g}.txt','-dt',1e-4)
    pattern('Plain',804+g, 800+g) ;# 804~903
# ---------- For S wave : x direction ---------------------
# ---------- NodeForce at Left Side Beam ----------------------
    load(22115+g,2,0,0)
# ---------- NodeForce at Right Side Beam ----------------------
    load(22216+g,2,0,0)

# ------------ Side Load Pattern：Side Beam Distributed Force -----------
for g in range(100):
# ------- timeSeries ID: 900~999 ----------------------
    timeSeries('Path',901+g, '-filePath',f'S_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
    pattern('Plain',905+g, 901+g) ;#  904~1003
# ---------- y direction : Sideforce ---------------------
# ---------- Distributed at Left Side Beam ----------------------
    eleLoad('-ele',21007+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wy
# ---------- Distributed at Right Side Beam ----------------------
    eleLoad('-ele',21107+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wy

print("finish SideBeam Force InputFile Apply")
#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
timeSeries('Path',702, '-filePath','2fs.txt','-dt',1e-4)
timeSeries('Linear',705)

pattern('Plain',703, 702)
# # ------------- P wave -----------------------------
# for m in range(nx):
#     eleLoad('-ele', 20001+m, '-type','-beamUniform',20,0)

# ------------- S wave -----------------------------
for m in range(nx):
    eleLoad('-ele', 20001+m, '-type','-beamUniform',0,20,0)

print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

#-------------- Recorder --------------------------------
# ------------- left column -------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele10001.out', '-time', '-ele',10001, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele19801.out', '-time', '-ele',19801, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node10051.out', '-time', '-node',10051,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node20101.out', '-time', '-node',20101,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', 'Stress/ele101.out', '-time', '-ele',101, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele10101.out', '-time', '-ele',10101, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele19901.out', '-time', '-ele',19901, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node101.out', '-time', '-node',101,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node10151.out', '-time', '-node',10151,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node20201.out', '-time', '-node',20201,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', 'Stress/ele200.out', '-time', '-ele',200, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele10200.out', '-time', '-ele',10200, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele20000.out', '-time', '-ele',20000, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node201.out', '-time', '-node',201,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node10251.out', '-time', '-node',10251,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node20301.out', '-time', '-node',20301,'-dof',1,2,3,'vel')

# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele19851.out', '-time', '-ele',19851, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node20151.out', '-time', '-node',20151,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele19951.out', '-time', '-ele',19951, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node20251.out', '-time', '-node',20251,'-dof',1,2,3,'vel')

# ================= Create an output directory ===================
filename = 'soil20m_NoSide_Swave'
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
