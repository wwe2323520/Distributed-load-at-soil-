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
soilLength = 10 #m
nx = 8
ny = 20
e1 = 1
n1 = 1
eleArgs = [1, 'PlaneStrain', 2000]
points = [1, 0.0,   0.0, 
          2, 1.0,  0.0, 
          3, 1.0,  10.0, 
          4, 0.0,   10.0]
block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)
# printModel('-ele',153,157,160)
# # -------- Soil B.C ---------------
# for i in range(ny+1):
#     equalDOF(9*i+1,9*i+9,1,2)

# ============== Build Beam element (190~198) (ele 161~168) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(190+j,0.125*j,0.0)
    mass(190+j,1,1,1)
# -------- fix rotate dof ------------
    fix(190+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 161+k, 190+k, 191+k, A,E1,Iz, 1, '-release', 3)
# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,190+k,1,2)

# ============================ Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 199,200~ 215,216)-> for S wave------------
    node(199+2*l, 0.125*l, 0.0)
    node(200+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(199+2*l, 0, 1, 1)      # x dir dashpot　
    fix(200+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 217,218~ 233,234)-> for P wave ------------
    node(217+2*l, 0.125*l, 0.0)
    node(218+2*l, 0.125*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(217+2*l, 1, 0, 1)      # y dir dashpot　
    fix(218+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k,199+2*k,1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+k,217+2*k,2)

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
element('zeroLength',169,200,199, '-mat',4001,'-dir',xdir)  # node 1: Left side

element('zeroLength',170,202,201, '-mat',4003,'-dir',xdir)
element('zeroLength',171,204,203, '-mat',4003,'-dir',xdir)
element('zeroLength',172,206,205, '-mat',4003,'-dir',xdir)
element('zeroLength',173,208,207, '-mat',4003,'-dir',xdir)
element('zeroLength',174,210,209, '-mat',4003,'-dir',xdir)
element('zeroLength',175,212,211, '-mat',4003,'-dir',xdir)
element('zeroLength',176,214,213, '-mat',4003,'-dir',xdir)

element('zeroLength',177,216,215, '-mat',4001,'-dir',xdir)  # node 8: Right side

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',178, 218, 217, '-mat',4000,'-dir',ydir)  # node 1: Left side

element('zeroLength',179, 220, 219, '-mat',4002,'-dir',ydir)
element('zeroLength',180,222,221, '-mat',4002,'-dir',ydir)
element('zeroLength',181,224,223, '-mat',4002,'-dir',ydir)
element('zeroLength',182,226,225, '-mat',4002,'-dir',ydir)
element('zeroLength',183,228,227, '-mat',4002,'-dir',ydir)
element('zeroLength',184,230,229, '-mat',4002,'-dir',ydir)
element('zeroLength',185,232,231, '-mat',4002,'-dir',ydir)

element('zeroLength',186,234,233, '-mat',4000,'-dir',ydir)  # node 8: Left side

print("Finished creating Bottom dashpot material and element...")

# ============== Soil Left and Right "Side" Dashpot =====================================
yMesh = soilLength/ny # Y row MeshSize
for l in range(ny+1):
# ========= Left Side =============
# --------- Normal dashpot (node 235,236~ 275,276)-> for S wave------------
    node(235+2*l, 0.0, yMesh*l)
    node(236+2*l, 0.0, yMesh*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(235+2*l, 0, 1, 1)      # x dir dashpot　
    fix(236+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 277,278~ 317,318)-> for P wave------------
    node(277+2*l, 0.0, yMesh*l)
    node(278+2*l, 0.0, yMesh*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(277+2*l, 1, 0, 1)      # y dir dashpot　
    fix(278+2*l, 1, 1, 1)      # fixed end to let soil fix
 
# ========= Right Side =============
# --------- Normal dashpot (node 319,320~ 359,360)-> for S wave------------
    node(319+2*l, 1.0, yMesh*l)
    node(320+2*l, 1.0, yMesh*l)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(319+2*l, 0, 1, 1)      # x dir dashpot　
    fix(320+2*l, 1, 1, 1)      # fixed end to let soil fix

# --------- Traction dashpot (node 361,362~ 401,402)-> for P wave------------
    node(361+2*l, 1.0, yMesh*l)
    node(362+2*l, 1.0, yMesh*l)
# ---------- dashpot dir: Vp -> y dir ---------------------     
    fix(361+2*l, 1, 0, 1)      # y dir dashpot　
    fix(362+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------
for l in range(ny+1):
# ========= Left Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(1+9*l, 235+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(1+9*l, 277+2*l, 2)  # y dir

# ========= Right Side =============
# --------------Normal dashpot: for S wave------------------
    equalDOF(9+9*l, 319+2*l, 1)  # x dir
# --------------Traction dashpot: for P wave------------------
    equalDOF(9+9*l, 361+2*l, 2)  # y dir

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
element('zeroLength',187, 236, 235, '-mat',4004,'-dir',xdir)  # node 1:  -> Smp
element('zeroLength',207, 276, 275, '-mat',4004,'-dir',xdir)  # node 801:  -> Smp
#  ----------- Left side Traction: P wave ----------
element('zeroLength',208, 278, 277, '-mat',4005,'-dir',ydir)  # node 1 -> Sms
element('zeroLength',228, 318, 317, '-mat',4005,'-dir',ydir)  # node 801 -> Sms

#  ----------- Right side Normal: S wave ----------
element('zeroLength',229, 320, 319, '-mat',4004,'-dir',xdir)  # node 8 -> Smp
element('zeroLength',249, 360, 359, '-mat',4004,'-dir',xdir)  # node 808 -> Smp
#  ----------- Right side Traction: P wave ----------
element('zeroLength',250, 362, 361, '-mat',4005,'-dir',ydir)  # node 8 -> Sms
element('zeroLength',270, 402, 401, '-mat',4005,'-dir',ydir)  # node 808 -> Sms

for w in range(1,ny): #1,ny
#----------- Left side Normal Dashpot: (ele 187~207)---------- -> Smp
    element('zeroLength',187+w, 236+2*w, 235+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Left side Traction Dashpot: (ele 208~228) ---------- -> Sms
    element('zeroLength',208+w, 278+2*w, 277+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

#----------- Right side Normal Dashpot:(ele 229 ~ 249) ---------- -> Smp
    element('zeroLength',229+w, 320+2*w, 319+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
#----------- Right side Traction Dashpot: (ele 250 ~ 270) ----------  -> Sms
    element('zeroLength',250+w, 362+2*w, 361+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave

print("Finished creating Side dashpot material and element...")

# ==================== Side Beam node (403~423 / 424~444) ====================
for i in range(ny+1):
# ----- Left Side: 403~423 -----------------
    node(403+i, 0.0, yMesh*i)
    fix(403+i,0,0,1)
# ----- Right Side: 424~444 -----------------
    node(424+i,1.0,yMesh*i)
    fix(424+i,0,0,1)

# ------------  Beam Element: 271 ~ 290 / 291 ~ 310 ------------------
for j in range(ny):
# ----- Left Side Beam:271 ~ 290 -----------------
    element('elasticBeamColumn', 271+j, 403+j, 404+j, A,E1,Iz, 1, '-release', 3)
# ----- Right Side Beam:291 ~ 310 -----------------
    element('elasticBeamColumn', 291+j, 424+j, 425+j, A,E1,Iz, 1, '-release', 3)

# --------- Side Beam and Soil BC -----------------
for j in range(ny+1):
    equalDOF(1+9*j,403+j,1,2)
    equalDOF(9+9*j,424+j,1,2)

# ============================== S wave ======================================
# ------------ Side Load Pattern ------------------------------
for g in range(ny):
# ------- timeSeries ID: 800~819 / Pattern ID: 804~823----------------------
    timeSeries('Path',800+g, '-filePath',f'SSideforce_20rowx/ele{1+g}.txt','-dt',2.5e-4)
    pattern('Plain',804+g, 800+g)
# ---------- x direction : Sideforce ---------------------
# ---------- Distributed at Left Side Beam ----------------------
    eleLoad('-ele',271+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# ---------- Distributed at Right Side Beam ----------------------
    eleLoad('-ele',291+g, '-type', '-beamUniform',-20,0)   # for local axes Wy +

for g in range(ny):
# ------- timeSeries ID: 820~839 / Pattern ID:824~843 ----------------------
# ---------- y direction : Sideforce --------------------
    timeSeries('Path',820+g, '-filePath',f'SSideforce_20rowy/ele{1+g}.txt','-dt',2.5e-4)
    pattern('Plain',824+g, 820+g)
# ---------- For P wave : y direction ---------------------
# ---------- Distributed at Left Side Beam ----------------------
    eleLoad('-ele',271+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# ---------- Distributed at Right Side Beam ----------------------
    eleLoad('-ele',291+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wx -

print("finish SideBeam Force InputFile Apply")

#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
timeSeries('Path',702, '-filePath','fs200_20row.txt','-dt',2.5e-4)
# timeSeries('Path',704, '-filePath','TopForce20row.txt','-dt',1.33e-4)

# # # # timeSeries('Linear',705)

pattern('Plain',703, 702)

# load(185,0,-1)
# # # ------------- P wave -----------------------------
# # eleLoad('-ele', 71, '-type','-beamUniform',20,0)
# # eleLoad('-ele', 72, '-type','-beamUniform',20,0)
# # eleLoad('-ele', 73, '-type','-beamUniform',20,0)
# # eleLoad('-ele', 74, '-type','-beamUniform',20,0)
# # eleLoad('-ele', 75, '-type','-beamUniform',20,0)
# # eleLoad('-ele', 76, '-type','-beamUniform',20,0)
# # eleLoad('-ele', 77, '-type','-beamUniform',20,0)

# ------------- S wave -----------------------------
eleLoad('-ele', 161, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 162, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 163, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 164, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 165, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 166, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 167, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 168, '-type','-beamUniform',0,20,0)

print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# -------------- Recorder --------------------------------
# recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# ------------- left column -------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele81.out', '-time', '-ele',81, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele153.out', '-time', '-ele',153, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node91.out', '-time', '-node',91,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node181.out', '-time', '-node',181,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', 'Stress/ele5.out', '-time', '-ele',5, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele85.out', '-time', '-ele',85, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele157.out', '-time', '-ele',157, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node5.out', '-time', '-node',5,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node95.out', '-time', '-node',95,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node185.out', '-time', '-node',185,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', 'Stress/ele8.out', '-time', '-ele',8, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele88.out', '-time', '-ele',88, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele160.out', '-time', '-ele',160, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node9.out', '-time', '-node',9,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node99.out', '-time', '-node',99,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node189.out', '-time', '-node',189,'-dof',1,2,3,'vel')

# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele155.out', '-time', '-ele',155, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node183.out', '-time', '-node',183,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele159.out', '-time', '-ele',159, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node187.out', '-time', '-node',187,'-dof',1,2,3,'vel')


system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(1600,2.5e-4)
print("finish analyze:0 ~ 0.8s")

# # # printModel('-ele', 701,702,703,704,705,707)
# --------- end to calculate time -------------
end = time.time()
print(end - start)
