# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 19:39:36 2024

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

E = 208000000 # (N/m^2)= (kg*m/s2)*(1/m2) = kg/(s2*m) 
nu = 0.0 #0.3
rho = 2000    # kg/m3 
nDMaterial('ElasticIsotropic', 2000, E, nu, rho)

soilLength = 10 #m
soilwidth =  1.0     #1.0/ 0.125

nx = int(soilwidth/0.125)
ny = 80 #80
e1 = 1
n1 = 1
eleArgs = [1, 'PlaneStrain', 2000]
points = [1, 0.0,   0.0, 
        2, soilwidth,  0.0, 
        3, soilwidth,  soilLength, 
        4, 0.0,   soilLength]
block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)

# -------- Soil B.C (Tie BC) ---------------
for i in range(ny+1):
    equalDOF((nx+1)*i+1,(nx+1)*i+(nx+1),1,2)

endNode = (1+nx) + (nx+1)*ny
endEle = nx*ny
# print(endNode, endEle)

Vp = 374.166    # m/s 
Vs = 200     ;# m/s 

yMesh = soilLength/ny # Y row MeshSize
dcell = yMesh / Vs 
dt = dcell/10.0

# ======= Totla Analysis Time ============================
analysisTime = (soilLength/Vs)*8
analystep = analysisTime/dt # int(800*(ny/10))
print(f"dt = {dt}; Analysis Total Time = {analysisTime} ;Analysis_step = {analystep}")
                  
widthMesh = soilwidth/nx

# ------ Recorde Node/Element ID -----------------------------------------------
LowerN_Left =  1
CenterN_Left = int(LowerN_Left + (nx+1)*(ny/2))
UpperN_Left = int(LowerN_Left + (nx+1)* ny)
print(f"LowerN_Left = {LowerN_Left},CenterN_Left = {CenterN_Left}, UpperN_Left = {UpperN_Left}")
LowerE_Left =  1
CenterE_Left = int(LowerE_Left + nx*(ny/2))
UpperE_Left = int(LowerE_Left + nx* (ny-1))
print(f"LowerE_Left = {LowerE_Left},CenterE_Left = {CenterE_Left}, UpperE_Left = {UpperE_Left}")

LowerN_Center =  int(1 + (nx/2))
CenterN_Center = int(LowerN_Center + (nx+1)*(ny/2))
UpperN_Center = int(LowerN_Center + (nx+1)* ny)
print(f"LowerN_Center = {LowerN_Center},CenterN_Center = {CenterN_Center}, UpperN_Center = {UpperN_Center}")
LowerE_Center =  int((nx/2)+1)
CenterE_Center = int(LowerE_Center + nx*(ny/2))
UpperE_Center = int(LowerE_Center + nx* (ny-1))
print(f"LowerE_Center = {LowerE_Center} ,CenterE_Center = {CenterE_Center}, UpperE_Center = {UpperE_Center}")

LowerN_Right =  int(nx+1)
CenterN_Right = int(LowerN_Right + (nx+1)*(ny/2))
UpperN_Right = int(LowerN_Right + (nx+1)* ny)
print(f"LowerN_Right = {LowerN_Right},CenterN_Right = {CenterN_Right}, UpperN_Right = {UpperN_Right}")
LowerE_Right =  int(nx)
CenterE_Right = int(LowerE_Right + nx*(ny/2))
UpperE_Right = int(LowerE_Right + nx* (ny-1))
print(f"LowerE_Right = {LowerE_Right} ,CenterE_Right = {CenterE_Right}, UpperE_Right = {UpperE_Right}")

# -------- Quarter(1/4) Node ------------------------
LowerN_LQuarter = int((nx/4)+1)
UpperrN_LQuarter = int(LowerN_LQuarter + (nx+1)* ny)
print(f"LowerN_LQuarter = {LowerN_LQuarter} ,UpperrN_LQuarter = {UpperrN_LQuarter}")
LowerE_LQuarter = int((nx/4)+1)
UpperrE_LQuarter = int(LowerE_LQuarter + (ny-1)* nx)
print(f"LowerE_LQuarter = {LowerE_LQuarter} ,UpperrE_LQuarter = {UpperrE_LQuarter}")
# -------- Quarter(3/4) Node ------------------------
LowerN_RQuarter = int((3*nx/4)+1)
UpperrN_RQuarter = int(LowerN_RQuarter + (nx+1)* ny)
print(f"LowerN_RQuarter = {LowerN_RQuarter} ,UpperrN_RQuarter = {UpperrN_RQuarter}")
LowerE_RQuarter = int((3*nx/4)+1)
UpperrE_RQuarter = int(LowerE_RQuarter + (ny-1)* nx)
print(f"LowerE_RQuarter = {LowerE_RQuarter} ,UpperrE_RQuarter = {UpperrE_RQuarter}")


# ============== Apply virtual Quad element to apply Rayleigh Dashpot =======================
BotNode = endNode+ 1 

BotEle = endEle + 1

for i in range(nx+1):
    node(BotNode+i, widthMesh*i, -0.125)

