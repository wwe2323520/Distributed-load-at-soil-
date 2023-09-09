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

nx = 100
ny = 100
e1 = 1
n1 = 1
eleArgs = [1, 'PlaneStrain', 2000]
points = [1, 0.0, 0.0, 
          2, 10.0, 0.0, 
          3, 10.0, 10.0, 
          4, 0.0, 10.0]
block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)

# # -------- Soil B.C (node 1~10201)---------------
# for i in range(ny+1):
#     equalDOF(101*i+1,101*i+101,1,2)

# ============== Build Beam element (10202~10302) (ele 10001~10100) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(10202+j,0.1*j,0.0)
    mass(10202+j,1,1,1)
# -------- fix rotate dof ------------
    fix(10202+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06   #1e-06 (M/EI); 1e+20
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 10001+k, 10202+k, 10203+k, A,E1,Iz, 1, '-release', 3)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,10202+k,1,2)

# ============================Bottom dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 10303,10304~ 10503,10504)-> for S wave------------
    node(10303+2*l, 0.1*l, 0.0)
    node(10304+2*l, 0.1*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(10303+2*l, 0, 1, 1)      # x dir dashpot　
    fix(10304+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 10505,10506~ 10705,10706)-> for P wave ------------
    node(10505+2*l, 0.1*l, 0.0)
    node(10506+2*l, 0.1*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(10505+2*l, 1, 0, 1)      # y dir dashpot　
    fix(10506+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for l in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+l, 10303+2*l, 1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+l, 10505+2*l, 2)

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
element('zeroLength',20000, 10304,10303, '-mat',4001,'-dir',xdir)  # node 1: Left side
element('zeroLength',20100, 10504,10503, '-mat',4001,'-dir',xdir)  # node 101: Left side

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',20101, 10506,10505, '-mat',4000,'-dir',ydir)  # node 1: Left side
element('zeroLength',20201, 10706,10705, '-mat',4000,'-dir',ydir)  # node 101: Left side

for q in range(1,nx):
# -------- Traction dashpot element: Vs with x dir (ele 20001~20099) ------------------
    element('zeroLength',20000+q, 10304+2*q,10303+2*q, '-mat',4003,'-dir',xdir)

# -------- Normal dashpot element: Vp with y dir (ele 20102~20200) ------------------
    element('zeroLength',20101+q, 10506+2*q,10505+2*q, '-mat',4002,'-dir',ydir)

print("Finished creating Bottom dashpot material and element...")

# ============ Side Beam Node =====================================
# ------- Left Side Beam Node (ndoe 10707~10907) (ele 20202~20401)-------------------
for l in range(ny+1):
    node(10707+2*l, 0.0, 0.1*l)
    mass(10707+2*l, 1, 1, 1)

    if l < ny:
        node(10708+2*l, 0.0, 0.05+0.10*l)
        mass(10708+2*l,1,1,1)
        fix(10708+2*l,0,0,1)
# -------- fix rotate dof ------------
    fix(10707+2*l,0,0,1)

# ------- Right Side Beam Node (ndoe 10908~11108) (ele 20402~20601) -------------------
for l in range(ny+1):
    node(10908+2*l, 10.0, 0.1*l)
    mass(10908+2*l, 1, 1, 1)

    if l < ny:
        node(10909+2*l, 10.0, 0.05+0.10*l)
        mass(10909+2*l,1,1,1)
        fix(10909+2*l,0,0,1)
# -------- fix rotate dof ------------
    fix(10908+2*l,0,0,1)

E2 = 1e-06  #1e+20 1e-06
# ---- Left Beam (ele 20202~20401)-----------------
for k in range(ny): #ny 
    element('elasticBeamColumn', 20202+2*k, 10707+2*k, 10708+2*k, A,E2,Iz, 1, '-release', 1)
    element('elasticBeamColumn', 20203+2*k, 10708+2*k, 10709+2*k, A,E2,Iz, 1, '-release', 2)

# ---- Right Beam (ele 20402~20601)-----------------
for k in range(ny): #ny 
    element('elasticBeamColumn', 20402+2*k, 10908+2*k, 10909+2*k, A,E2,Iz, 1, '-release', 1)
    element('elasticBeamColumn', 20403+2*k, 10909+2*k, 10910+2*k, A,E2,Iz, 1, '-release', 2)

# --------- Side Beam and Soil BC -----------------
for j in range(101):
    equalDOF(1+101*j,   10707+2*j,1,2)
    equalDOF(101+101*j, 10908+2*j,1,2)

# =============== Soil Left and Right "Side" Dashpot =============================== #
for o in range(ny):
# ======================== Left side ====================
# --------- Normal dashpot (node 11109,11110~ 11307,11308)-> for S wave------------
    node(11109+2*o, 0.0, 0.05+0.1*o)
    node(11110+2*o, 0.0, 0.05+0.1*o)

    fix(11109+2*o, 0 ,1 ,1)
    fix(11110+2*o, 1 ,1 ,1)

# --------- Traction dashpot (node 11309,11310~ 11507,11508)-> for P wave------------
    node(11309+2*o, 0.0, 0.05+0.1*o)
    node(11310+2*o, 0.0, 0.05+0.1*o)

    fix(11309+2*o, 1 ,0 ,1)
    fix(11310+2*o, 1 ,1 ,1)

# ======================== Right side ====================
# --------- Normal dashpot (node 11509,11510~ 11707,11708)-> for S wave------------
    node(11509+2*o, 10.0, 0.05+0.1*o)
    node(11510+2*o, 10.0, 0.05+0.1*o)

    fix(11509+2*o, 0 ,1 ,1)
    fix(11510+2*o, 1 ,1 ,1)

# --------- Traction dashpot (node 11709,11710~ 11907,11908)-> for P wave------------
    node(11709+2*o, 10.0, 0.05+0.1*o)
    node(11710+2*o, 10.0, 0.05+0.1*o)

    fix(11709+2*o, 1 ,0 ,1)
    fix(11710+2*o, 1 ,1 ,1)

# ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------
for o in range(ny):
# ========================== Left Side ============================
# --------------Normal dashpot: for S wave------------------
    equalDOF(10708+2*o, 11109+2*o, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(10708+2*o, 11309+2*o, 2)  # y dir

# ========================== Right Side ============================
# --------------Normal dashpot: for S wave------------------
    equalDOF(10909+2*o, 11509+2*o, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(10909+2*o, 11709+2*o, 2)  # y dir

print("Finished creating all Side dashpot boundary conditions and equalDOF...")

# ------------- Side dashpot material -----------------------
sizex1 = 0.05
S_Smp = 1.0*rho*Vp*sizex1    # side Normal dashpot for S wave   ; lower/Upper  Left and Right corner node
S_Sms = 1.0*rho*Vs*sizex1    # side Traction dashpot for P wave ; lower/Upper Left and Right corner node

S_Cmp = 1.0*rho*Vp*sizex1    # side Normal dashpot for S wave: Netwon
S_Cms = 1.0*rho*Vs*sizex1    # side Traction dashpot for P wave: Netwon

uniaxialMaterial('Viscous',4004, S_Smp, 1)    # "S" wave: Side node
uniaxialMaterial('Viscous',4005, S_Sms, 1)    # "P" wave: Side node

uniaxialMaterial('Viscous',4006, S_Cmp, 1)    # "S" wave: Center node
uniaxialMaterial('Viscous',4007, S_Cms, 1)    # "P" wave: Center node

# =============== Right and Left NODE :different dashpot element==================
#  ----------- Left side Normal: S wave ----------
element('zeroLength',20802, 11110, 11109, '-mat',4004,'-dir',xdir)  # node 1:  -> Smp
element('zeroLength',20901, 11308, 11307, '-mat',4004,'-dir',xdir)  # node 801:  -> Smp
# #  ----------- Left side Traction: P wave ----------
element('zeroLength',20902, 11310, 11309, '-mat',4005,'-dir',ydir)  # node 1 -> Sms
element('zeroLength',21001, 11508, 11507, '-mat',4005,'-dir',ydir)  # node 801 -> Sms

#  ----------- Right side Normal: S wave ----------
element('zeroLength',21002, 11510, 11509, '-mat',4004,'-dir',xdir)  # node 101:  -> Smp
element('zeroLength',21101, 11708, 11707, '-mat',4004,'-dir',xdir)  # node 10201:  -> Smp

# #  ----------- Right side Traction: P wave ----------
element('zeroLength',21102, 11710, 11709, '-mat',4005,'-dir',ydir)  # node 101 -> Sms
element('zeroLength',21201, 11908, 11907, '-mat',4005,'-dir',ydir)  # node 10201 -> Sms

for w in range(1,ny-1): #1,ny   1,ny-1
#----------- Left side Normal Dashpot: (ele 20802~20901)---------- -> Smp
    element('zeroLength',20802+w, 11110+2*w, 11109+2*w, '-mat',4006,'-dir',xdir)  # center node：S wave
#----------- Left side Traction Dashpot: (ele 20902~21001) ---------- -> Sms
    element('zeroLength',20902+w, 11310+2*w, 11309+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

#----------- Right side Normal Dashpot: (ele 21002~21101)---------- -> Smp
    element('zeroLength',21002+w, 11510+2*w, 11509+2*w, '-mat',4006,'-dir',xdir)  # center node：S wave
#----------- Right side Traction Dashpot: (ele 21102~21201) ---------- -> Sms
    element('zeroLength',21102+w, 11710+2*w, 11709+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

print("Finished creating Side dashpot material and element...")

# ==================== Side Load Pattern (Pwave) ============================
# --------------------- Side Beam Distributed Force ------------------------------
for g in range(200):
# ------- timeSeries ID: 800~999 (global x force) / pattern ID 804~1003----------------------
    timeSeries('Path',800+g, '-filePath',f'P_Sideforce200ele_x/ele{1+g}.txt','-dt',5e-5)
    pattern('Plain',804+g, 800+g)
# ---------- x direction : Sideforce  ---------------------
# ---------- Distributed at Left Side Beam (ele 816~1015)----------------------
    eleLoad('-ele',20202+g, '-type', '-beamUniform',-20,0)  # for local axes Wy
# ---------- Distributed at Right Side Beam (ele 1016~1215)----------------------
    eleLoad('-ele',20402+g, '-type', '-beamUniform',20,0)   # for local axes Wy

# for g in range(200):
# # ------- timeSeries ID: 900~999 (global y force)----------------------
# # ---------- y direction : Sideforce --------------------
#     timeSeries('Path',1000+g, '-filePath',f'P_Sideforce200ele_y/ele{1+g}.txt','-dt',5e-5)
#     pattern('Plain',1004+g, 1000+g)
# # ---------- For P wave : y direction ---------------------
# # ---------- Distributed at Left Side Beam ----------------------
#     eleLoad('-ele',816+g, '-type', '-beamUniform',0,20,0)  # for local axes Wx
# # ---------- Distributed at Right Side Beam ----------------------
#     eleLoad('-ele',1016+g, '-type', '-beamUniform',0,20,0)   # for local axes Wx

# ------------------------- Side Node Force ----------------------------------------
timeSeries('Path',1000, '-filePath',f'P_Sideforce_y/ele{1}.txt','-dt',1e-4)
pattern('Plain',1004, 1000)
# ---- NodeForce at Left Side Corner -----
load(10708,0,1,0)
# ---- NodeForce at Right Side Corner -----
load(10909,0,1,0)

timeSeries('Path',1099, '-filePath',f'P_Sideforce_y/ele{100}.txt','-dt',1e-4)
pattern('Plain',1103, 1099)
# ---- NodeForce at Left Side Corner -----
load(10906,0,1,0)
# ---- NodeForce at Right Side Corner -----
load(11107,0,1,0)

for g in range(1,ny-1): #101 1,100
# ------- timeSeries ID: 900~1000 (global y force): node 2~100----------------------
# ---------- y direction : Sideforce --------------------
    timeSeries('Path',1000+g, '-filePath',f'P_Sideforce_y/ele{1+g}.txt','-dt',1e-4)
    pattern('Plain',1004+g, 1000+g)
# ---------- For P wave : y direction ---------------------
# ---------- NodeForce at Left Side Beam ----------------------
    load(10708+2*g,0,2,0) #(0,2,0)
# ---------- NodeForce at Right Side Beam ----------------------
    load(10909+2*g,0,2,0) #(0,2,0)

# # ==================== Side Load Pattern (Swave) ============================
# # -------------------------- Side Node Force -------------------------------
# timeSeries('Path',800, '-filePath',f'S_Sideforce_x/ele{1}.txt','-dt',1e-4)
# pattern('Plain',804, 800)
# # ---- NodeForce at Left Side Corner -----
# load(10708,1,0,0)
# # ---- NodeForce at Right Side Corner -----
# load(10909,1,0,0)

# timeSeries('Path',899, '-filePath',f'S_Sideforce_x/ele{100}.txt','-dt',1e-4)
# pattern('Plain',903, 899)
# # ---- NodeForce at Left Side Corner -----
# load(10906,1,0,0)
# # ---- NodeForce at Right Side Corner -----
# load(11107,1,0,0)

# for g in range(1,ny-1): #1011,100
# # ------- timeSeries ID: 800~899 (global y force)----------------------
# # ---------- x direction : Nodeforce --------------------
#     timeSeries('Path',800+g, '-filePath',f'S_Sideforce_x/ele{1+g}.txt','-dt',1e-4)
#     pattern('Plain',804+g, 800+g)
# # ---------- For S wave : x direction ---------------------
# # ---------- NodeForce at Left Side Beam ----------------------
#     load(10708+2*g,1,0,0)
# # ---------- NodeForce at Right Side Beam ----------------------
#     load(10909+2*g,1,0,0)

# # ---------------------- Side Beam Distributed Force -------------------------------
# for g in range(100):
# # ------- timeSeries ID: 900~999 ----------------------
# # ---------- y direction : Sideforce --------------------
#     timeSeries('Path',900+g, '-filePath',f'S_Sideforce200ele_y/ele{1+g}.txt','-dt',5e-5)
#     pattern('Plain',904+g, 900+g)
# # ---------- For P wave : y direction ---------------------
# # ---------- Distributed at Left Side Beam ----------------------
#     eleLoad('-ele',20202+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # ---------- Distributed at Right Side Beam ----------------------
#     eleLoad('-ele',20402+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wx -

# print("finish SideBeam Force InputFile Apply")

#------------- Load Pattern ----------------------------
timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
# timeSeries('Path',702, '-filePath','2fs.txt','-dt',1e-4)
# timeSeries('Linear',705)

pattern('Plain',703, 702)
# ------------- P wave -----------------------------
for m in range(nx):
    eleLoad('-ele', 10001+m, '-type','-beamUniform',20,0)

# # ------------- S wave -----------------------------
# for m in range(nx):
#     eleLoad('-ele', 10001+m, '-type','-beamUniform',0,20,0)

# # load(1, 0, 1)
# # load(2, 0, 1) 
print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")


# #-------------- Recorder --------------------------------
# recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# ------------- left column -------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele5001.out', '-time', '-ele',5001, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele9901.out', '-time', '-ele',9901, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node5051.out', '-time', '-node',5051,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node10101.out', '-time', '-node',10101,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', 'Stress/ele51.out', '-time', '-ele',51, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele5051.out', '-time', '-ele',5051, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele9951.out', '-time', '-ele',9951, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node51.out', '-time', '-node',51,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node5101.out', '-time', '-node',5101,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node10151.out', '-time', '-node',10151,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', 'Stress/ele100.out', '-time', '-ele',100, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele5100.out', '-time', '-ele',5100, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele10000.out', '-time', '-ele',10000, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node101.out', '-time', '-node',101,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node5151.out', '-time', '-node',5151,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node10201.out', '-time', '-node',10201,'-dof',1,2,3,'vel')

# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele9926.out', '-time', '-ele',9926, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node10126.out', '-time', '-node',10126,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele9976.out', '-time', '-ele',9976, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node10176.out', '-time', '-node',10176,'-dof',1,2,3,'vel')

# # ================= Create an output directory ===================
# filename = 'soil10m_SideMidDash_Pwave'
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
