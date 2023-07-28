# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 12:23:16 2023

@author: User
"""

from openseespy.opensees import *
import opsvis as ops
import matplotlib.pyplot as plt

wipe()
# ============ Soil Column element : 1 column ============================
model('basic', '-ndm', 2, '-ndf' , 2)
E = 15005714.286
nu = 0.3
rho = 2020
nDMaterial('ElasticIsotropic', 2000, E, nu, rho)

nx = 2
ny = 100
e1 = 1
n1 = 1
eleArgs = [1, 'PlaneStrain', 2000]
points = [1, 0.0, 0.0, 2, 0.2,0.0, 3, 0.2,10.0, 4, 0.0,10.0]

block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)

# ----------- soil node Boundary condition: Left and right same disp:x,y-------------
for i in range(ny+1):
    equalDOF(3*i+1,3*i+3,1,2)
    
    # fix(3*i+1, 1,0)
    # fix(3*i+3, 1,0)
# ============ Beam element at bottom =================
model('basic', '-ndm', 2, '-ndf' , 3)
node(304,0.0,0.0)
node(305,0.1,0.0)
node(306,0.2,0.0)

mass(304,1,1,1)
mass(305,1,1,1)
mass(306,1,1,1)

# --------- Beam node B.C ------------
# fix(304,1,1,1)
# fix(305,1,1,1)

# -------- fix rotation freedom -----------
fix(304,0,0,1)
fix(305,0,0,1)
fix(306,0,0,1)

# --------- Build Beam element -----------
A = 0.1*1
E1 = 1e+20
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

element('elasticBeamColumn',500,304,305, A,E1,Iz,1,'-release', 3) #
element('elasticBeamColumn',501,305,306, A,E1,Iz,1,'-release', 3) #

equalDOF(304,306,1,2)
# ============== connect soil node with bot beam node =====================
equalDOF(304,1,1,2)
equalDOF(305,2,1,2)
equalDOF(306,3,1,2)

# ========== Apply Distributed load ===========================================
timeSeries('Path',702, '-filePath','fp.txt','-dt',1e-4)
timeSeries('Constant',705)

pattern('Plain',703, 702)
eleLoad('-ele', 500, '-type','-beamUniform',20,0)
eleLoad('-ele', 501, '-type','-beamUniform',20,0)
print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# ============= Recorder ====================================================
recorder('Element', '-file', 'Stress/ele500.out', '-time', '-ele',500, 'localForce')

# --------- Soil element Recorder -----------------
# -------- Left column ----------------
recorder('Element', '-file', 'Stress/ele1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele101.out', '-time', '-ele',101, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele199.out', '-time', '-ele',199, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node1.out', '-time', '-node',1,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node151.out', '-time', '-node',151,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node301.out', '-time', '-node',301,'-dof',1,2,3,'vel')
# -------- Right column ----------------
recorder('Element', '-file', 'Stress/ele2.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele102.out', '-time', '-ele',102, 'material ',1,'stresses')
recorder('Element', '-file', 'Stress/ele200.out', '-time', '-ele',200, 'material ',1,'stresses')

recorder('Node', '-file', 'Velocity/node3.out', '-time', '-node',3,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node153.out', '-time', '-node',153,'-dof',1,2,3,'vel')
recorder('Node', '-file', 'Velocity/node303.out', '-time', '-node',303,'-dof',1,2,3,'vel')

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

printModel('-ele', 500,501)




