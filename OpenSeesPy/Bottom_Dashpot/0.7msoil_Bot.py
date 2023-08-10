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

# ============== Build Beam element (810~817) (ele 701~707) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(810+j,0.1*j,0.0)
    mass(810+j,1,1,1)
# -------- fix rotate dof ------------
    fix(810+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 701+k, 810+k, 811+k, A,E1,Iz, 1, '-release', 3)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,810+k,1,2)

# ============================ Beam element dashpot =============================== #
for l in range(nx+1):
# ------------- traction dashpot (node 818,819~ 832,833)-> for S wave------------
    node(818+2*l, 0.1*l, 0.0)
    node(819+2*l, 0.1*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(818+2*l, 0, 1, 1)      # x dir dashpot　
    fix(819+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 834,835~ 848,849)-> for P wave ------------
    node(834+2*l, 0.1*l, 0.0)
    node(835+2*l, 0.1*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(834+2*l, 1, 0, 1)      # y dir dashpot　
    fix(835+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------

for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k,818+2*k,1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+k,834+2*k,2)


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
element('zeroLength',800,819,818, '-mat',4001,'-dir',xdir)  # node 1: Left side

element('zeroLength',801,821,820, '-mat',4003,'-dir',xdir)
element('zeroLength',802,823,822, '-mat',4003,'-dir',xdir)
element('zeroLength',803,825,824, '-mat',4003,'-dir',xdir)
element('zeroLength',804,827,826, '-mat',4003,'-dir',xdir)
element('zeroLength',805,829,828, '-mat',4003,'-dir',xdir)
element('zeroLength',806,831,830, '-mat',4003,'-dir',xdir)

element('zeroLength',807,833,832, '-mat',4001,'-dir',xdir)  # node 8: Right side

# ------ Normal dashpot element: Vp with y dir
element('zeroLength',808,835,834, '-mat',4000,'-dir',ydir)  # node 1: Left side

element('zeroLength',809,837,836, '-mat',4002,'-dir',ydir)
element('zeroLength',810,839,838, '-mat',4002,'-dir',ydir)
element('zeroLength',811,841,840, '-mat',4002,'-dir',ydir)
element('zeroLength',812,843,842, '-mat',4002,'-dir',ydir)
element('zeroLength',813,845,844, '-mat',4002,'-dir',ydir)
element('zeroLength',815,847,846, '-mat',4002,'-dir',ydir)

element('zeroLength',816,849,848, '-mat',4000,'-dir',ydir)  # node 8: Left side

print("Finished creating dashpot material and element...")
#------------- Load Pattern ----------------------------
# timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
timeSeries('Path',702, '-filePath','2fs.txt','-dt',1e-4)
timeSeries('Linear',705)

pattern('Plain',703, 702)
# ------------- P wave -----------------------------
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

system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(8000,1e-4)
print("finish analyze:0 ~ 0.8s")

printModel('-ele', 701,702,703,704,705,707)
# --------- end to calculate time -------------
end = time.time()
print(end - start)
