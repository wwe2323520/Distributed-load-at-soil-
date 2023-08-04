# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 11:02:11 2023

@author: User
"""
from openseespy.opensees import *
import opsvis as ops
import matplotlib.pyplot as plt
import time

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
for i in range(ny+1):
    equalDOF(201*i+1,201*i+201,1,2)

# ============== Build Beam element (20302~20502) (ele 20001~20200) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(20302+j,0.1*j,0.0)
    mass(20302+j,1,1,1)
# -------- fix rotate dof ------------
    fix(20302+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e+20   #1e-06 (M/EI)
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

#------------- Load Pattern ----------------------------
timeSeries('Path',702, '-filePath','fp.txt','-dt',1e-4)
# timeSeries('Path',702, '-filePath','fs.txt','-dt',1e-4)
timeSeries('Linear',705)

pattern('Plain',703, 702)
# ------------- P wave -----------------------------
for m in range(nx):
    eleLoad('-ele', 20001+m, '-type','-beamUniform',20,0)

# ------------- S wave -----------------------------
# for m in range(nx):
#     eleLoad('-ele', 20001+m, '-type','-beamUniform',0,20,0)

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
