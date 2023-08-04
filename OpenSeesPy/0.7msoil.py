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

# ============== Build Beam element (810~817) (ele 701~707) =========================
model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(810+j,0.1*j,0.0)
    mass(810+j,1,1,1)
# -------- fix rotate dof ------------
    fix(810+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1 #1e-4 0.1*1
E1 = 1e+20 #1e+20/ 1e-5
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', 701+k, 810+k, 811+k, A,E1,Iz, 1, '-release', 3)


# =========== Soil B.C  ======================
for i in range(ny+1):
    equalDOF(8*i+1,8*i+8,1,2)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(1+k,810+k,1,2)


#------------- Load Pattern ----------------------------
timeSeries('Path',702, '-filePath','fp.txt','-dt',1e-4)
# timeSeries('Path',702, '-filePath','fs.txt','-dt',1e-4)
timeSeries('Linear',705)

pattern('Plain',703, 702)
# ------------- P wave -----------------------------
eleLoad('-ele', 701, '-type','-beamUniform',20,0)
eleLoad('-ele', 702, '-type','-beamUniform',20,0)
eleLoad('-ele', 703, '-type','-beamUniform',20,0)
eleLoad('-ele', 704, '-type','-beamUniform',20,0)
eleLoad('-ele', 705, '-type','-beamUniform',20,0)
eleLoad('-ele', 706, '-type','-beamUniform',20,0)
eleLoad('-ele', 707, '-type','-beamUniform',20,0)

# ------------- S wave -----------------------------
eleLoad('-ele', 701, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 702, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 703, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 704, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 705, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 706, '-type','-beamUniform',0,20,0)
eleLoad('-ele', 707, '-type','-beamUniform',0,20,0)

print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# # printModel('-ele',700)
# #-------------- Recorder --------------------------------
# recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# ------------- left column -------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele351.out', '-time', '-ele',351, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele694.out', '-time', '-ele',694, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node401.out', '-time', '-node',401,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node801.out', '-time', '-node',801,'-dof',1,2,3,'vel')

recorder('Node', '-file', 'Disp/node1.out', '-time', '-node',1,'-dof',1,2,3,'disp')
# recorder('Node', '-file', 'Disp/node401.out', '-time', '-node',401,'-dof',1,2,3,'disp')
# recorder('Node', '-file', 'Disp/node801.out', '-time', '-node',801,'-dof',1,2,3,'disp')
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

recorder('Node', '-file', 'Disp/node8.out', '-time', '-node',8,'-dof',1,2,3,'disp')
# recorder('Node', '-file', 'Disp/node408.out', '-time', '-node',408,'-dof',1,2,3,'disp')
# recorder('Node', '-file', 'Disp/node808.out', '-time', '-node',808,'-dof',1,2,3,'disp')

# ============ Disp recorder(second layse) =========================
recorder('Node', '-file', 'Disp/node9.out', '-time', '-node',9,'-dof',1,2,3,'disp')
recorder('Node', '-file', 'Disp/node16.out', '-time', '-node',16,'-dof',1,2,3,'disp')

# ============= Dynamic Analysis =============================================
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
# printModel('-node', 810, 811, 812, 813, 814, 815, 816, 817)
# --------- end to calculate time -------------
end = time.time()
print(end - start)
