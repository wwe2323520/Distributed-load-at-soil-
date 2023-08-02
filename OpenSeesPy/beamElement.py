# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 12:23:16 2023

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
# # ============ Soil Column element : 1 column ============================
# model('basic', '-ndm', 2, '-ndf' , 2)
# E = 15005714.286
# nu = 0.3
# rho = 2020
# nDMaterial('ElasticIsotropic', 2000, E, nu, rho)

nx = 7
# ny = 100
# e1 = 1
# n1 = 1
# eleArgs = [1, 'PlaneStrain', 2000]
# points = [1, 0.0, 0.0, 2, 0.2,0.0, 3, 0.2,10.0, 4, 0.0,10.0]

# block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)

# # ----------- soil node Boundary condition: Left and right same disp:x,y-------------
# for i in range(ny+1):
#     equalDOF(3*i+1,3*i+3,1,2)
    
#     # fix(3*i+1, 1,0)
#     # fix(3*i+3, 1,0)
# ============ Beam element at bottom =================
model('basic', '-ndm', 2, '-ndf' , 3)
for i in range(8):
    node(810+i, 0.1*i, 0.0)
    mass(810+i, 1,1,1)
# --------- fix rotation dir ----------
    fix(810+i, 0,0,1)

# --------- Beam node B.C (Both fixed end)-----------
    # fix(810+i, 1,1,1)
# -------- fix rotation freedom -----------
# fix(304,0,0,1)
# fix(305,0,0,1)
# fix(306,0,0,1)

# --------- Build Beam element -----------
A = 0.1*1
E1 = 1e+20
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for j in range(7):
    element('elasticBeamColumn',701+j,810+j,811+j, A,E1,Iz,1,'-release', 3)



# equalDOF(304,306,1,2)
# # ============== connect soil node with bot beam node =====================
# equalDOF(304,1,1,2)
# equalDOF(305,2,1,2)
# equalDOF(306,3,1,2)

# ========== Apply Distributed load ===========================================
timeSeries('Path',702, '-filePath','fp.txt','-dt',1e-4)
timeSeries('Constant',705)

pattern('Plain',703, 702)
eleLoad('-ele', 701, '-type','-beamUniform',20,0)
eleLoad('-ele', 702, '-type','-beamUniform',20,0)
eleLoad('-ele', 703, '-type','-beamUniform',20,0)
eleLoad('-ele', 704, '-type','-beamUniform',20,0)
eleLoad('-ele', 705, '-type','-beamUniform',20,0)
eleLoad('-ele', 706, '-type','-beamUniform',20,0)
eleLoad('-ele', 707, '-type','-beamUniform',20,0)

print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# ============= Recorder ====================================================
recorder('Element', '-file', 'Stress/ele701.out', '-time', '-ele',701, 'globalForce')
recorder('Element', '-file', 'Stress/ele702.out', '-time', '-ele',702, 'globalForce')
recorder('Element', '-file', 'Stress/ele703.out', '-time', '-ele',703, 'globalForce')
recorder('Element', '-file', 'Stress/ele704.out', '-time', '-ele',704, 'globalForce')
recorder('Element', '-file', 'Stress/ele705.out', '-time', '-ele',705, 'globalForce')
recorder('Element', '-file', 'Stress/ele706.out', '-time', '-ele',706, 'globalForce')
recorder('Element', '-file', 'Stress/ele707.out', '-time', '-ele',707, 'globalForce')

# # --------- Soil element Recorder -----------------
# # -------- Left column ----------------
# recorder('Element', '-file', 'try/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
# recorder('Element', '-file', 'try/ele101.out', '-time', '-ele',101, 'material ',1,'stresses')
# recorder('Element', '-file', 'try/ele199.out', '-time', '-ele',199, 'material ',1,'stresses')

# recorder('Node', '-file', 'try/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
# recorder('Node', '-file', 'try/node151.out', '-time', '-node',151,'-dof',1,2,3,'vel')
# recorder('Node', '-file', 'try/node301.out', '-time', '-node',301,'-dof',1,2,3,'vel')
# # -------- Right column ----------------
# recorder('Element', '-file', 'try/ele2.out', '-time', '-ele',1, 'material ',1,'stresses')
# recorder('Element', '-file', 'try/ele102.out', '-time', '-ele',102, 'material ',1,'stresses')
# recorder('Element', '-file', 'try/ele200.out', '-time', '-ele',200, 'material ',1,'stresses')

# recorder('Node', '-file', 'try/node3.out', '-time', '-node',3,'-dof',1,2,3,'vel')
# recorder('Node', '-file', 'try/node153.out', '-time', '-node',153,'-dof',1,2,3,'vel')
# recorder('Node', '-file', 'try/node303.out', '-time', '-node',303,'-dof',1,2,3,'vel')

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

printModel('-ele', 701,702,703,704,705,706,707)
# --------- end to calculate time -------------
end = time.time()
print(end - start)


