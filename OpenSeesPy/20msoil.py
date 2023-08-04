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
