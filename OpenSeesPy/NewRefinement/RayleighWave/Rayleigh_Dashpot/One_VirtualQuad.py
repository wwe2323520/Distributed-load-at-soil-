# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 19:39:36 2024

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
soilWidth = 0.125 #m
soilLength = 0.125 #m


model('basic', '-ndm', 2, '-ndf' , 2)
rho = 2000  # kg/m3
E = 208000000
nu = 0.3

Vp = 374.166    # m/s 
Vs = 200     ;# m/s 

ny = 1
yMesh = soilLength/ny # Y row MeshSize
dcell = yMesh / Vs 
dt = dcell/10.0
print(f'yMesh = {yMesh}; dt = {dt}')

# ======= Totla Analysis Time ============================
analysisTime = (soilLength/Vs)*8
analystep = analysisTime/dt # int(800*(ny/10))
print(f"dt = {dt}; Analysis Total Time = {analysisTime} ;Analysis_step = {analystep}")

# ============= Virtual Element Elastic Modules (E' control by M or G) =====================
M = rho*Vp*Vp
G = rho*Vs*Vs

nu2 = 0.0
Scale = 1e-1#(1/10000000) # Control Size 
E_M = Scale* M*((1+nu2)*(1-2*nu2)/(1-nu2)) # young's Module Control by M (P wave Velocity) # (N/m^2)= (kg*m/s2)*(1/m2) = kg/(s2*m) 
E_G = Scale* 2*G*(1+nu2) # young's Module Control by G (S wave Velocity) # (N/m^2)= (kg*m/s2)*(1/m2) = kg/(s2*m) 

rho2 =  Scale*rho   # kg/m3 
print(f"rho_ = {rho2}, E_G= {E_G}; E_M = {E_M}")
# nDMaterial('ElasticIsotropic', 2000, E, nu, rho)

nDMaterial('ElasticIsotropic', 2006, E_G, nu2, rho2)

node(1, 0.0, 0.0)
node(2, soilWidth, 0.0)
node(3, 0.0, -0.125)
node(4, soilWidth, -0.125)

fix(3,1,1)
fix(4,1,1)

# fix(1, 0,1)
# fix(2, 0,1)

equalDOF(1,2,1,2)
# equalDOF(3,4,1,2)

BotEle = 1
element('quad', BotEle, 3,4,2,1,   1, 'PlaneStrain', 2006) #PlaneStrain / PlaneStress

# # =========== Bottom Beam element ===================
# # --------- Bot Virtual quad -----------
# BeamNode_Start = 5
# BeamEle_Start = BotEle + 1
# model('basic', '-ndm', 2, '-ndf' , 3)
# for j in range(2):
#     node(BeamNode_Start+j, 0.125*j,0.0)
#     mass(BeamNode_Start+j,1,1,1)
# # -------- fix rotate dof ------------
#     fix(BeamNode_Start+j,0,0,1)

# # ------------- Beam parameter -----------------
# A = 0.1*1
# E1 = 1e-06 ;#1e-06
# Iz = (0.1*0.1*0.1)/12
# geomTransf('Linear', 1)

# for k in range(1):
#     element('elasticBeamColumn', BeamEle_Start+k, BeamNode_Start+k, BeamNode_Start+1+k, A,E1,Iz, 1, '-release', 3)

# # =========== connect bot beam and soil element =========================
# for k in range(2):
#     equalDOF(1+k,BeamNode_Start+k,1,2)

# yMesh = 0.125 #m
# =========== Apply Rayleigh Dashpot ============================
alphaM = (6/yMesh)*(rho/rho2)*(-Vp + 2*Vs) 
betaK = (4*yMesh)*(1/E_G)*rho*(Vp-Vs)
betaKinit = 0.0
betaKcomm = 0.0

print(f"alphaM = {alphaM}; betaK = {betaK}")
region(10000, '-ele ', BotEle ,'-rayleigh',alphaM, betaK, betaKinit,betaKcomm)

# # ============================ Apply Load Pattern ============================================
# # timeSeries('Path',702, '-filePath', f'TimeSeries/fp_80row.txt','-dt',cpdt) #1e-4
# # timeSeries('Path',702, '-filePath', f'TimeSeries/fs200_{80}row.txt','-dt', dt)
# # timeSeries('Path',704, '-filePath','TopForce10row.txt','-dt',2.67e-4)

# timeSeries('Path',702, '-filePath', f'fs.txt','-dt', dt)
# # timeSeries('Linear', 704, '-factor', 1.0)
# P = 20*yMesh*0.5

