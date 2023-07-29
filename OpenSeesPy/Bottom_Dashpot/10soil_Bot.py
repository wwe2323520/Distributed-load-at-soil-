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

# -------- Soil B.C (node 1~10201)---------------
for i in range(ny+1):
# ------- P wave -----------
    # fix(101*i+1,  1,0)
    # fix(101*i+101,1,0)
# ------- S wave -----------
    fix(101*i+1,  0,1)
    fix(101*i+101,0,1)
    # equalDOF(101*i+1,101*i+101,1,2)
    
# ============== Build Beam element (10202~10302) (ele 10001~10100) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(10202+j,0.1*j,0.0)
    mass(10202+j,1,1,1)
# -------- fix rotate dof ------------
    fix(10202+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e+20   #1e-06 (M/EI)
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 10001+k, 10202+k, 10203+k, A,E1,Iz, 1, '-release', 3)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(10202+k,1+k,1,2)

# ============================ Beam element dashpot =============================== #
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
    equalDOF(10202+l, 10303+2*l, 1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(10202+l, 10505+2*l, 2)

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
element('zeroLength',20000, 10304,10303, '-mat',4001,'-dir',xdir)  # node 1: Left side
element('zeroLength',20100, 10504,10503, '-mat',4001,'-dir',xdir)  # node 101: Left side

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',20101, 10506,10505, '-mat',4000,'-dir',ydir)  # node 1: Left side
element('zeroLength',20201, 10706,10705, '-mat',4000,'-dir',ydir)  # node 101: Left side

for q in range(1,nx):
# -------- Traction dashpot element: Vs with x dir (ele 20001~20099) ------------------
    element('zeroLength',20000+q, 10304+2*q,10303+2*q, '-mat',4003,'-dir',xdir)

# -------- Normal dashpot element: Vp with y dir (ele 20102~20200) ------------------
    element('zeroLength',20101+q, 10506+2*q,10505+2*q, '-mat',4002,'-dir',xdir)

print("Finished creating dashpot material and element...")
#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
timeSeries('Path',702, '-filePath','2fs.txt','-dt',1e-4)
timeSeries('Linear',705)

pattern('Plain',703, 702)
# ------------- P wave -----------------------------
# for m in range(nx):
#     eleLoad('-ele', 10001+m, '-type','-beamUniform',20,0)

# ------------- S wave -----------------------------
for m in range(nx):
    eleLoad('-ele', 10001+m, '-type','-beamUniform',0,20,0)
# load(1, 0, 1)
# load(2, 0, 1) 
print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# printModel('-ele',700)
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