for k in range(nx):
    element('quad', BotEle+k, BotNode+k, (BotNode+1)+k, (n1+1)+k,  n1+k, *eleArgs)

    # print( BotEle+k, BotNode+k, (BotNode+1)+k, (BotNode+nx+2)+k,  (BotNode+nx+1)+k)

# # ========= soil with  virtual Quad element have same dof ===================
# for i in range(nx+1):
#     equalDOF(n1+i, (BotNode+nx+1)+i, 1,2)

# =========== Bottom Beam element ===================
BeamNode_Start = BotNode + nx + 1
BeamEle_Start = BotEle + nx

model('basic', '-ndm', 2, '-ndf' , 3)

for j in range(nx+1):
    node(BeamNode_Start+j, widthMesh*j,0.0)
    mass(BeamNode_Start+j,1,1,1)
# -------- fix rotate dof ------------
    fix(BeamNode_Start+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', BeamEle_Start+k, BeamNode_Start+k, BeamNode_Start+1+k, A,E1,Iz, 1, '-release', 3)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(n1+k,BeamNode_Start+k,1,2)

# # ============= Bottom Beam element Dashpot ==========================
# BotTDash_Start = BeamNode_Start + (nx+1)
# BotNDash_Start = BotTDash_Start + 2*(nx+1)
# # print(f'BotTDash_Start= {BotTDash_Start}; BotNDash_Start={BotNDash_Start}')

# for l in range(nx+1):
#     # ------------- traction dashpot -> for S wave------------
#     node(BotTDash_Start+2*l, widthMesh*l, 0.0)
#     node((BotTDash_Start+1)+2*l, widthMesh*l, 0.0)
#     # =============== dashpot dir: Vs -> x dir ---------------------     
#     fix(BotTDash_Start+2*l, 0, 1, 1)      # x dir dashpot　
#     fix((BotTDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix

#     # ------------- Normal dashpot -> for P wave ------------
#     node(BotNDash_Start+2*l, widthMesh*l, 0.0)
#     node((BotNDash_Start+1)+2*l, widthMesh*l, 0.0)
#     # ---------- dashpot dir: Vp -> y dir---------------------     
#     fix(BotNDash_Start+2*l, 1, 0, 1)      # y dir dashpot　
#     fix((BotNDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix

# # ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
# for k in range(nx+1):
# # --------------traction dashpot: for S wave------------------
#     equalDOF(1+k,BotTDash_Start+2*k,1)
# # --------------Normal dashpot: for P wave------------------
#     equalDOF(1+k,BotNDash_Start+2*k,2)

# # ------------------- ZeroLength to Build dashpot: Material ----------------------------------
# sizeX = 0.125  # m ******
# B_Smp = 0.5*rho*Vp*sizeX      # lower Left and Right corner node dashpot :N (newton)
# B_Sms = 0.5*rho*Vs*sizeX      # lower Left and Right corner node dashpot :N (newton)

# B_Cmp = 1.0*rho*Vp*sizeX      # Bottom Center node dashpot :N (newton)
# B_Cms = 1.0*rho*Vs*sizeX      # Bottom Center node dashpot :N (newton)

# uniaxialMaterial('Viscous',4000, B_Smp, 1)    # P wave: Side node
# uniaxialMaterial('Viscous',4001, B_Sms, 1)    # S wave: Side node

# uniaxialMaterial('Viscous',4002, B_Cmp, 1)    # P wave: Center node
# uniaxialMaterial('Viscous',4003, B_Cms, 1)    # S wave: Center node

# #----------- dashpot elements: Vs with x dir / Vp with y-dir------------------
# xdir = 1
# ydir = 2
# # ------ Traction dashpot element: Vs with x dir
# BotTEle_Start = BeamEle_Start + nx
# BotTEle_End = BotTEle_Start + nx

# element('zeroLength',BotTEle_Start,(BotTDash_Start+1),BotTDash_Start, '-mat',4001,'-dir',xdir)  # node 1: Left side
# element('zeroLength',BotTEle_Start+1,(BotTDash_Start+1)+2*1,BotTDash_Start+2*1, '-mat',4001,'-dir',xdir)  # node 1: Left side

# # ------ Normal dashpot element: Vp with y dir (98~106)
# BotNEle_Start = BotTEle_End+1
# BotNEle_End = BotNEle_Start+nx

# element('zeroLength',BotNEle_Start,(BotNDash_Start+1),BotNDash_Start, '-mat',4000,'-dir',ydir)
# element('zeroLength',BotNEle_Start+1,(BotNDash_Start+1)+2*1,BotNDash_Start+2*1, '-mat',4000,'-dir',ydir)

# ================== Apply Rayleigh Dashpot ============================= 
alphaM = -(6/yMesh)*(Vp*(1-2*nu) + Vs*(2*nu-2)) # Vs = *1.5 ; Vp = *2.0 (special coff)
betaK = -(-4*yMesh)*((1+nu)*(1-2*nu)/E)*rho*(Vp-Vs) 
betaKinit = 0.0
betaKcomm = 0.0
print(f"alphaM = {alphaM}; betaK = {betaK}")
# region(10000, '-nodeRange ', BotNode, BotNode+3 ,'-rayleigh',alphaM, betaK, betaKinit,betaKcomm)
# for j in range(nx):
#     region(10000+j, '-node', Bot2Node+j,'-rayleigh',alphaM, betaK, betaKinit,betaKcomm)

region(10000, '-eleRange ', BotEle, BotEle+nx-1,'-rayleigh',alphaM, betaK, betaKinit,betaKcomm) #Bot2Node
#=========================== Load Pattern 1: Shear wave / P wave ============================
tnscp = soilLength/Vp # wave transport time
dcellcp = tnscp/ny #each cell time
cpdt = round(dcellcp/10, 7) #eace cell have 10 steps
print(f"tnscp = {tnscp}; dcellcp= {dcellcp}, cp_dt = {cpdt}")

# timeSeries('Path',702, '-filePath', f'TimeSeries/fp_80row.txt','-dt',cpdt) #1e-4
timeSeries('Path',702, '-filePath', f'TimeSeries/fs200_{ny}row.txt','-dt', dt)
# timeSeries('Path',704, '-filePath','TopForce10row.txt','-dt',2.67e-4)

# # # # timeSeries('Linear',705)

pattern('Plain',703, 702)
# load(1, 0, 1)
# load(2, 0, 1)
# # ------------- P wave -----------------------------
# for o in range(nx):
#     eleLoad('-ele', BeamEle_Start+o, '-type','-beamUniform',20,0)

# ------------- S wave -----------------------------
for o in range(nx):
    eleLoad('-ele', BeamEle_Start+o, '-type','-beamUniform',0,20,0)

# # # ===================== Load Pattern 2: TopForce on the top Middle Point ======================
# UpperN_Center = 1 + (1+nx)*ny
# tnscp = soilLength/Vp # wave transport time
# dcellcp = tnscp/ny #each cell time
# cpdt = round(dcellcp/10, 7) #eace cell have 10 steps
# print(f"tnscp = {tnscp}; dcellcp= {dcellcp}, cp_dt = {cpdt}")

# timeSeries('Path',704, '-filePath',f'TimeSeries/TopForce{ny}row.txt','-dt', cpdt)
# pattern('Plain',703, 704)
# load(UpperN_Center,0,-1)
# load(UpperN_Center-1,0,-1)
# print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")


# # -------------- Recorder --------------------------------
# ------------- left column -------------
recorder('Element', '-file', f'Stress/ele{LowerE_Left}.out', '-time', '-ele',LowerE_Left, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{CenterE_Left}.out', '-time', '-ele',CenterE_Left, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{UpperE_Left}.out', '-time', '-ele',UpperE_Left, 'material ',1,'stresses')

recorder('Node', '-file', f'Velocity/node{LowerN_Left}.out', '-time', '-node',LowerN_Left,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{CenterN_Left}.out', '-time', '-node',CenterN_Left,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{UpperN_Left}.out', '-time', '-node',UpperN_Left,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', f'Stress/ele{LowerE_Center}.out', '-time', '-ele',LowerE_Center, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{CenterE_Center}.out', '-time', '-ele',CenterE_Center, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{UpperE_Center}.out', '-time', '-ele',UpperE_Center, 'material ',1,'stresses')

recorder('Node', '-file', f'Velocity/node{LowerN_Center}.out', '-time', '-node',LowerN_Center,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{CenterN_Center}.out', '-time', '-node',CenterN_Center,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{UpperN_Center}.out', '-time', '-node',UpperN_Center,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', f'Stress/ele{LowerE_Right}.out', '-time', '-ele',LowerE_Right, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{CenterE_Right}.out', '-time', '-ele',CenterE_Right, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{UpperE_Right}.out', '-time', '-ele',UpperE_Right, 'material ',1,'stresses')

recorder('Node', '-file', f'Velocity/node{LowerN_Right}.out', '-time', '-node',LowerN_Right,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{CenterN_Right}.out', '-time', '-node',CenterN_Right,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{UpperN_Right}.out', '-time', '-node',UpperN_Right,'-dof',1,2,3,'vel')

# ==== Left 1/4 node ======================================
recorder('Element', '-file', f'Stress/ele{UpperrE_LQuarter}.out', '-time', '-ele',UpperrE_LQuarter, 'material ',1,'stresses')
recorder('Node', '-file', f'Velocity/node{UpperrN_LQuarter}.out', '-time', '-node',UpperrN_LQuarter,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', f'Stress/ele{UpperrE_RQuarter}.out', '-time', '-ele',UpperrE_RQuarter, 'material ',1,'stresses')
recorder('Node', '-file', f'Velocity/node{UpperrN_RQuarter}.out', '-time', '-node',UpperrN_RQuarter,'-dof',1,2,3,'vel')

system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(int(analystep),dt)
# analyze(int(analystep),cpdt)
print("finish analyze:0 ~ 0.8s")

end = time.time()
print(end - start)