# pattern('Plain',703, 702)
# # load(1, 1,0)
# # load(2, 1,0)
# # ------------- S wave -----------------------------
# for o in range(1):
#     eleLoad('-ele', BeamEle_Start+o, '-type','-beamUniform',0,20,0)


# #----------Use velocity timeseries to make wave transport and Input velocity boundary(node 1,2)------------
# iSupportNode = [1,2]
# iGMdirection = [1,1] # Control Apply direction
IDloadTag = 400   # load tag
IDgmSeries = 500  # for multipleSupport Excitation

timeSeries('Path',706, '-filePath', f'TimeSeries/Accel_fs.txt','-dt', dt) # Acceleration_TimeSeries
timeSeries('Path',708, '-filePath', f'TimeSeries/Vel_fs.txt','-dt', dt) # Velocity_TimeSeries
timeSeries('Path',710, '-filePath', f'TimeSeries/Disp_fs.txt','-dt', dt) # Displacement_TimeSeries


pattern('MultipleSupport', IDloadTag)
groundMotion(IDgmSeries, 'Plain', '-vel', 708, 'int', 'Trapezoidal')
imposedMotion(1, 1,IDgmSeries)
imposedMotion(2, 1,IDgmSeries)

# for i in range(len(iSupportNode)):
#     # timeSeries('Path',706+i, '-filePath', f'TimeSeries/Accel_fs.txt','-dt', dt) # Acceleration_TimeSeries
#     # timeSeries('Path',708+i, '-filePath', f'TimeSeries/Vel_fs.txt','-dt', dt) # Velocity_TimeSeries
#     # timeSeries('Path',710+i, '-filePath', f'TimeSeries/Disp_fs.txt','-dt', dt) # Displacement_TimeSeries

#     groundMotion(IDgmSeries+i, 'Plain','-accel', 706,'int', 'Simpson') # 'int', 'Trapezoidal'/'Simpson'  '-disp',710, '-vel', 708, '-accel', 706
#     imposedMotion(iSupportNode[i], iGMdirection[i], IDgmSeries+i)
#     # print(iSupportNode[i], iGMdirection[i], IDgmSeries+i)

# =============== Recorder =============================
recorder('Node', '-file', f'Velocity/Disp1.out', '-time', '-node',1,'-dof',1,2,'disp')
recorder('Node', '-file', f'Velocity/Disp2.out', '-time', '-node',2,'-dof',1,2,'disp')
recorder('Node', '-file', f'Velocity/Disp3.out', '-time', '-node',3,'-dof',1,2,'disp')
recorder('Node', '-file', f'Velocity/Disp4.out', '-time', '-node',4,'-dof',1,2,'disp')

recorder('Node', '-file', f'Velocity/Vel1.out', '-time', '-node',1,'-dof',1,2,'vel')
recorder('Node', '-file', f'Velocity/Vel2.out', '-time', '-node',2,'-dof',1,2,'vel')
recorder('Node', '-file', f'Velocity/Vel3.out', '-time', '-node',3,'-dof',1,2,'vel')
recorder('Node', '-file', f'Velocity/Vel4.out', '-time', '-node',4,'-dof',1,2,'vel')

recorder('Node', '-file', f'Velocity/accel1.out', '-time', '-node',1,'-dof',1,2,'accel')
recorder('Node', '-file', f'Velocity/accel2.out', '-time', '-node',2,'-dof',1,2,'accel')
recorder('Node', '-file', f'Velocity/accel3.out', '-time', '-node',3,'-dof',1,2,'accel')
recorder('Node', '-file', f'Velocity/accel4.out', '-time', '-node',4,'-dof',1,2,'accel')

recorder('Element', '-file', f'Stress/ele{BotEle}.out', '-time', '-ele',BotEle, 'material ',1,'stresses')
recorder('Node', '-file', f'Stress/Reac1.out', '-time', '-node',1,'-dof',1,2,3,'rayleighForces')
recorder('Node', '-file', f'Stress/Reac2.out', '-time', '-node',2,'-dof',1,2,3,'rayleighForces')

recorder('Node', '-file', f'Stress/Reac3.out', '-time', '-node',3,'-dof',1,2,3,'rayleighForces') #rayleighForces / reaction
recorder('Node', '-file', f'Stress/Reac4.out', '-time', '-node',4,'-dof',1,2,3,'rayleighForces')

system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(3200,dt)
# analyze(int(analystep),cpdt)
print("finish analyze:0 ~ 0.8s")

end = time.time()
print(end - start)
